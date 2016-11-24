Mastodon.py
===========
.. code-block:: python

   mastodon = Mastodon(
       client_id = 'pytooter_clientcred.txt',
       access_token = 'pytooter_usercred.txt'
   )
   mastodon.toot('Tooting from python!')

Python wrapper for the Mastodon ( https://github.com/Gargron/mastodon/ ) API. 
Feature complete for public API version v1 and easy to get started with.

You can install Mastodon.py via pypi:

.. code-block:: Bash

   # Python 2
   pip install Mastodon.py
   
   # Python 3
   pip3 install Mastodon.py

Full documentation and basic "how to post a toot" usage example can be found 
at http://mastodonpy.readthedocs.io/en/latest/ .

Full "real life" example of how to use this library to write a Mastodon bot 
will be linked here shortly.
