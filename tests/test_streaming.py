import six
import pytest
import itertools
from mastodon.streaming import StreamListener
from mastodon.Mastodon import MastodonMalformedEventError



class Listener(StreamListener):
    def __init__(self):
        self.updates = []
        self.notifications = []
        self.deletes = []
        self.heartbeats = 0

    def on_update(self, status):
        self.updates.append(status)

    def on_notification(self, notification):
        self.notifications.append(notification)

    def on_delete(self, status_id):
        self.deletes.append(status_id)

    def on_blahblah(self, data):
        pass

    def handle_heartbeat(self):
        self.heartbeats += 1

    def handle_stream_(self, lines):
        """Test helper to avoid littering all tests with six.b()."""
        return self.handle_stream(map(six.b, lines))


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
    assert listener.deletes == [123]


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
    assert listener.deletes == [123]
    assert listener.heartbeats == 2


def test_unknown_event():
    """Be tolerant of new event types"""
    listener = Listener()
    listener.handle_stream_([
        'event: blahblah',
        'data: {}',
        '',
    ])
    assert listener.updates == []
    assert listener.notifications == []
    assert listener.deletes == []
    assert listener.heartbeats == 0


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
