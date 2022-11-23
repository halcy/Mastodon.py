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

   mastodon = Mastodon(
       client_id = 'pytooter_clientcred.secret',
       api_base_url = 'https://mastodon.social'
   )
   mastodon.log_in(
       'my_login_email@example.com',
       'incrediblygoodpassword',
       to_file = 'pytooter_usercred.secret'
   )

To post, create an actual API instance:

.. code-block:: python

   from mastodon import Mastodon

   mastodon = Mastodon(
       access_token = 'pytooter_usercred.secret',
       api_base_url = 'https://mastodon.social'
   )
   mastodon.toot('Tooting from Python using #mastodonpy !')

`Mastodon`_ is an ActivityPub-based Twitter-like federated social
network node. It has an API that allows you to interact with its
every aspect. This is a simple Python wrapper for that API, provided
as a single Python module. By default, it talks to the
`Mastodon flagship instance`_, but it can be set to talk to any
node running Mastodon by setting `api_base_url` when creating the
API object (or creating an app).

Mastodon.py aims to implement the complete public Mastodon API. As
of this time, it is feature complete for Mastodon version 3.0.1. Pleroma's
Mastodon API layer, while not an official target, should also be basically
compatible, and Mastodon.py does make some allowances for behaviour that isn't
strictly like that of Mastodon.

A note about rate limits
------------------------
Mastodon's API rate limits per user account. By default, the limit is 300 requests
per 5 minute time slot. This can differ from instance to instance and is subject to change.
Mastodon.py has three modes for dealing with rate limiting that you can pass to
the constructor, "throw", "wait" and "pace", "wait" being the default.

In "throw" mode, Mastodon.py makes no attempt to stick to rate limits. When
a request hits the rate limit, it simply throws a `MastodonRateLimitError`. This is
for applications that need to handle all rate limiting themselves (i.e. interactive apps),
or applications wanting to use Mastodon.py in a multi-threaded context ("wait" and "pace"
modes are not thread safe).

.. note::
   Rate limit information is available on the `Mastodon` object for applications that
   implement their own rate limit handling.

   .. attribute:: Mastodon.ratelimit_remaining

      Number of requests allowed until the next reset.

   .. attribute:: Mastodon.ratelimit_reset

      Time at which the rate limit will next be reset, as a POSIX timestamp.

   .. attribute:: Mastodon.ratelimit_limit

      Total number of requests allowed between resets. Typically 300.

   .. attribute:: Mastodon.ratelimit_lastcall

      Time at which these values have last been seen and updated, as a POSIX timestamp.

In "wait" mode, once a request hits the rate limit, Mastodon.py will wait until
the rate limit resets and then try again, until the request succeeds or an error
is encountered. This mode is for applications that would rather just not worry about rate limits
much, don't poll the API all that often, and are okay with a call sometimes just taking
a while.

In "pace" mode, Mastodon.py will delay each new request after the first one such that,
if requests were to continue at the same rate, only a certain fraction (set in the
constructor as `ratelimit_pacefactor`) of the rate limit will be used up. The fraction can
be (and by default, is) greater than one. If the rate limit is hit, "pace" behaves like
"wait". This mode is probably the most advanced one and allows you to just poll in
a loop without ever sleeping at all yourself. It is for applications that would rather
just pretend there is no such thing as a rate limit and are fine with sometimes not
being very interactive.

In addition to the per-user limit, there is a per-IP limit of 7500 requests per 5
minute time slot, and tighter limits on logins. Mastodon.py does not make any effort
to respect these.

If your application requires many hits to endpoints that are available without logging
in, do consider using Mastodon.py without authenticating to get the full per-IP limit.


A note about pagination
-----------------------
Many of Mastodon's API endpoints are paginated. What this means is that if you request
data from them, you might not get all the data at once - instead, you might only get the
first few results.

All endpoints that are paginated have four parameters: `since_id`, `max_id`, `min_id` and
`limit`. `since_id` allows you to specify the smallest id you want in the returned data, but
you will still always get the newest data, so if there are too many statuses between
the newest one and `since_id`, some will not be returned. `min_id`, on the other hand, gives
you statuses with that minimum id and newer, starting at the given id. `max_id`, similarly,
allows you to specify the largest id you want. By specifying either min_id or `max_id`
(generally, only one, not both, though specifying both is supported starting with Mastodon
version 3.3.0) of them you can go through pages forwards and backwards.

On Mastodon mainline, you can, pass datetime objects as IDs when fetching posts,
since the IDs used are Snowflake IDs and dates can be approximately converted to those.
This is guaranteed to work on mainline Mastodon servers and very likely to work on all
forks, but will **not** work on other servers implementing the API, like Pleroma, Misskey
or Gotosocial. You should not use this if you want your application to be universally
compatible. It's also relatively coarse-grained.

`limit` allows you to specify how many results you would like returned. Note that an
instance may choose to return less results than you requested - by default, Mastodon
will return no more than 40 statuses and no more than 80 accounts no matter how high
you set the limit.

The responses returned by paginated endpoints contain a "link" header that specifies
which parameters to use to get the next and previous pages. Mastodon.py parses these
and stores them (if present) in the first (for the previous page) and last (for the
next page) item of the returned list as _pagination_prev and _pagination_next. They
are accessible only via attribute-style access. Note that this means that if you
want to persist pagination info with your data, you'll have to take care of that
manually (or persist objects, not just dicts).

There are convenience functions available for fetching the previous and next page of
a paginated request as well as for fetching all pages starting from a first page.

Two notes about IDs
-------------------
Mastodon's API uses IDs in several places: User IDs, Toot IDs, ...

While debugging, it might be tempting to copy-paste IDs from the
web interface into your code. This will not work, as the IDs on the web
interface and in the URLs are not the same as the IDs used internally
in the API, so don't do that.

ID unpacking
~~~~~~~~~~~~
Wherever Mastodon.py expects an ID as a parameter, you can also pass a
dict that contains an id - this means that, for example, instead of writing

