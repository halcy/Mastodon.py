# streaming_websocket.py - WebSocket streaming transport

import json
import threading
import time

from mastodon.streaming import StreamHandle
from mastodon.compat import IMPL_HAS_WEBSOCKET, websocket
from mastodon.errors import MastodonAPIError, MastodonIllegalArgumentError, MastodonMalformedEventError, MastodonNetworkError, MastodonReadTimeout


def _open_websocket(url, headers, timeout):
    if not IMPL_HAS_WEBSOCKET:
        raise NotImplementedError(
            "WebSocket streaming requires the websocket_streaming feature dependencies. "
            "Install Mastodon.py[websocket_streaming]."
        )

    return websocket.create_connection(
        url,
        header=headers,
        timeout=timeout,
        enable_multithread=True,
    )


def _translate_websocket_error(error):
    if isinstance(error, (NotImplementedError, MastodonMalformedEventError, MastodonNetworkError)):
        return error

    if IMPL_HAS_WEBSOCKET and isinstance(error, websocket.WebSocketTimeoutException):
        return MastodonReadTimeout("Timed out while reading from the WebSocket streaming server.")
    return MastodonNetworkError("WebSocket streaming connection failed.", str(error))


class WebSocketSubscription:
    """One subscription carried by a shared WebSocket connection."""

    def __init__(self, websocket, stream, params, listener):
        self.websocket = websocket
        self.stream = stream
        self.params = dict(params)
        self.listener = listener
        self.active = True

    def close(self):
        if self.active:
            self.websocket._unsubscribe(self)

    def is_alive(self):
        return self.active and self.websocket.is_alive()

    def is_receiving(self):
        return self.active and self.websocket.is_receiving()


