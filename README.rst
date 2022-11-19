Mastodon.py
===========
Python wrapper for the Mastodon ( https://github.com/mastodon/mastodon/ ) API.
Feature complete for public API as of Mastodon version 3.4.0 and easy to get started with:

.. code-block:: python

    # Register your app! This only needs to be done once. Uncomment the code and substitute in your information.

    from mastodon import Mastodon

    '''
    Mastodon.create_app(
         'pytooterapp',
         api_base_url = 'https://mastodon.social',
         to_file = 'pytooter_clientcred.secret'
    )
    '''

    # Then login. This can be done every time, or use persisted.

    from mastodon import Mastodon

    mastodon = Mastodon(client_id = 'pytooter_clientcred.secret')
    mastodon.log_in(
        'my_login_email@example.com',
        'incrediblygoodpassword',
        to_file = 'pytooter_usercred.secret'
    )

    # To post, create an actual API instance.

    from mastodon import Mastodon

    mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
    mastodon.toot('Tooting from Python using #mastodonpy !')

You can install Mastodon.py via pypi:

.. code-block:: Bash

   # Python 3
   pip3 install Mastodon.py

Note that Python 2.7 is now no longer officially supported. It will still
work for a while, and we will fix issues as they come up, but we will not
be testing specifically for Python 2.7 any longer.

Full documentation and basic usage examples can be found
at https://mastodonpy.readthedocs.io/en/stable/

Acknowledgements
----------------
Mastodon.py contains work by a large amount of contributors, many of which have
put significant work into making it a better library. You can find some information
about who helped with which particular feature or fix in the changelog.

.. image:: https://circleci.com/gh/halcy/Mastodon.py.svg?style=svg
    :target: https://app.circleci.com/pipelines/github/halcy/Mastodon.py
.. image:: https://codecov.io/gh/halcy/Mastodon.py/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/halcy/Mastodon.py

