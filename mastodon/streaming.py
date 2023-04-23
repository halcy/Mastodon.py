"""
Handlers for the Streaming API:
https://github.com/mastodon/documentation/blob/master/content/en/methods/timelines/streaming.md
"""

import json
import six
try:
    from inspect import signature
except:
    pass

from mastodon import Mastodon
from mastodon.Mastodon import MastodonMalformedEventError, MastodonNetworkError, MastodonReadTimeout
from requests.exceptions import ChunkedEncodingError, ReadTimeout, ConnectionError


class StreamListener(object):
    """Callbacks for the streaming API. Create a subclass, override the on_xxx
    methods for the kinds of events you're interested in, then pass an instance
    of your subclass to Mastodon.user_stream(), Mastodon.public_stream(), or
    Mastodon.hashtag_stream()."""

    def on_update(self, status):
        """A new status has appeared. `status` is the parsed `status dict`
        describing the status."""
        pass

    def on_delete(self, status_id):
        """A status has been deleted. `status_id` is the status' integer ID."""
        pass

    def on_notification(self, notification):
        """A new notification. `notification` is the parsed `notification dict`
        describing the notification."""
        pass

    def on_filters_changed(self):
        """Filters have changed. Does not contain a payload, you will have to
           refetch filters yourself."""
        pass

    def on_conversation(self, conversation):
        """A direct message (in the direct stream) has been received. `conversation`
        is the parsed `conversation dict` dictionary describing the conversation"""
        pass

    def on_announcement(self, annoucement):
        """A new announcement has been published. `announcement` is the parsed
        `announcement dict` describing the newly posted announcement."""
        pass

    def on_announcement_reaction(self, TODO):
        """Someone has reacted to an announcement. TODO: what is payload lol"""
        pass

    def on_announcement_delete(self, annoucement_id):
        """An announcement has been deleted. `annoucement_id` is the id of the
        deleted announcement."""
        pass

    def on_status_update(self, status):
        """A status has been edited. 'status' is the parsed JSON dictionary
        describing the updated status."""
        pass

    def on_encrypted_message(self, unclear):
        """An encrypted message has been received. Currently unused."""
        pass

    def on_abort(self, err):
        """There was a connection error, read timeout or other error fatal to
        the streaming connection. The exception object about to be raised
        is passed to this function for reference.

        Note that the exception will be raised properly once you return from this
        function, so if you are using this handler to reconnect, either never
        return or start a thread and then catch and ignore the exception.
        """
        pass

    def on_unknown_event(self, name, unknown_event=None):
        """An unknown mastodon API event has been received. The name contains the event-name and unknown_event
        contains the content of the unknown event.
        """
        pass

    def handle_heartbeat(self):
        """The server has sent us a keep-alive message. This callback may be
        useful to carry out periodic housekeeping tasks, or just to confirm
        that the connection is still open."""
        pass

    def handle_stream(self, response):
        """
        Handles a stream of events from the Mastodon server. When each event
        is received, the corresponding .on_[name]() method is called.

        When the Mastodon API changes, the on_unknown_event(name, content)
        function is called.
        The default behavior is to throw an error. Define a callback handler
        to intercept unknown events if needed (and avoid errors)

        response; a requests response object with the open stream for reading.
        """
        event = {}
        line_buffer = bytearray()
        try:
            for chunk in response.iter_content(chunk_size=1):
                if chunk:
                    for chunk_part in chunk:
                        chunk_part = bytearray([chunk_part])
                        if chunk_part == b'\n':
                            try:
                                line = line_buffer.decode('utf-8')
                            except UnicodeDecodeError as err:
                                exception = MastodonMalformedEventError(
                                    "Malformed UTF-8")
                                self.on_abort(exception)
                                six.raise_from(
                                    exception,
                                    err
                                )
                            if line == '':
                                self._dispatch(event)
                                event = {}
                            else:
                                event = self._parse_line(line, event)
                            line_buffer = bytearray()
                        else:
                            line_buffer.extend(chunk_part)
        except ChunkedEncodingError as err:
            exception = MastodonNetworkError("Server ceased communication.")
            self.on_abort(exception)
            six.raise_from(
                exception,
                err
            )
        except ReadTimeout as err:
            exception = MastodonReadTimeout(
                "Timed out while reading from server."),
            self.on_abort(exception)
            six.raise_from(
                exception,
                err
            )
        except ConnectionError as err:
            exception = MastodonNetworkError(
                "Requests reports connection error."),
            self.on_abort(exception)
            six.raise_from(
                exception,
                err
            )

    def _parse_line(self, line, event):
        if line.startswith(':'):
            self.handle_heartbeat()
        else:
            try:
                key, value = line.split(': ', 1)
            except:
                exception = MastodonMalformedEventError("Malformed event.")
                self.on_abort(exception)
                raise exception
            # According to the MDN spec, repeating the 'data' key
            # represents a newline(!)
            if key in event:
                event[key] += '\n' + value
            else:
                event[key] = value
        return event

    def _dispatch(self, event):
        try:
            name = event['event']
            data = event['data']
            try:
                for_stream = json.loads(event['stream'])
            except:
                for_stream = None
            payload = json.loads(data, object_hook=Mastodon._Mastodon__json_hooks)
        except KeyError as err:
            exception = MastodonMalformedEventError(
                'Missing field', err.args[0], event)
            self.on_abort(exception)
            six.raise_from(
                exception,
                err
            )
        except ValueError as err:
            # py2: plain ValueError
            # py3: json.JSONDecodeError, a subclass of ValueError
            exception = MastodonMalformedEventError('Bad JSON', data)
            self.on_abort(exception)
            six.raise_from(
                exception,
                err
            )

        # New mastodon API also supports event names with dots,
        # specifically, status_update.
        handler_name = 'on_' + name.replace('.', '_')

        # A generic way to handle unknown events to make legacy code more stable for future changes
        handler = getattr(self, handler_name, self.on_unknown_event)
        try:
            handler_args = list(signature(handler).parameters)
        except:
            handler_args = handler.__code__.co_varnames[:handler.__code__.co_argcount]

        # The "for_stream" is right now only theoretical - it's only supported on websocket,
        # and we do not support websocket based multiplexed streams (yet).
        if "for_stream" in handler_args:
            if handler != self.on_unknown_event:
                handler(payload, for_stream)
            else:
                handler(name, payload, for_stream)
        else:
            if handler != self.on_unknown_event:
                if handler == self.on_filters_changed:
                    handler()
                else:
                    handler(payload)
            else:
                handler(name, payload)


