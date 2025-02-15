Reading data: Timelines
=======================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

These functions allow you to access the timelines a logged in
user could see, as well as hashtag timelines and the public (federated)
and local timelines. For the public, local and hashtag timelines,
access is allowed even when not authenticated if the instance admin has enabled this functionality.

.. _timeline():
.. automethod:: Mastodon.timeline
.. automethod:: Mastodon.timeline_home
.. automethod:: Mastodon.timeline_local
.. _timeline_public():
.. automethod:: Mastodon.timeline_public
.. _timeline_hashtag():
.. automethod:: Mastodon.timeline_hashtag
.. automethod:: Mastodon.timeline_list
.. automethod:: Mastodon.conversations
    