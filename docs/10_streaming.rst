Streaming
=========
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

These functions allow access to the streaming API. Since Mastodon v4.2.0 the support for anonymous streaming api access was dropped.
You need to generate an access token now.

If `run_async` is False, these  methods block forever (or until an error is encountered).

If `run_async` is True, the listener will listen on another thread and these methods
will return a handle corresponding to the open connection. If, in addition, `reconnect_async` is True,
the thread will attempt to reconnect to the streaming API if any errors are encountered, waiting
`reconnect_async_wait_sec` seconds between reconnection attempts. Note that no effort is made
to "catch up" - events created while the connection is broken will not be received. If you need to make
sure to get absolutely all notifications / deletes / toots, you will have to do that manually, e.g.
using the `on_abort` handler to fill in events since the last received one and then reconnecting.
Both `run_async` and `reconnect_async` default to false, and you'll have to set each to true
separately to get the behaviour described above.

The connection may be closed at any time by calling the handles close() method. The
current status of the handler thread can be checked with the handles is_alive() function,
and the streaming status can be checked by calling is_receiving().

The streaming functions take instances of `StreamListener` as the `listener` parameter.
A `CallbackStreamListener` class that allows you to specify function callbacks
directly is included for convenience.

For new well-known events implement the streaming function in `StreamListener` or `CallbackStreamListener`.
The function name is `on_` + the event name. If the event name contains dots, they are replaced with
underscored, e.g. for an event called 'status.update' the listener function should be named `on_status_update`.

It may be that future Mastodon versions will come with completely new (unknown) event names.
If you want to do something when such an event is received, override the listener function `on_unknown_event`. 
This has an additional parameter `name` which informs about the name of the event. `unknown_event` contains the 
content of the event. Alternatively, a callback function can be passed in the `unknown_event_handler` parameter 
in the `CallbackStreamListener` constructor.

Note that the `unknown_event` handler is *not* guaranteed to receive events once they have been implemented.
Events will only go to this handler temporarily, while Mastodon.py has not been updated. Changes to what events
do and do not go into the handler will not be considered a breaking change. If you want to handle a new event whose
name you _do_ know, define an appropriate handler in your StreamListener, which will work even if it is not listed here.

When in not-async mode or async mode without async_reconnect, the stream functions may raise
various exceptions: `MastodonMalformedEventError` if a received event cannot be parsed and
`MastodonNetworkError` if any connection problems occur.

Mastodon.py currently does not support websocket based, multiplexed streams, but might in the future.

Stream endpoints
----------------
.. automethod:: Mastodon.stream_user
.. automethod:: Mastodon.stream_public
.. automethod:: Mastodon.stream_local
.. automethod:: Mastodon.stream_hashtag
.. automethod:: Mastodon.stream_list
.. automethod:: Mastodon.stream_healthy

StreamListener
--------------

.. autoclass:: StreamListener
.. automethod:: StreamListener.on_update
.. automethod:: StreamListener.on_notification
.. automethod:: StreamListener.on_delete
.. automethod:: StreamListener.on_conversation
.. automethod:: StreamListener.on_status_update
.. automethod:: StreamListener.on_unknown_event
.. automethod:: StreamListener.on_abort
.. automethod:: StreamListener.handle_heartbeat

CallbackStreamListener
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CallbackStreamListener