.. code-block:: python

    mastodon.status_post("@somebody wow!", in_reply_to_id = toot["id"])

you can also just write

.. code-block:: python

    mastodon.status_post("@somebody wow!", in_reply_to_id = toot)

and everything will work as intended.

Error handling
--------------
When Mastodon.py encounters an error, it will raise an exception, generally with
some text included to tell you what went wrong.

The base class that all Mastodon exceptions inherit from is `MastodonError`.
If you are only interested in the fact an error was raised somewhere in
Mastodon.py, and not the details, this is the exception you can catch.

`MastodonIllegalArgumentError` is generally a programming problem - you asked the
API to do something obviously invalid (i.e. specify a privacy option that does
not exist).

`MastodonFileNotFoundError` and `MastodonNetworkError` are IO errors - could be you
specified a wrong URL, could be the internet is down or your hard drive is
dying. They inherit from `MastodonIOError`, for easy catching. There is a sub-error
of `MastodonNetworkError`, `MastodonReadTimeout`, which is thrown when a streaming
API stream times out during reading.

`MastodonAPIError` is an error returned from the Mastodon instance - the server
has decided it can't fulfil your request (i.e. you requested info on a user that
does not exist). It is further split into `MastodonNotFoundError` (API returned 404)
and `MastodonUnauthorizedError` (API returned 401). Different error codes might exist,
but are not currently handled separately.

`MastodonMalformedEventError` is raised when a streaming API listener receives an
invalid event. There have been reports that this can sometimes happen after prolonged
operation due to an upstream problem in the requests/urllib libraries.

`MastodonRatelimitError` is raised when you hit an API rate limit. You should try
again after a while (see the rate limiting section above).

`MastodonServerError` is raised when the server throws an internal error, likely due
to server misconfiguration.

`MastodonVersionError` is raised when a version check for an API call fails.

A brief note on block lists
---------------------------
Mastodon.py used to block three instances because these were particularly notorious for
harassing trans people and I don't feel like I have an obligation to let software I 
distribute help people who want my friends to die. I don't want to be associated with 
that, at all. 

Those instances are now all gone, any point that could have been has been made, and 
there is no list anymore.

Trans rights are human rights. 

Return values
-------------
Unless otherwise specified, all data is returned as Python dictionaries, matching
the JSON format used by the API. Dates returned by the API are in ISO 8601 format
and are parsed into Python datetime objects.

To make access easier, the dictionaries returned are wrapped by a class that adds
read-only attributes for all dict values - this means that, for example, instead of
writing

.. code-block:: python

    description = mastodon.account_verify_credentials()["source"]["note"]

you can also just write

.. code-block:: python

    description = mastodon.account_verify_credentials().source.note

and everything will work as intended. The class used for this is exposed as
`AttribAccessDict`.

User / account dicts
~~~~~~~~~~~~~~~~~~~~
.. _user dict:

.. code-block:: python

    mastodon.account(<numerical id>)
    # Returns the following dictionary:
    {
        'id': # Same as <numerical id>
        'username': # The username (what you @ them with)
        'acct': # The user's account name as username@domain (@domain omitted for local users)
        'display_name': # The user's display name
        'discoverable': # True if the user is listed in the user directory, false if not. None
                        # for remote users.
        'group': # A boolean indicating whether the account represents a group rather than an
                 # individual.
        'locked': # Denotes whether the account can be followed without a follow request
        'created_at': # Account creation time
        'following_count': # How many people they follow
        'followers_count': # How many followers they have
        'statuses_count': # How many statuses they have
        'note': # Their bio
        'url': # Their URL; for example 'https://mastodon.social/users/<acct>'
        'avatar': # URL for their avatar, can be animated
        'header': # URL for their header image, can be animated
        'avatar_static': # URL for their avatar, never animated
        'header_static': # URL for their header image, never animated
        'source': # Additional information - only present for user dict returned
                  # from account_verify_credentials()
        'moved_to_account': # If set, a user dict of the account this user has
                            # set up as their moved-to address.
        'bot': # Boolean indicating whether this account is automated.
        'fields': # List of up to four dicts with free-form 'name' and 'value' profile info.
                  # For fields with "this is me" type verification, verified_at is set to the
                  # last verification date (It is None otherwise)
        'emojis': # List of custom emoji used in name, bio or fields
        'discoverable': # Indicates whether or not a user is visible on the discovery page
    }

    mastodon.account_verify_credentials()["source"]
    # Returns the following dictionary:
    {
        'privacy': # The user's default visibility setting ("private", "unlisted" or "public")
        'sensitive': # Denotes whether user media should be marked sensitive by default
        'note': # Plain text version of the user's bio
    }

Toot dicts
~~~~~~~~~~
.. _toot dict:

.. code-block:: python

    mastodon.toot("Hello from Python")
    # Returns the following dictionary:
    {
        'id': # Numerical id of this toot
        'uri': # Descriptor for the toot
            # EG 'tag:mastodon.social,2016-11-25:objectId=<id>:objectType=Status'
        'url': # URL of the toot
        'account': # User dict for the account which posted the status
        'in_reply_to_id': # Numerical id of the toot this toot is in response to
        'in_reply_to_account_id': # Numerical id of the account this toot is in response to
        'reblog': # Denotes whether the toot is a reblog. If so, set to the original toot dict.
        'content': # Content of the toot, as HTML: '<p>Hello from Python</p>'
        'created_at': # Creation time
        'reblogs_count': # Number of reblogs
        'favourites_count': # Number of favourites
        'reblogged': # Denotes whether the logged in user has boosted this toot
        'favourited': # Denotes whether the logged in user has favourited this toot
        'sensitive': # Denotes whether media attachments to the toot are marked sensitive
        'spoiler_text': # Warning text that should be displayed before the toot content
        'visibility': # Toot visibility ('public', 'unlisted', 'private', or 'direct')
        'mentions': # A list of users dicts mentioned in the toot, as Mention dicts
        'media_attachments': # A list of media dicts of attached files
        'emojis': # A list of custom emojis used in the toot, as Emoji dicts
        'tags': # A list of hashtag used in the toot, as Hashtag dicts
        'bookmarked': # True if the status is bookmarked by the logged in user, False if not.
        'application': # Application dict for the client used to post the toot (Does not federate
                       # and is therefore always None for remote toots, can also be None for
                       # local toots for some legacy applications).
        'language': # The language of the toot, if specified by the server,
                    # as ISO 639-1 (two-letter) language code.
        'muted': # Boolean denoting whether the user has muted this status by
                 # way of conversation muting
        'pinned': # Boolean denoting whether or not the status is currently pinned for the
                  # associated account.
        'replies_count': # The number of replies to this status.
        'card': # A preview card for links from the status, if present at time of delivery,
                # as card dict.
        'poll': # A poll dict if a poll is attached to this status.
    }

