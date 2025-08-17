App registration, authentication and preferences
================================================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Before you can use the Mastodon API, you have to register your
application (which gets you a client key and client secret)
and then log in (which gets you an access token) and out (revoking
the access token you are logged in with). These functions
allow you to do those things. Additionally, it is also possible
to programmatically register a new user.

For convenience, once you have a client id, secret and access token,
you can simply pass them to the constructor of the class, too!

Note that while it is perfectly reasonable to log back in whenever
your app starts, registering a new application on every
startup is not, so don't do that - instead, register an application
once, and then persist your client id and secret. A convenient method
for this is provided by the functions dealing with registering the app,
logging in and the Mastodon classes constructor.

App registration and information
--------------------------------
.. automethod:: Mastodon.create_app
.. automethod:: Mastodon.app_verify_credentials

Authentication
--------------    
.. automethod:: Mastodon.__init__
.. _log_in():
.. automethod:: Mastodon.log_in
.. _auth_request_url():
.. automethod:: Mastodon.auth_request_url
.. _set_language():
.. automethod:: Mastodon.set_language
.. automethod:: Mastodon.revoke_access_token
.. automethod:: Mastodon.create_account
.. automethod:: Mastodon.email_resend_confirmation

OAuth information
-----------------
.. automethod:: Mastodon.oauth_authorization_server_info
.. automethod:: Mastodon.oauth_userinfo

User preferences
----------------
.. automethod:: Mastodon.preferences
    