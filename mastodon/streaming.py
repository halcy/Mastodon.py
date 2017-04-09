'''
Handlers for the Streaming API:
https://github.com/tootsuite/mastodon/blob/master/docs/Using-the-API/Streaming-API.md
'''

import json
import logging
import six


log = logging.getLogger(__name__)


class MalformedEventError(Exception):
    '''Raised when the server-sent event stream is malformed.'''
    pass


class StreamListener(object):
    '''Callbacks for the streaming API. Create a subclass, override the on_xxx
    methods for the kinds of events you're interested in, then pass an instance
    of your subclass to Mastodon.user_stream(), Mastodon.public_stream(), or
    Mastodon.hashtag_stream().'''

    def on_update(self, status):
        '''A new status has appeared! 'status' is the parsed JSON dictionary
        describing the status.'''
        pass

    def on_notification(self, notification):
        '''A new notification. 'notification' is the parsed JSON dictionary
        describing the notification.'''
        pass

    def on_delete(self, status_id):
        '''A status has been deleted. status_id is the status' integer ID.'''
        pass

    def handle_heartbeat(self):
        '''The server has sent us a keep-alive message. This callback may be
        useful to carry out periodic housekeeping tasks, or just to confirm
        that the connection is still open.'''

    def handle_stream(self, lines):
        '''
        Handles a stream of events from the Mastodon server. When each event
        is received, the corresponding .on_[name]() method is called.

        lines: an iterable of lines of bytes sent by the Mastodon server, as
        returned by requests.Response.iter_lines().
        '''
        event = {}
        for raw_line in lines:
            try:
                line = raw_line.decode('utf-8')
            except UnicodeDecodeError as err:
                six.raise_from(
                    MalformedEventError("Malformed UTF-8", line),
                    err
                )

            if line.startswith(':'):
                self.handle_heartbeat()
            elif line == '':
                # end of event
                self._despatch(event)
                event = {}
            else:
                key, value = line.split(': ', 1)
                # According to the MDN spec, repeating the 'data' key
                # represents a newline(!)
                if key in event:
                    event[key] += '\n' + value
                else:
                    event[key] = value

        # end of stream
        if event:
            log.warn("outstanding partial event at end of stream: %s", event)

    def _despatch(self, event):
        try:
            name = event['event']
            data = event['data']
            payload = json.loads(data)
        except KeyError as err:
            six.raise_from(
                MalformedEventError('Missing field', err.args[0], event),
                err
            )
        except ValueError as err:
            # py2: plain ValueError
            # py3: json.JSONDecodeError, a subclass of ValueError
            six.raise_from(
                MalformedEventError('Bad JSON', data),
                err
            )

        handler_name = 'on_' + name
        try:
            handler = getattr(self, handler_name)
        except AttributeError:
            log.warn("Unhandled event '%s'", name)
        else:
            # TODO: allow handlers to return/raise to stop streaming cleanly
            handler(payload)

