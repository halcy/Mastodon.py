Mastodon.py
===========
.. code-block:: python

   from mastodon import Mastodon

   # Register app - only once!
   '''
   Mastodon.create_app(
        'pytooterapp',
        api_base_url = 'https://mastodon.social',
        to_file = 'pytooter_clientcred.secret'
   )
   '''

   # Log in - either every time, or use persisted
   '''
   mastodon = Mastodon(
       client_id = 'pytooter_clientcred.secret',
       api_base_url = 'https://mastodon.social'
   )
   mastodon.log_in(
       'my_login_email@example.com',
       'incrediblygoodpassword',
       to_file = 'pytooter_usercred.secret'
   )
   '''

   # Create actual API instance
   mastodon = Mastodon(
       client_id = 'pytooter_clientcred.secret', 
       access_token = 'pytooter_usercred.secret',
       api_base_url = 'https://mastodon.social'
   )
   mastodon.toot('Tooting from python using #mastodonpy !')

Python wrapper for the Mastodon ( https://github.com/tootsuite/mastodon/ ) API. 
Feature complete for public API as of version v1.4 and easy to get started with.

You can install Mastodon.py via pypi:

.. code-block:: Bash

   # Python 2
   pip install Mastodon.py
   
   # Python 3
   pip3 install Mastodon.py

Full documentation and basic usage examples can be found 
at http://mastodonpy.readthedocs.io/en/latest/ .