Mention dicts
~~~~~~~~~~~~~
.. _mention dict:

.. code-block:: python

    {
        'url': # Mentioned user's profile URL (potentially remote)
        'username': # Mentioned user's user name (not including domain)
        'acct': # Mentioned user's account name (including domain)
        'id': # Mentioned user's (local) account ID
    }

Scheduled toot dicts
~~~~~~~~~~~~~~~~~~~~
.. _scheduled toot dict:

.. code-block:: python

    mastodon.status_post("text", scheduled_at=the_future)
    # Returns the following dictionary:
    {
        'id': # Scheduled toot ID (note: Not the id of the toot once it gets posted!)
        'scheduled_at': # datetime object describing when the toot is to be posted
        'params': # Parameters for the scheduled toot, specifically
        {
            'text': # Toot text
            'in_reply_to_id': # ID of the toot this one is a reply to
            'media_ids': # IDs of media attached to this toot
            'sensitive': # Whether this toot is sensitive or not
            'visibility': # Visibility of the toot
            'idempotency': # Idempotency key for the scheduled toot
            'scheduled_at': # Present, but generally "None"
            'spoiler_text': # CW text for this toot
            'application_id': # ID of the application that scheduled the toot
            'poll': # Poll parameters, as a poll dict
        },
        'media_attachments': # Array of media dicts for the attachments to the scheduled toot
    }

Poll dicts
~~~~~~~~~~
.. _poll dict:

.. code-block:: python

    # Returns the following dictionary:
    mastodon.poll(id)
    {
        'id': # The polls ID
        'expires_at': # The time at which the poll is set to expire
        'expired': # Boolean denoting whether you can still vote in this poll
        'multiple': # Boolean indicating whether it is allowed to vote for more than one option
        'votes_count': # Total number of votes cast in this poll
        'voted': # Boolean indicating whether the logged-in user has already voted in this poll
        'options': # The poll options as a list of dicts, each option with a title and a
                   # votes_count field. votes_count can be None if the poll creator has
                   # chosen to hide vote totals until the poll expires and it hasn't yet.
        'emojis': # List of emoji dicts for all emoji used in answer strings,
        'own_votes': # The logged-in users votes, as a list of indices to the options.
    }


Conversation dicts
~~~~~~~~~~~~~~~~~~
.. _conversation dict:

.. code-block:: python

    mastodon.conversations()[0]
    # Returns the following dictionary:
    {
        'id': # The ID of this conversation object
        'unread': # Boolean indicating whether this conversation has yet to be
                  # read by the user
        'accounts': # List of accounts (other than the logged-in account) that
                    # are part of this conversation
        'last_status': # The newest status in this conversation
    }

Hashtag dicts
~~~~~~~~~~~~~
.. _hashtag dict:

.. code-block:: python

    {
        'name': # Hashtag name (not including the #)
        'url': # Hashtag URL (can be remote)
        'history': # List of usage history dicts for up to 7 days. Not present in statuses.
    }

Hashtag usage history dicts
~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. _hashtag usage history dict:

.. code-block:: python

    {
        'day': # Date of the day this history dict is for
        'uses': # Number of statuses using this hashtag on that day
        'accounts': # Number of accounts using this hashtag in at least one status on that day
    }

Emoji dicts
~~~~~~~~~~~
.. _emoji dict:

.. code-block:: python

    {
        'shortcode': # Emoji shortcode, without surrounding colons
        'url': # URL for the emoji image, can be animated
        'static_url': # URL for the emoji image, never animated
        'visible_in_picker': # True if the emoji is enabled, False if not.
        'category': # The category to display the emoji under (not present if none is set)
    }

Application dicts
~~~~~~~~~~~~~~~~~
 .. _application dict:

.. code-block:: python

    {
        'name': # The applications name
        'website': # The applications website
        'vapid_key': # A vapid key that can be used in web applications
    }


Relationship dicts
~~~~~~~~~~~~~~~~~~
.. _relationship dict:

.. code-block:: python

    mastodon.account_follow(<numerical id>)
    # Returns the following dictionary:
    {
        'id': # Numerical id (same one as <numerical id>)
        'following': # Boolean denoting whether the logged-in user follows the specified user
        'followed_by': # Boolean denoting whether the specified user follows the logged-in user
        'blocking': # Boolean denoting whether the logged-in user has blocked the specified user
        'blocked_by': # Boolean denoting whether the logged-in user has been blocked by the specified user, if information is available
        'muting': # Boolean denoting whether the logged-in user has muted the specified user
        'muting_notifications': # Boolean denoting wheter the logged-in user has muted notifications
                                # related to the specified user
        'requested': # Boolean denoting whether the logged-in user has sent the specified
                     # user a follow request
        'domain_blocking': # Boolean denoting whether the logged-in user has blocked the
                           # specified users domain
        'showing_reblogs': # Boolean denoting whether the specified users reblogs show up on the
                           # logged-in users Timeline
        'endorsed': # Boolean denoting wheter the specified user is being endorsed / featured by the
                    # logged-in user
        'note': # A free text note the logged in user has created for this account (not publicly visible)
        'notifying' # Boolean denoting whether the logged-in user has requested to get notified every time the followed user posts
    }

