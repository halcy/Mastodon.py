Instance-wide data and search
=============================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Instance information
--------------------
These functions allow you to fetch information associated with the
current instance as well as data from the instance-wide profile directory.

.. _instance():
.. automethod:: Mastodon.instance
.. automethod:: Mastodon.instance_v1    
.. automethod:: Mastodon.instance_v2
.. automethod:: Mastodon.instance_activity
.. automethod:: Mastodon.instance_peers
.. automethod:: Mastodon.instance_health
.. automethod:: Mastodon.instance_nodeinfo
.. automethod:: Mastodon.instance_rules
.. automethod:: Mastodon.instance_extended_description
.. automethod:: Mastodon.instance_terms_of_service
    
Profile directory
~~~~~~~~~~~~~~~~~
.. automethod:: Mastodon.directory

Emoji
~~~~~
.. automethod:: Mastodon.custom_emojis

Announcements
-------------
These functions allow you to fetch announcements, mark annoucements read and modify reactions.

Reading
~~~~~~~
.. automethod:: Mastodon.announcements

Writing
~~~~~~~
.. automethod:: Mastodon.announcement_dismiss
.. automethod:: Mastodon.announcement_reaction_create
.. automethod:: Mastodon.announcement_reaction_delete

Trends
------
These functions, when enabled, allow you to fetch trending tags, statuses and links.

.. _trending_tags():
.. automethod:: Mastodon.trending_tags
.. _trending_statuses():
.. automethod:: Mastodon.trending_statuses
.. _trending_links():    
.. automethod:: Mastodon.trending_links
.. automethod:: Mastodon.trends

Search
------
These functions allow you to search for users, tags and, when enabled, full text, by default within your own posts and those you have interacted with.

.. automethod:: Mastodon.search
.. automethod:: Mastodon.search_v2

Domain blocks
-------------
.. automethod:: Mastodon.instance_domain_blocks

Translation support
-------------------
.. automethod:: Mastodon.instance_languages
.. automethod:: Mastodon.instance_translation_languages
    