Accounts, relationships and lists
=================================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Accounts
--------
These functions allow you to get information about accounts and associated data as well as update that data - profile data (incuding pinned statuses and endorsements) for the logged in users account, and notes for everyone else

Reading
~~~~~~~~
.. automethod:: Mastodon.account_verify_credentials
.. automethod:: Mastodon.me

.. automethod:: Mastodon.account
.. automethod:: Mastodon.account_search
.. automethod:: Mastodon.account_lookup
.. automethod:: Mastodon.accounts

.. automethod:: Mastodon.featured_tags
.. automethod:: Mastodon.featured_tag_suggestions
.. automethod:: Mastodon.account_featured_tags

.. automethod:: Mastodon.endorsements

.. automethod:: Mastodon.account_statuses
.. automethod:: Mastodon.account_familiar_followers

.. automethod:: Mastodon.account_lists

Writing
~~~~~~~
.. automethod:: Mastodon.account_update_credentials

.. automethod:: Mastodon.account_endorse
.. automethod:: Mastodon.account_unendorse

.. automethod:: Mastodon.account_note_set

.. automethod:: Mastodon.tag_feature
.. automethod:: Mastodon.tag_unfeature

.. _status_pin():
.. automethod:: Mastodon.status_pin
.. _status_unpin():    
.. automethod:: Mastodon.status_unpin

.. automethod:: Mastodon.account_delete_avatar
.. automethod:: Mastodon.account_delete_header

Deprecated
~~~~~~~~~~
.. automethod:: Mastodon.account_pin
.. automethod:: Mastodon.account_unpin

.. automethod:: Mastodon.featured_tag_create
.. automethod:: Mastodon.featured_tag_delete
    
Following and followers
-----------------------
These functions allow you to get information about the logged in users followers and users that the logged in users follows as well as follow requests and follow suggestions, and to
manage that data - most importantly, follow and unfollow users.

Reading
~~~~~~~
.. automethod:: Mastodon.account_followers
.. automethod:: Mastodon.account_following    
.. automethod:: Mastodon.account_relationships
.. automethod:: Mastodon.follows

.. automethod:: Mastodon.follow_requests

.. automethod:: Mastodon.suggestions

Writing
~~~~~~~
.. _account_follow():
.. automethod:: Mastodon.account_follow
.. automethod:: Mastodon.account_unfollow

.. automethod:: Mastodon.follow_request_authorize
.. automethod:: Mastodon.follow_request_reject

.. automethod:: Mastodon.suggestion_delete

Mutes and blocks
----------------
These functions allow you to get information about accounts and domains that are muted or blocked by the logged in user, and to block and mute users and domains

Reading
~~~~~~~
.. automethod:: Mastodon.mutes
.. automethod:: Mastodon.blocks
.. automethod:: Mastodon.domain_blocks
    
Writing
~~~~~~~
.. automethod:: Mastodon.account_mute
.. automethod:: Mastodon.account_unmute

.. automethod:: Mastodon.account_block
.. automethod:: Mastodon.account_unblock

.. automethod:: Mastodon.account_remove_from_followers

.. automethod:: Mastodon.domain_block
.. automethod:: Mastodon.domain_unblock

Lists
-----
These functions allow you to view information about lists as well as to create and update them.
By default, the maximum number of lists for a user is 50.

Reading
~~~~~~~
.. automethod:: Mastodon.lists
.. automethod:: Mastodon.list
.. automethod:: Mastodon.list_accounts

Writing
~~~~~~~
.. automethod:: Mastodon.list_create
.. automethod:: Mastodon.list_update
.. automethod:: Mastodon.list_delete
.. automethod:: Mastodon.list_accounts_add
.. automethod:: Mastodon.list_accounts_delete


Following tags
--------------
These functions allow you to get information about tags that the logged in user is following and to follow 
and unfollow tags.

Reading
~~~~~~~
.. automethod:: Mastodon.followed_tags

Writing
~~~~~~~
.. automethod:: Mastodon.tag_follow
.. automethod:: Mastodon.tag_unfollow
    