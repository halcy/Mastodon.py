Utility: Pagination and Blurhash
================================
.. py:module:: mastodon
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

Blurhash decoding
-----------------
This function allows for easy basic decoding of blurhash strings to images.
This requires Mastodon.pys optional "blurhash" feature dependencies.

.. automethod:: Mastodon.decode_blurhash