Filter dicts
~~~~~~~~~~~~
.. _filter dict:

.. code-block:: python

    mastodon.filter(<numerical id>)
    # Returns the following dictionary:
    {
        'id': # Numerical id of the filter
        'phrase': # Filtered keyword or phrase
        'context': # List of places where the filters are applied ('home', 'notifications', 'public', 'thread')
        'expires_at': # Expiry date for the filter
        'irreversible': # Boolean denoting if this filter is executed server-side
                        # or if it should be ran client-side.
        'whole_word': # Boolean denoting whether this filter can match partial words
    }

Notification dicts
~~~~~~~~~~~~~~~~~~
.. _notification dict:

.. code-block:: python

    mastodon.notifications()[0]
    # Returns the following dictionary:
    {
        'id': # id of the notification
        'type': # "mention", "reblog", "favourite", "follow", "poll" or "follow_request"
        'created_at': # The time the notification was created
        'account': # User dict of the user from whom the notification originates
        'status': # In case of "mention", the mentioning status
                  # In case of reblog / favourite, the reblogged / favourited status
    }

Context dicts
~~~~~~~~~~~~~
.. _context dict:

.. code-block:: python

    mastodon.status_context(<numerical id>)
    # Returns the following dictionary:
    {
        'ancestors': # A list of toot dicts
        'descendants': # A list of toot dicts
    }

List dicts
~~~~~~~~~~
.. _list dict:

.. code-block:: python

    mastodon.list(<numerical id>)
    # Returns the following dictionary:
    {
        'id': # id of the list
        'title': # title of the list
    }

Media dicts
~~~~~~~~~~~
.. _media dict:

