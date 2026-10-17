import pytest
import itertools
from http.client import HTTPConnection as StdlibHTTPConnection
from mastodon.streaming import StreamListener, CallbackStreamListener
from mastodon.Mastodon import MastodonMalformedEventError, MastodonNetworkError, MastodonReadTimeout
from mastodon import Mastodon
from requests.exceptions import ChunkedEncodingError, ConnectionError, ReadTimeout

import threading
import time

import sys


def test_sse_stream_handle_join():
    from unittest.mock import Mock
    from mastodon import SSEStreamHandle, StreamHandle

    receiving = threading.Event()
    stopped = threading.Event()
    connection = Mock(status_code=200)
    connection.close.side_effect = stopped.set

    def receive(response):
        receiving.set()
        assert stopped.wait(timeout=5), 'Stream was not closed'

    listener = Mock(handle_stream=receive)
    handle = SSEStreamHandle(None, lambda: connection, False, 0, listener)._start()
    try:
        assert isinstance(handle, StreamHandle)
        assert receiving.wait(timeout=5), 'Stream did not start'
        assert handle.join(timeout=0) is None
        assert handle.is_alive()
        handle.close()
        assert handle.join(timeout=5) is None
        assert not handle.is_alive()
        assert not handle.is_receiving()
    finally:
        handle.close()
        handle.join(timeout=5)


streaming_is_patched = False
real_connections = []
close_connections = False
real_get_response = None

@pytest.fixture(scope='module')
def vcr_config():
    return {
        "match_on": ["path"],
    }

def patch_streaming():
    # For monkeypatching so we can make vcrpy work for our purposes for
    # SSE streams.
    import vcr.stubs

    global streaming_is_patched
    global close_connections
    global real_get_response
    if streaming_is_patched is True:
        return
    streaming_is_patched = True

    import http.client

    close_connections = False
    real_get_response = vcr.stubs.VCRConnection.getresponse

    def fake_get_response(vcr_connection, *args, **kwargs):
        if not vcr_connection._vcr_request.path.startswith("/api/v1/streaming/"):
            return real_get_response(vcr_connection, *args, **kwargs)

        connection = vcr_connection.real_connection
        original_getresponse = connection.getresponse

        def capture_response(*args, **kwargs):
            response = StdlibHTTPConnection.getresponse(connection)
            real_connections.append(connection)
            chunks = []
            try:
                while not close_connections:
                    chunk = response.read1(65536)
                    if not chunk:
                        break
                    chunks.append(chunk)
            except (OSError, http.client.HTTPException):
                if not close_connections:
                    raise
            finally:
                response.close()
                connection.close()
            body = b"".join(chunks)
            response.read = lambda *args, **kwargs: body
            return response

        connection.getresponse = capture_response
        try:
            return real_get_response(vcr_connection, *args, **kwargs)
        finally:
            connection.getresponse = original_getresponse

    vcr.stubs.VCRConnection.getresponse = fake_get_response

def unpatch_streaming():
    import vcr.stubs

    global streaming_is_patched
    global real_get_response
    if streaming_is_patched is False:
        return
    streaming_is_patched = False
    vcr.stubs.VCRConnection.getresponse = real_get_response

def streaming_close():
    global real_connections
    global close_connections
    close_connections = True
    import socket
    for connection in real_connections:
        if connection.sock is not None:
            try:
                connection.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
    real_connections = []
    
@pytest.fixture(autouse=True)
def cleanup_streaming_recording():
    yield
    if streaming_is_patched:
        streaming_close()
        unpatch_streaming()


class Listener(StreamListener):
    def __init__(self):
        self.updates = []
        self.notifications = []
        self.deletes = []
        self.heartbeats = 0
        self.bla_called = False
        self.do_something_called = False
        self.aborts = []

    def on_abort(self, err):
        self.aborts.append(err)

    def on_update(self, status):
        self.updates.append(status)

    def on_notification(self, notification):
        self.notifications.append(notification)

    def on_delete(self, status_id):
        self.deletes.append(status_id)

    def on_blahblah(self, data):
        self.bla_called = True
        pass

    def on_do_something(self, data):
        self.do_something_called = True
        pass

    def handle_heartbeat(self):
        self.heartbeats += 1

    def handle_stream_(self, lines):
        """Test helper to avoid littering all tests with six.b()."""
        def six_b(s):
            return s.encode("latin-1")

        class MockResponse():
            def __init__(self, data):
                self.data = data

            def iter_content(self, chunk_size):
                for line in self.data:
                    for byte in line:
                        bytearr = bytearray()
                        bytearr.append(byte)
                        yield(bytearr)
                    yield(b'\n')
        return self.handle_stream(MockResponse(map(six_b, lines)))


