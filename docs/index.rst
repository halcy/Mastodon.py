Mastodon.py
===========

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

For complete documentation on what every function returns, 
check the `Mastodon API docs`_, or just play around a bit.

.. py:module:: mastodon
.. py:class: Mastodon

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

Reading data: Statuses
----------------------
These functions allow you to get information about single statuses.

.. automethod:: Mastodon.status
.. automethod:: Mastodon.status_context
.. automethod:: Mastodon.status_reblogged_by
.. automethod:: Mastodon.status_favourited_by

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
.. automethod:: Mastodon.account_suggestions
.. automethod:: Mastodon.account_search

Writing data: Statuses
----------------------
These functions allow you to post statuses to Mastodon and to
interact with already posted statuses.

.. automethod:: Mastodon.status_post
.. automethod:: Mastodon.toot
.. automethod:: Mastodon.status_delete
.. automethod:: Mastodon.status_reblog
.. automethod:: Mastodon.status_unreblog
.. automethod:: Mastodon.status_favourite
.. automethod:: Mastodon.status_unfavourite

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
