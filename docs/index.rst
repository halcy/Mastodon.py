Mastodon.py
===========
.. py:module:: mastodon
.. py:class: Mastodon

.. code-block:: python

   from mastodon import Mastodon

   # Register app - only once!
   '''
   Mastodon.create_app(
        'pytooterapp', 
         to_file = 'pytooter_clientcred.txt'
   )
   '''

   # Log in - either every time, or use persisted
   '''
   mastodon = Mastodon(client_id = 'pytooter_clientcred.txt')
   mastodon.log_in(
       'pytooter', 
       'incrediblygoodpassword', 
       to_file = 'pytooter_usercred.txt'
   )
   '''

   # Create actual instance
   mastodon = Mastodon(
       client_id = 'pytooter_clientcred.txt', 
       access_token = 'pytooter_usercred.txt'
   )
   mastodon.toot('Tooting from python!')

`Mastodon`_ is an ostatus based twitter-like federated social 
network node. It has an API that allows you to interact with its 
every aspect. This is a simple python wrapper for that api, provided
as a single python module. By default, it talks to the 
`Mastodon flagship instance`_, but it can be set to talk to any 
node running Mastodon.

A note about IDs
----------------
Mastodons API uses IDs in several places: User IDs, Toot IDs, ...

While debugging, it might be tempting to copy-paste in IDs from the
web interface into your code. This will not work, as the IDs on the web
interface and in the URLs are not the same as the IDs used internally
in the API, so don't do that.

Return values
-------------
Unless otherwise specified, all data is returned as python 
dictionaries, matching the JSON format used by the API.

User dicts
~~~~~~~~~~
.. code-block:: python

    {
     'display_name': The user's display name
     'acct': The user's account name as username@domain (@domain omitted for local users)
     'following_count': How many people they follow
     'url': Their URL; usually 'https://mastodon.social/users/<acct>'
     'statuses_count': How many statuses they have
     'followers_count': How many followers they have
     'avatar': URL for their avatar
     'note': Their bio
     'header': URL for their header image
     'id': Same as <numerical id>
     'username': The username (what you @ them with)
    }

Toot dicts
~~~~~~~~~~
.. code-block:: python

   mastodon.toot("Hello from Python")
   # Returns the following dictionary:
   {
    'sensitive': Denotes whether the toot is marked sensitive
    'created_at': Creation time
    'mentions': A list of account dicts mentioned in the toot
    'uri': Descriptor for the toot
           EG 'tag:mastodon.social,2016-11-25:objectId=<id>:objectType=Status'
    'tags': A list of hashtag dicts used in the toot
    'in_reply_to_id': Numerical id of the toot this toot is in response to
    'id': Numerical id of this toot
    'reblogs_count': Number of reblogs
    'favourites_count': Number of favourites
    'reblog': Denotes whether the toot is a reblog
    'url': URL of the toot
    'content': Content of the toot, as HTML: '<p>Hello from Python</p>'
    'favourited': Denotes whether the logged in user has favourited this toot
    'account': Account dict for the logged in account
   }

Relationship dicts
~~~~~~~~~~~~~~~~~~
.. code-block:: python

    mastodon.account_follow(<numerical id>)
    # Returns
    {
     'followed_by': Boolean denoting whether they follow you back
     'following': Boolean denoting whether you follow them
     'id': Numerical id (same one as <numerical id>)
     'blocking': Boolean denoting whether you are blocking them
    }

Context dicts
~~~~~~~~~~~~~
.. code-block:: python

    mastodon.status_context(<numerical id>)
    # Returns
    {
     'descendants': A list of toot dicts
     'ancestors': A list of toot dicts
    }

Media dicts
~~~~~~~~~~~
.. code-block:: python

    mastodon.media_post("image.jpg", "image/jpeg")
    # Returns
    {
     'text_url': The display text for the media (what shows up in toots)
     'preview_url': The URL for the media preview
     'type': Media type, EG 'image'
     'url': The URL for the media
    }

App registration and user authentication
----------------------------------------
Before you can use the mastodon API, you have to register your 
application (which gets you a client key and client secret) 
and then log in (which gets you an access token). These functions 
allow you to do those things.
For convenience, once you have a client id, secret and access token, 
you can simply pass them to the constructor of the class, too!

Note that while it is perfectly reasonable to log back in whenever 
your app starts, registering a new application on every 
startup is not, so don't do that - instead, register an application 
once, and then persist your client id and secret. Convenience
methods for this are provided.

.. automethod:: Mastodon.create_app
.. automethod:: Mastodon.__init__
.. automethod:: Mastodon.log_in

Reading data: Timelines
-----------------------
This function allows you to access the timelines a logged in
user could see, as well as hashtag timelines and the public timeline.

.. automethod:: Mastodon.timeline
.. automethod:: Mastodon.timeline_home
.. automethod:: Mastodon.timeline_mentions
.. automethod:: Mastodon.timeline_public
.. automethod:: Mastodon.timeline_hashtag

Reading data: Statuses
----------------------
These functions allow you to get information about single statuses.

.. automethod:: Mastodon.status
.. automethod:: Mastodon.status_context
.. automethod:: Mastodon.status_reblogged_by
.. automethod:: Mastodon.status_favourited_by

Reading data: Notifications
---------------------------
This function allows you to get information about a users notifications.

.. automethod:: Mastodon.notifications

Reading data: Accounts
----------------------
These functions allow you to get information about accounts and
their relationships.

.. automethod:: Mastodon.account
.. automethod:: Mastodon.account_verify_credentials
.. automethod:: Mastodon.account_statuses
.. automethod:: Mastodon.account_following
.. automethod:: Mastodon.account_followers
.. automethod:: Mastodon.account_relationships
.. automethod:: Mastodon.account_search

Writing data: Statuses
----------------------
These functions allow you to post statuses to Mastodon and to
interact with already posted statuses.

.. automethod:: Mastodon.status_post
.. automethod:: Mastodon.toot
.. automethod:: Mastodon.status_reblog
.. automethod:: Mastodon.status_unreblog
.. automethod:: Mastodon.status_favourite
.. automethod:: Mastodon.status_unfavourite
.. automethod:: Mastodon.status_delete

Writing data: Accounts
----------------------
These functions allow you to interact with other accounts: To (un)follow and
(un)block.

.. automethod:: Mastodon.account_follow  
.. automethod:: Mastodon.account_unfollow
.. automethod:: Mastodon.account_block
.. automethod:: Mastodon.account_unblock

Writing data: Media
-------------------
This function allows you to upload media to Mastodon. The returned
media IDs (Up to 4 at the same time) can then be used with post_status
to attach media to statuses.

.. automethod:: Mastodon.media_post


.. _Mastodon: https://github.com/Gargron/mastodon
.. _Mastodon flagship instance: http://mastodon.social/
.. _Mastodon api docs: https://github.com/Gargron/mastodon/wiki/API