def test_heartbeat():
    listener = Listener()
    listener.handle_stream_([':one', ':two'])
    assert listener.heartbeats == 2



def test_heartbeat_empty_line():
    """Empty event after heartbeat should not raise an error."""
    listener = Listener()
    # Heartbeat followed by empty line triggers _dispatch with empty event
    listener.handle_stream_([':thump', ''])
    assert listener.heartbeats == 1

def test_status():
    listener = Listener()
    listener.handle_stream_([
        'event: update',
        'data: {"foo": "bar"}',
        '',
    ])
    assert listener.updates == [{"foo": "bar"}]


def test_notification():
    listener = Listener()
    listener.handle_stream_([
        'event: notification',
        'data: {"foo": "bar"}',
        '',
    ])
    assert listener.notifications == [{"foo": "bar"}]


def test_delete():
    listener = Listener()
    listener.handle_stream_([
        'event: delete',
        'data: 123',
        '',
    ])
    assert listener.deletes == ["123"]


@pytest.mark.parametrize('events', list(itertools.permutations([
    ['event: update', 'data: {"foo": "bar"}', ''],
    ['event: notification', 'data: {"foo": "bar"}', ''],
    ['event: delete', 'data: 123', ''],
    [':toot toot'],
    [':beep beep'],
])))
def test_many(events):
    listener = Listener()
    stream = [
        line
        for event in events
        for line in event
    ]
    listener.handle_stream_(stream)
    assert listener.updates == [{"foo": "bar"}]
    assert listener.notifications == [{"foo": "bar"}]
    assert listener.deletes == ["123"]
    assert listener.heartbeats == 2


def test_unknown_event():
    """Be tolerant of new event types"""
    listener = Listener()
    listener.handle_stream_([
        'event: blahblah',
        'data: {}',
        '',
    ])
    assert listener.bla_called is True
    assert listener.updates == []
    assert listener.notifications == []
    assert listener.deletes == []
    assert listener.heartbeats == 0

def test_unknown_handled_event():
    """Be tolerant of new unknown event types, if on_unknown_event is available"""
    listener = Listener()
    listener.on_unknown_event = lambda name, payload: None

    listener.handle_stream_([
        'event: complete.new.event',
        'data: {"k": "v"}',
        '',
    ])

    assert listener.updates == []
    assert listener.notifications == []
    assert listener.deletes == []
    assert listener.heartbeats == 0

def test_dotted_unknown_event():
    """Be tolerant of new event types with dots in the event-name"""
    listener = Listener()
    listener.handle_stream_([
        'event: do.something',
        'data: {}',
        '',
    ])
    assert listener.do_something_called is True
    assert listener.updates == []
    assert listener.notifications == []
    assert listener.deletes == []
    assert listener.heartbeats == 0

def test_invalid_json():
    """But not too tolerant"""
    listener = Listener()
    with pytest.raises(MastodonMalformedEventError):
        listener.handle_stream_([
            'event: blahblah',
            'data: {kjaslkdjalskdjasd asdkjhak ajdasldasd}',
            '',
        ])

def test_missing_event_name():
    listener = Listener()
    with pytest.raises(MastodonMalformedEventError):
        listener.handle_stream_([
            'data: {}',
            '',
        ])

    assert listener.updates == []
    assert listener.notifications == []
    assert listener.deletes == []
    assert listener.heartbeats == 0


def test_missing_data():
    listener = Listener()
    with pytest.raises(MastodonMalformedEventError):
        listener.handle_stream_([
            'event: update',
            '',
        ])

    assert listener.updates == []
    assert listener.notifications == []
    assert listener.deletes == []
    assert listener.heartbeats == 0


def test_sse_order_doesnt_matter():
    listener = Listener()
    listener.handle_stream_([
        'data: {"foo": "bar"}',
        'event: update',
        '',
    ])
    assert listener.updates == [{"foo": "bar"}]


def test_extra_keys_ignored():
    """
    https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format
    defines 'id' and 'retry' keys which the Mastodon streaming API doesn't use,
    and alleges that "All other field names are ignored".
    """
    listener = Listener()
    listener.handle_stream_([
        'event: update',
        'data: {"foo": "bar"}',
        'id: 123',
        'retry: 456',
        'ignoreme: blah blah blah',
        '',
    ])
    assert listener.updates == [{"foo": "bar"}]


