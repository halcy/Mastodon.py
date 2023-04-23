Notifications and filtering
===========================
.. py:module:: mastodon
.. py:class: Mastodon

Notifications
-------------
This function allows you to get information about a user's notifications as well as to clear all or some notifications and to mark conversations as read.

Reading
~~~~~~~
.. automethod:: Mastodon.notifications

Writing
~~~~~~~
.. automethod:: Mastodon.notifications_clear
.. automethod:: Mastodon.notifications_dismiss
.. automethod:: Mastodon.conversations_read


Keyword filters
---------------
These functions allow you to get information about keyword filters as well as to create and update filters.

**Very Important Note: The filtering system was revised in 4.0.0. This means that these functions will now not work anymore if an instance is on Mastodon 4.0.0 or above.
When updating Mastodon.py for 4.0.0, we'll make an effort to emulate old behaviour, but this will not always be possible. Consider these methods deprecated, for now.**

Reading
~~~~~~~
.. automethod:: Mastodon.filters
.. automethod:: Mastodon.filter
.. automethod:: Mastodon.filters_apply

Writing
~~~~~~~
.. automethod:: Mastodon.filter_create
.. automethod:: Mastodon.filter_update
.. automethod:: Mastodon.filter_delete

Push notifications
------------------
Mastodon supports the delivery of notifications via webpush.

These functions allow you to manage webpush subscriptions and to decrypt received
pushes. Note that the intended setup is not Mastodon pushing directly to a user's client -
the push endpoint should usually be a relay server that then takes care of delivering the
(encrypted) push to the end user via some mechanism, where it can then be decrypted and
displayed.

Mastodon allows an application to have one webpush subscription per user at a time.

All crypto utilities require Mastodon.py's optional "webpush" feature dependencies
(specifically, the "cryptography" and "http_ece" packages).

.. automethod:: Mastodon.push_subscription
.. automethod:: Mastodon.push_subscription_set
.. automethod:: Mastodon.push_subscription_update

.. _push_subscription_generate_keys():
.. automethod:: Mastodon.push_subscription_generate_keys
.. automethod:: Mastodon.push_subscription_decrypt_push

Usage example
~~~~~~~~~~~~~

This is a minimal usage example for the push API, including a small http server to receive webpush notifications.

.. code-block:: python

    api = Mastodon(...)
    keys = api.push_subscription_generate_keys()
    api.push_subscription_set(endpoint, keys[1], mention_events=1)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            self.send_response(201)
            self.send_header('Location', '')  # Mastodon doesn't seem to care about this
            self.end_headers()
            data = self.rfile.read(int(self.headers['content-length']))
            np = api.push_subscription_decrypt_push(data, keys[0], self.headers['Encryption'], self.headers['Crypto-Key'])
            n = api.notifications(id=np.notification_id)
            s = n.status
            self.log_message('\nFrom: %s\n%s', s.account.acct, s.content)
    httpd = http.server.HTTPServer(('', 42069), Handler)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        api.push_subscription_delete()