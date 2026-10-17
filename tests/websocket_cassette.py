import json
import threading
from collections import deque
from urllib.parse import urlsplit

import yaml

# Instrumentation so that we can record websocket interactions because
# apparently every library only suppoorts asyncio websockets and/or 
# requires new python versions

class _RecordingWebSocket:
    def __init__(self, websocket, recording):
        self._websocket = websocket
        self._recording = recording
        self._lock = threading.Lock()
        self._closing = False

    @property
    def connected(self):
        return self._websocket.connected

    def send(self, message):
        with self._lock:
            self._recording.append({"send": json.loads(message)})
        return self._websocket.send(message)

    def recv(self):
        try:
            message = self._websocket.recv()
        except Exception:
            with self._lock:
                if not self._closing:
                    self._recording.append({"close": {}})
            raise
        with self._lock:
            if message in (None, ""):
                if not self._closing:
                    self._recording.append({"close": {}})
            else:
                if isinstance(message, bytes):
                    message = message.decode("utf-8")
                self._recording.append({"receive": json.loads(message)})
        return message

    def close(self):
        with self._lock:
            self._closing = True
        return self._websocket.close()


class _ReplayingWebSocket:
    def __init__(self, recording):
        self._sends = deque()
        self._receives = deque()
        for interaction in recording:
            if "send" in interaction:
                self._sends.append(interaction["send"])
            elif "receive" in interaction or "close" in interaction:
                # A received message cannot precede the sends that triggered it.
                self._receives.append((len(self._sends), interaction))
        self._sent_count = 0
        self._closed = False
        self._condition = threading.Condition()

    @property
    def connected(self):
        return not self._closed

    def send(self, message):
        actual = json.loads(message)
        with self._condition:
            if not self._sends:
                raise AssertionError(f"Unexpected WebSocket send: {actual!r}")
            expected = self._sends[0]
            if expected != actual:
                raise AssertionError(
                    f"Expected WebSocket send {expected!r}, got {actual!r}"
                )
            self._sends.popleft()
            self._sent_count += 1
            self._condition.notify_all()

    def recv(self):
        with self._condition:
            self._condition.wait_for(lambda: self._closed or (
                self._receives and self._receives[0][0] <= self._sent_count
            ))
            if self._closed:
                return ""
            _, interaction = self._receives.popleft()
            if "receive" in interaction:
                return json.dumps(interaction["receive"], separators=(",", ":"))
            self.close()
            return ""

    def close(self):
        with self._condition:
            self._closed = True
            self._condition.notify_all()

    def assert_consumed(self):
        if self._sends:
            raise AssertionError(f"Unplayed WebSocket sends: {list(self._sends)!r}")


class WebSocketCassette:
    def __init__(self, path, record_mode, real_open):
        self.path = path
        self.real_open = real_open
        self.connections = []
        self._replaying_connections = []
        self._lock = threading.Lock()

        exists = path.exists()
        self.recording = record_mode in ("all", "rewrite", "new_episodes") or (
            record_mode == "once" and not exists
        )
        if not self.recording:
            if not exists:
                raise AssertionError(f"WebSocket cassette does not exist: {path}")
            with path.open("r", encoding="utf-8") as cassette_file:
                cassette = yaml.safe_load(cassette_file)
            self.connections = (cassette or {}).get("connections", [])

    def open_websocket(self, url, headers, timeout):
        request = {
            "path": urlsplit(url).path,
            "authorization": any(header.lower().startswith("authorization:") for header in headers),
        }
        if self.recording:
            connection = {
                "request": request,
                "interactions": [],
            }
            with self._lock:
                self.connections.append(connection)
            websocket = self.real_open(url, headers, timeout)
            return _RecordingWebSocket(websocket, connection["interactions"])

        with self._lock:
            connection_index = len(self._replaying_connections)
            if connection_index >= len(self.connections):
                raise AssertionError(f"Unexpected WebSocket connection to {request['path']}")
            connection = self.connections[connection_index]
            if connection["request"] != request:
                raise AssertionError(
                    f"Expected WebSocket request {connection['request']!r}, got {request!r}"
                )
            websocket = _ReplayingWebSocket(connection["interactions"])
            self._replaying_connections.append(websocket)
            return websocket

    def finish(self):
        if self.recording:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("w", encoding="utf-8") as cassette_file:
                yaml.safe_dump(
                    {"version": 1, "connections": self.connections},
                    cassette_file,
                    sort_keys=False,
                    allow_unicode=True,
                )
            return

        if len(self._replaying_connections) != len(self.connections):
            raise AssertionError(
                f"Expected {len(self.connections)} WebSocket connections, "
                f"opened {len(self._replaying_connections)}"
            )
        for websocket in self._replaying_connections:
            websocket.assert_consumed()
