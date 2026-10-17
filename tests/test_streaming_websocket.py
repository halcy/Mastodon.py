import time

import pytest

from mastodon.streaming import CallbackStreamListener
from mastodon.streaming_websocket import WebSocketStreamHandle
from mastodon.errors import MastodonIllegalArgumentError
from .test_streaming import Listener


def test_closed_websocket_cannot_subscribe(monkeypatch):
    from unittest.mock import Mock

    connection = Mock()
    open_websocket = Mock(return_value=connection)
    monkeypatch.setattr('mastodon.streaming_websocket._open_websocket', open_websocket)
    handle = WebSocketStreamHandle('ws://localhost', 'token', 'tests', reconnect=True)
    handle.close()

    with pytest.raises(MastodonIllegalArgumentError, match='closed'):
        handle.subscribe('user', listener=CallbackStreamListener())

    open_websocket.assert_called_once()
    connection.close.assert_called_once()
    assert handle.connection is None
    assert not handle.is_alive()
    assert not handle.is_receiving()


def test_websocket_closed_during_reconnect(monkeypatch):
    from unittest.mock import Mock

    connection = Mock()
    monkeypatch.setattr('mastodon.streaming_websocket._open_websocket', Mock(return_value=connection))
    handle = WebSocketStreamHandle('ws://localhost', 'token', 'tests', reconnect=True)
    replacement = Mock()

    def open_and_close(*args):
        handle.close()
        return replacement

    monkeypatch.setattr('mastodon.streaming_websocket._open_websocket', open_and_close)
    handle._connect()

    replacement.close.assert_called_once()
    assert handle.closed
    assert handle.connection is None

def wait_for(predicate, timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.1)
    raise AssertionError("Timed out waiting for WebSocket streaming event")


class MultiplexListener(CallbackStreamListener):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.streams = []

    def on_any_event(self, name, data=None, for_stream=None):
        self.streams.append((name, for_stream))


@pytest.mark.vcr(match_on=['path'])
def test_stream_websocket_user_direct(api, api2, websocket_cassette):
    updates = []
    conversations = []
    listener = MultiplexListener(
        update_handler=updates.append,
        conversation_handler=conversations.append,
    )

    stream = api.stream_open_websocket(listener)
    user_subscription = api.stream_user(listener, websocket_handle=stream)
    direct_subscription = api.stream_direct(listener, websocket_handle=stream)

    posted = []
    try:
        if websocket_cassette.recording:
            time.sleep(2)
        posted.append((api, api.status_post("WebSocket user stream test")))
        posted.append((
            api2,
            api2.status_post(
                "@mastodonpy_test WebSocket direct stream test",
                visibility="direct",
            )
        ))

        wait_for(lambda: len(updates) >= 1 and len(conversations) >= 1)

        assert updates[0].id == posted[0][1].id
        assert conversations[0].last_status.id == posted[1][1].id
        assert ("update", ["user"]) in listener.streams
        assert ("conversation", ["direct"]) in listener.streams
        assert user_subscription.is_receiving()
        assert direct_subscription.is_receiving()
    finally:
        stream.close()
        stream.join()
        for owner, status in posted:
            owner.status_delete(status)


@pytest.mark.vcr(match_on=['path'])
def test_stream_user_shared_websocket(api, websocket_cassette):
    updates = []
    listener = CallbackStreamListener(update_handler=updates.append)
    stream = api.stream_open_websocket()
    subscription = api.stream_user(listener, websocket_handle=stream)

    posted = None
    try:
        if websocket_cassette.recording:
            time.sleep(2)
        posted = api.status_post("WebSocket shared connection test")
        wait_for(lambda: len(updates) >= 1)
        assert updates[0].id == posted.id
    finally:
        subscription.close()
        stream.close()
        stream.join()
        if posted is not None:
            api.status_delete(posted)


@pytest.mark.vcr(match_on=['path'])
def test_stream_websocket_subscribe_unsubscribe(api, websocket_cassette):
    stream = api.stream_open_websocket()
    try:
        assert stream.subscriptions == []

        subscription = stream.subscribe("hashtag", listener=CallbackStreamListener(), tag="mastodonpy")
        assert stream.subscriptions == [subscription]
        assert subscription.stream == "hashtag"
        assert subscription.params == {"tag": "mastodonpy"}
        assert subscription.is_alive()

        subscription.close()
        assert stream.subscriptions == []
        assert not subscription.is_alive()
    finally:
        stream.close()
        stream.join()


def test_websocket_event_with_stream():
    listener = Listener()
    streams = []
    listener.on_any_event = lambda name, data, for_stream=None: streams.append(for_stream)

    listener.handle_websocket_message({
        "stream": ["user"],
        "event": "update",
        "payload": '{"foo": "bar"}',
    })

    assert listener.updates == [{"foo": "bar"}]
    assert streams == [["user"]]


def test_websocket_payloadless_event():
    listener = Listener()
    merged = []
    listener.on_notifications_merged = lambda: merged.append(True)

    listener.handle_websocket_message({
        "stream": ["user"],
        "event": "notifications_merged",
    })

    assert merged == [True]



@pytest.mark.vcr(match_on=['method', 'path', 'query'])
def test_stream_websocket_only_media(api, websocket_cassette):
    media = api.media_post('tests/image.jpg', synchronous=True, file_name='only-media.jpg')
    updates = []
    media_updates = []
    posted = []
    stream = api.stream_open_websocket()
    try:
        api.stream_public(
            CallbackStreamListener(update_handler=updates.append),
            local=True, websocket_handle=stream,
        )
        api.stream_public(
            CallbackStreamListener(update_handler=media_updates.append),
            local=True, only_media=True, websocket_handle=stream,
        )
        if websocket_cassette.recording:
            time.sleep(2)

        posted.append(api.status_post('WebSocket text-only stream test', visibility='public'))
        posted.append(api.status_post(
            'WebSocket media-only stream test', media_ids=[media], visibility='public',
        ))
        wait_for(lambda: len(updates) >= 2 and len(media_updates) >= 1)
        if websocket_cassette.recording:
            time.sleep(5)  # Also catch an incorrectly delivered text-only event.
        stream.close()
        stream.join()

        assert len(updates) == 2
        assert {status.id for status in updates} == {status.id for status in posted}
        assert [status.id for status in media_updates] == [posted[1].id]
        assert media_updates[0].media_attachments[0].id == media.id
    finally:
        stream.close()
        stream.join()
        for status in posted:
            api.status_delete(status, delete_media=True)