def test_valid_utf8():
    """Snowman Cat Face With Tears Of Joy"""
    listener = Listener()
    listener.handle_stream_([
        'event: update',
        'data: {"foo": "\xE2\x98\x83\xF0\x9F\x98\xB9"}',
        '',
    ])
    assert listener.updates == [{"foo": u"\u2603\U0001F639"}]


def test_invalid_utf8():
    """Cat Face With Tears O"""
    listener = Listener()
    with pytest.raises(MastodonMalformedEventError):
        listener.handle_stream_([
            'event: update',
            'data: {"foo": "\xF0\x9F\x98"}',
            '',
        ])


def test_multiline_payload():
    """
    https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Data-only_messages
    says that newlines in the 'data' field can be encoded by sending the field
    twice! This would be really pathological for Mastodon because the payload
    is JSON, but technically literal newlines are permissible (outside strings)
    so let's handle this case.
    """
    listener = Listener()
    listener.handle_stream_([
        'event: update',
        'data: {"foo":',
        'data: "bar"',
        'data: }',
        '',
    ])
    assert listener.updates == [{"foo": "bar"}]


class RaisingResponse():
    """A response object whose iter_content immediately raises `exception`."""
    def __init__(self, exception):
        self.exception = exception

    def iter_content(self, chunk_size):
        raise self.exception
        yield  # pragma: no cover - makes this a generator function


@pytest.mark.parametrize("raised,expected", [
    (ChunkedEncodingError("nope"), MastodonNetworkError),
    (ReadTimeout("nope"), MastodonReadTimeout),
    (ConnectionError("nope"), MastodonNetworkError),
])
def test_handle_stream_transport_errors(raised, expected):
    """
    Transport level errors have to surface as the matching Mastodon.py error, and the
    same object has to be handed to on_abort. Everything that reaches the caller of
    handle_stream must also be a MastodonNetworkError, because that is what the
    auto-reconnect handler in Mastodon.__stream catches to decide to reconnect.
    """
    listener = Listener()
    with pytest.raises(expected) as exc_info:
        listener.handle_stream(RaisingResponse(raised))
    assert isinstance(exc_info.value, MastodonNetworkError)
    assert exc_info.value.__cause__ is raised
    assert listener.aborts == [exc_info.value]

@pytest.mark.vcr(match_on=['path'])
def test_stream_user_direct(api, api2, api3, vcr):
    patch_streaming()

    # Be extra super paranoid
    vcr.match_on = ["path"]

    # Make sure we are in the right state to not receive updates from api2
    time.sleep(1)
    user = api2.account_verify_credentials()
    time.sleep(1)
    api.account_unfollow(user)
    time.sleep(2)

    updates = []
    local_updates = []
    notifications = []
    deletes = []
    conversations = []
    edits = []
    listener = CallbackStreamListener(
        update_handler=updates.append,
        local_update_handler=local_updates.append,
        notification_handler=notifications.append,
        delete_handler=deletes.append,
        conversation_handler=conversations.append,
        status_update_handler=edits.append,
        filters_changed_handler=lambda x: 0,
        announcement_handler=lambda x: 0,
        announcement_reaction_handler=lambda x: 0,
        announcement_delete_handler=lambda x: 0,
        encryted_message_handler=lambda x: 0,
    )
    
    posted = []
    def do_activities():
        vcr.match_on = ["path"]
        time.sleep(5)
        posted.append(api.status_post("only real cars respond."))
        time.sleep(1)
        posted.append(api2.status_post("@mastodonpy_test beep beep I'm a jeep"))
        time.sleep(1)
        posted.append(api2.status_post("on the internet, nobody knows you're a plane"))
        time.sleep(1)
        posted.append(api.status_post("@mastodonpy_test_2 pssssst", visibility="direct"))
        time.sleep(1)
        posted.append(api3.status_post("@mastodonpy_test pssssst!", visibility="direct", in_reply_to_id=posted[-1]))
        time.sleep(2)
        api.status_update(posted[0], "only real animals respond.")
        time.sleep(1)
        api.status_delete(posted[0])
        time.sleep(7)
        streaming_close()
        
    t = threading.Thread(args=(), target=do_activities)
    t.start()
    
    stream = api.stream_user(listener, run_async=True)
    time.sleep(1)
    stream2 = api.stream_direct(listener, run_async=True)
    time.sleep(25)
    stream.close()
    stream2.close()

    assert len(updates) == 2
    assert len(local_updates) == 2
    assert len(notifications) == 2
    assert len(deletes) == 1
    assert len(conversations) == 2
    assert len(edits) == 1

    assert updates[0].id == posted[0].id
    assert deletes[0] == posted[0].id
    assert notifications[0].status.id == posted[1].id
    
    t.join()
    unpatch_streaming()
    
