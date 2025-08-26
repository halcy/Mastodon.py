Mastodon.py
===========
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

Usage
-----
Register your app! This only needs to be done once (per server, or when distributing rather than hosting an application, most likely per device and server). Uncomment the code and substitute in your information:

.. code-block:: python

    from mastodon import Mastodon

    '''
    Mastodon.create_app(
        'pytooterapp',
        api_base_url = 'https://mastodon.social',
        to_file = 'pytooter_clientcred.secret'
    )
    '''

Then, log in. This can be done every time your application starts, or you can use the persisted information:

.. code-block:: python

    from mastodon import Mastodon

    mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
    print(mastodon.auth_request_url())

    # open the URL in the browser and paste the code you get
    mastodon.log_in(
        code=input("Enter the OAuth authorization code: "),
        to_file="pytooter_usercred.secret"
    )


Note that previous versions of Mastodon allowed logging in with username and 
password - unfortunately, due to security concerns, Mastodon has started 
requiring OAuth starting with version 4.4.0. If you're building a bot, you
may wish to instead just generate a token in the UI (On Mastodon: 
your-server.com/settings/applications) and use it directly

To post, create an actual API instance:

.. code-block:: python

    from mastodon import Mastodon

    mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
    mastodon.toot('Tooting from Python using #mastodonpy !')

Introduction
------------
`Mastodon`_ is an ActivityPub-based Twitter-like federated social
network node. It has an API that allows you to interact with its
every aspect. This is a simple Python wrapper for that API, provided
as a single Python module.

Mastodon.py aims to implement the complete public Mastodon API. As
of this time, it is feature complete for Mastodon version 4.4.3. The
Mastodon compatible API layers of various other pieces of software as well
as forks, while not an official target, should also be basically
compatible, and Mastodon.py does make some allowances for behaviour that isn't
strictly like that of Mastodon, and attempts to support extensions to the API.

Some usage examples (not neccesarily following app development best practices,
but enough to get you started if you learn best by example) can be found
at https://github.com/halcy/MastodonpyExamples

Acknowledgements
----------------
Mastodon.py contains work by a large number of contributors, many of which have
put significant work into making it a better library. You can find some information
about who helped with which particular feature or fix in the changelog.

.. _Mastodon.py on GitHub: https://github.com/halcy/Mastodon.py
.. _Mastodon: https://github.com/mastodon/mastodon
.. _The mastodon project as such: https://joinmastodon.org/
.. _Official Mastodon API docs: https://docs.joinmastodon.org/api/guidelines/

Research use and citing
-----------------------
If you use Mastodon.py in your research, please cite it according to the latest CITATION.cff from the repository:

https://github.com/halcy/Mastodon.py/blob/master/CITATION.cff

As a personal request, It is important to me to ask you to make sure that the subjects of 
your research - fediverse users - are alright with the research you are doing on them
and/or that you have secured the approval of your institutions ethics board.

.. toctree::
    :caption: Introduction

    Mastodon.py <self>
    01_general
    02_return_values
    03_errors

.. toctree::
    :caption: API methods

    04_auth
    05_statuses
    06_accounts
    07_timelines
    08_instances
    09_notifications
    10_streaming
    11_misc
    12_utilities
    13_admin

.. toctree::
    :caption: Appendix

    14_contributing
    15_everything