class CallbackStreamListener(StreamListener):
    """
    Simple callback stream handler class.
    Can optionally additionally send local update events to a separate handler.
    Define an unknown_event_handler for new Mastodon API events. This handler is
    *not* guaranteed to receive these events forever, and should only be used
    for diagnostics.
    """

    def __init__(self,
                 update_handler=None,
                 local_update_handler=None,
                 delete_handler=None,
                 notification_handler=None,
                 conversation_handler=None,
                 unknown_event_handler=None,
                 status_update_handler=None,
                 filters_changed_handler=None,
                 announcement_handler=None,
                 announcement_reaction_handler=None,
                 announcement_delete_handler=None,
                 encryted_message_handler=None
                 ):
        super(CallbackStreamListener, self).__init__()
        self.update_handler = update_handler
        self.local_update_handler = local_update_handler
        self.delete_handler = delete_handler
        self.notification_handler = notification_handler
        self.filters_changed_handler = filters_changed_handler
        self.conversation_handler = conversation_handler
        self.unknown_event_handler = unknown_event_handler
        self.status_update_handler = status_update_handler
        self.announcement_handler = announcement_handler
        self.announcement_reaction_handler = announcement_reaction_handler
        self.announcement_delete_handler = announcement_delete_handler
        self.encryted_message_handler = encryted_message_handler

    def on_update(self, status):
        if self.update_handler is not None:
            self.update_handler(status)

        try:
            if self.local_update_handler is not None and not "@" in status["account"]["acct"]:
                self.local_update_handler(status)
        except Exception as err:
            six.raise_from(
                MastodonMalformedEventError('received bad update', status),
                err
            )

    def on_delete(self, deleted_id):
        if self.delete_handler is not None:
            self.delete_handler(deleted_id)

    def on_notification(self, notification):
        if self.notification_handler is not None:
            self.notification_handler(notification)

    def on_filters_changed(self):
        if self.filters_changed_handler is not None:
            self.filters_changed_handler()

    def on_conversation(self, conversation):
        if self.conversation_handler is not None:
            self.conversation_handler(conversation)

    def on_announcement(self, annoucement):
        if self.announcement_handler is not None:
            self.announcement_handler(annoucement)

    def on_announcement_reaction(self, TODO):
        if self.announcement_reaction_handler is not None:
            self.announcement_reaction_handler(TODO)

    def on_announcement_delete(self, annoucement_id):
        if self.announcement_delete_handler is not None:
            self.announcement_delete_handler(annoucement_id)

    def on_status_update(self, status):
        if self.status_update_handler is not None:
            self.status_update_handler(status)

    def on_encrypted_message(self, unclear):
        if self.encryted_message_handler is not None:
            self.encryted_message_handler(unclear)

    def on_unknown_event(self, name, unknown_event=None):
        if self.unknown_event_handler is not None:
            self.unknown_event_handler(name, unknown_event)