@pytest.mark.vcr(match_on=['path'])
def test_stream_user_local(api, api2, vcr):
    patch_streaming()
    vcr.match_on = ["path"]
    time.sleep(1)

    # Make sure we are in the right state to not receive updates from api2
    time.sleep(1)
    user = api2.account_verify_credentials()
    time.sleep(1)
    api.account_unfollow(user)
    time.sleep(2)

    updates = []
    listener = CallbackStreamListener(
        local_update_handler=updates.append,
    )
    
    posted = []
    def do_activities():
        vcr.match_on = ["path"]
        time.sleep(5)
        posted.append(api.status_post("it's cool guy"))
        time.sleep(10)
        streaming_close()
        
    t = threading.Thread(args=(), target=do_activities)
    t.start()
    
    stream = api.stream_user(listener, run_async=True)
    time.sleep(20)
    stream.close()
        
    assert len(updates) == 1
    assert updates[0].id == posted[0].id
    
    t.join()
    unpatch_streaming()

@pytest.mark.vcr(match_on=['path'])
def test_stream_direct(api, api2, vcr):
    time.sleep(1)
    patch_streaming()
    
    # Make sure we are in the right state to receive updates from api2
    time.sleep(1)
    user = api2.account_verify_credentials()
    time.sleep(1)
    api.account_follow(user)
    time.sleep(2)

    vcr.match_on = ["path"]
    conversations = []
    listener = CallbackStreamListener(
        conversation_handler=conversations.append,
    )
    
    def do_activities():
        vcr.match_on = ["path"]
        time.sleep(5)
        api2.status_post("@mastodonpy_test todo funny text here", visibility = "direct")
        api2.status_post("you can't say that on television")
        time.sleep(10)
        streaming_close()
        
    t = threading.Thread(args=(), target=do_activities)
    t.start()
    
    stream = api.stream_direct(listener, run_async=True)
    time.sleep(20)
    stream.close()

    assert len(conversations) == 1
    t.join()
    unpatch_streaming()
    
@pytest.mark.vcr()
def test_stream_healthy(api_anonymous):
    assert api_anonymous.stream_healthy()


@pytest.mark.vcr(match_on=['method', 'path', 'query'])
def test_stream_public_only_media(api):
    media = api.media_post('tests/image.jpg', synchronous=True, file_name='only-media.jpg')
    updates = []
    media_updates = []
    streams = []
    posted = []
    patch_streaming()
    try:
        for only_media, received in [(False, updates), (True, media_updates)]:
            stream = api.stream_public(
                CallbackStreamListener(update_handler=received.append),
                local=True, only_media=only_media, run_async=True,
            )
            streams.append(stream)
            # Open one connection at a time: VCR temporarily unpatches HTTP
            # globally while sending a live request. A second concurrent open
            # during that window could bypass the recorder.
            deadline = time.monotonic() + 30
            while len(real_connections) < len(streams) and stream.connection is None:
                assert time.monotonic() < deadline, 'Public stream did not connect'
                time.sleep(0.1)

        # VCR buffers live SSE responses until streaming_close(). On replay,
        # the handles receive the already buffered responses immediately.
        if real_connections:
            time.sleep(2)

        posted.append(api.status_post('SSE text-only stream test', visibility='public'))
        posted.append(api.status_post(
            'SSE media-only stream test', media_ids=[media], visibility='public',
        ))
        if real_connections:
            time.sleep(20)  # Allow background distribution to both streams.
        streaming_close()
        for stream in streams:
            stream._thread.join(timeout=10)
            assert not stream.is_alive(), 'SSE recording did not finish'

        assert len(updates) == 2
        assert {status.id for status in updates} == {status.id for status in posted}
        assert [status.id for status in media_updates] == [posted[1].id]
        assert media_updates[0].media_attachments[0].id == media.id
    finally:
        streaming_close()
        for stream in streams:
            stream.close()
            stream._thread.join(timeout=5)
        for status in posted:
            api.status_delete(status, delete_media=True)
