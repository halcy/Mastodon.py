Utility: Pagination, Blurhash, Other Utilities
==============================================
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Pagination
----------
These functions allow for convenient retrieval of paginated data.

.. _fetch_next():
.. automethod:: Mastodon.fetch_next
.. _fetch_previous():    
.. automethod:: Mastodon.fetch_previous
.. _fetch_remaining():    
.. automethod:: Mastodon.fetch_remaining
.. _pagination_iterator():
.. automethod:: Mastodon.pagination_iterator
.. _get_pagination_info():
.. automethod:: Mastodon.get_pagination_info

Async refreshes
---------------
Some API responses may include an ``Mastodon-Async-Refresh`` header, indicating that
the server is still fetching additional data in the background. These functions allow
you to check the status of such a refresh, wait for it to complete, or extract the
async refresh information from an API result.

Note that this functionality is considered *experimental*  by the Mastodon project
and may be subject to changes in the future.

.. _get_async_refresh_info():
.. automethod:: Mastodon.get_async_refresh_info
.. _get_async_refresh_status():
.. automethod:: Mastodon.get_async_refresh_status
.. _await_async_refresh():
.. automethod:: Mastodon.await_async_refresh

Blurhash decoding
-----------------
This function allows for easy basic decoding of blurhash strings to images.
This requires Mastodon.pys optional "blurhash" feature dependencies.

.. automethod:: Mastodon.decode_blurhash

Cache control
-------------
.. automethod:: Mastodon.clear_caches

Other utilities
---------------
.. automethod:: Mastodon.get_approx_server_time
.. _get_status_length():
.. automethod:: Mastodon.get_status_length

