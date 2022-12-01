Return values
=============
.. py:module:: mastodon
.. py:class: Mastodon

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

Currently, some of these may be out of date - refer to the Mastodon documentation at
https://docs.joinmastodon.org/entities/ for when fields seem to be missing. This will
be addressed in the next version of Mastodon.py.

User / account dicts
--------------------
.. _user dict:
.. _user dicts:
.. _account dict:
.. _account dicts:

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

Toot / Status dicts
----------
.. _toot dict:
.. _toot dicts:
.. _status dict:
.. _status dicts:

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

Status edit dicts
-----------------
.. _status edit dict:

.. code-block:: python

    mastodonstatus_history(id)[0]
    # Returns the following dictionary
    {
        'content': # Content for this version of the status
        'spoiler_text': # CW / Spoiler text for this version of the status
        'sensitive': # Whether media in this version of the status is marked as sensitive 
        'created_at': # Time at which this version of the status was posted
        'account': # Account dict of the user that posted the status
        'media_attachments': # List of media dicts with the attached media for this version of the status
        'emojis'# List of emoji dicts for this version of the status
    }

Mention dicts
-------------
.. _mention dict:

.. code-block:: python

    {
        'url': # Mentioned user's profile URL (potentially remote)
        'username': # Mentioned user's user name (not including domain)
        'acct': # Mentioned user's account name (including domain)
        'id': # Mentioned user's (local) account ID
    }

Scheduled status / toot dicts
-----------------------------
.. _scheduled status dict:
.. _scheduled status dicts:
.. _scheduled toot dict:
.. _scheduled toot dicts:

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
----------
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
------------------
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
-------------
.. _hashtag dict:

.. code-block:: python

    {
        'name': # Hashtag name (not including the #)
        'url': # Hashtag URL (can be remote)
        'history': # List of usage history dicts for up to 7 days. Not present in statuses.
    }

Hashtag usage history dicts
---------------------------
.. _hashtag usage history dict:

.. code-block:: python

    {
        'day': # Date of the day this history dict is for
        'uses': # Number of statuses using this hashtag on that day
        'accounts': # Number of accounts using this hashtag in at least one status on that day
    }

Emoji dicts
-----------
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
-----------------
 .. _application dict:

.. code-block:: python

    {
        'name': # The applications name
        'website': # The applications website
        'vapid_key': # A vapid key that can be used in web applications
    }


Relationship dicts
------------------
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
------------
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
------------------
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
-------------
.. _context dict:

.. code-block:: python

    mastodon.status_context(<numerical id>)
    # Returns the following dictionary:
    {
        'ancestors': # A list of toot dicts
        'descendants': # A list of toot dicts
    }

List dicts
----------
.. _list dict:

.. code-block:: python

    mastodon.list(<numerical id>)
    # Returns the following dictionary:
    {
        'id': # id of the list
        'title': # title of the list
    }

Media dicts
-----------
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
        'x': # Focus point x coordinate (between -1 and 1)
        'y': # Focus point x coordinate (between -1 and 1)
    }

    # Media colors dict:
    {
        'foreground': # Estimated foreground colour for the attachment thumbnail
        'background': # Estimated background colour for the attachment thumbnail
        'accent': # Estimated accent colour for the attachment thumbnail

Card dicts
----------
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
-------------------
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
--------------
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
        'stats': # A dictionary containing three stats, user_count (number of local users),
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
--------------
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
------------
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
-----------------------
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
-----------------------
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
----------------
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
------------------
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
-----------------
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
------------------
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
            'name': # Name of the custom emoji or unicode emoji of the reaction
            'count': # Reaction counter (i.e. number of users who have added this reaction)
            'me': # True if the logged-in user has reacted with this emoji, false otherwise
            'url': # URL for the custom emoji image
            'static_url': # URL for a never-animated version of the custom emoji image
        } ],
    }

Familiar follower dicts
-----------------------
.. _familiar follower dict:

.. code-block:: python

    mastodon.account_familiar_followers(1)[0]
    # Returns the following dictionary:
    {
        'id': # ID of the account for which the familiar followers are being returned
        'accounts': # List of account dicts of the familiar followers
    }
    
Admin account dicts
-------------------
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
        'invite_request': # If the user requested an invite, the invite request comment of that user.
        'invited_by_account_id': # Present if the user was invited by another user and set to the inviting users id.
        'account': # The user's account, as a standard user dict
    }

Admin domain block dicts
------------------------
.. _admin domain block dict:

.. code-block::python 

    mastodon.domain_blocks(id=1)
    #Returns the following dictionary:
    {
        'id': #Str. The database id of a domain block,
        'domain': #Str. The root domain of a block, ie: "example.com",
        'created_at': #Datetime of the block creation.
        'severity': #Str. Severity of the domain block, ie: "suspend".
        'reject_media': #Boolean. True if media is not downloaded from this domain.
        'reject_reports': #Boolean. True if reports are automatically ignored from this domain.
        'private_comment': #Str. Private admin comment for a block. None if not set.
        'public_comment': #Str. Publicly viewable (depending on settings) comment about this domain. None if not set.
        'obfuscate': #Boolean. True if domain name is obfuscated when listing.
    }

Admin measure dicts
-------------------
.. _admin measure dict:

.. code-block:: python

    api.admin_measures(datetime.now() - timedelta(hours=24*5), datetime.now(), active_users=True)
    # Returns the following dictionary
    {
        'key': # Name of the measure returned
        'unit': # Unit for the measure, if available
        'total': # Value of the measure returned
        'human_value': # Human readable variant of the measure returned
        'data': # A list of dicts with the measure broken down by date, as below
    }

    # The data dicts:
    [
        'date': # Date for this row
        'value': # Value of the measure for this row
    }

Admin dimension dicts
---------------------
.. _admin dimension dict:

.. code-block:: python

    api.admin_dimensions(datetime.now() - timedelta(hours=24*5), datetime.now(), languages=True)
    # Returns the following dictionary
    {
        'key': # Name of the dimension returned
        'data': # A list of data dicts, as below
    }
    
    # the data dicts:
    {
        'key': # category for this row
        'human_key': # Human readable name for the category for this row, when available
        'value': # Numeric value for the category
    },
Admin retention dicts
---------------------
.. _admin retention dict:

.. code-block:: python

    api.admin_retention(datetime.now() - timedelta(hours=24*5), datetime.now())
    # Returns the following dictionary
    {
        'period': # Starting time of the period that the data is being returned for
        'frequency': # Time resolution (day or month) for the returned data
        'data': # List of data dicts, as below
    }

    # the data dicts:
    {
        'date': # Date for this entry
        'rate': # Fraction of users retained 
        'value': # Absolute number of users retained
    }
    