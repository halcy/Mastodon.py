.. py:currentmodule:: mastodon
.. py:class:: Mastodon

Mastodon.py
===========

App creation and auth
---------------------

Before you can use the mastodon API, you have to register your application (which gets you a client key and client secret) 
and then log in (which gets you an access token). These functions allow you to do those things.
For convenience, once you have a client id, secret and access token, you can simply pass them to the constructor of the class, too!

Note that while it is perfectly reasonable to log back in whenever your app starts, registering a new application on every 
startup is not, so don't do that - instead, register an application once, and then persist your client id and secret. Convenience
methods for this are provided.

.. autofunction:: create_app
.. automethod:: __init__
.. automethod:: log_in

Reading timelines
-----------------


