import pytest
import itertools
from mastodon.streaming import StreamListener, CallbackStreamListener
from mastodon.Mastodon import MastodonMalformedEventError
from mastodon import Mastodon

import threading
import time

import select
import sys

streaming_is_patched = False
real_connections = []
close_connections = False

@pytest.fixture(scope='module')
def vcr_config():
    return {
        "match_on": ["path"],
    }

def patch_streaming():
    # For monkeypatching so we can make vcrpy better
    import vcr.stubs

    global streaming_is_patched
    global close_connections
    if streaming_is_patched is True:
        return
    streaming_is_patched = True
    
    real_get_response = vcr.stubs.VCRConnection.getresponse
    def fake_get_response(*args, **kwargs):
        global close_connections
        close_connections = False
        if args[0]._vcr_request.path.startswith("/api/v1/streaming/"):
            real_connections.append(args[0].real_connection)
            real_connection_real_get_response = args[0].real_connection.getresponse
            def fakeRealConnectionGetresponse(*args, **kwargs):
                response = real_connection_real_get_response(*args, **kwargs)
                real_body = b""
                try:
                    while close_connections is False:
                        if len(select.select([response], [], [], 0.01)[0]) > 0:
                            chunk = response.read(1)
                            real_body += chunk
                except AttributeError: 
                    pass # Connection closed
                response.read = (lambda: real_body)
                return response
            args[0].real_connection.getresponse = fakeRealConnectionGetresponse
        return real_get_response(*args, **kwargs)
    vcr.stubs.VCRConnection.getresponse = fake_get_response

def streaming_close():
    global real_connections
    global close_connections
    for connection in real_connections:
        connection.close()
    real_connections = []
    close_connections = True
    
class Listener(StreamListener):
    def __init__(self):
        self.updates = []
        self.notifications = []
        self.deletes = []
        self.heartbeats = 0
        self.bla_called = False
        self.do_something_called = False

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


@pytest.mark.parametrize('events', itertools.permutations([
    ['event: update', 'data: {"foo": "bar"}', ''],
    ['event: notification', 'data: {"foo": "bar"}', ''],
    ['event: delete', 'data: 123', ''],
    [':toot toot'],
    [':beep beep'],
]))
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

@pytest.mark.vcr(match_on=['path'])
def test_stream_user_direct(api, api2, api3, vcr):
    # NB: Streaming tests *run only on 3.9* until someone figures out why the patch for vcrpy isn't working on versions > 1.0.2
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
    
@pytest.mark.vcr(match_on=['path'])
def test_stream_user_local(api, api2, vcr):
    # NB: Streaming tests *run only on 3.9* until someone figures out why the patch for vcrpy isn't working on versions > 1.0.2
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
        # Have to do some other network event after the first one for vcrpy reasons
        api2.status_post("it's cool guy too")
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

@pytest.mark.vcr(match_on=['path'])
def test_stream_direct(api, api2, vcr):
    # NB: Streaming test *run only on 3.9* until someone figures out why the patch for vcrpy isn't working on versions > 1.0.2
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

@pytest.mark.vcr()
def test_stream_healthy(api_anonymous):
    assert api_anonymous.stream_healthy()
