"""
Handlers for the Streaming API:
https://github.com/tootsuite/mastodon/blob/master/docs/Using-the-API/Streaming-API.md
"""

import json
import six
from mastodon import Mastodon
from mastodon.Mastodon import MastodonMalformedEventError, MastodonNetworkError, MastodonReadTimeout
from requests.exceptions import ChunkedEncodingError, ReadTimeout

class StreamListener(object):
    """Callbacks for the streaming API. Create a subclass, override the on_xxx
    methods for the kinds of events you're interested in, then pass an instance
    of your subclass to Mastodon.user_stream(), Mastodon.public_stream(), or
    Mastodon.hashtag_stream()."""

    def on_update(self, status):
        """A new status has appeared! 'status' is the parsed JSON dictionary
        describing the status."""
        pass

    def on_notification(self, notification):
        """A new notification. 'notification' is the parsed JSON dictionary
        describing the notification."""
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

    def on_delete(self, status_id):
        """A status has been deleted. status_id is the status' integer ID."""
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

        response; a requests response object with the open stream for reading.
        """
        event = {}
        line_buffer = bytearray()
        try:
            for chunk in response.iter_content(chunk_size = 1):
                if chunk:
                    if chunk == b'\n':
                        try:
                            line = line_buffer.decode('utf-8')
                        except UnicodeDecodeError as err:
                            exception = MastodonMalformedEventError("Malformed UTF-8")
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
                        line_buffer.extend(chunk)
        except ChunkedEncodingError as err:
            exception = MastodonNetworkError("Server ceased communication.")
            self.on_abort(exception)
            six.raise_from(
                exception,
                err
            )
        except MastodonReadTimeout as err:
            exception = MastodonReadTimeout("Timed out while reading from server."),
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
            payload = json.loads(data, object_hook = Mastodon._Mastodon__json_hooks)
        except KeyError as err:
            exception = MastodonMalformedEventError('Missing field', err.args[0], event)
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
           
        handler_name = 'on_' + name
        try:
            handler = getattr(self, handler_name)
        except AttributeError as err:
            exception = MastodonMalformedEventError('Bad event type', name)
            self.on_abort(exception)
            six.raise_from(
               exception,
               err
            )
        else:
            handler(payload)

class CallbackStreamListener(StreamListener):
    """
    Simple callback stream handler class.
    Can optionally additionally send local update events to a separate handler.
    """
    def __init__(self, update_handler = None, local_update_handler = None, delete_handler = None, notification_handler = None):
        super(CallbackStreamListener, self).__init__()
        self.update_handler = update_handler
        self.local_update_handler = local_update_handler
        self.delete_handler = delete_handler
        self.notification_handler = notification_handler
        
    def on_update(self, status):
        if self.update_handler != None:
            self.update_handler(status)
        
        try:
            if self.local_update_handler != None and not "@" in status["account"]["acct"]:
                self.local_update_handler(status)
        except Exception as err:
            six.raise_from(
               MastodonMalformedEventError('received bad update', status),
               err
            )
    
    def on_delete(self, deleted_id):
        if self.delete_handler != None:
            self.delete_handler(deleted_id)
    
    def on_notification(self, notification):
        if self.notification_handler != None:
            self.notification_handler(notification)