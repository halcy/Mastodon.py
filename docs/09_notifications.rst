Notifications and filtering
===========================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Notifications
-------------
These functions allow you to get information about a user's notifications as well as to clear all or some notifications and to mark conversations as read.

Reading
~~~~~~~
.. automethod:: Mastodon.notifications
.. automethod:: Mastodon.notifications_unread_count

Writing
~~~~~~~
.. automethod:: Mastodon.notifications_clear
.. automethod:: Mastodon.notifications_dismiss
.. automethod:: Mastodon.conversations_read


Grouped notifications
---------------------
This is the more modern notification API, which delivers notifications grouped.

.. automethod:: Mastodon.grouped_notifications
.. automethod:: Mastodon.grouped_notification
.. automethod:: Mastodon.dismiss_grouped_notification
.. automethod:: Mastodon.grouped_notification_accounts
.. automethod:: Mastodon.unread_grouped_notifications_count

Source filtering for notifications
----------------------------------
These functions allow you to get information about source filters as well as to create and update filters, and
to accept or reject notification requests for filtered notifications.

.. automethod:: Mastodon.notifications_policy
.. automethod:: Mastodon.update_notifications_policy
.. automethod:: Mastodon.notification_requests
.. automethod:: Mastodon.notification_request
.. automethod:: Mastodon.accept_notification_request
.. automethod:: Mastodon.dismiss_notification_request
.. automethod:: Mastodon.accept_multiple_notification_requests
.. automethod:: Mastodon.dismiss_multiple_notification_requests
.. automethod:: Mastodon.notifications_merged        


Keyword Filters (v2)
--------------------
These functions allow you to get information about keyword filters as well as to create and update filters.

NB: The filters are checked server side, but the server still returns all statuses to the client, just with 
a `filtered` attribute. Filtered notifications most likely end up as notification requests, but I have not
validated this.

.. automethod:: Mastodon.filters_v2
.. automethod:: Mastodon.filter_v2
.. automethod:: Mastodon.create_filter_v2
.. automethod:: Mastodon.update_filter_v2
.. automethod:: Mastodon.delete_filter_v2
.. automethod:: Mastodon.filter_keywords_v2
.. automethod:: Mastodon.add_filter_keyword_v2
.. automethod:: Mastodon.delete_filter_keyword_v2
.. automethod:: Mastodon.filter_statuses_v2
.. automethod:: Mastodon.add_filter_status_v2
.. automethod:: Mastodon.filter_status_v2
.. automethod:: Mastodon.delete_filter_status_v2


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

Keyword filters (v1, deprecated)
--------------------------------
These functions allow you to get information about keyword filters as well as to create and update filters.

These APIs are deprecated in favor of the v2 APIs - I would recommend using those instead.

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
    