class WebSocketStreamHandle(StreamHandle):
    """A live WebSocket connection that can carry multiple Mastodon streams."""

    def __init__(
        self,
        url,
        access_token,
        user_agent,
        listener=None,
        timeout=300,
        reconnect=False,
        reconnect_wait_sec=5,
    ):
        self.url = url
        self.access_token = access_token
        self.user_agent = user_agent
        self.listener = listener
        self.timeout = timeout
        self.reconnect = reconnect
        self.reconnect_wait_sec = reconnect_wait_sec

        self.closed = False
        self.running = False
        self.reconnecting = False
        self.connection = None
        self._thread = None
        self._lock = threading.RLock()
        self._subscriptions = {}

        self._connect()

    def subscriptions(self):
        """Return a list of active subscriptions."""
        with self._lock:
            return list(self._subscriptions.values())

    def _connect(self):
        headers = []
        if self.access_token:
            headers.append(f"Authorization: Bearer {self.access_token}")
        if self.user_agent:
            headers.append(f"User-Agent: {self.user_agent}")

        try:
            connection = _open_websocket(self.url, headers, self.timeout)
        except Exception as error:
            translated = _translate_websocket_error(error)
            if translated is error:
                raise
            raise translated from error

        with self._lock:
            if self.closed:
                connection.close()
                return
            self.connection = connection

    @staticmethod
    def _subscription_key(stream, params):
        if stream == "list":
            return (stream, str(params.get("list")))
        if stream in ("hashtag", "hashtag:local"):
            return (stream, str(params.get("tag")).lower())
        return (stream,)

    def _send(self, message):
        encoded = json.dumps(message, separators=(",", ":"))
        with self._lock:
            connection = self.connection
            if connection is None:
                return
        try:
            connection.send(encoded)
        except Exception as error:
            translated = _translate_websocket_error(error)
            if translated is error:
                raise
            raise translated from error

    def subscribe(self, stream, listener=None, **params):  # TODO maybe we dont want this
        """Subscribe to a stream and return a :class:`~mastodon.WebSocketSubscription`.

        Valid stream names as of Mastodon version 4.7.3 are:

        * `user`: Home timeline updates and events for the logged-in user,
          including notifications.
        * `user:notification`: Notifications for the logged-in user only.
        * `direct`: Direct message conversation events.
        * `public`: All public statuses known to the server.
        * `public:local`: Public statuses from local accounts.
        * `public:remote`: Public statuses from remote accounts.
        * `public:media`: Public statuses with media attachments.
        * `public:local:media`: Local public statuses with media attachments.
        * `public:remote:media`: Remote public statuses with media attachments.
        * `hashtag`: Public statuses containing the hashtag specified by `tag`.
        * `hashtag:local`: Local public statuses containing that hashtag.
        * `list`: Updates for the list specified by `list`.

        For hashtag streams, pass `tag="python"` (without a leading `#`).
        For list streams, pass the list ID as `list="123"`.
        The listener defaults to the one passed to
        :meth:`~mastodon.Mastodon.stream_open_websocket`.

        You can pass a separate listener for each subscription if desired. If you pass
        one as `listener`, then events will be delivered to that listener instead of
        the default listener passed to `stream_open_websocket`.
        """
        listener = listener if listener is not None else self.listener
        if listener is None:
            raise MastodonIllegalArgumentError(
                "A listener is required when subscribing to a WebSocket stream."
            )
        subscription = WebSocketSubscription(self, stream, params, listener)
        key = self._subscription_key(stream, params)
        with self._lock:
            if self.closed:
                raise MastodonIllegalArgumentError("Cannot subscribe using a closed WebSocket stream.")
            if key in self._subscriptions:
                raise MastodonIllegalArgumentError(f"Already subscribed to WebSocket stream {key!r}.")
            self._subscriptions[key] = subscription

        try:
            self._send({"type": "subscribe", "stream": stream, **params})
        except Exception:
            with self._lock:
                self._subscriptions.pop(key, None)
                subscription.active = False
            raise
        return subscription

    def unsubscribe(self, stream, **params):
        """Unsubscribe using the same stream name and parameters as for subscribe()."""
        key = self._subscription_key(stream, params)
        with self._lock:
            subscription = self._subscriptions.get(key)
            if subscription is None:
                raise MastodonIllegalArgumentError(f"Not subscribed to WebSocket stream {key!r}.")
        self._unsubscribe(subscription)
        return self

    def _unsubscribe(self, subscription):
        key = self._subscription_key(subscription.stream, subscription.params)
        with self._lock:
            if not subscription.active or self._subscriptions.get(key) is not subscription:
                subscription.active = False
                return
            self._subscriptions.pop(key)
            subscription.active = False
        self._send({
            "type": "unsubscribe",
            "stream": subscription.stream,
            **subscription.params,
        })

    def _listeners(self):
        with self._lock:
            listeners = [self.listener]
            listeners.extend(subscription.listener for subscription in self._subscriptions.values())
        return list({id(listener): listener for listener in listeners if listener is not None}.values())

    def _listener_for_message(self, message):
        stream = message.get("stream")
        if isinstance(stream, str):
            stream = [stream]
        if isinstance(stream, list):
            key_parts = [str(part) for part in stream]
            if len(key_parts) > 1 and key_parts[0] in ("hashtag", "hashtag:local"):
                key_parts[1] = key_parts[1].lower()
            key = tuple(key_parts)
        else:
            key = None
        with self._lock:
            subscription = self._subscriptions.get(key)
            if subscription is not None:
                return subscription.listener
        return self.listener

    def _handle_message(self, raw_message):
        try:
            message = json.loads(raw_message)
        except (TypeError, ValueError) as error:
            raise MastodonMalformedEventError("Bad WebSocket JSON", raw_message) from error

        if not isinstance(message, dict):
            raise MastodonMalformedEventError("Malformed WebSocket event", message)

        if "error" in message:
            error = MastodonAPIError(
                "WebSocket streaming subscription failed",
                message.get("status"),
                message["error"],
            )
            for listener in self._listeners():
                listener.on_websocket_error(error, message.get("stream"))
            return

        listener = self._listener_for_message(message)
        if listener is not None:
            listener.handle_websocket_message(message)

    def _notify_abort(self, error):
        for listener in self._listeners():
            listener.on_abort(error)

    def _sleep_attentive(self):
        remaining = self.reconnect_wait_sec
        while remaining > 0 and not self.closed:
            wait = min(0.5, remaining)
            time.sleep(wait)
            remaining -= wait

    def _reconnect(self):
        self.reconnecting = True
        while not self.closed:
            self._sleep_attentive()
            if self.closed:
                break
            try:
                self._connect()
                with self._lock:
                    subscriptions = list(self._subscriptions.values())
                for subscription in subscriptions:
                    self._send({
                        "type": "subscribe",
                        "stream": subscription.stream,
                        **subscription.params,
                    })
                self.reconnecting = False
                return
            except MastodonNetworkError as error:
                self._notify_abort(error)
        self.reconnecting = False

    def _start(self):
        def threadproc():
            try:
                self.running = True
                try:
                    while not self.closed:
                        try:
                            raw_message = self.connection.recv()
                            if raw_message in (None, ""):
                                raise MastodonNetworkError("WebSocket streaming server closed the connection.")
                            if isinstance(raw_message, bytes):
                                raw_message = raw_message.decode("utf-8")
                            self._handle_message(raw_message)
                        except Exception as error:
                            if self.closed:
                                break
                            translated = _translate_websocket_error(error)
                            self._notify_abort(translated)
                            if not self.reconnect:
                                if translated is error:
                                    raise
                                raise translated from error
                            with self._lock:
                                connection = self.connection
                                self.connection = None
                            if connection is not None:
                                connection.close()
                            self._reconnect()
                finally:
                    self.running = False
                    self.reconnecting = False
            except MastodonNetworkError:
                pass

        self._thread = threading.Thread(target=threadproc, daemon=True)
        self._thread.start()
        return self

    def close(self):
        """Permanently close this connection and all of its subscriptions."""
        self.closed = True
        with self._lock:
            connection = self.connection
            self.connection = None
            subscriptions = list(self._subscriptions.values())
            self._subscriptions.clear()
            for subscription in subscriptions:
                subscription.active = False
        if connection is not None:
            connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        self.join()