.. code-block:: python

    mastodon.media_post("image.jpg", "image/jpeg")
    # Returns the following dictionary:
    {
        'id': # The ID of the attachment.
        'type': # Media type: 'image', 'video', 'gifv', 'audio' or 'unknown'.
        'url': # The URL for the image in the local cache
        'remote_url': # The remote URL for the media (if the image is from a remote instance)
        'preview_url': # The URL for the media preview
        'text_url': # The display text for the media (what shows up in toots)
        'meta': # Dictionary of two metadata dicts (see below),
                # 'original' and 'small' (preview). Either may be empty.
                # May additionally contain an "fps" field giving a videos frames per second (possibly
                # rounded), and a "length" field giving a videos length in a human-readable format.
                # Note that a video may have an image as preview.
                # May also contain a 'focus' dict and a media 'colors' dict.
        'blurhash': # The blurhash for the image, used for preview / placeholder generation
        'description': # If set, the user-provided description for this media.
    }

    # Metadata dicts (image) - all fields are optional:
    {
       'width': # Width of the image in pixels
       'height': # Height of the image in pixels
       'aspect': # Aspect ratio of the image as a floating point number
       'size': # Textual representation of the image size in pixels, e.g. '800x600'
    }

    # Metadata dicts (video, gifv) - all fields are optional:
    {
        'width': # Width of the video in pixels
        'heigh': # Height of the video in pixels
        'frame_rate': # Exact frame rate of the video in frames per second.
                      # Can be an integer fraction (i.e. "20/7")
        'duration': # Duration of the video in seconds
        'bitrate': # Average bit-rate of the video in bytes per second
    }

    # Metadata dicts (audio) - all fields are optional:
    {
        'duration': # Duration of the audio file in seconds
        'bitrate': # Average bit-rate of the audio file in bytes per second
    }

    # Focus Metadata dict:
    {
        'x': Focus point x coordinate (between -1 and 1)
        'y': Focus point x coordinate (between -1 and 1)
    }

    # Media colors dict:
    {
        'foreground': # Estimated foreground colour for the attachment thumbnail
        'background': # Estimated background colour for the attachment thumbnail
        'accent': # Estimated accent colour for the attachment thumbnail

Card dicts
~~~~~~~~~~
.. _card dict:

.. code-block:: python

    mastodon.status_card(<numerical id>):
    # Returns the following dictionary
    {
        'url': # The URL of the card.
        'title': # The title of the card.
        'description': # The description of the card.
        'type': # Embed type: 'link', 'photo', 'video', or 'rich'
        'image': # (optional) The image associated with the card.

        # OEmbed data (all optional):
        'author_name': # Name of the embedded contents author
        'author_url': # URL pointing to the embedded contents author
        'description': # Description of the embedded content
        'width': # Width of the embedded object
        'height': # Height of the embedded object
        'html': # HTML string of the embed
        'provider_name': # Name of the provider from which the embed originates
        'provider_url': # URL pointing to the embeds provider
        'blurhash': # (optional) Blurhash of the preview image
    }

Search result dicts
~~~~~~~~~~~~~~~~~~~
.. _search result dict:

.. code-block:: python

    mastodon.search("<query>")
    # Returns the following dictionary
    {
        'accounts': # List of user dicts resulting from the query
        'hashtags': # List of hashtag dicts resulting from the query
        'statuses': # List of toot dicts resulting from the query
    }

Instance dicts
~~~~~~~~~~~~~~
.. _instance dict:

.. code-block:: python

    mastodon.instance()
    # Returns the following dictionary
    {
        'domain': # The instances domain name
        'description': # A brief instance description set by the admin
        'short_description': # An even briefer instance description
        'email': # The admin contact email
        'title': # The instance's title
        'uri': # The instance's URL
        'version': # The instance's Mastodon version
        'urls': # Additional URLs dict, presently only 'streaming_api' with the
                # stream websocket address.
        'stats: # A dictionary containing three stats, user_count (number of local users),
                # status_count (number of local statuses) and domain_count (number of known
                # instance domains other than this one).
        'contact_account': # User dict of the primary contact for the instance
        'languages': # Array of ISO 639-1 (two-letter) language codes the instance
                     # has chosen to advertise.
        'registrations': # Boolean indication whether registrations on this instance are open
                         # (True) or not (False)
        'approval_required': # True if account approval is required when registering,
        'rules': # List of dicts with `id` and `text` fields, one for each server rule set by the admin
    }

Activity dicts
~~~~~~~~~~~~~~
.. _activity dict:

.. code-block:: python

    mastodon.instance_activity()[0]
    # Returns the following dictionary
    {
        'week': # Date of the first day of the week the stats were collected for
        'logins': # Number of users that logged in that week
        'registrations': # Number of new users that week
        'statuses': # Number of statuses posted that week
    }

Report dicts
~~~~~~~~~~~~
.. _report dict:

.. code-block:: python

    mastodon.admin_reports()[0]
    # Returns the following dictionary
    {
        'id': # Numerical id of the report
        'action_taken': # True if a moderator or admin has processed the
                        # report, False otherwise.

        # The following fields are only present in the report dicts returned by moderation API:
        'comment': # Text comment submitted with the report
        'created_at': # Time at which this report was created, as a datetime object
        'updated_at': # Last time this report has been updated, as a datetime object
        'account': # User dict of the user that filed this report
        'target_account': # Account that has been reported with this report
        'assigned_account': # If the report as been assigned to an account,
                            # User dict of that account (None if not)
        'action_taken_by_account': # User dict of the account that processed this report
        'statuses': # List of statuses attached to the report, as toot dicts
    }

Push subscription dicts
~~~~~~~~~~~~~~~~~~~~~~~
.. _push subscription dict:

.. code-block:: python

    mastodon.push_subscription()
    # Returns the following dictionary
    {
        'id': # Numerical id of the push subscription
        'endpoint': # Endpoint URL for the subscription
        'server_key': # Server pubkey used for signature verification
        'alerts': # Subscribed events - dict that may contain keys 'follow',
                  # 'favourite', 'reblog' and 'mention', with value True
                  # if webpushes have been requested for those events.
    }

Push notification dicts
~~~~~~~~~~~~~~~~~~~~~~~
.. _push notification dict:

.. code-block:: python

    mastodon.push_subscription_decrypt_push(...)
    # Returns the following dictionary
    {
        'access_token': # Access token that can be used to access the API as the
                        # notified user
        'body': # Text body of the notification
        'icon': # URL to an icon for the notification
        'notification_id': # ID that can be passed to notification() to get the full
                           # notification object,
        'notification_type': # 'mention', 'reblog', 'follow' or 'favourite'
        'preferred_locale': # The user's preferred locale
        'title': # Title for the notification
    }

Preference dicts
~~~~~~~~~~~~~~~~
.. _preference dict:

.. code-block:: python

    mastodon.preferences()
    # Returns the following dictionary
    {
        'posting:default:visibility': # The default visibility setting for the user's posts,
                                      # as a string
        'posting:default:sensitive': # Boolean indicating whether the user's uploads should
                                     # be marked sensitive by default
        'posting:default:language': # The user's default post language, if set (None if not)
        'reading:expand:media': # How the user wishes to be shown sensitive media. Can be
                                # 'default' (hide if sensitive), 'hide_all' or 'show_all'
        'reading:expand:spoilers': # Boolean indicating whether the user wishes to expand
                                   # content warnings by default
    }

Featured tag dicts
~~~~~~~~~~~~~~~~~~
.. _featured tag dict:

.. code-block:: python

    mastodon.featured_tags()[0]
    # Returns the following dictionary:
    {
        'id': # The featured tags id
        'name': # The featured tags name (without leading #)
        'statuses_count': # Number of publicly visible statuses posted with this hashtag that this instance knows about
        'last_status_at': # The last time a public status containing this hashtag was added to this instance's database
                          # (can be None if there are none)
    }

Read marker dicts
~~~~~~~~~~~~~~~~~
.. _read marker dict:

.. code-block:: python

    mastodon.markers_get()["home"]
    # Returns the following dictionary:
    {
        'last_read_id': # ID of the last read object in the timeline
        'version': # A counter that is incremented whenever the marker is set to a new status
        'updated_at': # The time the marker was last set, as a datetime object
    }

Announcement dicts
~~~~~~~~~~~~~~~~~~
.. _announcement dict:

.. code-block:: python

    mastodon.annoucements()[0]
    # Returns the following dictionary:
    {
        'id': # The annoucements id
        'content': # The contents of the annoucement, as an html string
        'starts_at': # The annoucements start time, as a datetime object. Can be None
        'ends_at': # The annoucements end time, as a datetime object. Can be None
        'all_day': # Boolean indicating whether the annoucement represents an "all day" event
        'published_at': # The annoucements publish time, as a datetime object
        'updated_at': # The annoucements last updated time, as a datetime object
        'read': # A boolean indicating whether the logged in user has dismissed the annoucement
        'mentions': # Users mentioned in the annoucement, as a list of mention dicts
        'tags': # Hashtags mentioned in the announcement, as a list of hashtag dicts
        'emojis': # Custom emoji used in the annoucement, as a list of emoji dicts
        'reactions': # Reactions to the annoucement, as a list of reaction dicts (documented inline here):
        [ {
            'name': '# Name of the custom emoji or unicode emoji of the reaction
            'count': # Reaction counter (i.e. number of users who have added this reaction)
            'me': # True if the logged-in user has reacted with this emoji, false otherwise
            'url': # URL for the custom emoji image
            'static_url': # URL for a never-animated version of the custom emoji image
        } ],
    }

Admin account dicts
~~~~~~~~~~~~~~~~~~~
.. _admin account dict:

.. code-block:: python

    mastodon.admin_account(id)
    # Returns the following dictionary
    {
        'id': # The users id,
        'username': # The users username, no leading @
        'domain': # The users domain
        'created_at': # The time of account creation
        'email': # For local users, the user's email
        'ip': # For local users, the user's last known IP address
        'role': # 'admin', 'moderator' or None
        'confirmed': # For local users, False if the user has not confirmed their email, True otherwise
        'suspended': # Boolean indicating whether the user has been suspended
        'silenced': # Boolean indicating whether the user has been suspended
        'disabled': # For local users, boolean indicating whether the user has had their login disabled
        'approved': # For local users, False if the user is pending, True otherwise
        'locale': # For local users, the locale the user has set,
        'invite_request': # If the user requested an invite, the invite request comment of that user. (TODO permanent?)
        'invited_by_account_id': # Present if the user was invited by another user and set to the inviting users id.
        'account': # The user's account, as a standard user dict
    }

Status edit dicts
~~~~~~~~~~~~~~~~~
.. _status edit dict:

.. code-block:: python

    mastodonstatus_history(id)[0]
    # Returns the following dictionary
    {
        TODO
    }


App registration and user authentication
----------------------------------------
Before you can use the Mastodon API, you have to register your
application (which gets you a client key and client secret)
and then log in (which gets you an access token). These functions
allow you to do those things. Additionally, it is also possible
to programmatically register a new user.

For convenience, once you have a client id, secret and access token,
you can simply pass them to the constructor of the class, too!

Note that while it is perfectly reasonable to log back in whenever
your app starts, registering a new application on every
startup is not, so don't do that - instead, register an application
once, and then persist your client id and secret. A convenient method
for this is provided by the functions dealing with registering the app,
logging in and the Mastodon classes constructor.

To talk to an instance different from the flagship instance, specify
the api_base_url (usually, just the URL of the instance, i.e.
https://mastodon.social/ for the flagship instance). If no protocol
is specified, Mastodon.py defaults to https.

.. automethod:: Mastodon.create_app
.. automethod:: Mastodon.__init__
.. _log_in():
.. automethod:: Mastodon.log_in
.. _auth_request_url():
.. automethod:: Mastodon.auth_request_url
.. automethod:: Mastodon.create_account
.. automethod:: Mastodon.email_resend_confirmation

Versioning
----------
Mastodon.py will check if a certain endpoint is available before doing API
calls. By default, it checks against the version of Mastodon retrieved on
init(), or the version you specified. Mastodon.py can be set (in the
constructor) to either check if an endpoint is available at all (this is the
default) or to check if the endpoint is available and behaves as in the newest
Mastodon version (with regards to parameters as well as return values).
Version checking can also be disabled altogether. If a version check fails,
Mastodon.py throws a `MastodonVersionError`.

Some functions need to check what version of Mastodon they are talking to.
These will generally use a cached version to avoid sending a lot of pointless
requests.

Many non-mainline forks have various different formats for their versions and
they have different, incompatible ideas about how to report version. Mastodon.py
tries its best to figure out what is going on, but success is not guaranteed.

With the following functions, you can make Mastodon.py re-check the server
version or explicitly determine if a specific minimum Version is available.
Long-running applications that aim to support multiple Mastodon versions
should do this from time to time in case a server they are running against
updated.

.. automethod:: Mastodon.retrieve_mastodon_version
.. automethod:: Mastodon.verify_minimum_version

Reading data: Instances
-----------------------
These functions allow you to fetch information associated with the
current instance.

.. automethod:: Mastodon.instance
.. automethod:: Mastodon.instance_activity
.. automethod:: Mastodon.instance_peers
.. automethod:: Mastodon.instance_health
.. automethod:: Mastodon.instance_nodeinfo
.. automethod:: Mastodon.instance_rules

Reading data: Timelines
-----------------------
This function allows you to access the timelines a logged in
user could see, as well as hashtag timelines and the public (federated)
and local timelines. For the public, local and hashtag timelines,
access is allowed even when not authenticated.

.. _timeline():
.. automethod:: Mastodon.timeline
.. automethod:: Mastodon.timeline_home
.. automethod:: Mastodon.timeline_local
.. _timeline_public():
.. automethod:: Mastodon.timeline_public
.. _timeline_hashtag():
.. automethod:: Mastodon.timeline_hashtag
.. automethod:: Mastodon.timeline_list
.. automethod:: Mastodon.conversations

Reading data: Statuses
----------------------
These functions allow you to get information about single statuses.

.. automethod:: Mastodon.status
.. automethod:: Mastodon.status_context
.. automethod:: Mastodon.status_reblogged_by
.. automethod:: Mastodon.status_favourited_by
.. automethod:: Mastodon.status_card
.. automethod:: Mastodon.status_history
.. automethod:: Mastodon.status_source

Reading data: Scheduled statuses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
These functions allow you to get information about scheduled statuses.

.. automethod:: Mastodon.scheduled_statuses
.. automethod:: Mastodon.scheduled_status

Reading data: Polls
~~~~~~~~~~~~~~~~~~~
This function allows you to get and refresh information about polls.

.. automethod:: Mastodon.poll

Reading data: Notifications
---------------------------
This function allows you to get information about a user's notifications.

.. automethod:: Mastodon.notifications

Reading data: Accounts
----------------------
These functions allow you to get information about accounts and
their relationships.

.. automethod:: Mastodon.account
.. automethod:: Mastodon.account_verify_credentials
.. automethod:: Mastodon.me
.. automethod:: Mastodon.account_statuses
.. automethod:: Mastodon.account_following
.. automethod:: Mastodon.account_followers
.. automethod:: Mastodon.account_relationships
.. automethod:: Mastodon.account_search
.. automethod:: Mastodon.account_lists
.. automethod:: Mastodon.account_lookup

Reading data: Featured tags
~~~~~~~~~~~~~~~~~~~~~~~~~~~
These functions allow retrieving info about a users featured and suggested tags.

.. automethod:: Mastodon.featured_tags
.. automethod:: Mastodon.featured_tag_suggestions

Reading data: Keyword filters
-----------------------------
These functions allow you to get information about keyword filters.

.. automethod:: Mastodon.filters
.. automethod:: Mastodon.filter
.. automethod:: Mastodon.filters_apply

Reading data: Follow suggestions
--------------------------------

.. automethod:: Mastodon.suggestions

Reading data: Profile directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: Mastodon.directory

Reading data: Lists
-------------------
These functions allow you to view information about lists.

.. automethod:: Mastodon.lists
.. automethod:: Mastodon.list
.. automethod:: Mastodon.list_accounts

Reading data: Follows
---------------------

.. automethod:: Mastodon.follows

Reading data: Favourites
------------------------

.. automethod:: Mastodon.favourites

Reading data: Follow requests
-----------------------------

.. automethod:: Mastodon.follow_requests

Reading data: Searching
-----------------------

.. automethod:: Mastodon.search
.. automethod:: Mastodon.search_v2

Reading data: Trends
--------------------

.. automethod:: Mastodon.trends

Reading data: Mutes and blocks
------------------------------
These functions allow you to get information about accounts that are
muted or blocked by the logged in user.

.. automethod:: Mastodon.mutes
.. automethod:: Mastodon.blocks

Reading data: Bookmarks
-----------------------

.. automethod:: Mastodon.bookmarks

Reading data: Reports
---------------------
In Mastodon versions before 2.5.0 this function allowed for the retrieval
of reports filed by the logged in user. It has since been removed.

.. automethod:: Mastodon.reports


Writing data: Last-read markers
--------------------------------
This function allows you to set get last read position for timelines.

.. automethod:: Mastodon.markers_get

Reading data: Domain blocks
---------------------------

.. automethod:: Mastodon.domain_blocks

Reading data: Emoji
-------------------

.. automethod:: Mastodon.custom_emojis

Reading data: Apps
------------------

.. automethod:: Mastodon.app_verify_credentials

Reading data: Endorsements
--------------------------

.. automethod:: Mastodon.endorsements

Reading data: Preferences
--------------------------

.. automethod:: Mastodon.preferences

Reading data: Announcements
---------------------------

.. automethod:: Mastodon.announcements


Writing data: Statuses
----------------------
These functions allow you to post statuses to Mastodon and to
interact with already posted statuses.

.. _status_post():
.. automethod:: Mastodon.status_post
.. automethod:: Mastodon.status_reply
.. automethod:: Mastodon.toot
.. _make_poll():
.. automethod:: Mastodon.make_poll
.. automethod:: Mastodon.status_reblog
.. automethod:: Mastodon.status_unreblog
.. automethod:: Mastodon.status_favourite
.. automethod:: Mastodon.status_unfavourite
.. automethod:: Mastodon.status_mute
.. automethod:: Mastodon.status_unmute
.. automethod:: Mastodon.status_pin
.. automethod:: Mastodon.status_unpin
.. automethod:: Mastodon.status_bookmark
.. automethod:: Mastodon.status_unbookmark
.. automethod:: Mastodon.status_delete
.. automethod:: Mastodon.status_update


Writing data: Scheduled statuses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mastodon allows you to schedule statuses (using `status_post()`_).
The functions in this section allow you to update or delete
scheduled statuses.

.. automethod:: Mastodon.scheduled_status_update
.. automethod:: Mastodon.scheduled_status_delete

Writing data: Polls
~~~~~~~~~~~~~~~~~~~
This function allows you to vote in polls.

.. automethod:: Mastodon.poll_vote

Writing data: Notifications
---------------------------
These functions allow you to clear all or some notifications.

.. automethod:: Mastodon.notifications_clear
.. automethod:: Mastodon.notifications_dismiss

Writing data: Conversations
---------------------------
This function allows you to mark conversations read.

.. automethod:: Mastodon.conversations_read

Writing data: Accounts
----------------------
These functions allow you to interact with other accounts: To (un)follow and
(un)block.

.. automethod:: Mastodon.account_follow
.. automethod:: Mastodon.account_unfollow
.. automethod:: Mastodon.account_block
.. automethod:: Mastodon.account_unblock
.. automethod:: Mastodon.account_mute
.. automethod:: Mastodon.account_unmute
.. automethod:: Mastodon.account_pin
.. automethod:: Mastodon.account_unpin
.. automethod:: Mastodon.account_update_credentials
.. automethod:: Mastodon.account_note_set
.. automethod:: Mastodon.account_featured_tags

Writing data: Featured tags
~~~~~~~~~~~~~~~~~~~~~~~~~~~
These functions allow setting which tags are featured on a user's profile.

.. automethod:: Mastodon.featured_tag_create
.. automethod:: Mastodon.featured_tag_delete

Writing data: Keyword filters
-----------------------------
These functions allow you to manipulate keyword filters.

.. automethod:: Mastodon.filter_create
.. automethod:: Mastodon.filter_update
.. automethod:: Mastodon.filter_delete

Writing data: Follow suggestions
--------------------------------

.. automethod:: Mastodon.suggestion_delete

Writing data: Lists
-------------------
These functions allow you to create, maintain and delete lists.

When creating lists, note that a user can only
have a maximum of 50 lists.

.. automethod:: Mastodon.list_create
.. automethod:: Mastodon.list_update
.. automethod:: Mastodon.list_delete
.. automethod:: Mastodon.list_accounts_add
.. automethod:: Mastodon.list_accounts_delete

Writing data: Follow requests
-----------------------------
These functions allow you to accept or reject incoming follow requests.

.. automethod:: Mastodon.follow_request_authorize
.. automethod:: Mastodon.follow_request_reject

Writing data: Media
-------------------
This function allows you to upload media to Mastodon. The returned
media IDs (Up to 4 at the same time) can then be used with post_status
to attach media to statuses.

.. _media_post():

.. automethod:: Mastodon.media_post
.. automethod:: Mastodon.media_update

Writing data: Reports
---------------------

.. automethod:: Mastodon.report

Writing data: Last-read markers
-------------------------------
This function allows you to set the last read position for timelines to
allow for persisting where the user was reading a timeline between sessions
and clients / devices.

.. automethod:: Mastodon.markers_set

Writing data: Domain blocks
---------------------------
These functions allow you to block and unblock all statuses from a domain
for the logged-in user.

.. automethod:: Mastodon.domain_block
.. automethod:: Mastodon.domain_unblock


Writing data: Announcements
---------------------------
These functions allow you to mark annoucements read and modify reactions.

.. automethod:: Mastodon.announcement_dismiss
.. automethod:: Mastodon.announcement_reaction_create
.. automethod:: Mastodon.announcement_reaction_delete

Pagination
----------
These functions allow for convenient retrieval of paginated data.

.. automethod:: Mastodon.fetch_next
.. automethod:: Mastodon.fetch_previous
.. automethod:: Mastodon.fetch_remaining

Blurhash decoding
-----------------
This function allows for easy basic decoding of blurhash strings to images.
This requires Mastodon.pys optional "blurhash" feature dependencies.

.. automethod:: Mastodon.decode_blurhash

Streaming
---------
These functions allow access to the streaming API. For the public, local and hashtag streams,
access is generally possible without authenticating.

If `run_async` is False, these  methods block forever (or until an error is encountered).

If `run_async` is True, the listener will listen on another thread and these methods
will return a handle corresponding to the open connection. If, in addition, `reconnect_async` is True,
the thread will attempt to reconnect to the streaming API if any errors are encountered, waiting
`reconnect_async_wait_sec` seconds between reconnection attempts. Note that no effort is made
to "catch up" - events created while the connection is broken will not be received. If you need to make
sure to get absolutely all notifications / deletes / toots, you will have to do that manually, e.g.
using the `on_abort` handler to fill in events since the last received one and then reconnecting.
Both `run_async` and `reconnect_async` default to false, and you'll have to set each to true
separately to get the behaviour described above.

The connection may be closed at any time by calling the handles close() method. The
current status of the handler thread can be checked with the handles is_alive() function,
and the streaming status can be checked by calling is_receiving().

The streaming functions take instances of `StreamListener` as the `listener` parameter.
A `CallbackStreamListener` class that allows you to specify function callbacks
directly is included for convenience.

For new well-known events implement the streaming function in `StreamListener` or `CallbackStreamListener`.
The function name is `on_` + the event name. If the event name contains dots, they are replaced with
underscored, e.g. for an event called 'status.update' the listener function should be named `on_status_update`.

It may be that future Mastodon versions will come with completely new (unknown) event names.
If you want to do something when such an event is received, override the listener function `on_unknown_event`. 
This has an additional parameter `name` which informs about the name of the event. `unknown_event` contains the 
content of the event. Alternatively, a callback function can be passed in the `unknown_event_handler` parameter 
in the `CallbackStreamListener` constructor.

Note that the `unknown_event` handler is *not* guaranteed to receive events once they have been implemented.
Events will only go to this handler temporarily, while Mastodon.py has not been updated. Changes to what events
do and do not go into the handler will not be considered a breaking change. If you want to handle a new event whose
name you _do_ know, define an appropriate handler in your StreamListener, which will work even if it is not listed here.

When in not-async mode or async mode without async_reconnect, the stream functions may raise
various exceptions: `MastodonMalformedEventError` if a received event cannot be parsed and
`MastodonNetworkError` if any connection problems occur.

.. automethod:: Mastodon.stream_user
.. automethod:: Mastodon.stream_public
.. automethod:: Mastodon.stream_local
.. automethod:: Mastodon.stream_hashtag
.. automethod:: Mastodon.stream_list
.. automethod:: Mastodon.stream_healthy

StreamListener
~~~~~~~~~~~~~~

.. autoclass:: StreamListener
.. automethod:: StreamListener.on_update
.. automethod:: StreamListener.on_notification
.. automethod:: StreamListener.on_delete
.. automethod:: StreamListener.on_conversation
.. automethod:: StreamListener.on_status_update
.. automethod:: StreamListener.on_unknown_event
.. automethod:: StreamListener.on_abort
.. automethod:: StreamListener.handle_heartbeat

CallbackStreamListener
~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: CallbackStreamListener

Push subscriptions
------------------
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


Moderation API
--------------
These functions allow you to perform moderation actions on users and generally
process reports using the API. To do this, you need access to the "admin:read" and/or
"admin:write" scopes or their more granular variants (both for the application and the
access token), as well as at least moderator access. Mastodon.py will not request these
by default, as that would be very dangerous.

BIG WARNING: TREAT ANY ACCESS TOKENS THAT HAVE ADMIN CREDENTIALS AS EXTREMELY, MASSIVELY
SENSITIVE DATA AND MAKE EXTRA SURE TO REVOKE THEM AFTER TESTING, NOT LET THEM SIT IN FILES
SOMEWHERE, TRACK WHICH ARE ACTIVE, ET CETERA. ANY EXPOSURE OF SUCH ACCESS TOKENS MEANS YOU
EXPOSE THE PERSONAL DATA OF ALL YOUR USERS TO WHOEVER HAS THESE TOKENS. TREAT THEM WITH
EXTREME CARE.

This is not to say that you should not treat access tokens from admin accounts that do not
have admin: scopes attached with a lot of care, but be extra careful with those that do.

.. automethod:: Mastodon.admin_accounts
.. automethod:: Mastodon.admin_account
.. automethod:: Mastodon.admin_account_enable
.. automethod:: Mastodon.admin_account_approve
.. automethod:: Mastodon.admin_account_reject
.. automethod:: Mastodon.admin_account_unsilence
.. automethod:: Mastodon.admin_account_unsuspend
.. automethod:: Mastodon.admin_account_moderate

.. automethod:: Mastodon.admin_reports
.. automethod:: Mastodon.admin_report
.. automethod:: Mastodon.admin_report_assign
.. automethod:: Mastodon.admin_report_unassign
.. automethod:: Mastodon.admin_report_reopen
.. automethod:: Mastodon.admin_report_resolve

Acknowledgements
----------------
Mastodon.py contains work by a large number of contributors, many of which have
put significant work into making it a better library. You can find some information
about who helped with which particular feature or fix in the changelog.

.. _Mastodon: https://github.com/mastodon/mastodon
.. _Mastodon flagship instance: https://mastodon.social/
.. _Official Mastodon API docs: https://docs.joinmastodon.org/client/intro/

.. toctree::
   :maxdepth: -1
   :collapse_navigation: False
