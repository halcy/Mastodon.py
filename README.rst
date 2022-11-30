Mastodon.py
===========
Python wrapper for the Mastodon ( https://github.com/mastodon/mastodon/ ) API.
Feature complete for public API as of Mastodon version 3.5.5 and easy to get started with:

.. code-block:: python

    from mastodon import Mastodon

    # Register your app! This only needs to be done once (per server, or when 
    # distributing rather than hosting an application, most likely per device and server). 
    # Uncomment the code and substitute in your information:
    '''
    Mastodon.create_app(
        'pytooterapp',
        api_base_url = 'https://mastodon.social',
        to_file = 'pytooter_clientcred.secret'
    )
    '''

    # Then, log in. This can be done every time your application starts (e.g. when writing a 
    # simple bot), or you can use the persisted information:
    mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
    mastodon.log_in(
        'my_login_email@example.com', 
        'incrediblygoodpassword', 
        to_file = 'pytooter_usercred.secret'
    )

    # Note that this won't work when using 2FA - you'll have to use OAuth, in that case. 
    # To post, create an actual API instance:
    mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
    mastodon.toot('Tooting from Python using #mastodonpy !')

You can install Mastodon.py via pypi:

.. code-block:: Bash

   # Python 3
   pip3 install Mastodon.py

We currently try to support Python 3.7 and above, and try to at least not break Python 3 versions
below that. Python 2 support is no longer a goal.

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

