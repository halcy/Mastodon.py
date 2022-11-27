Mastodon.py
===========
.. py:module:: mastodon
.. py:class: Mastodon

Register your app! This only needs to be done once. Uncomment the code and substitute in your information:

.. code-block:: python

   from mastodon import Mastodon

   '''
   Mastodon.create_app(
        'pytooterapp',
        api_base_url = 'https://mastodon.social',
        to_file = 'pytooter_clientcred.secret'
   )
   '''

Then login. This can be done every time, or you can use the persisted information:

.. code-block:: python

   from mastodon import Mastodon

   mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
   mastodon.log_in('my_login_email@example.com', 'incrediblygoodpassword', to_file = 'pytooter_usercred.secret')

To post, create an actual API instance:

.. code-block:: python

   from mastodon import Mastodon

   mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
   mastodon.toot('Tooting from Python using #mastodonpy !')

`Mastodon`_ is an ActivityPub-based Twitter-like federated social
network node. It has an API that allows you to interact with its
every aspect. This is a simple Python wrapper for that API, provided
as a single Python module.

Mastodon.py aims to implement the complete public Mastodon API. As
of this time, it is feature complete for Mastodon version 3.5.0. The
Mastodon compatible API layers of various other pieces of software as well
as forks, while not an official target, should also be basically
compatible, and Mastodon.py does make some allowances for behaviour that isn't
strictly like that of Mastodon, and attempts to support extensions to the API.

Acknowledgements
----------------
Mastodon.py contains work by a large number of contributors, many of which have
put significant work into making it a better library. You can find some information
about who helped with which particular feature or fix in the changelog.

.. _Mastodon: https://github.com/mastodon/mastodon
.. _Mastodon flagship instance: https://mastodon.social/
.. _Official Mastodon API docs: https://docs.joinmastodon.org/client/intro/

.. toctree::
    :caption: Introduction
    Mastodon.py <self>
    01_general
    02_return_values
    03_errors

.. toctree::
    :caption: API methods
    Mastodon.py <self>
    04_auth
