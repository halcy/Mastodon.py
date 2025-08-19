Statuses, media and polls
=========================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Statuses
--------
These functions allow you to get information about single statuses and to post and update them, as well as to favourite, bookmark, mute reblog ("boost") and to undo all of those.
For status pinning, check out TODO and TODO on the accounts page.

Reading
~~~~~~~
.. automethod:: Mastodon.status
.. automethod:: Mastodon.status_context
.. automethod:: Mastodon.status_reblogged_by
.. automethod:: Mastodon.status_favourited_by
.. automethod:: Mastodon.status_card
.. automethod:: Mastodon.status_history
.. automethod:: Mastodon.status_source
.. automethod:: Mastodon.statuses

.. automethod:: Mastodon.favourites

.. automethod:: Mastodon.bookmarks

Writing
~~~~~~~
.. _status_post():
.. automethod:: Mastodon.status_post
.. automethod:: Mastodon.status_reply
.. automethod:: Mastodon.toot
.. _make_poll():
.. automethod:: Mastodon.make_poll

.. automethod:: Mastodon.status_reblog
.. automethod:: Mastodon.status_unreblog

.. automethod:: Mastodon.status_favourite
.. automethod:: Mastodon.status_unfavourite

.. automethod:: Mastodon.status_mute
.. automethod:: Mastodon.status_unmute

.. automethod:: Mastodon.status_bookmark
.. automethod:: Mastodon.status_unbookmark

.. automethod:: Mastodon.status_delete
.. _status_update():    
.. automethod:: Mastodon.status_update
.. automethod:: Mastodon.generate_media_edit_attributes

Scheduled statuses
------------------
These functions allow you to get information about scheduled statuses and to update scheduled statuses that already exist.
To create new scheduled statuses, use :ref:`status_post() <status_post()>` with the `scheduled_at` parameter.

Reading
~~~~~~~
.. automethod:: Mastodon.scheduled_statuses
.. automethod:: Mastodon.scheduled_status

Writing
~~~~~~~
.. automethod:: Mastodon.scheduled_status_update
.. automethod:: Mastodon.scheduled_status_delete

Media
-----
This function allows you to upload media to Mastodon and update media uploads.
The returned media IDs (Up to 4 at the same time on a default configuration Mastodon instance) can then be used with post_status to attach media to statuses.

.. _media_post():
.. automethod:: Mastodon.media_post
.. automethod:: Mastodon.media_update
.. automethod:: Mastodon.media

Polls
-----
This function allows you to get and refresh information about polls as well as to vote in polls

Reading
~~~~~~~
.. automethod:: Mastodon.poll

Writing
~~~~~~~
.. automethod:: Mastodon.poll_vote

Translation
-----------
These functions allow you to get machine translations for statuses, if the instance supports it.

.. automethod:: Mastodon.status_translate

    
