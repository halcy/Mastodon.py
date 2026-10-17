import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from unittest.mock import Mock

import pytest

from tests.websocket_cassette import WebSocketCassette, _ReplayingWebSocket


SUBSCRIBE = {'type': 'subscribe', 'stream': 'user'}
UNSUBSCRIBE = {'type': 'unsubscribe', 'stream': 'user'}


def test_replay_validates_sends_without_blocking_on_pending_receives():
    socket = _ReplayingWebSocket([
        {'send': SUBSCRIBE}, {'receive': {'event': 'update'}},
        {'send': UNSUBSCRIBE}, {'close': {}},
    ])
    with pytest.raises(AssertionError, match='Expected WebSocket send'):
        socket.send(json.dumps(UNSUBSCRIBE))
    with pytest.raises(AssertionError, match='Unplayed WebSocket sends'):
        socket.assert_consumed()
    socket.send(json.dumps(SUBSCRIBE))
    # The application can unsubscribe before the reader consumes earlier events.
    socket.send(json.dumps(UNSUBSCRIBE))
    assert json.loads(socket.recv()) == {'event': 'update'}
    assert socket.recv() == ''
    assert not socket.connected
    socket.assert_consumed()
    with pytest.raises(AssertionError, match='Unexpected WebSocket send'):
        socket.send(json.dumps(SUBSCRIBE))


def test_replay_waits_for_send_and_close_unblocks_exhausted_reader():
    socket = _ReplayingWebSocket([
        {'send': SUBSCRIBE}, {'receive': {'event': 'update'}},
    ])
    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            received = executor.submit(socket.recv)
            with pytest.raises(TimeoutError):
                received.result(timeout=0.05)
            socket.send(json.dumps(SUBSCRIBE))
            assert json.loads(received.result(timeout=1)) == {'event': 'update'}
            exhausted = executor.submit(socket.recv)
            with pytest.raises(TimeoutError):
                exhausted.result(timeout=0.05)
            socket.close()
            assert exhausted.result(timeout=1) == ''
        finally:
            socket.close()


def test_cassette_records_and_replays_without_credentials(tmp_path):
    path = tmp_path / 'websocket.yaml'
    real_socket = Mock(connected=True)
    real_socket.recv.side_effect = ['{"event":"update"}', '']
    real_open = Mock(return_value=real_socket)
    headers = ['Authorization: Bearer secret-test-token']

    cassette = WebSocketCassette(path, 'once', real_open)
    socket = cassette.open_websocket('ws://example.test/api/v1/streaming', headers, 5)
    socket.send(json.dumps(SUBSCRIBE))
    assert json.loads(socket.recv()) == {'event': 'update'}
    assert socket.recv() == ''
    socket.close()
    cassette.finish()
    assert 'secret-test-token' not in path.read_text()

    real_open.reset_mock()
    cassette = WebSocketCassette(path, 'once', real_open)
    assert not cassette.recording
    with pytest.raises(AssertionError, match='Expected WebSocket request'):
        cassette.open_websocket('ws://example.test/api/v1/streaming', [], 5)
    socket = cassette.open_websocket('ws://example.test/api/v1/streaming', headers, 5)
    socket.send(json.dumps(SUBSCRIBE))
    assert json.loads(socket.recv()) == {'event': 'update'}
    assert socket.recv() == ''
    cassette.finish()
    real_open.assert_not_called()
