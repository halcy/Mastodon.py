"""
Handlers for the Streaming API:
https://github.com/tootsuite/mastodon/blob/master/docs/Using-the-API/Streaming-API.md
"""

import json
import six
from mastodon import Mastodon
from mastodon.Mastodon import MastodonMalformedEventError

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
        for chunk in response.iter_content(chunk_size = 1):
            if chunk:
                if chunk == b'\n':
                    try:
                        line = line_buffer.decode('utf-8')
                    except UnicodeDecodeError as err:
                        six.raise_from(
                            MastodonMalformedEventError("Malformed UTF-8"),
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
        
    def _parse_line(self, line, event):
        if line.startswith(':'):
            self.handle_heartbeat()
        else:
            key, value = line.split(': ', 1)
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
           six.raise_from(
               MastodonMalformedEventError('Missing field', err.args[0], event),
               err
           )
        except ValueError as err:
           # py2: plain ValueError
           # py3: json.JSONDecodeError, a subclass of ValueError
           six.raise_from(
               MastodonMalformedEventError('Bad JSON', data),
               err
           )
           
        handler_name = 'on_' + name
        try:
            handler = getattr(self, handler_name)
        except AttributeError as err:
            six.raise_from(
               MastodonMalformedEventError('Bad event type', name),
               err
            )
        else:
            # TODO: allow handlers to return/raise to stop streaming cleanly
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