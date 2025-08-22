Mastodon.py
===========
Python wrapper for the Mastodon ( https://github.com/mastodon/mastodon/ ) API.
Feature complete for public API as of Mastodon version 4.4.3 and easy to get started with:

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

    # Then, log in. This can be done every time your application starts, or you can use the persisted information:
    mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
    print(mastodon.auth_request_url())

    # open the URL in the browser and paste the code you get
    mastodon.log_in(
        code=input("Enter the OAuth authorization code: "),
        to_file="pytooter_usercred.secret"
    )

    # To post, create an actual API instance:
    mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
    mastodon.toot('Tooting from Python using #mastodonpy !')

You can install Mastodon.py via pypi:

.. code-block:: Bash

   pip install Mastodon.py

We currently try to support Python 3.7 and above, and try to at least not break Python 3 versions
below that. Python 2 support is no longer a goal.

Full documentation and basic usage examples can be found
at https://mastodonpy.readthedocs.io/en/stable/ . Some more extensive examples can be
found at https://github.com/halcy/MastodonpyExamples

If you have any questions about using the library or think you have found a bug,
please feel free to open an issue, a github discussion thread, or to just directly
contact @halcy@icosahedron.website on the Fediverse or .halcy on Discord - we'll
try to respond as quickly as possible.

Acknowledgements
----------------
Mastodon.py contains work by a large amount of contributors, many of which have
put significant work into making it a better library. You can find some information
about who helped with which particular feature or fix in the changelog.

.. image:: https://circleci.com/gh/halcy/Mastodon.py.svg?style=svg
    :target: https://app.circleci.com/pipelines/github/halcy/Mastodon.py
.. image:: https://codecov.io/gh/halcy/Mastodon.py/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/halcy/Mastodon.py

