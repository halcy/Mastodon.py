from __future__ import annotations # python< 3.9 compat
from datetime import datetime
from typing import Union, Optional, Tuple, List, IO, Dict
from mastodon.types_base import AttribAccessDict, IdType, MaybeSnowflakeIdType, PaginationInfo, PrimitiveIdType, EntityList, PaginatableList, NonPaginatableList, PathOrFile, WebpushCryptoParamsPubkey, WebpushCryptoParamsPrivkey, try_cast_recurse, try_cast, real_issubclass

class Account(AttribAccessDict):
    """
    A user acccount, local or remote.

    Example:

    .. code-block:: python

        # Returns a Account object
        mastodon.account(<account id>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Account/
    """

    id: "MaybeSnowflakeIdType"
    """
    The accounts id.

    Version history:
      * 0.1.0: added
    """

    username: "str"
    """
    The username, without the domain part.

    Version history:
      * 0.1.0: added
    """

    acct: "str"
    """
    The user's account name as username@domain (@domain omitted for local users).

    Version history:
      * 0.1.0: added
    """

    display_name: "str"
    """
    The user's display name.

    Version history:
      * 0.1.0: added
    """

    discoverable: "Optional[bool]"
    """
    Indicates whether or not a user is visible on the discovery page. (nullable)

    Version history:
      * 3.1.0: added
    """

    group: "bool"
    """
    A boolean indicating whether the account represents a group rather than an individual.

    Version history:
      * 3.1.0: added
    """

    locked: "bool"
    """
    Denotes whether the account can be followed without a follow request.

    Version history:
      * 0.1.0: added
    """

    created_at: "datetime"
    """
    The accounts creation time.

    Version history:
      * 0.1.0: added
      * 3.4.0: now resolves to midnight instead of an exact time
    """

    following_count: "int"
    """
    How many accounts this account follows.

    Version history:
      * 0.1.0: added
    """

    followers_count: "int"
    """
    How many followers this account has.

    Version history:
      * 0.1.0: added
    """

    statuses_count: "int"
    """
    How many statuses this account has created, excluding: 1) later deleted posts 2) direct messages / 'mentined users only' posts, except in earlier versions mastodon.

    Version history:
      * 0.1.0: added
      * 2.4.2: no longer includes direct / mentioned-only visibility statuses
    """

    note: "str"
    """
    The users bio / profile text / 'note'.

    Version history:
      * 0.1.0: added
    """

    url: "str"
    """
    A URL pointing to this users profile page (can be remote).
    Should contain (as text): URL

    Version history:
      * 0.1.0: added
    """

    uri: "str"
    """
    Webfinger-resolvable URI for this account.
    Should contain (as text): URL

    Version history:
      * 4.2.0: added
    """

    avatar: "str"
    """
    URL for this users avatar, can be animated.
    Should contain (as text): URL

    Version history:
      * 0.1.0: added
    """

    header: "str"
    """
    URL for this users header image, can be animated.
    Should contain (as text): URL

    Version history:
      * 0.1.0: added
    """

    avatar_static: "str"
    """
    URL for this users avatar, never animated.
    Should contain (as text): URL

    Version history:
      * 1.1.2: added
    """

    header_static: "str"
    """
    URL for this users header image, never animated.
    Should contain (as text): URL

    Version history:
      * 1.1.2: added
    """

    moved: "Optional[Account]"
    """
    If set, Account that this user has set up as their moved-to address. (optional)

    Version history:
      * 2.1.0: added
    """

    suspended: "Optional[bool]"
    """
    Boolean indicating whether the user has been suspended. (optional)

    Version history:
      * 3.3.0: added
    """

    limited: "Optional[bool]"
    """
    Boolean indicating whether the user has been silenced. (optional)

    Version history:
      * 3.5.3: added
    """

    bot: "bool"
    """
    Boolean indicating whether this account is automated.

    Version history:
      * 2.4.0: added
    """

    fields: "NonPaginatableList[AccountField]"
    """
    List of up to four (by default) AccountFields.

    Version history:
      * 2.4.0: added
    """

    emojis: "NonPaginatableList[CustomEmoji]"
    """
    List of custom emoji used in name, bio or fields.

    Version history:
      * 2.4.0: added
    """

    last_status_at: "Optional[datetime]"
    """
    When the most recent status was posted. (nullable)

    Version history:
      * 3.0.0: added
      * 3.1.0: now returns date only, no time
    """

    noindex: "Optional[bool]"
    """
    Whether the local user has opted out of being indexed by search engines. (nullable)

    Version history:
      * 4.0.0: added
    """

    roles: "Optional[NonPaginatableList]"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Deprecated. Was a list of strings with the users roles. Now just an empty list. Mastodon.py makes no attempt to fill it, and the field may be removed if Mastodon removes it. Use the `role` field instead. (optional, nullable)

    Version history:
      * 0.1.0: added
      * 4.0.0: deprecated
    """

    role: "Optional[Role]"
    """
    The users role. Only present for account returned from account_verify_credentials(). (optional)

    Version history:
      * 4.0.0: added
    """

    source: "Optional[CredentialAccountSource]"
    """
    Additional information about the account, useful for profile editing. Only present for account returned from account_verify_credentials(). (optional)

    Version history:
      * 2.4.0: added
    """

    mute_expires_at: "Optional[datetime]"
    """
    If the user is muted by the logged in user with a timed mute, when the mute expires. (nullable)

    Version history:
      * 3.3.0: added
    """

    indexable: "bool"
    """
    Boolean indicating whether public posts by this account should be searchable by anyone.

    Version history:
      * 4.2.0: added
    """

    hide_collections: "bool"
    """
    Boolean indicating whether a user has chosen to hide their network (followers/followed accounts).

    Version history:
      * 4.1.0: added
    """

    memorial: "Optional[bool]"
    """
    Boolean indicating whether the account is an in-memoriam account. (optional)

    Version history:
      * 4.2.0: added
    """

    _version = "4.2.0"

class AccountField(AttribAccessDict):
    """
    A field, displayed on a users profile (e.g. "Pronouns", "Favorite color").

    Example:

    .. code-block:: python

        # Returns a AccountField object
        mastodon.account(<account id>).fields[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Account/
    """

    name: "str"
    """
    The key of a given field's key-value pair.

    Version history:
      * 2.4.0: added
    """

    value: "str"
    """
    The value associated with the `name` key.

    Version history:
      * 2.4.0: added
    """

    verified_at: "Optional[str]"
    """
    Timestamp of when the server verified a URL value for a rel="me" link. (nullable)

    Version history:
      * 2.6.0: added
    """

    _version = "2.6.0"

class Role(AttribAccessDict):
    """
    A role granting a user a set of permissions.

    Example:

    .. code-block:: python

        # Returns a Role object
        mastodon.account_verify_credentials().role

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Role/
    """

    id: "IdType"
    """
    The ID of the Role in the database.

    Version history:
      * 4.0.0: added
    """

    name: "str"
    """
    The name of the role.

    Version history:
      * 4.0.0: added
    """

    permissions: "str"
    """
    A bitmask that represents the sum of all permissions granted to the role.

    Version history:
      * 4.0.0: added
    """

    color: "str"
    """
    The hex code assigned to this role. If no hex code is assigned, the string will be empty.

    Version history:
      * 4.0.0: added
    """

    highlighted: "bool"
    """
    Whether the role is publicly visible as a badge on user profiles.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class CredentialAccountSource(AttribAccessDict):
    """
    Source values useful for editing a user's profile.

    Example:

    .. code-block:: python

        # Returns a CredentialAccountSource object
        mastodon.account_verify_credentials()["source"]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Account/
    """

    privacy: "str"
    """
    The user's default visibility setting ("private", "unlisted" or "public").

    Version history:
      * 1.5.0: added
    """

    sensitive: "bool"
    """
    Denotes whether user media should be marked sensitive by default.

    Version history:
      * 1.5.0: added
    """

    note: "str"
    """
    Plain text version of the user's bio.

    Version history:
      * 1.5.0: added
    """

    language: "Optional[str]"
    """
    The default posting language for new statuses. (nullable)
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 2.4.2: added
    """

    fields: "NonPaginatableList[AccountField]"
    """
    Metadata about the account.

    Version history:
      * 2.4.0: added
    """

    follow_requests_count: "int"
    """
    The number of pending follow requests.

    Version history:
      * 3.0.0: added
    """

    indexable: "bool"
    """
    Boolean indicating whether public posts by this user should be searchable by anyone.

    Version history:
      * 4.2.0: added
    """

    hide_collections: "bool"
    """
    Boolean indicating whether the user has chosen to hide their network (followers/followed accounts).

    Version history:
      * 4.1.0: added
    """

    discoverable: "Optional[bool]"
    """
    Indicates whether or not the user is visible on the discovery page. (nullable)

    Version history:
      * 3.1.0: added
    """

    attribution_domains: "NonPaginatableList[str]"
    """
    List of domains that are allowed to be shown as having published something from this user.

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class Status(AttribAccessDict):
    """
    A single status / toot / post.

    Example:

    .. code-block:: python

        # Returns a Status object
        mastodon.toot("Hello from Python")

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Status/
    """

    id: "MaybeSnowflakeIdType"
    """
    Id of this status.

    Version history:
      * 0.1.0: added
    """

    uri: "str"
    """
    Descriptor for the status EG 'tag:mastodon.social,2016-11-25:objectId=<id>:objectType=Status'.

    Version history:
      * 0.1.0: added
    """

    url: "Optional[str]"
    """
    URL of the status. (nullable)
    Should contain (as text): URL

    Version history:
      * 0.1.0: added
    """

    account: "Account"
    """
    Account which posted the status.

    Version history:
      * 0.1.0: added
    """

    in_reply_to_id: "Optional[MaybeSnowflakeIdType]"
    """
    Id of the status this status is in response to. (nullable)

    Version history:
      * 0.1.0: added
    """

    in_reply_to_account_id: "Optional[MaybeSnowflakeIdType]"
    """
    Id of the account this status is in response to. (nullable)

    Version history:
      * 0.1.0: added
    """

    reblog: "Optional[Status]"
    """
    Denotes whether the status is a reblog. If so, set to the original status. (nullable)

    Version history:
      * 0.1.0: added
    """

    content: "str"
    """
    Content of the status, as HTML: '<p>Hello from Python</p>'.
    Should contain (as text): HTML

    Version history:
      * 0.1.0: added
    """

    created_at: "datetime"
    """
    Creation time.

    Version history:
      * 0.1.0: added
    """

    reblogs_count: "int"
    """
    Number of reblogs.

    Version history:
      * 0.1.0: added
    """

    favourites_count: "int"
    """
    Number of favourites.

    Version history:
      * 0.1.0: added
    """

    reblogged: "Optional[bool]"
    """
    Denotes whether the logged in user has boosted this status. (optional)

    Version history:
      * 0.1.0: added
    """

    favourited: "Optional[bool]"
    """
    Denotes whether the logged in user has favourited this status. (optional)

    Version history:
      * 0.1.0: added
    """

    sensitive: "bool"
    """
    Denotes whether media attachments to the status are marked sensitive.

    Version history:
      * 0.9.9: added
    """

    spoiler_text: "str"
    """
    Warning text that should be displayed before the status content.

    Version history:
      * 1.0.0: added
    """

    visibility: "str"
    """
    Toot visibility.
    Should contain (as text): VisibilityEnum

    Version history:
      * 0.9.9: added
    """

    mentions: "NonPaginatableList[StatusMention]"
    """
    A list of StatusMention this status includes.

    Version history:
      * 0.6.0: added
    """

    media_attachments: "NonPaginatableList[MediaAttachment]"
    """
    List files attached to this status.

    Version history:
      * 0.6.0: added
    """

    emojis: "NonPaginatableList[CustomEmoji]"
    """
    A list of CustomEmoji used in the status.

    Version history:
      * 2.0.0: added
    """

    tags: "NonPaginatableList[Tag]"
    """
    A list of Tags used in the status.

    Version history:
      * 0.6.0: added
    """

    bookmarked: "Optional[bool]"
    """
    True if the status is bookmarked by the logged in user, False if not. (optional)

    Version history:
      * 3.1.0: added
    """

    application: "Optional[Application]"
    """
    Application for the client used to post the status (Does not federate and is therefore always None for remote statuses, can also be None for local statuses for some legacy applications registered before this field was introduced). (optional)

    Version history:
      * 0.9.9: added
    """

    language: "Optional[str]"
    """
    The language of the status, if specified by the server, as ISO 639-1 (two-letter) language code. (nullable)
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 1.4.0: added
    """

    muted: "Optional[bool]"
    """
    Boolean denoting whether the user has muted this status by way of conversation muting. (optional)

    Version history:
      * 1.4.0: added
    """

    pinned: "Optional[bool]"
    """
    Boolean denoting whether or not the status is currently pinned for the associated account. (optional)

    Version history:
      * 1.6.0: added
    """

    replies_count: "int"
    """
    The number of replies to this status.

    Version history:
      * 2.5.0: added
    """

    card: "Optional[PreviewCard]"
    """
    A preview card for links from the status, if present at time of delivery. (nullable)

    Version history:
      * 2.6.0: added
    """

    poll: "Optional[Poll]"
    """
    A poll object if a poll is attached to this status. (nullable)

    Version history:
      * 2.8.0: added
    """

    edited_at: "Optional[datetime]"
    """
    Time the status was last edited. (nullable)

    Version history:
      * 3.5.0: added
    """

    filtered: "Optional[NonPaginatableList[FilterResult]]"
    """
    If present, a list of filter application results that indicate which of the users filters matched and what actions should be taken. (optional)

    Version history:
      * 4.0.0: added
    """

    quote: "Optional[Union[Quote, ShallowQuote]]"
    """
    Information about a quoted status. Can be shallow (ShallowQuote, id only) or full (Quote, full status object included). (nullable)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class Quote(AttribAccessDict):
    """
    A full quote of a status, including the full status object in case of an accepted quote None if the quote is not accepted.

    Example:

    .. code-block:: python

        # Returns a Quote object
        mastodon.status(<status id>).quote

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Quote/
    """

    state: "str"
    """
    The state of the quote.

    Version history:
      * 4.4.0: added
    """

    quoted_status: "Optional[Status]"
    """
    The quoted status object, if the quote has been accepted. (optional)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class ShallowQuote(AttribAccessDict):
    """
    A shallow quote of a status, containing only the ID of the quoted status. Used in multi-level quotes.

    Example:

    .. code-block:: python

        # Returns a ShallowQuote object
        mastodon.status(<status id>).quote.quoted_status.quote

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/ShallowQuote/
    """

    quoted_status_id: "Optional[MaybeSnowflakeIdType]"
    """
    The ID of the quoted status. None if the quote is not accepted. (nullable)

    Version history:
      * 4.4.0: added
    """

    state: "str"
    """
    The state of the quote.

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class StatusEdit(AttribAccessDict):
    """
    An object representing a past version of an edited status.

    Example:

    .. code-block:: python

        # Returns a StatusEdit object
        mastodon.status_history(<status id>)[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/StatusEdit/
    """

    content: "str"
    """
    Content for this version of the status.

    Version history:
      * 3.5.0: added
    """

    spoiler_text: "str"
    """
    CW / Spoiler text for this version of the status.

    Version history:
      * 3.5.0: added
    """

    sensitive: "bool"
    """
    Whether media in this version of the status is marked as sensitive.

    Version history:
      * 3.5.0: added
    """

    created_at: "datetime"
    """
    Time at which this version of the status was posted.

    Version history:
      * 3.5.0: added
    """

    account: "Account"
    """
    Account object of the user that posted the status.

    Version history:
      * 3.5.0: added
    """

    media_attachments: "NonPaginatableList[MediaAttachment]"
    """
    List of MediaAttachment objects with the attached media for this version of the status.

    Version history:
      * 3.5.0: added
    """

    emojis: "NonPaginatableList[CustomEmoji]"
    """
    List of custom emoji used in this version of the status.

    Version history:
      * 3.5.0: added
    """

    poll: "Optional[Poll]"
    """
    The current state of the poll options at this revision. Note that edits changing the poll options will be collapsed together into one edit, since this action resets the poll. (optional)

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class FilterResult(AttribAccessDict):
    """
    A filter action that should be taken on a status.

    Example:

    .. code-block:: python

        # Returns a FilterResult object
        mastodon.status(<status id>).filtered[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/FilterResult/
    """

    filter: "Union[Filter, FilterV2]"
    """
    The filter that was matched.

    Version history:
      * 4.0.0: added
    """

    keyword_matches: "Optional[NonPaginatableList[str]]"
    """
    The keyword within the filter that was matched. (nullable)

    Version history:
      * 4.0.0: added
    """

    status_matches: "Optional[NonPaginatableList]"
    """
    The status ID within the filter that was matched. (nullable)

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class StatusMention(AttribAccessDict):
    """
    A mention of a user within a status.

    Example:

    .. code-block:: python

        # Returns a StatusMention object
        mastodon.toot("@admin he doing it sideways").mentions[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Mention/
    """

    url: "str"
    """
    Mentioned user's profile URL (potentially remote).
    Should contain (as text): URL

    Version history:
      * 0.6.0: added
    """

    username: "str"
    """
    Mentioned user's user name (not including domain).

    Version history:
      * 0.6.0: added
    """

    acct: "str"
    """
    Mentioned user's account name (including domain).

    Version history:
      * 0.6.0: added
    """

    id: "IdType"
    """
    Mentioned user's (local) account ID.

    Version history:
      * 0.6.0: added
    """

    _version = "0.6.0"

class ScheduledStatus(AttribAccessDict):
    """
    A scheduled status / toot to be eventually posted.

    Example:

    .. code-block:: python

        # Returns a ScheduledStatus object
        mastodon.status_post("futureposting", scheduled_at=the_future)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/ScheduledStatus/
    """

    id: "IdType"
    """
    Scheduled status ID (note: Not the id of the status once it gets posted!).

    Version history:
      * 2.7.0: added
    """

    scheduled_at: "datetime"
    """
    datetime object describing when the status is to be posted.

    Version history:
      * 2.7.0: added
    """

    params: "ScheduledStatusParams"
    """
    Parameters for the scheduled status, specifically.

    Version history:
      * 2.7.0: added
    """

    media_attachments: "NonPaginatableList"
    """
    Array of MediaAttachment objects for the attachments to the scheduled status.

    Version history:
      * 2.7.0: added
    """

    _version = "2.7.0"

class ScheduledStatusParams(AttribAccessDict):
    """
    Parameters for a status / toot to be posted in the future.

    Example:

    .. code-block:: python

        # Returns a ScheduledStatusParams object
        mastodon.status_post("futureposting... 2", scheduled_at=the_future).params

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/ScheduledStatus/
    """

    text: "str"
    """
    Toot text.

    Version history:
      * 2.7.0: added
    """

    in_reply_to_id: "Optional[MaybeSnowflakeIdType]"
    """
    ID of the status this one is a reply to. (nullable)

    Version history:
      * 2.7.0: added
    """

    media_ids: "Optional[NonPaginatableList[str]]"
    """
    IDs of media attached to this status. (nullable)

    Version history:
      * 2.7.0: added
    """

    sensitive: "Optional[bool]"
    """
    Whether this status is sensitive or not. (nullable)

    Version history:
      * 2.7.0: added
    """

    visibility: "Optional[str]"
    """
    Visibility of the status. (nullable)

    Version history:
      * 2.7.0: added
    """

    idempotency: "Optional[str]"
    """
    Idempotency key for the scheduled status. (nullable)

    Version history:
      * 2.7.0: added
    """

    scheduled_at: "Optional[datetime]"
    """
    Present, but generally "None". Unsure what this is for - the actual scheduled_at is in the ScheduledStatus object, not here. If you know, let me know. (nullable)

    Version history:
      * 2.7.0: added
    """

    spoiler_text: "Optional[str]"
    """
    CW text for this status. (nullable)

    Version history:
      * 2.7.0: added
    """

    application_id: "IdType"
    """
    ID of the application that scheduled the status.

    Version history:
      * 2.7.0: added
    """

    poll: "Optional[Poll]"
    """
    Poll parameters. (nullable)

    Version history:
      * 2.8.0: added
    """

    language: "Optional[str]"
    """
    The language that will be used for the status. (nullable)
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 2.7.0: added
    """

    allowed_mentions: "Optional[NonPaginatableList[str]]"
    """
    Undocumented. If you know what this does, please let me know. (nullable)

    Version history:
      * 2.7.0: added
    """

    with_rate_limit: "bool"
    """
    Whether the status should be rate limited. It is unclear to me what this does. If you know, please let met know.

    Version history:
      * 2.7.0: added
    """

    quoted_status_id: "Optional[MaybeSnowflakeIdType]"
    """
    ID for a status this status will quote, once posted. (nullable)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class Poll(AttribAccessDict):
    """
    A poll attached to a status.

    Example:

    .. code-block:: python

        # Returns a Poll object
        mastodon.poll(<poll id>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Poll/
    """

    id: "IdType"
    """
    The polls ID.

    Version history:
      * 2.8.0: added
    """

    expires_at: "Optional[datetime]"
    """
    The time at which the poll is set to expire. (nullable)

    Version history:
      * 2.8.0: added
    """

    expired: "bool"
    """
    Boolean denoting whether users can still vote in this poll.

    Version history:
      * 2.8.0: added
    """

    multiple: "bool"
    """
    Boolean indicating whether it is allowed to vote for more than one option.

    Version history:
      * 2.8.0: added
    """

    votes_count: "int"
    """
    Total number of votes cast in this poll.

    Version history:
      * 2.8.0: added
    """

    voted: "bool"
    """
    Boolean indicating whether the logged-in user has already voted in this poll.

    Version history:
      * 2.8.0: added
    """

    options: "NonPaginatableList[PollOption]"
    """
    The poll options.

    Version history:
      * 2.8.0: added
    """

    emojis: "NonPaginatableList[CustomEmoji]"
    """
    List of CustomEmoji used in answer strings,.

    Version history:
      * 2.8.0: added
    """

    own_votes: "NonPaginatableList[int]"
    """
    The logged-in users votes, as a list of indices to the options.

    Version history:
      * 2.8.0: added
    """

    voters_count: "Optional[int]"
    """
    How many unique accounts have voted on a multiple-choice poll. (nullable)

    Version history:
      * 2.8.0: added
    """

    _version = "2.8.0"

class PollOption(AttribAccessDict):
    """
    A poll option within a poll.

    Example:

    .. code-block:: python

        # Returns a PollOption object
        mastodon.poll(<poll id>).options[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Poll/
    """

    title: "str"
    """
    Text of the option.

    Version history:
      * 2.8.0: added
    """

    votes_count: "Optional[int]"
    """
    Count of votes for the option. Can be None if the poll creator has chosen to hide vote totals until the poll expires and it hasn't yet. (nullable)

    Version history:
      * 2.8.0: added
    """

    _version = "2.8.0"

class Conversation(AttribAccessDict):
    """
    A conversation (using direct / mentions-only visibility) between two or more users.

    Example:

    .. code-block:: python

        # Returns a Conversation object
        mastodon.conversations()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Conversation/
    """

    id: "IdType"
    """
    The ID of this conversation object.

    Version history:
      * 2.6.0: added
    """

    unread: "bool"
    """
    Boolean indicating whether this conversation has yet to be read by the user.

    Version history:
      * 2.6.0: added
    """

    accounts: "NonPaginatableList[Account]"
    """
    List of accounts (other than the logged-in account) that are part of this conversation.

    Version history:
      * 2.6.0: added
    """

    last_status: "Optional[Status]"
    """
    The newest status in this conversation. (nullable)

    Version history:
      * 2.6.0: added
    """

    _version = "2.6.0"

class Tag(AttribAccessDict):
    """
    A hashtag, as part of a status or on its own (e.g. trending).

    Example:

    .. code-block:: python

        # Returns a Tag object
        mastodon.trending_tags()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Tag/
    """

    name: "str"
    """
    Hashtag name (not including the #).

    Version history:
      * 0.9.0: added
    """

    url: "str"
    """
    Hashtag URL (can be remote).
    Should contain (as text): URL

    Version history:
      * 0.9.0: added
    """

    history: "Optional[NonPaginatableList[TagHistory]]"
    """
    List of TagHistory for up to 7 days. Not present in statuses. (optional)

    Version history:
      * 2.4.1: added
    """

    following: "Optional[bool]"
    """
    Boolean indicating whether the logged-in user is following this tag. (optional)

    Version history:
      * 4.0.0: added
    """

    id: "Optional[str]"
    """
    The ID of the Tag in the database. Only present for data returned from admin endpoints. (optional)

    Version history:
      * 3.5.0: added
    """

    trendable: "Optional[bool]"
    """
    Whether the hashtag has been approved to trend. Only present for data returned from admin endpoints. (optional)

    Version history:
      * 3.5.0: added
    """

    usable: "Optional[bool]"
    """
    Whether the hashtag has not been disabled from auto-linking. Only present for data returned from admin endpoints. (optional)

    Version history:
      * 3.5.0: added
    """

    requires_review: "Optional[bool]"
    """
    Whether the hashtag has not been reviewed yet to approve or deny its trending. Only present for data returned from admin endpoints. (optional)

    Version history:
      * 3.5.0: added
    """

    featuring: "Optional[bool]"
    """
    Whether the hashtag is featured on the logged-in users profile. (optional)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class TagHistory(AttribAccessDict):
    """
    Usage history for a hashtag.

    Example:

    .. code-block:: python

        # Returns a TagHistory object
        mastodon.trending_tags()[0].history[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Tag/
    """

    day: "datetime"
    """
    Date of the day this TagHistory is for.
    Should contain (as text): datetime

    Version history:
      * 2.4.1: added
    """

    uses: "str"
    """
    Number of statuses using this hashtag on that day.

    Version history:
      * 2.4.1: added
    """

    accounts: "str"
    """
    Number of accounts using this hashtag in at least one status on that day.

    Version history:
      * 2.4.1: added
    """

    _version = "2.4.1"

class CustomEmoji(AttribAccessDict):
    """
    A custom emoji.

    Example:

    .. code-block:: python

        # Returns a CustomEmoji object
        mastodon.toot(":sidekiqin:").emojis[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/CustomEmoji/
    """

    shortcode: "str"
    """
    Emoji shortcode, without surrounding colons.

    Version history:
      * 2.0.0: added
    """

    url: "str"
    """
    URL for the emoji image, can be animated.
    Should contain (as text): URL

    Version history:
      * 2.0.0: added
    """

    static_url: "str"
    """
    URL for the emoji image, never animated.
    Should contain (as text): URL

    Version history:
      * 2.0.0: added
    """

    visible_in_picker: "bool"
    """
    True if the emoji is enabled, False if not.

    Version history:
      * 2.0.0: added
    """

    category: "Optional[str]"
    """
    The category to display the emoji under (not present if none is set). (nullable)

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class Application(AttribAccessDict):
    """
    Information about an app (in terms of the API).

    Example:

    .. code-block:: python

        # Returns a Application object
        mastodon.app_verify_credentials()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Application/
    """

    id: "IdType"
    """
    ID of the application.

    Version history:
      * 2.7.0: added
    """

    name: "str"
    """
    The applications name.

    Version history:
      * 0.9.9: added
    """

    website: "Optional[str]"
    """
    The applications website. (nullable)

    Version history:
      * 0.9.9: added
      * 3.5.1: this property is now nullable
    """

    vapid_key: "str"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    A vapid key that can be used in web applications.

    Version history:
      * 2.8.0: added
      * 4.3.0: deprecated
    """

    redirect_uri: "str"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    The applications redirect URI or urn:ietf:wg:oauth:2.0:oob. Deprecated, it is recommended to use redirect_uris instead.

    Version history:
      * 0.0.0: added
      * 4.3.0: deprecated
    """

    redirect_uris: "NonPaginatableList[str]"
    """
    The applications redirect URI or urn:ietf:wg:oauth:2.0:oob. Deprecated, it is recommended to use redirect_uris instead.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    scopes: "NonPaginatableList[str]"
    """
    The applications available scopes.
    Should contain (as text): Scopes

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class Relationship(AttribAccessDict):
    """
    Information about the relationship between two users.

    Example:

    .. code-block:: python

        # Returns a Relationship object
        mastodon.account_relationships(<account id>)[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Relationship/
    """

    id: "IdType"
    """
    ID of the relationship object.

    Version history:
      * 0.6.0: added
    """

    following: "bool"
    """
    Boolean denoting whether the logged-in user follows the specified user.

    Version history:
      * 0.6.0: added
    """

    followed_by: "bool"
    """
    Boolean denoting whether the specified user follows the logged-in user.

    Version history:
      * 0.6.0: added
    """

    blocking: "bool"
    """
    Boolean denoting whether the logged-in user has blocked the specified user.

    Version history:
      * 0.6.0: added
    """

    blocked_by: "bool"
    """
    Boolean denoting whether the logged-in user has been blocked by the specified user, if information is available.

    Version history:
      * 2.8.0: added
    """

    muting: "bool"
    """
    Boolean denoting whether the logged-in user has muted the specified user.

    Version history:
      * 1.1.0: added
    """

    muting_notifications: "bool"
    """
    Boolean denoting wheter the logged-in user has muted notifications related to the specified user.

    Version history:
      * 2.1.0: added
    """

    requested: "bool"
    """
    Boolean denoting whether the logged-in user has sent the specified user a follow request.

    Version history:
      * 0.9.9: added
    """

    domain_blocking: "bool"
    """
    Boolean denoting whether the logged-in user has blocked the specified users domain.

    Version history:
      * 1.4.0: added
    """

    showing_reblogs: "bool"
    """
    Boolean denoting whether the specified users reblogs show up on the logged-in users Timeline.

    Version history:
      * 2.1.0: added
    """

    endorsed: "bool"
    """
    Boolean denoting wheter the specified user is being endorsed / featured by the logged-in user.

    Version history:
      * 2.5.0: added
    """

    note: "str"
    """
    A free text note the logged in user has created for this account (not publicly visible).

    Version history:
      * 3.2.0: added
    """

    notifying: "bool"
    """
    Boolean indicating whether the logged-in user has enabled notifications for this users posts.

    Version history:
      * 3.3.0: added
    """

    languages: "Optional[NonPaginatableList[str]]"
    """
    List of languages that the logged in user is following this user for (if any). (nullable)
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 4.0.0: added
    """

    requested_by: "bool"
    """
    Boolean indicating whether the specified user has sent the logged-in user a follow request.

    Version history:
      * 0.9.9: added
    """

    _version = "4.0.0"

class Filter(AttribAccessDict):
    """
    Information about a keyword / status filter.

    THIS ENTITY IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Example:

    .. code-block:: python

        # Returns a Filter object
        mastodon.filters()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/V1_Filter/
    """

    id: "IdType"
    """
    Id of the filter.

    Version history:
      * 2.4.3: added
    """

    phrase: "str"
    """
    Filtered keyword or phrase.

    Version history:
      * 2.4.3: added
    """

    context: "NonPaginatableList[str]"
    """
    List of places where the filters are applied.
    Should contain (as text): FilterContextEnum

    Version history:
      * 2.4.3: added
      * 3.1.0: added `account`
    """

    expires_at: "Optional[datetime]"
    """
    Expiry date for the filter. (nullable)

    Version history:
      * 2.4.3: added
    """

    irreversible: "bool"
    """
    Boolean denoting if this filter is executed server-side or if it should be ran client-side.

    Version history:
      * 2.4.3: added
    """

    whole_word: "bool"
    """
    Boolean denoting whether this filter can match partial words.

    Version history:
      * 2.4.3: added
    """

    _version = "3.1.0"

class FilterV2(AttribAccessDict):
    """
    Information about a keyword / status filter.

    Example:

    .. code-block:: python

        # Returns a FilterV2 object
        mastodon.filters_v2()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Filter/
    """

    id: "IdType"
    """
    Id of the filter.

    Version history:
      * 4.0.0: added
    """

    context: "NonPaginatableList[str]"
    """
    List of places where the filters are applied.
    Should contain (as text): FilterContextEnum

    Version history:
      * 4.0.0: added
    """

    expires_at: "Optional[datetime]"
    """
    Expiry date for the filter. (nullable)

    Version history:
      * 4.0.0: added
    """

    title: "str"
    """
    Name the user has chosen for this filter.

    Version history:
      * 4.0.0: added
    """

    filter_action: "str"
    """
    The action to be taken when a status matches this filter.
    Should contain (as text): FilterActionEnum

    Version history:
      * 4.0.0: added
    """

    keywords: "NonPaginatableList[FilterKeyword]"
    """
    A list of keywords that will trigger this filter.

    Version history:
      * 4.0.0: added
    """

    statuses: "NonPaginatableList[FilterStatus]"
    """
    A list of statuses that will trigger this filter.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class Notification(AttribAccessDict):
    """
    A notification about some event, like a new reply or follower.

    Example:

    .. code-block:: python

        # Returns a Notification object
        mastodon.notifications()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Notification/
    """

    id: "IdType"
    """
    id of the notification.

    Version history:
      * 0.9.9: added
    """

    type: "str"
    """
    "mention", "reblog", "favourite", "follow", "poll" or "follow_request".
    Should contain (as text): NotificationTypeEnum

    Version history:
      * 0.9.9: added
      * 2.8.0: added `poll`
      * 3.1.0: added `follow_request`
      * 3.3.0: added `status`
      * 3.5.0: added `update` and `admin.sign_up`
      * 4.0.0: added `admin.report`
      * 4.3.0: added `severed_relationships` and `moderation_warning`
    """

    created_at: "datetime"
    """
    The time the notification was created.

    Version history:
      * 0.9.9: added
    """

    account: "Account"
    """
    Account of the user from whom the notification originates.

    Version history:
      * 0.9.9: added
    """

    status: "Optional[Status]"
    """
    In case of "mention", the mentioning status In case of reblog / favourite, the reblogged / favourited status. (optional)

    Version history:
      * 0.9.9: added
      * 4.0.0: is now optional
    """

    group_key: "str"
    """
    A key to group notifications by. Structure is unspecified and subject to change, so please do not make assumptions about it.

    Version history:
      * 4.3.0: added
    """

    report: "Optional[Report]"
    """
    Report that was the object of the notification. (optional)

    Version history:
      * 4.0.0: added
    """

    event: "Optional[RelationshipSeveranceEvent]"
    """
    Summary of the event that caused follow relationships to be severed. (optional)

    Version history:
      * 4.3.0: added
    """

    moderation_warning: "Optional[AccountWarning]"
    """
    Moderation warning that caused the notification. (optional)

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class Context(AttribAccessDict):
    """
    The conversation context for a given status, i.e. its predecessors (that it replies to) and successors (that reply to it).

    Example:

    .. code-block:: python

        # Returns a Context object
        mastodon.status_context(<status id>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Context/
    """

    ancestors: "NonPaginatableList[Status]"
    """
    A list of Statuses that the Status with this Context is a reply to.

    Version history:
      * 0.6.0: added
    """

    descendants: "NonPaginatableList[Status]"
    """
    A list of Statuses that are replies to the Status with this Context.

    Version history:
      * 0.6.0: added
    """

    _version = "0.6.0"

class UserList(AttribAccessDict):
    """
    A list of users.

    Example:

    .. code-block:: python

        # Returns a UserList object
        mastodon.lists()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/List/
    """

    id: "IdType"
    """
    id of the list.

    Version history:
      * 2.1.0: added
    """

    title: "str"
    """
    title of the list.

    Version history:
      * 2.1.0: added
    """

    replies_policy: "str"
    """
    Which replies should be shown in the list.
    Should contain (as text): RepliesPolicyEnum

    Version history:
      * 3.3.0: added
    """

    exclusive: "Optional[bool]"
    """
    Boolean indicating whether users on this list are removed from the home feed (appearing exclusively as part of the list). nb: This setting applies to posts at the time they are put into a feed. (optional)

    Version history:
      * 4.2.0: added
    """

    _version = "4.2.0"

class MediaAttachment(AttribAccessDict):
    """
    A piece of media (like an image, video, or audio file) that can be or has been attached to a status.

    Example:

    .. code-block:: python

        # Returns a MediaAttachment object
        mastodon.media_post("image.jpg", "image/jpeg")["meta"]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/MediaAttachment/
    """

    id: "MaybeSnowflakeIdType"
    """
    The ID of the attachment.

    Version history:
      * 0.6.0: added
    """

    type: "str"
    """
    Media type: 'image', 'video', 'gifv', 'audio' or 'unknown'.

    Version history:
      * 0.6.0: added
      * 2.9.1: added `audio`
    """

    url: "str"
    """
    The URL for the image in the local cache.
    Should contain (as text): URL

    Version history:
      * 0.6.0: added
    """

    remote_url: "Optional[str]"
    """
    The remote URL for the media (if the image is from a remote instance). (nullable)
    Should contain (as text): URL

    Version history:
      * 0.6.0: added
    """

    preview_url: "Optional[str]"
    """
    The URL for the media preview. (nullable)
    Should contain (as text): URL

    Version history:
      * 0.6.0: added
    """

    text_url: "Optional[str]"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Deprecated. The display text for the media (what shows up in text). May not be present in mastodon versions after 3.5.0. (optional)
    Should contain (as text): URL

    Version history:
      * 0.6.0: added
      * 3.5.0: removed
    """

    meta: "MediaAttachmentMetadataContainer"
    """
    MediaAttachmentMetadataContainer that contains metadata for 'original' and 'small' (preview) versions of the MediaAttachment. Either may be empty. May additionally contain an "fps" field giving a videos frames per second (possibly rounded), and a "length" field giving a videos length in a human-readable format. Note that a video may have an image as preview. May also contain a 'focus' object and a media 'colors' object.

    Version history:
      * 1.5.0: added
      * 2.3.0: added focus
      * 4.0.0: added colors
    """

    blurhash: "str"
    """
    The blurhash for the image, used for preview / placeholder generation.
    Should contain (as text): Blurhash

    Version history:
      * 2.8.1: added
    """

    description: "Optional[str]"
    """
    If set, the user-provided description for this media. (nullable)

    Version history:
      * 2.0.0: added
    """

    preview_remote_url: "Optional[str]"
    """
    If set, the remote URL for the thumbnail of this media attachment on the or originating instance. (nullable)
    Should contain (as text): URL

    Version history:
      * 0.6.0: added
    """

    _version = "4.0.0"

class MediaAttachmentMetadataContainer(AttribAccessDict):
    """
    An object holding metadata about a media attachment and its thumbnail. In addition to the documented fields, there may be additional fields. These are not documented, not guaranteed to be present (they are a Mastodon implementation detail), and may change without notice, so relying on them is not recommended.

    Example:

    .. code-block:: python

        # Returns a MediaAttachmentMetadataContainer object
        mastodon.media_post("audio.mp3").meta

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/MediaAttachment/
    """

    original: "Union[MediaAttachmentImageMetadata, MediaAttachmentVideoMetadata, MediaAttachmentAudioMetadata]"
    """
    Metadata for the original media attachment.

    Version history:
      * 0.6.0: added
    """

    small: "MediaAttachmentImageMetadata"
    """
    Metadata for the thumbnail of this media attachment.

    Version history:
      * 0.6.0: added
    """

    colors: "Optional[MediaAttachmentColors]"
    """
    Information about accent colors for the media. (optional)

    Version history:
      * 4.0.0: added
    """

    focus: "Optional[MediaAttachmentFocusPoint]"
    """
    Information about the focus point for the media. (optional)

    Version history:
      * 3.3.0: added
    """

    _version = "4.0.0"

class MediaAttachmentImageMetadata(AttribAccessDict):
    """
    Metadata for an image media attachment.

    Example:

    .. code-block:: python

        # Returns a MediaAttachmentImageMetadata object
        mastodon.media_post("image.jpg").meta.original

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/MediaAttachment/
    """

    width: "int"
    """
    Width of the image in pixels.

    Version history:
      * 0.6.0: added
    """

    height: "int"
    """
    Height of the image in pixels.

    Version history:
      * 0.6.0: added
    """

    aspect: "float"
    """
    Aspect ratio of the image as a floating point number.

    Version history:
      * 0.6.0: added
    """

    size: "str"
    """
    Textual representation of the image size in pixels, e.g. '800x600'.

    Version history:
      * 0.6.0: added
    """

    _version = "0.6.0"

class MediaAttachmentVideoMetadata(AttribAccessDict):
    """
    Metadata for a video attachment. This can be a proper video, or a gifv (a looping, soundless animation). Both use the same data model currently, though there is a possibility that they could be split in the future.

    Example:

    .. code-block:: python

        # Returns a MediaAttachmentVideoMetadata object
        mastodon.media_post("video.mp4").meta.original

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/MediaAttachment/
    """

    width: "int"
    """
    Width of the video in pixels.

    Version history:
      * 0.6.0: added
    """

    height: "int"
    """
    Height of the video in pixels.

    Version history:
      * 0.6.0: added
    """

    frame_rate: "str"
    """
    Exact frame rate of the video in frames per second. Can be an integer fraction (i.e. "20/7").

    Version history:
      * 0.6.0: added
    """

    duration: "float"
    """
    Duration of the video in seconds.

    Version history:
      * 0.6.0: added
    """

    bitrate: "int"
    """
    Average bit-rate of the video in bytes per second.

    Version history:
      * 0.6.0: added
    """

    _version = "0.6.0"

class MediaAttachmentAudioMetadata(AttribAccessDict):
    """
    Metadata for an audio media attachment.

    Example:

    .. code-block:: python

        # Returns a MediaAttachmentAudioMetadata object
        mastodon.media_post("audio.mp3").meta.original

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/MediaAttachment/
    """

    duration: "float"
    """
    Duration of the audio file in seconds.

    Version history:
      * 0.6.0: added
    """

    bitrate: "int"
    """
    Average bit-rate of the audio file in bytes per second.

    Version history:
      * 0.6.0: added
    """

    _version = "0.6.0"

class MediaAttachmentFocusPoint(AttribAccessDict):
    """
    The focus point for a media attachment, for cropping purposes.

    Example:

    .. code-block:: python

        # Returns a MediaAttachmentFocusPoint object
        mastodon.media_post("image.jpg").meta.focus

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/MediaAttachment/
    """

    x: "float"
    """
    Focus point x coordinate (between -1 and 1), with 0 being the center and -1 and 1 being the left and right edges respectively.

    Version history:
      * 2.3.0: added
    """

    y: "float"
    """
    Focus point x coordinate (between -1 and 1), with 0 being the center and -1 and 1 being the upper and lower edges respectively.

    Version history:
      * 2.3.0: added
    """

    _version = "2.3.0"

class MediaAttachmentColors(AttribAccessDict):
    """
    Object describing the accent colors for a media attachment.

    Example:

    .. code-block:: python

        # Returns a MediaAttachmentColors object
        mastodon.media_post("image.jpg").meta.colors

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/MediaAttachment/
    """

    foreground: "str"
    """
    Estimated foreground colour for the attachment thumbnail, as a html format hex color (#rrggbb).

    Version history:
      * 4.0.0: added
    """

    background: "str"
    """
    Estimated background colour for the attachment thumbnail, as a html format hex color (#rrggbb).

    Version history:
      * 4.0.0: added
    """

    accent: "str"
    """
    Estimated accent colour for the attachment thumbnail.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class PreviewCard(AttribAccessDict):
    """
    A preview card attached to a status, e.g. for an embedded video or link.

    Example:

    .. code-block:: python

        # Returns a PreviewCard object
        mastodon.status_card(<status id>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/PreviewCard/
    """

    url: "str"
    """
    The URL of the card.
    Should contain (as text): URL

    Version history:
      * 1.0.0: added
    """

    title: "str"
    """
    The title of the card.

    Version history:
      * 1.0.0: added
    """

    description: "str"
    """
    Description of the embedded content.

    Version history:
      * 1.0.0: added
    """

    type: "str"
    """
    Embed type: 'link', 'photo', 'video', or 'rich'.

    Version history:
      * 1.3.0: added
    """

    image: "Optional[str]"
    """
    (optional) The image associated with the card. (nullable)
    Should contain (as text): URL

    Version history:
      * 1.0.0: added
    """

    author_name: "str"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Name of the embedded contents author. Deprecated in favour of the `authors` field.

    Version history:
      * 1.3.0: added
      * 4.3.0: deprecated
    """

    author_url: "str"
    """
    URL pointing to the embedded contents author. Deprecated in favour of the `authors` field.
    Should contain (as text): URL

    Version history:
      * 1.3.0: added
      * 4.3.0: deprecated
    """

    width: "int"
    """
    Width of the embedded object.

    Version history:
      * 1.3.0: added
    """

    height: "int"
    """
    Height of the embedded object.

    Version history:
      * 1.3.0: added
    """

    html: "str"
    """
    HTML string representing the embed.
    Should contain (as text): HTML

    Version history:
      * 1.3.0: added
    """

    provider_name: "str"
    """
    Name of the provider from which the embed originates.

    Version history:
      * 1.3.0: added
    """

    provider_url: "str"
    """
    URL pointing to the embeds provider.
    Should contain (as text): URL

    Version history:
      * 1.3.0: added
    """

    blurhash: "Optional[str]"
    """
    Blurhash of the preview image. (nullable)
    Should contain (as text): Blurhash

    Version history:
      * 3.2.0: added
    """

    language: "Optional[str]"
    """
    Language of the embedded content. (optional)
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 1.3.0: added
    """

    embed_url: "str"
    """
    Used for photo embeds, instead of custom `html`.
    Should contain (as text): URL

    Version history:
      * 2.1.0: added
    """

    authors: "NonPaginatableList[PreviewCardAuthor]"
    """
    List of fediverse accounts of the authors of this post, as `PreviewCardAuthor`.

    Version history:
      * 4.3.0: added
    """

    image_description: "str"
    """
    Alt text / image description for the image preview for the card.

    Version history:
      * 4.2.0: added
    """

    published_at: "Optional[datetime]"
    """
    Publication time of the embedded content, if available, as a `datetime` object. (nullable)

    Version history:
      * 4.2.0: added
    """

    history: "Optional[NonPaginatableList[TrendingLinkHistory]]"
    """
    Only present for trending links. A list of TrendingLinkHistory objects. (optional)

    Version history:
      * 3.5.0: added
    """

    _version = "4.3.0"

class TrendingLinkHistory(AttribAccessDict):
    """
    A history entry for a trending link.

    Example:

    .. code-block:: python

        # Returns a TrendingLinkHistory object
        mastodon.trending_links()[0].history[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/PreviewCard/#trends-link
    """

    day: "datetime"
    """
    The day this history entry is for, as a `datetime` object.

    Version history:
      * 3.5.0: added
    """

    uses: "int"
    """
    The number of times this link was used on this day.

    Version history:
      * 3.5.0: added
    """

    accounts: "int"
    """
    The number of accounts that used this link on this day.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class PreviewCardAuthor(AttribAccessDict):
    """
    A preview card attached to a status, e.g. for an embedded video or link.

    Example:

    .. code-block:: python

        # Returns a PreviewCardAuthor object
        mastodon.status_card(<status id>).authors[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/PreviewCardAuthor/
    """

    name: "str"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Name of the embedded contents author.

    Version history:
      * 4.3.0: added
    """

    url: "str"
    """
    URL pointing to the embedded contents author.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    account: "Account"
    """
    Account of the author of this post, as `Account`.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class Search(AttribAccessDict):
    """
    A search result, with accounts, hashtags and statuses.

    THIS ENTITY IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Example:

    .. code-block:: python

        # Returns a Search object
        mastodon.search_v1("<search query>")

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Search/
    """

    accounts: "NonPaginatableList[Account]"
    """
    List of Accounts resulting from the query.

    Version history:
      * 1.1.0: added
    """

    hashtags: "NonPaginatableList[str]"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    List of Tags resulting from the query.

    Version history:
      * 1.1.0: added
      * 2.4.1: v1 search deprecated because it returns a list of strings. v2 search added which returns a list of tags.
      * 3.0.0: v1 removed
    """

    statuses: "NonPaginatableList[Status]"
    """
    List of Statuses resulting from the query.

    Version history:
      * 1.1.0: added
    """

    _version = "3.0.0"

class SearchV2(AttribAccessDict):
    """
    A search result, with accounts, hashtags and statuses.

    Example:

    .. code-block:: python

        # Returns a SearchV2 object
        mastodon.search("<search query>")

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Search/
    """

    accounts: "NonPaginatableList[Account]"
    """
    List of Accounts resulting from the query.

    Version history:
      * 1.1.0: added
    """

    hashtags: "NonPaginatableList[Tag]"
    """
    List of Tags resulting from the query.

    Version history:
      * 2.4.1: added
    """

    statuses: "NonPaginatableList[Status]"
    """
    List of Statuses resulting from the query.

    Version history:
      * 1.1.0: added
    """

    _version = "2.4.1"

class Instance(AttribAccessDict):
    """
    Information about an instance. V1 API version.

    Example:

    .. code-block:: python

        # Returns a Instance object
        mastodon.instance_v1()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/V1_Instance/
    """

    uri: "str"
    """
    The instance's domain name. Moved to 'domain' for the v2 API, though Mastodon.py will mirror it here for backwards compatibility.
    Should contain (as text): DomainName

    Version history:
      * 1.1.0: added
    """

    title: "str"
    """
    The instance's title.

    Version history:
      * 1.1.0: added
    """

    short_description: "str"
    """
    An very brief text only instance description. Moved to 'description' for the v2 API.

    Version history:
      * 2.9.2: added
    """

    description: "str"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    A brief instance description set by the admin. The V1 variant could contain html, but this is now deprecated. Likely to be empty on many instances.
    Should contain (as text): HTML

    Version history:
      * 1.1.0: added
      * 4.0.0: deprecated - likely to be empty.
    """

    email: "str"
    """
    The admin contact email. Moved to InstanceContacts for the v2 API, though Mastodon.py will mirror it here for backwards compatibility.
    Should contain (as text): Email

    Version history:
      * 1.1.0: added
    """

    version: "str"
    """
    The instance's Mastodon version. For a more robust parsed major/minor/patch version see TODO IMPLEMENT FUNCTION TO RETURN VERSIONS.

    Version history:
      * 1.3.0: added
    """

    urls: "InstanceURLs"
    """
    Additional InstanceURLs, in the v1 api version likely to be just 'streaming_api' with the stream server websocket address.

    Version history:
      * 1.4.2: added
    """

    stats: "Optional[InstanceStatistics]"
    """
    InstanceStatistics containing three stats, user_count (number of local users), status_count (number of local statuses) and domain_count (number of known instance domains other than this one). This information is not present in the v2 API variant in this form - there is a 'usage' field instead. (optional)

    Version history:
      * 1.6.0: added
    """

    thumbnail: "Optional[str]"
    """
    Information about thumbnails to represent the instance. In the v1 API variant, simply an URL pointing to a banner image representing the instance. The v2 API provides a more complex structure with a list of thumbnails of different sizes in this field. (nullable)
    Should contain (as text): URL

    Version history:
      * 1.6.1: added
    """

    languages: "NonPaginatableList[str]"
    """
    Array of ISO 639-1 (two-letter) language codes the instance has chosen to advertise.
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 2.3.0: added
    """

    registrations: "bool"
    """
    A boolean indication whether registrations on this instance are open (True) or not (False). The v2 API variant instead provides a dict with more information about possible registration requirements here.

    Version history:
      * 1.6.0: added
    """

    approval_required: "bool"
    """
    True if account approval is required when registering, False if not. Moved to InstanceRegistrations object for the v2 API.

    Version history:
      * 2.9.2: added
    """

    invites_enabled: "bool"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Boolean indicating whether invites are enabled on this instance. Changed in 4.0.0 from being true when the instance setting to enable invites is true to be true when the default user role has invites enabled (i.e. everyone can invite people). The v2 API does not contain this field, and it is not clear whether it will stay around.

    Version history:
      * 3.1.4: added
      * 4.0.0: changed specifics of when field is true, deprecated
    """

    configuration: "InstanceConfiguration"
    """
    Various instance configuration settings - especially various limits (character counts, media upload sizes, ...).

    Version history:
      * 3.1.4: added
    """

    contact_account: "Account"
    """
    Account of the primary contact for the instance. Moved to InstanceContacts for the v2 API.

    Version history:
      * 1.1.0: added
    """

    rules: "NonPaginatableList[Rule]"
    """
    List of Rules with `id` and `text` fields, one for each server rule set by the admin.

    Version history:
      * 3.4.0: added
    """

    _version = "4.0.0"
    _access_map = {
        "uri": "domain",
        "short_description": "description",
        "email": "contact.email",
        "urls": "configuration.urls",
        "contact_account": "contact.account",
    }

class InstanceConfiguration(AttribAccessDict):
    """
    Configuration values for this instance, especially limits and enabled features.

    Example:

    .. code-block:: python

        # Returns a InstanceConfiguration object
        mastodon.instance_v1().configuration

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    accounts: "InstanceAccountConfiguration"
    """
    Account-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    statuses: "InstanceStatusConfiguration"
    """
    Status-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    media_attachments: "InstanceMediaConfiguration"
    """
    Media-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    polls: "InstancePollConfiguration"
    """
    Poll-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    _version = "3.4.2"

class InstanceURLs(AttribAccessDict):
    """
    A list of URLs related to an instance.

    Example:

    .. code-block:: python

        # Returns a InstanceURLs object
        mastodon.instance_v1().urls

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/V1_Instance/
    """

    streaming_api: "str"
    """
    The Websockets URL for connecting to the streaming API. Renamed to 'streaming' for the v2 API.
    Should contain (as text): URL

    Version history:
      * 3.4.2: added
    """

    _version = "3.4.2"
    _access_map = {
        "streaming_api": "streaming",
    }

class InstanceV2(AttribAccessDict):
    """
    Information about an instance.

    Example:

    .. code-block:: python

        # Returns a InstanceV2 object
        mastodon.instance_v2()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    domain: "str"
    """
    The instances domain name.
    Should contain (as text): DomainName

    Version history:
      * 4.0.0: added
    """

    title: "str"
    """
    The instance's title.

    Version history:
      * 4.0.0: added
    """

    version: "str"
    """
    The instance's Mastodon version. For a more robust parsed major/minor/patch version see TODO IMPLEMENT FUNCTION TO RETURN VERSIONS.

    Version history:
      * 4.0.0: added
    """

    source_url: "str"
    """
    URL pointing to a copy of the source code that is used to run this instance. For Mastodon instances, the AGPL requires that this code be available.
    Should contain (as text): URL

    Version history:
      * 4.0.0: added
    """

    description: "str"
    """
    A brief instance description set by the admin. Contains what in the v1 version was the short description.
    Should contain (as text): HTML

    Version history:
      * 4.0.0: added
    """

    usage: "InstanceUsage"
    """
    Information about recent activity on this instance.

    Version history:
      * 4.0.0: added
    """

    thumbnail: "Optional[InstanceThumbnail]"
    """
    Information about thumbnails to represent the instance. (nullable)

    Version history:
      * 4.0.0: added
    """

    languages: "NonPaginatableList[str]"
    """
    Array of ISO 639-1 (two-letter) language codes the instance has chosen to advertise.
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 4.0.0: added
    """

    configuration: "InstanceConfigurationV2"
    """
    Various instance configuration settings - especially various limits (character counts, media upload sizes, ...).

    Version history:
      * 4.0.0: added
    """

    registrations: "InstanceRegistrations"
    """
    InstanceRegistrations object with information about how users can sign up on this instance.

    Version history:
      * 4.0.0: added
    """

    contact: "InstanceContact"
    """
    Contact information for this instance.

    Version history:
      * 4.0.0: added
    """

    rules: "NonPaginatableList[Rule]"
    """
    List of Rules with `id` and `text` fields, one for each server rule set by the admin.

    Version history:
      * 4.0.0: added
    """

    icon: "NonPaginatableList[InstanceIcon]"
    """
    The instance icon, as a list of `InstanceIcon` , with entries representing different available size variants.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    api_versions: "AttribAccessDict"
    """
    A list of API versions supported by this instance, each as an entry in a dict with the name of the implementation as the key (such as 'mastodon'). The exact format is unspecified, any fork or implementation can put what if feels like there. Mastodon currently puts just '2'.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class InstanceIcon(AttribAccessDict):
    """
    Icon for the instance, in a specific size.

    Example:

    .. code-block:: python

        # Returns a InstanceIcon object
        mastodon.instance_v2().icon[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/#InstanceIcon
    """

    src: "str"
    """
    URL for this icon size.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    size: "str"
    """
    Textual representation of the icon size in pixels as (width)x(height) string, e.g. '64x64'.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class InstanceConfigurationV2(AttribAccessDict):
    """
    Configuration values for this instance, especially limits and enabled features.

    Example:

    .. code-block:: python

        # Returns a InstanceConfigurationV2 object
        mastodon.instance_v2().configuration

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    accounts: "InstanceAccountConfiguration"
    """
    Account-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    statuses: "InstanceStatusConfiguration"
    """
    Status-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    media_attachments: "InstanceMediaConfiguration"
    """
    Media-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    polls: "InstancePollConfiguration"
    """
    Poll-related instance configuration fields.

    Version history:
      * 3.4.2: added
    """

    translation: "InstanceTranslationConfiguration"
    """
    Translation-related instance configuration fields. Only present for the v2 API variant of the instance API.

    Version history:
      * 4.0.0: added
    """

    urls: "InstanceURLsV2"
    """
    Instance related URLs. Only present for the v2 API variant of the instance API.

    Version history:
      * 4.0.0: added
    """

    vapid: "InstanceVapidKey"
    """
    VAPID key used by this instance to sign webpush requests. Only present for the v2 API variant of the instance API.

    Version history:
      * 4.3.0: added
    """

    limited_federation: "bool"
    """
    Whether federation on this instance is limited to explicitly allowed domains ('allowlist mode').

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class InstanceVapidKey(AttribAccessDict):
    """
    The VAPID key used by this instance to sign webpush requests.

    Example:

    .. code-block:: python

        # Returns a InstanceVapidKey object
        mastodon.instance_v2().configuration.vapid

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    public_key: "str"
    """
    The public key in VAPID format.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class InstanceURLsV2(AttribAccessDict):
    """
    A list of URLs related to an instance.

    Example:

    .. code-block:: python

        # Returns a InstanceURLsV2 object
        mastodon.instance_v2().configuration.urls

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    streaming: "str"
    """
    The Websockets URL for connecting to the streaming API.
    Should contain (as text): URL

    Version history:
      * 4.0.0: added
    """

    status: "Optional[str]"
    """
    If present, a URL where the status and possibly current issues with the instance can be checked. (optional)
    Should contain (as text): URL

    Version history:
      * 4.0.0: added
    """

    about: "Optional[str]"
    """
    If present, a URL where the instance's about page can be found. (optional)
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    privacy_policy: "Optional[str]"
    """
    If present, a URL where the instance's privacy policy can be found. (optional)
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    terms_of_service: "Optional[str]"
    """
    If present, a URL where the instance's terms of service can be found. (optional)
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class InstanceThumbnail(AttribAccessDict):
    """
    Extended information about an instances thumbnail.

    Example:

    .. code-block:: python

        # Returns a InstanceThumbnail object
        mastodon.instance().thumbnail

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/V1_Instance/
    """

    url: "str"
    """
    The URL for an image representing the instance.
    Should contain (as text): URL

    Version history:
      * 4.0.0: added
    """

    blurhash: "Optional[str]"
    """
    The blurhash for the image representing the instance. (optional)
    Should contain (as text): Blurhash

    Version history:
      * 4.0.0: added
    """

    versions: "Optional[InstanceThumbnailVersions]"
    """
    Different resolution versions of the image representing the instance. (optional)

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class InstanceThumbnailVersions(AttribAccessDict):
    """
    Different resolution versions of the image representing the instance.

    Example:

    .. code-block:: python

        # Returns a InstanceThumbnailVersions object
        mastodon.instance().thumbnail.versions

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    at1x: "Optional[str]"
    """
    The URL for an image representing the instance, for devices with 1x resolution / 96 dpi. (optional)
    Should contain (as text): URL

    Version history:
      * 4.0.0: added
    """

    at2x: "Optional[str]"
    """
    The URL for the image representing the instance, for devices with 2x resolution / 192 dpi. (optional)
    Should contain (as text): URL

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"
    _rename_map = {
        "at1x": "@1x",
        "at2x": "@2x",
    }

class InstanceStatistics(AttribAccessDict):
    """
    Usage statistics for an instance.

    Example:

    .. code-block:: python

        # Returns a InstanceStatistics object
        mastodon.instance_v1().stats

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    user_count: "int"
    """
    The total number of accounts that have been created on this instance.

    Version history:
      * 1.6.0: added
    """

    status_count: "int"
    """
    The total number of local posts that have been made on this instance.

    Version history:
      * 1.6.0: added
    """

    domain_count: "int"
    """
    The total number of other instances that this instance is aware of.

    Version history:
      * 1.6.0: added
    """

    _version = "1.6.0"

class InstanceUsage(AttribAccessDict):
    """
    Usage / recent activity information for this instance.

    Example:

    .. code-block:: python

        # Returns a InstanceUsage object
        mastodon.instance().usage

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    users: "InstanceUsageUsers"
    """
    Information about user counts on this instance.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class InstanceUsageUsers(AttribAccessDict):
    """
    Recent active user information about this instance.

    Example:

    .. code-block:: python

        # Returns a InstanceUsageUsers object
        mastodon.instance().usage.users

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    active_month: "int"
    """
    This instances most recent monthly active user count.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class RuleTranslation(AttribAccessDict):
    """
    A translation for a rule into a specific language.

    Example:

    .. code-block:: python

        # Returns a RuleTranslation object
        mastodon.instance().rules[0].translations['de']

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Rule/#translations
    """

    text: "str"
    """
    The rule to be followed, in few words, in the specified language.

    Version history:
      * 4.4.0: added
    """

    hint: "str"
    """
    Potentially, the rule to be followed, in more words, in the specified language.

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class Rule(AttribAccessDict):
    """
    A rule that instance staff has specified users must follow on this instance.

    Example:

    .. code-block:: python

        # Returns a Rule object
        mastodon.instance().rules[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Rule/
    """

    id: "IdType"
    """
    An identifier for the rule.

    Version history:
      * 3.4.0: added
    """

    text: "str"
    """
    The rule to be followed, in few words.

    Version history:
      * 3.4.0: added
    """

    hint: "str"
    """
    Potentially, the rule to be followed, in more words.

    Version history:
      * 4.3.0: added
    """

    translations: "AttribAccessDict[str, RuleTranslation]"
    """
    A list of translations for the rule, as a dictionary with the key being ISO 639-1 (two-letter) language codes for available languages.

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class InstanceRegistrations(AttribAccessDict):
    """
    Registration information for this instance, like whether registrations are open and whether they require approval.

    Example:

    .. code-block:: python

        # Returns a InstanceRegistrations object
        mastodon.instance_v2().registrations

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    approval_required: "bool"
    """
    Boolean indicating whether registrations on the instance require approval.

    Version history:
      * 4.0.0: added
    """

    enabled: "bool"
    """
    Boolean indicating whether registrations are enabled on this instance.

    Version history:
      * 4.0.0: added
    """

    message: "Optional[str]"
    """
    A message to be shown instead of the sign-up form when registrations are closed. (nullable)
    Should contain (as text): HTML

    Version history:
      * 4.0.0: added
    """

    url: "Optional[str]"
    """
    A custom URL for account registration, when using external authentication. (nullable)
    Should contain (as text): URL

    Version history:
      * 4.2.0: added
    """

    sign_up_url: "Optional[str]"
    """
    URL to the sign-up form for this instance. Only present for the v2 API variant of the instance API. (optional)

    Version history:
      * 4.2.0: added
    """

    reason_required: "Optional[bool]"
    """
    Boolean indicating whether a reason for registration is required on this instance. (nullable)

    Version history:
      * 4.4.0: added
    """

    min_age: "Optional[int]"
    """
    Minimum age in years required to register on this instance. (nullable)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class InstanceContact(AttribAccessDict):
    """
    Contact information for this instances' staff.

    Example:

    .. code-block:: python

        # Returns a InstanceContact object
        mastodon.instance().contact

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    account: "Account"
    """
    Account that has been designated as the instances contact account.

    Version history:
      * 4.0.0: added
    """

    email: "str"
    """
    E-mail address that can be used to contact the instance staff.
    Should contain (as text): Email

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class InstanceAccountConfiguration(AttribAccessDict):
    """
    Configuration values relating to accounts.

    Example:

    .. code-block:: python

        # Returns a InstanceAccountConfiguration object
        mastodon.instance().configuration.accounts

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    max_featured_tags: "int"
    """
    The maximum number of featured tags that can be displayed on a profile.

    Version history:
      * 4.0.0: added
    """

    max_pinned_statuses: "int"
    """
    The maximum number of pinned statuses for an account.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class InstanceStatusConfiguration(AttribAccessDict):
    """
    Configuration values relating to statuses.

    Example:

    .. code-block:: python

        # Returns a InstanceStatusConfiguration object
        mastodon.instance().configuration.statuses

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    max_characters: "int"
    """
    Maximum number of characters in a status this instance allows local users to use.

    Version history:
      * 3.4.2: added
    """

    max_media_attachments: "int"
    """
    Maximum number of media attachments per status this instance allows local users to use.

    Version history:
      * 3.4.2: added
    """

    characters_reserved_per_url: "int"
    """
    Number of characters that this instance counts a URL as when counting charaters.

    Version history:
      * 3.4.2: added
    """

    _version = "3.4.2"

class InstanceTranslationConfiguration(AttribAccessDict):
    """
    Configuration values relating to translation.

    Example:

    .. code-block:: python

        # Returns a InstanceTranslationConfiguration object
        mastodon.instance_v2().configuration.translation

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    enabled: "bool"
    """
    Boolean indicating whether the translation API is enabled on this instance.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class InstanceMediaConfiguration(AttribAccessDict):
    """
    Configuration values relating to media attachments.

    Example:

    .. code-block:: python

        # Returns a InstanceMediaConfiguration object
        mastodon.instance().configuration.media_attachments

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    supported_mime_types: "NonPaginatableList[str]"
    """
    Mime types the instance accepts for media attachment uploads.

    Version history:
      * 3.4.2: added
    """

    image_size_limit: "int"
    """
    Maximum size (in bytes) the instance will accept for image uploads.

    Version history:
      * 3.4.2: added
    """

    image_matrix_limit: "int"
    """
    Maximum total number of pixels (i.e. width * height) the instance will accept for image uploads.

    Version history:
      * 3.4.2: added
    """

    video_size_limit: "int"
    """
    Maximum size (in bytes) the instance will accept for video uploads.

    Version history:
      * 3.4.2: added
    """

    video_frame_rate_limit: "int"
    """
    Maximum frame rate the instance will accept for video uploads.

    Version history:
      * 3.4.2: added
    """

    video_matrix_limit: "int"
    """
    Maximum total number of pixels (i.e. width * height) the instance will accept for video uploads.

    Version history:
      * 3.4.2: added
    """

    description_limit: "int"
    """
    Maximum number of characters in a media attachment description this instance allows local users to use.

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class InstancePollConfiguration(AttribAccessDict):
    """
    Configuration values relating to polls.

    Example:

    .. code-block:: python

        # Returns a InstancePollConfiguration object
        mastodon.instance().configuration.polls

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    max_options: "int"
    """
    How many poll options this instance allows local users to use per poll.

    Version history:
      * 3.4.2: added
    """

    max_characters_per_option: "int"
    """
    Maximum number of characters this instance allows local users to use per poll option.

    Version history:
      * 3.4.2: added
    """

    min_expiration: "int"
    """
    The shortest allowed duration for a poll on this instance, in seconds.

    Version history:
      * 3.4.2: added
    """

    max_expiration: "int"
    """
    The longest allowed duration for a poll on this instance, in seconds.

    Version history:
      * 3.4.2: added
    """

    _version = "3.4.2"

class Nodeinfo(AttribAccessDict):
    """
    The instances standardized NodeInfo data.

    Example:

    .. code-block:: python

        # Returns a Nodeinfo object
        mastodon.instance_nodeinfo()

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    version: "str"
    """
    Version of the nodeinfo schema spec that was used for this response.

    Version history:
      * 3.0.0: added
    """

    software: "NodeinfoSoftware"
    """
    Information about the server software being used on this instance.

    Version history:
      * 3.0.0: added
    """

    protocols: "NonPaginatableList[str]"
    """
    A list of strings specifying the federation protocols this instance supports. Typically, just "activitypub".

    Version history:
      * 3.0.0: added
    """

    services: "NodeinfoServices"
    """
    Services that this instance can retrieve messages from or send messages to.

    Version history:
      * 3.0.0: added
    """

    usage: "NodeinfoUsage"
    """
    Information about recent activity on this instance.

    Version history:
      * 3.0.0: added
    """

    openRegistrations: "bool"
    """
    Bool indicating whether the instance is open for registrations.

    Version history:
      * 3.0.0: added
    """

    metadata: "NodeinfoMetadata"
    """
    Additional node metadata. Can be entirely empty.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class NodeinfoSoftware(AttribAccessDict):
    """
    NodeInfo software-related information.

    Example:

    .. code-block:: python

        # Returns a NodeinfoSoftware object
        mastodon.instance_nodeinfo().software

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    name: "str"
    """
    Name of the software used by this instance.

    Version history:
      * 3.0.0: added
    """

    version: "str"
    """
    String indicating the version of the software used by this instance.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class NodeinfoServices(AttribAccessDict):
    """
    Nodeinfo services-related information.

    Example:

    .. code-block:: python

        # Returns a NodeinfoServices object
        mastodon.instance_nodeinfo().services

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    outbound: "NonPaginatableList"
    """
    List of services that this instance can send messages to. On Mastodon, typically an empty list.

    Version history:
      * 3.0.0: added
    """

    inbound: "NonPaginatableList"
    """
    List of services that this instance can retrieve messages from. On Mastodon, typically an empty list.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class NodeinfoUsage(AttribAccessDict):
    """
    Nodeinfo usage-related information.

    Example:

    .. code-block:: python

        # Returns a NodeinfoUsage object
        mastodon.instance_nodeinfo().usage

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    users: "NodeinfoUsageUsers"
    """
    Information about user counts on this instance.

    Version history:
      * 3.0.0: added
    """

    localPosts: "int"
    """
    The total number of local posts that have been made on this instance.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class NodeinfoUsageUsers(AttribAccessDict):
    """
    Nodeinfo user count statistics.

    Example:

    .. code-block:: python

        # Returns a NodeinfoUsageUsers object
        mastodon.instance_nodeinfo().usage.users

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    total: "int"
    """
    The total number of accounts that have been created on this instance.

    Version history:
      * 3.0.0: added
    """

    activeMonth: "int"
    """
    Number of users that have been active, by some definition (Mastodon: Have logged in at least once) in the last month.

    Version history:
      * 3.0.0: added
    """

    activeHalfyear: "int"
    """
    Number of users that have been active, by some definition (Mastodon: Have logged in at least once) in the last half year.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class NodeinfoMetadata(AttribAccessDict):
    """
    Nodeinfo extra metadata. Entirely freeform, be careful about consuming it programatically. Survey of real world usage: https://codeberg.org/thefederationinfo/nodeinfo_metadata_survey.

    Example:

    .. code-block:: python

        # Returns a NodeinfoMetadata object
        mastodon.instance_nodeinfo().metadata

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    nodeName: "str"
    """
    Name of the instance, as specified by the instance admin.

    Version history:
      * 4.4.0: added
    """

    nodeDescription: "Optional[str]"
    """
    Description of the instance, as specified by the instance admin. (nullable)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class Activity(AttribAccessDict):
    """
    Information about recent activity on an instance.

    Example:

    .. code-block:: python

        # Returns a Activity object
        mastodon.instance_activity()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/#activity
    """

    week: "datetime"
    """
    Date of the first day of the week the stats were collected for.

    Version history:
      * 2.1.2: added
    """

    logins: "int"
    """
    Number of users that logged in that week.

    Version history:
      * 2.1.2: added
    """

    registrations: "int"
    """
    Number of new users that week.

    Version history:
      * 2.1.2: added
    """

    statuses: "int"
    """
    Number of statuses posted that week.

    Version history:
      * 2.1.2: added
    """

    _version = "2.1.2"

class Report(AttribAccessDict):
    """
    Information about a report that has been filed against a user. Currently largely pointless, as updated reports cannot be fetched.

    Example:

    .. code-block:: python

        # Returns a Report object
        mastodon.report(<account id>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Report/
    """

    id: "IdType"
    """
    Id of the report.

    Version history:
      * 2.9.1: added
    """

    action_taken: "bool"
    """
    True if a moderator or admin has processed the report, False otherwise.

    Version history:
      * 2.9.1: added
    """

    comment: "str"
    """
    Text comment submitted with the report.

    Version history:
      * 2.9.1: added
    """

    created_at: "datetime"
    """
    Time at which this report was created, as a datetime object.

    Version history:
      * 2.9.1: added
    """

    target_account: "Account"
    """
    Account that has been reported with this report.

    Version history:
      * 2.9.1: added
    """

    status_ids: "NonPaginatableList[IdType]"
    """
    List of status IDs attached to the report.

    Version history:
      * 2.9.1: added
    """

    action_taken_at: "Optional[datetime]"
    """
    When an action was taken, if this report is currently resolved. (nullable)

    Version history:
      * 2.9.1: added
    """

    category: "str"
    """
    The category under which the report is classified.
    Should contain (as text): ReportReasonEnum

    Version history:
      * 3.5.0: added
    """

    forwarded: "bool"
    """
    Whether a report was forwarded to a remote instance.

    Version history:
      * 4.0.0: added
    """

    rules_ids: "NonPaginatableList[IdType]"
    """
    IDs of the rules selected for this report.

    Version history:
      * 3.5.0: added
    """

    _version = "4.0.0"

class AdminReport(AttribAccessDict):
    """
    Information about a report that has been filed against a user.

    Example:

    .. code-block:: python

        # Returns a AdminReport object
        mastodon.admin_reports()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Report/
    """

    id: "IdType"
    """
    Id of the report.

    Version history:
      * 2.9.1: added
    """

    action_taken: "bool"
    """
    True if a moderator or admin has processed the report, False otherwise.

    Version history:
      * 2.9.1: added
    """

    comment: "str"
    """
    Text comment submitted with the report.

    Version history:
      * 2.9.1: added
    """

    created_at: "datetime"
    """
    Time at which this report was created, as a datetime object.

    Version history:
      * 2.9.1: added
    """

    updated_at: "datetime"
    """
    Last time this report has been updated, as a datetime object.

    Version history:
      * 2.9.1: added
    """

    account: "Account"
    """
    Account of the user that filed this report.

    Version history:
      * 2.9.1: added
    """

    target_account: "Account"
    """
    Account that has been reported with this report.

    Version history:
      * 2.9.1: added
    """

    assigned_account: "Optional[AdminAccount]"
    """
    If the report as been assigned to an account, that Account (None if not). (nullable)

    Version history:
      * 2.9.1: added
    """

    action_taken_by_account: "Optional[AdminAccount]"
    """
    Account that processed this report. (nullable)

    Version history:
      * 2.9.1: added
    """

    statuses: "NonPaginatableList[Status]"
    """
    List of Statuses attached to the report.

    Version history:
      * 2.9.1: added
    """

    action_taken_at: "Optional[datetime]"
    """
    When an action was taken, if this report is currently resolved. (nullable)

    Version history:
      * 2.9.1: added
    """

    category: "str"
    """
    The category under which the report is classified.
    Should contain (as text): ReportReasonEnum

    Version history:
      * 3.5.0: added
    """

    forwarded: "Optional[bool]"
    """
    Whether a report was forwarded to a remote instance. Can be None. (nullable)

    Version history:
      * 4.0.0: added
    """

    rules: "NonPaginatableList[Rule]"
    """
    Rules attached to the report, for context.

    Version history:
      * 3.5.0: added
    """

    _version = "4.0.0"

class WebPushSubscription(AttribAccessDict):
    """
    Information about the logged-in users web push subscription for the authenticated application.

    Example:

    .. code-block:: python

        # Returns a WebPushSubscription object
        mastodon.push_subscription()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/WebPushSubscription/
    """

    id: "IdType"
    """
    Id of the push subscription.

    Version history:
      * 2.4.0: added
    """

    endpoint: "str"
    """
    Endpoint URL for the subscription.
    Should contain (as text): URL

    Version history:
      * 2.4.0: added
    """

    server_key: "str"
    """
    Server pubkey used for signature verification.

    Version history:
      * 2.4.0: added
    """

    alerts: "WebPushSubscriptionAlerts"
    """
    Subscribed events - object that may contain various keys, with value True if webpushes have been requested for those events.

    Version history:
      * 2.4.0: added
      * 2.8.0: added poll`
      * 3.1.0: added follow_request`
      * 3.3.0: added status
      * 3.5.0: added update and admin.sign_up
      * 4.0.0: added admin.report
    """

    policy: "str"
    """
    Which sources should generate webpushes.

    Version history:
      * 2.4.0: added
    """

    standard: "bool"
    """
    Boolean indicatign whether the push messages follow the standardized specifications (RFC8030+RFC8291+RFC8292). Else they follow a legacy version of the specifications (4th draft of RFC8291 and 1st draft of RFC8292).

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class WebPushSubscriptionAlerts(AttribAccessDict):
    """
    Information about alerts as part of a push subscription.

    Example:

    .. code-block:: python

        # Returns a WebPushSubscriptionAlerts object
        mastodon.push_subscription().alerts

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/WebPushSubscription/
    """

    follow: "Optional[bool]"
    """
    True if push subscriptions for follow events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 2.4.0: added
    """

    favourite: "Optional[bool]"
    """
    True if push subscriptions for favourite events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 2.4.0: added
    """

    reblog: "Optional[bool]"
    """
    True if push subscriptions for reblog events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 2.4.0: added
    """

    mention: "Optional[bool]"
    """
    True if push subscriptions for mention events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 2.4.0: added
    """

    poll: "Optional[bool]"
    """
    True if push subscriptions for poll events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 2.8.0: added
    """

    follow_request: "Optional[bool]"
    """
    True if push subscriptions for follow request events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 2.4.0: added
    """

    status: "Optional[bool]"
    """
    True if push subscriptions for status creation (watched users only) events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 3.1.0: added
    """

    update: "Optional[bool]"
    """
    True if push subscriptions for status update (edit) events have been requested, false or not present otherwise. (nullable)

    Version history:
      * 3.3.0: added
    """

    admin_sign_up: "Optional[bool]"
    """
    True if push subscriptions for sign up events have been requested, false or not present otherwise. Admins only. (nullable)

    Version history:
      * 3.5.0: added
    """

    admin_report: "Optional[bool]"
    """
    True if push subscriptions for report creation events have been requested, false or not present otherwise. Admins only. (nullable)

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class PushNotification(AttribAccessDict):
    """
    A single Mastodon push notification received via WebPush, after decryption.

    Example:

    .. code-block:: python

        # Returns a PushNotification object
        mastodon.push_subscription_decrypt_push(...)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/WebPushSubscription/
    """

    access_token: "str"
    """
    Access token that can be used to access the API as the notified user.

    Version history:
      * 2.4.0: added
    """

    body: "str"
    """
    Text body of the notification.

    Version history:
      * 2.4.0: added
    """

    icon: "str"
    """
    URL to an icon for the notification.
    Should contain (as text): URL

    Version history:
      * 2.4.0: added
    """

    notification_id: "IdType"
    """
    ID that can be passed to notification() to get the full notification object,.

    Version history:
      * 2.4.0: added
    """

    notification_type: "str"
    """
    String indicating the type of notification.

    Version history:
      * 2.4.0: added
    """

    preferred_locale: "str"
    """
    The user's preferred locale.
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 2.4.0: added
    """

    title: "str"
    """
    Title for the notification.

    Version history:
      * 2.4.0: added
    """

    _version = "2.4.0"

class Preferences(AttribAccessDict):
    """
    The logged in users preferences.

    Example:

    .. code-block:: python

        # Returns a Preferences object
        mastodon.preferences()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Preferences/
    """

    posting_default_visibility: "str"
    """
    Default visibility for new posts. Also found in CredentialAccountSource as `privacy`.

    Version history:
      * 2.8.0: added
    """

    posting_default_sensitive: "bool"
    """
    Default sensitivity flag for new posts. Also found in CredentialAccountSource as `sensitive`.

    Version history:
      * 2.8.0: added
    """

    posting_default_language: "Optional[str]"
    """
    Default language for new posts. Also found in CredentialAccountSource as `language`. (nullable)
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 2.8.0: added
    """

    reading_expand_media: "str"
    """
    String indicating whether media attachments should be automatically displayed or blurred/hidden.

    Version history:
      * 2.8.0: added
    """

    reading_expand_spoilers: "bool"
    """
    Boolean indicating whether CWs should be expanded by default.

    Version history:
      * 2.8.0: added
    """

    reading_autoplay_gifs: "bool"
    """
    Boolean indicating whether gifs should be autoplayed (True) or not (False).

    Version history:
      * 2.8.0: added
    """

    _version = "2.8.0"
    _rename_map = {
        "posting_default_visibility": "posting:default:visibility",
        "posting_default_sensitive": "posting:default:sensitive",
        "posting_default_language": "posting:default:language",
        "reading_expand_media": "reading:expand:media",
        "reading_expand_spoilers": "reading:expand:spoilers",
        "reading_autoplay_gifs": "reading:autoplay:gifs",
    }

class FeaturedTag(AttribAccessDict):
    """
    A tag featured on a users profile.

    Example:

    .. code-block:: python

        # Returns a FeaturedTag object
        mastodon.featured_tags()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/FeaturedTag/
    """

    id: "IdType"
    """
    The featured tags id.

    Version history:
      * 3.0.0: added
    """

    name: "str"
    """
    The featured tags name (without leading #).

    Version history:
      * 3.0.0: added
    """

    statuses_count: "str"
    """
    Number of publicly visible statuses posted with this hashtag that this instance knows about.

    Version history:
      * 3.0.0: added
    """

    last_status_at: "Optional[datetime]"
    """
    The last time a public status containing this hashtag was added to this instance's database (can be None if there are none). (nullable)

    Version history:
      * 3.0.0: added
    """

    url: "str"
    """
    A link to all statuses by a user that contain this hashtag.
    Should contain (as text): URL

    Version history:
      * 3.3.0: added
    """

    _version = "3.3.0"

class Marker(AttribAccessDict):
    """
    A read marker indicating where the logged in user has left off reading a given timeline.

    Example:

    .. code-block:: python

        # Returns a Marker object
        mastodon.markers_get()["home"]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Marker/
    """

    last_read_id: "IdType"
    """
    ID of the last read object in the timeline.

    Version history:
      * 3.0.0: added
    """

    version: "int"
    """
    A counter that is incremented whenever the marker is set to a new status.

    Version history:
      * 3.0.0: added
    """

    updated_at: "datetime"
    """
    The time the marker was last set, as a datetime object.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class Announcement(AttribAccessDict):
    """
    An announcement sent by the instances staff.

    Example:

    .. code-block:: python

        # Returns a Announcement object
        mastodon.announcements()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Announcement/
    """

    id: "IdType"
    """
    The annoucements id.

    Version history:
      * 3.1.0: added
    """

    content: "str"
    """
    The contents of the annoucement, as an html string.
    Should contain (as text): HTML

    Version history:
      * 3.1.0: added
    """

    starts_at: "Optional[datetime]"
    """
    The annoucements start time, as a datetime object. Can be None. (nullable)

    Version history:
      * 3.1.0: added
    """

    ends_at: "Optional[datetime]"
    """
    The annoucements end time, as a datetime object. Can be None. (nullable)

    Version history:
      * 3.1.0: added
    """

    all_day: "bool"
    """
    Boolean indicating whether the annoucement represents an "all day" event.

    Version history:
      * 3.1.0: added
    """

    published_at: "datetime"
    """
    The annoucements publish time, as a datetime object.

    Version history:
      * 3.1.0: added
    """

    updated_at: "datetime"
    """
    The annoucements last updated time, as a datetime object.

    Version history:
      * 3.1.0: added
    """

    read: "bool"
    """
    A boolean indicating whether the logged in user has dismissed the annoucement.

    Version history:
      * 3.1.0: added
    """

    mentions: "NonPaginatableList[StatusMention]"
    """
    Users mentioned in the annoucement.

    Version history:
      * 3.1.0: added
    """

    tags: "NonPaginatableList"
    """
    Hashtags mentioned in the announcement.

    Version history:
      * 3.1.0: added
    """

    emojis: "NonPaginatableList"
    """
    Custom emoji used in the annoucement.

    Version history:
      * 3.1.0: added
    """

    reactions: "NonPaginatableList[Reaction]"
    """
    Reactions to the annoucement.

    Version history:
      * 3.1.0: added
    """

    statuses: "NonPaginatableList"
    """
    Statuses linked in the announcement text.

    Version history:
      * 3.1.0: added
    """

    _version = "3.1.0"

class Reaction(AttribAccessDict):
    """
    A reaction to an announcement.

    Example:

    .. code-block:: python

        # Returns a Reaction object
        mastodon.announcements()[0].reactions[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Reaction/
    """

    name: "str"
    """
    Name of the custom emoji or unicode emoji of the reaction.

    Version history:
      * 3.1.0: added
    """

    count: "int"
    """
    Reaction counter (i.e. number of users who have added this reaction).

    Version history:
      * 3.1.0: added
    """

    me: "bool"
    """
    True if the logged-in user has reacted with this emoji, false otherwise.

    Version history:
      * 3.1.0: added
    """

    url: "Optional[str]"
    """
    URL for the custom emoji image. (nullable)
    Should contain (as text): URL

    Version history:
      * 3.1.0: added
    """

    static_url: "Optional[str]"
    """
    URL for a never-animated version of the custom emoji image. (nullable)
    Should contain (as text): URL

    Version history:
      * 3.1.0: added
    """

    _version = "3.1.0"

class StreamReaction(AttribAccessDict):
    """
    A reaction to an announcement.

    Example:

    .. code-block:: python

        # Returns a StreamReaction object
        # Only available via the streaming API

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/streaming/
    """

    name: "str"
    """
    Name of the custom emoji or unicode emoji of the reaction.

    Version history:
      * 3.1.0: added
    """

    count: "int"
    """
    Reaction counter (i.e. number of users who have added this reaction).

    Version history:
      * 3.1.0: added
    """

    announcement_id: "IdType"
    """
    If of the announcement this reaction was for.

    Version history:
      * 3.1.0: added
    """

    _version = "3.1.0"

class FamiliarFollowers(AttribAccessDict):
    """
    A follower of a given account that is also followed by the logged-in user.

    Example:

    .. code-block:: python

        # Returns a FamiliarFollowers object
        mastodon.account_familiar_followers(<account id>)[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/FamiliarFollowers/
    """

    id: "IdType"
    """
    ID of the account for which the familiar followers are being returned.

    Version history:
      * 3.5.0: added
    """

    accounts: "NonPaginatableList[Account]"
    """
    List of Accounts of the familiar followers.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminAccount(AttribAccessDict):
    """
    Admin variant of the Account entity, with some additional information.

    Example:

    .. code-block:: python

        # Returns a AdminAccount object
        mastodon.admin_account(<account id>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Account/
    """

    id: "IdType"
    """
    The users id,.

    Version history:
      * 2.9.1: added
    """

    username: "str"
    """
    The users username, no leading @.

    Version history:
      * 2.9.1: added
    """

    domain: "Optional[str]"
    """
    The users domain. (nullable)

    Version history:
      * 2.9.1: added
    """

    created_at: "datetime"
    """
    The time of account creation.

    Version history:
      * 2.9.1: added
    """

    email: "str"
    """
    For local users, the user's email.
    Should contain (as text): Email

    Version history:
      * 2.9.1: added
    """

    ip: "Optional[str]"
    """
    For local users, the user's last known IP address. (nullable)

    Version history:
      * 2.9.1: added
      * 3.5.0: return type changed from String to AdminIP
      * 4.0.0: bug fixed, return type is now a String again
    """

    role: "Role"
    """
    The users role.

    Version history:
      * 2.9.1: added, returns a String (enumerable, oneOf `user` `moderator` `admin`)
      * 4.0.0: now uses Role entity
    """

    confirmed: "bool"
    """
    For local users, False if the user has not confirmed their email, True otherwise.

    Version history:
      * 2.9.1: added
    """

    suspended: "bool"
    """
    Boolean indicating whether the user has been suspended.

    Version history:
      * 2.9.1: added
    """

    silenced: "bool"
    """
    Boolean indicating whether the user has been silenced.

    Version history:
      * 2.9.1: added
    """

    disabled: "bool"
    """
    For local users, boolean indicating whether the user has had their login disabled.

    Version history:
      * 2.9.1: added
    """

    approved: "bool"
    """
    For local users, False if the user is pending, True otherwise.

    Version history:
      * 2.9.1: added
    """

    locale: "str"
    """
    For local users, the locale the user has set,.
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 2.9.1: added
    """

    invite_request: "Optional[str]"
    """
    If the user requested an invite, the invite request comment of that user. (nullable)

    Version history:
      * 2.9.1: added
    """

    account: "Account"
    """
    The user's Account.

    Version history:
      * 2.9.1: added
    """

    sensitized: "bool"
    """
    Boolean indicating whether the account has been marked as force-sensitive.

    Version history:
      * 2.9.1: added
    """

    ips: "NonPaginatableList[AdminIp]"
    """
    All known IP addresses associated with this account.

    Version history:
      * 3.5.0: added
    """

    created_by_application_id: "Optional[IdType]"
    """
    Present if the user was created by an application and set to the application id. (optional)

    Version history:
      * 2.9.1: added
    """

    invited_by_account_id: "Optional[IdType]"
    """
    Present if the user was created via invite and set to the inviting users id. (optional)

    Version history:
      * 2.9.1: added
    """

    _version = "4.0.0"

class AdminIp(AttribAccessDict):
    """
    An IP address used by some user or other instance, visible as part of some admin APIs.

    Example:

    .. code-block:: python

        # Returns a AdminIp object
        mastodon.admin_account(<account id>).ips[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Ip/
    """

    ip: "str"
    """
    The IP address.

    Version history:
      * 3.5.0: added
    """

    used_at: "str"
    """
    The timestamp of when the IP address was last used for this account.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminMeasure(AttribAccessDict):
    """
    A measurement, such as the number of active users, as returned by the admin reporting API.

    Example:

    .. code-block:: python

        # Returns a AdminMeasure object
        mastodon.admin_measures(datetime.now() - timedelta(hours=24*5), datetime.now(), interactions=True)[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Measure/
    """

    key: "str"
    """
    Name of the measure returned.
    Should contain (as text): AdminMeasureTypeEnum

    Version history:
      * 3.5.0: added
    """

    unit: "Optional[str]"
    """
    Unit for the measure, if available. (nullable)

    Version history:
      * 3.5.0: added
    """

    total: "str"
    """
    Value of the measure returned.

    Version history:
      * 3.5.0: added
    """

    human_value: "Optional[str]"
    """
    Human readable variant of the measure returned. (nullable)

    Version history:
      * 3.5.0: added
    """

    previous_total: "Optional[str]"
    """
    Previous measurement period value of the measure returned, if available. (nullable)

    Version history:
      * 3.5.0: added
    """

    data: "NonPaginatableList[AdminMeasureData]"
    """
    A list of AdminMeasureData with the measure broken down by date.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminMeasureData(AttribAccessDict):
    """
    A single row of data for an admin reporting api measurement.

    Example:

    .. code-block:: python

        # Returns a AdminMeasureData object
        mastodon.admin_measures(datetime.now() - timedelta(hours=24*5), datetime.now(), active_users=True)[0].data[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Measure/
    """

    date: "datetime"
    """
    Date for this row.

    Version history:
      * 3.5.0: added
    """

    value: "int"
    """
    Value of the measure for this row.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminDimension(AttribAccessDict):
    """
    A qualitative measurement about the server, as returned by the admin reporting api.

    Example:

    .. code-block:: python

        # Returns a AdminDimension object
        mastodon.admin_dimensions(datetime.now() - timedelta(hours=24*5), datetime.now(), languages=True)[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Dimension/
    """

    key: "str"
    """
    Name of the dimension returned.

    Version history:
      * 3.5.0: added
    """

    data: "NonPaginatableList[AdminDimensionData]"
    """
    A list of data AdminDimensionData objects.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminDimensionData(AttribAccessDict):
    """
    A single row of data for qualitative measurements about the server, as returned by the admin reporting api.

    Example:

    .. code-block:: python

        # Returns a AdminDimensionData object
        mastodon.admin_dimensions(datetime.now() - timedelta(hours=24*5), datetime.now(), languages=True)[0].data[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Dimension/
    """

    key: "str"
    """
    category for this row.

    Version history:
      * 3.5.0: added
    """

    human_key: "str"
    """
    Human readable name for the category for this row, when available.

    Version history:
      * 3.5.0: added
    """

    value: "int"
    """
    Numeric value for the category.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminRetention(AttribAccessDict):
    """
    User retention data for a given cohort, as returned by the admin reporting api.

    Example:

    .. code-block:: python

        # Returns a AdminRetention object
        mastodon.admin_retention(datetime.now() - timedelta(hours=24*5), datetime.now())[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Cohort/
    """

    period: "datetime"
    """
    Starting time of the period that the data is being returned for.

    Version history:
      * 3.5.0: added
    """

    frequency: "str"
    """
    Time resolution (day or month) for the returned data.

    Version history:
      * 3.5.0: added
    """

    data: "NonPaginatableList[AdminCohort]"
    """
    List of AdminCohort objects.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminCohort(AttribAccessDict):
    """
    A single data point regarding user retention for a given cohort, as returned by the admin reporting api.

    Example:

    .. code-block:: python

        # Returns a AdminCohort object
        mastodon.admin_retention(datetime.now() - timedelta(hours=24*5), datetime.now())[0].data[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Cohort/
    """

    date: "datetime"
    """
    Date for this entry.

    Version history:
      * 3.5.0: added
    """

    rate: "float"
    """
    Fraction of users retained.

    Version history:
      * 3.5.0: added
    """

    value: "int"
    """
    Absolute number of users retained.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminDomainBlock(AttribAccessDict):
    """
    A domain block, as returned by the admin API.

    Example:

    .. code-block:: python

        # Returns a AdminDomainBlock object
        mastodon.admin_domain_blocks()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_DomainBlock/
    """

    id: "IdType"
    """
    The ID of the DomainBlock in the database.

    Version history:
      * 4.0.0: added
    """

    domain: "str"
    """
    The domain that is not allowed to federate.

    Version history:
      * 4.0.0: added
    """

    created_at: "datetime"
    """
    When the domain was blocked from federating.

    Version history:
      * 4.0.0: added
    """

    severity: "str"
    """
    The policy to be applied by this domain block.
    Should contain (as text): AdminDomainLimitEnum

    Version history:
      * 4.0.0: added
    """

    reject_media: "bool"
    """
    Whether to reject media attachments from this domain.

    Version history:
      * 4.0.0: added
    """

    reject_reports: "bool"
    """
    Whether to reject reports from this domain.

    Version history:
      * 4.0.0: added
    """

    private_comment: "Optional[str]"
    """
    A private comment (visible only to other moderators) for the domain block. (nullable)

    Version history:
      * 4.0.0: added
    """

    public_comment: "Optional[str]"
    """
    A public comment (visible to either all users, or the whole world) for the domain block. (nullable)

    Version history:
      * 4.0.0: added
    """

    obfuscate: "bool"
    """
    Whether to obfuscate public displays of this domain block.

    Version history:
      * 4.0.0: added
    """

    digest: "Optional[str]"
    """
    SHA256 hex digest of the blocked domain. (nullable)

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class AdminCanonicalEmailBlock(AttribAccessDict):
    """
    An e-mail block that has been set up to prevent certain e-mails to be used when signing up, via hash matching.

    Example:

    .. code-block:: python

        # Returns a AdminCanonicalEmailBlock object
        mastodon.admin_create_canonical_email_block(email=<some email>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_CanonicalEmailBlock
    """

    id: "IdType"
    """
    The ID of the email block in the database.

    Version history:
      * 4.0.0: added
    """

    canonical_email_hash: "str"
    """
    The SHA256 hash of the canonical email address.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class AdminDomainAllow(AttribAccessDict):
    """
    The opposite of a domain block, specifically allowing a domain to federate when the instance is in allowlist mode.

    Example:

    .. code-block:: python

        # Returns a AdminDomainAllow object
        mastodon.admin_domain_allows()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_DomainAllow
    """

    id: "IdType"
    """
    The ID of the DomainAllow in the database.

    Version history:
      * 4.0.0: added
    """

    domain: "str"
    """
    The domain that is allowed to federate.

    Version history:
      * 4.0.0: added
    """

    created_at: "datetime"
    """
    When the domain was allowed to federate.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class AdminEmailDomainBlock(AttribAccessDict):
    """
    A block that has been set up to prevent e-mails from certain domains to be used when signing up.

    Example:

    .. code-block:: python

        # Returns a AdminEmailDomainBlock object
        mastodo.admin_email_domain_blocks()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_EmailDomainBlock
    """

    id: "IdType"
    """
    The ID of the EmailDomainBlock in the database.

    Version history:
      * 4.0.0: added
    """

    domain: "str"
    """
    The email domain that is not allowed to be used for signups.

    Version history:
      * 4.0.0: added
    """

    created_at: "datetime"
    """
    When the email domain was disallowed from signups.

    Version history:
      * 4.0.0: added
    """

    history: "NonPaginatableList[AdminEmailDomainBlockHistory]"
    """
    Usage statistics for given days (typically the past week).

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class AdminEmailDomainBlockHistory(AttribAccessDict):
    """
    Historic data about attempted signups using e-mails from a given domain.

    Example:

    .. code-block:: python

        # Returns a AdminEmailDomainBlockHistory object
        mastodo.admin_email_domain_blocks()[0].history[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_EmailDomainBlock
    """

    day: "datetime"
    """
    The time (in day increments) for which this row of historical data is valid.

    Version history:
      * 4.0.0: added
    """

    accounts: "int"
    """
    The number of different account creation attempts that have been made.

    Version history:
      * 4.0.0: added
    """

    uses: "int"
    """
    The number of different ips used in account creation attempts.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class AdminIpBlock(AttribAccessDict):
    """
    An admin IP block, to prevent certain IP addresses or address ranges from accessing the instance.

    Example:

    .. code-block:: python

        # Returns a AdminIpBlock object
        mastodon.admin_ip_blocks()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_IpBlock
    """

    id: "IdType"
    """
    The ID of the DomainBlock in the database.

    Version history:
      * 4.0.0: added
    """

    ip: "str"
    """
    The IP address range that is not allowed to federate.

    Version history:
      * 4.0.0: added
    """

    severity: "str"
    """
    The associated policy with this IP block.

    Version history:
      * 4.0.0: added
    """

    comment: "str"
    """
    The recorded reason for this IP block.

    Version history:
      * 4.0.0: added
    """

    created_at: "datetime"
    """
    When the IP block was created.

    Version history:
      * 4.0.0: added
    """

    expires_at: "Optional[datetime]"
    """
    When the IP block will expire. (nullable)

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class DomainBlock(AttribAccessDict):
    """
    A domain block that has been implemented by instance staff, limiting the way posts from the blocked instance are handled.

    Example:

    .. code-block:: python

        # Returns a DomainBlock object
        mastodon.instance_domain_blocks()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/DomainBlock
    """

    domain: "str"
    """
    The domain which is blocked. This may be obfuscated or partially censored.

    Version history:
      * 4.0.0: added
    """

    digest: "str"
    """
    The SHA256 hash digest of the domain string.

    Version history:
      * 4.0.0: added
    """

    severity: "str"
    """
    The level to which the domain is blocked.
    Should contain (as text): DomainLimitEnum

    Version history:
      * 4.0.0: added
    """

    comment: "Optional[str]"
    """
    An optional reason for the domain block. (nullable)

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class ExtendedDescription(AttribAccessDict):
    """
    An extended instance description that can contain HTML.

    Example:

    .. code-block:: python

        # Returns a ExtendedDescription object
        mastodon.instance_extended_description()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/ExtendedDescription
    """

    updated_at: "datetime"
    """
    A timestamp of when the extended description was last updated.

    Version history:
      * 4.0.0: added
    """

    content: "str"
    """
    The rendered HTML content of the extended description.
    Should contain (as text): HTML

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class FilterKeyword(AttribAccessDict):
    """
    A keyword that is being matched as part of a filter.

    Example:

    .. code-block:: python

        # Returns a FilterKeyword object
        mastodon.filters_v2()[0].keywords[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/FilterKeyword
    """

    id: "IdType"
    """
    The ID of the FilterKeyword in the database.

    Version history:
      * 4.0.0: added
    """

    keyword: "str"
    """
    The phrase to be matched against.

    Version history:
      * 4.0.0: added
    """

    whole_word: "bool"
    """
    Should the filter consider word boundaries? See implementation guidelines for filters().

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class FilterStatus(AttribAccessDict):
    """
    A single status that is being matched as part of a filter.

    Example:

    .. code-block:: python

        # Returns a FilterStatus object
        mastodon.filter_statuses_v2(mastodon.filters_v2()[0])[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/FilterStatus
    """

    id: "IdType"
    """
    The ID of the FilterStatus in the database.

    Version history:
      * 4.0.0: added
    """

    status_id: "MaybeSnowflakeIdType"
    """
    The ID of the Status that will be filtered.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class IdentityProof(AttribAccessDict):
    """
    A cryptographic proof-of-identity. Deprecated since 3.5.0.

    THIS ENTITY IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Example:

    .. code-block:: python

        # Returns a IdentityProof object
        # Deprecated since 3.5.0 and eventually removed, there is no way to get this on current versions of Mastodon.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/IdentityProof
    """

    provider: "str"
    """
    The name of the identity provider.

    Version history:
      * 2.8.0: added
    """

    provider_username: "str"
    """
    The account owner's username on the identity provider's service.

    Version history:
      * 2.8.0: added
    """

    updated_at: "datetime"
    """
    When the identity proof was last updated.

    Version history:
      * 2.8.0: added
    """

    proof_url: "str"
    """
    A link to a statement of identity proof, hosted by the identity provider.

    Version history:
      * 2.8.0: added
    """

    profile_url: "str"
    """
    The account owner's profile URL on the identity provider.

    Version history:
      * 2.8.0: added
    """

    _version = "2.8.0"

class StatusSource(AttribAccessDict):
    """
    The source data of a status, useful when editing a status.

    Example:

    .. code-block:: python

        # Returns a StatusSource object
        mastodon.status_source(<status id>)

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/StatusSource
    """

    id: "IdType"
    """
    ID of the status in the database.

    Version history:
      * 3.5.0: added
    """

    text: "str"
    """
    The plain text used to compose the status.

    Version history:
      * 3.5.0: added
    """

    spoiler_text: "str"
    """
    The plain text used to compose the status's subject or content warning.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class Suggestion(AttribAccessDict):
    """
    A follow suggestion.

    Example:

    .. code-block:: python

        # Returns a Suggestion object
        mastodon.suggestions_v2()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Suggestion
    """

    source: "str"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    The reason this account is being suggested.

    Version history:
      * 3.4.0: added
      * 4.3.0: deprecated
    """

    sources: "NonPaginatableList[str]"
    """
    The reasons this account is being suggested.
    Should contain (as text): SuggestionSourceEnum

    Version history:
      * 4.3.0: added
    """

    account: "Account"
    """
    The account being recommended to follow.

    Version history:
      * 3.4.0: added
    """

    _version = "4.3.0"

class Translation(AttribAccessDict):
    """
    A translation of a status.

    Example:

    .. code-block:: python

        # Returns a Translation object
        mastodon.status_translate(<status_id>, 'de')

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Translation
    """

    content: "str"
    """
    The translated text of the status.

    Version history:
      * 4.0.0: added
    """

    detected_source_language: "str"
    """
    The language of the source text, as auto-detected by the machine translation provider.

    Version history:
      * 4.0.0: added
    """

    provider: "str"
    """
    The service that provided the machine translation.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class AccountCreationError(AttribAccessDict):
    """
    An error response returned when creating an account fails.

    Example:

    .. code-block:: python

        # Returns a AccountCreationError object
        mastodon.create_account('halcy', 'secret', 'invalid email lol', True, return_detailed_error=True)[1]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/accounts/#create
    """

    error: "str"
    """
    The error as a localized string.

    Version history:
      * 2.7.0: added
    """

    details: "AccountCreationErrorDetails"
    """
    A dictionary giving more details about what fields caused errors and in which ways.

    Version history:
      * 3.4.0: added
    """

    _version = "3.4.0"

class AccountCreationErrorDetails(AttribAccessDict):
    """
    An object containing detailed errors for different fields in the account creation attempt.

    Example:

    .. code-block:: python

        # Returns a AccountCreationErrorDetails object
        mastodon.create_account('halcy', 'secret', 'invalid email lol', False, return_detailed_error=True)[1].details

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/accounts/#create
    """

    username: "Optional[NonPaginatableList[AccountCreationErrorDetailsField]]"
    """
    An object giving more details about an error caused by the username. (optional)

    Version history:
      * 3.4.0: added
    """

    password: "Optional[NonPaginatableList[AccountCreationErrorDetailsField]]"
    """
    An object giving more details about an error caused by the password. (optional)

    Version history:
      * 3.4.0: added
    """

    email: "Optional[NonPaginatableList[AccountCreationErrorDetailsField]]"
    """
    An object giving more details about an error caused by the e-mail. (optional)

    Version history:
      * 3.4.0: added
    """

    agreement: "Optional[NonPaginatableList[AccountCreationErrorDetailsField]]"
    """
    An object giving more details about an error caused by the usage policy agreement. (optional)

    Version history:
      * 3.4.0: added
    """

    locale: "Optional[NonPaginatableList[AccountCreationErrorDetailsField]]"
    """
    An object giving more details about an error caused by the locale. (optional)

    Version history:
      * 3.4.0: added
    """

    reason: "Optional[NonPaginatableList[AccountCreationErrorDetailsField]]"
    """
    An object giving more details about an error caused by the registration reason. (optional)

    Version history:
      * 3.4.0: added
    """

    date_of_birth: "Optional[NonPaginatableList[AccountCreationErrorDetailsField]]"
    """
    An object giving more details about an error caused by the date of birth. (optional)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class AccountCreationErrorDetailsField(AttribAccessDict):
    """
    An object giving details about what specifically is wrong with a given field in an account registration attempt.

    Example:

    .. code-block:: python

        # Returns a AccountCreationErrorDetailsField object
        mastodon.create_account('halcy', 'secret', 'invalid email lol', True, return_detailed_error=True)[1].details.email[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/accounts/#create
    """

    error: "str"
    """
    A machine readable string giving an error category.

    Version history:
      * 3.4.0: added
    """

    description: "str"
    """
    A description of the issue as a localized string.

    Version history:
      * 3.4.0: added
    """

    _version = "3.4.0"

class NotificationPolicy(AttribAccessDict):
    """
    Represents the notification filtering policy of the user.

    Example:

    .. code-block:: python

        # Returns a NotificationPolicy object
        mastodon.notifications_policy()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/NotificationPolicy
    """

    for_not_following: "str"
    """
    Whether to accept, filter or drop notifications from accounts the user is not following.

    Version history:
      * 4.3.0: added
    """

    for_not_followers: "str"
    """
    Whether to accept, filter or drop notifications from accounts that are not following the user.

    Version history:
      * 4.3.0: added
    """

    for_new_accounts: "str"
    """
    Whether to accept, filter or drop notifications from accounts created in the past 30 days.

    Version history:
      * 4.3.0: added
    """

    for_private_mentions: "str"
    """
    Whether to accept, filter or drop notifications from private mentions.

    Version history:
      * 4.3.0: added
    """

    for_limited_accounts: "str"
    """
    Whether to accept, filter or drop notifications from accounts that were limited by a moderator.

    Version history:
      * 4.3.0: added
    """

    summary: "NotificationPolicySummary"
    """
    A summary of the filtered notifications.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class NotificationPolicySummary(AttribAccessDict):
    """
    A summary of the filtered notifications.

    Example:

    .. code-block:: python

        # Returns a NotificationPolicySummary object
        mastodon.notifications_policy().summary

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/NotificationPolicy
    """

    pending_requests_count: "int"
    """
    Number of different accounts from which the user has non-dismissed filtered notifications. Capped at 100.

    Version history:
      * 4.3.0: added
    """

    pending_notifications_count: "int"
    """
    Number of total non-dismissed filtered notifications. May be inaccurate.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class RelationshipSeveranceEvent(AttribAccessDict):
    """
    Summary of a moderation or block event that caused follow relationships to be severed.

    Example:

    .. code-block:: python

        # Returns a RelationshipSeveranceEvent object
        # There isn't really a good way to get this manually - you get it if a moderation takes action.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/RelationshipSeveranceEvent
    """

    id: "str"
    """
    The ID of the relationship severance event in the database.

    Version history:
      * 4.3.0: added
    """

    type: "str"
    """
    Type of event.
    Should contain (as text): RelationshipSeveranceEventType

    Version history:
      * 4.3.0: added
    """

    purged: "bool"
    """
    Whether the list of severed relationships is unavailable because the data has been purged.

    Version history:
      * 4.3.0: added
    """

    target_name: "str"
    """
    Name of the target of the moderation/block event. This is either a domain name or a user handle, depending on the event type.

    Version history:
      * 4.3.0: added
    """

    followers_count: "int"
    """
    Number of followers that were removed as result of the event.

    Version history:
      * 4.3.0: added
    """

    following_count: "int"
    """
    Number of accounts the user stopped following as result of the event.

    Version history:
      * 4.3.0: added
    """

    created_at: "datetime"
    """
    When the event took place.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class GroupedNotificationsResults(AttribAccessDict):
    """
    Container for grouped notifications plus referenced accounts and statuses.

    Example:

    .. code-block:: python

        # Returns a GroupedNotificationsResults object
        mastodon.grouped_notifications()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/GroupedNotificationsResults
    """

    accounts: "NonPaginatableList[Account]"
    """
    Accounts referenced by grouped notifications.

    Version history:
      * 4.3.0: added
    """

    partial_accounts: "Optional[NonPaginatableList[PartialAccountWithAvatar]]"
    """
    Partial accounts referenced by grouped notifications. Only returned with expand_accounts=partial_avatars. (optional)

    Version history:
      * 4.3.0: added
    """

    statuses: "NonPaginatableList[Status]"
    """
    Statuses referenced by grouped notifications.

    Version history:
      * 4.3.0: added
    """

    notification_groups: "NonPaginatableList[NotificationGroup]"
    """
    The grouped notifications themselves. Is actually in fact paginatable, but via the parent object.

    Version history:
      * 4.3.0: added
    """

    _pagination_next: "Optional[PaginationInfo]"
    """
    Information about the next page of results. Added here as a special case to allow for pagination of the lists inside of this object. (optional)

    Version history:
      * 4.3.0: added
    """

    _pagination_prev: "Optional[PaginationInfo]"
    """
    Information about the previous page of results. Added here as a special case to allow for pagination of the lists inside of this object. (optional)

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class PartialAccountWithAvatar(AttribAccessDict):
    """
    A stripped-down version of Account, containing only what is necessary to display avatars and a few other fields.

    Example:

    .. code-block:: python

        # Returns a PartialAccountWithAvatar object
        mastodon.grouped_notifications().partial_accounts[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/GroupedNotificationsResults
    """

    id: "str"
    """
    The account ID.

    Version history:
      * 4.3.0: added
    """

    acct: "str"
    """
    The Webfinger account URI.

    Version history:
      * 4.3.0: added
    """

    url: "str"
    """
    The location of the user’s profile page.

    Version history:
      * 4.3.0: added
    """

    avatar: "str"
    """
    An image icon (avatar) shown in the profile.

    Version history:
      * 4.3.0: added
    """

    avatar_static: "str"
    """
    A static version of the avatar. May differ if the main avatar is animated.

    Version history:
      * 4.3.0: added
    """

    locked: "bool"
    """
    Whether the account manually approves follow requests.

    Version history:
      * 4.3.0: added
    """

    bot: "bool"
    """
    Indicates that the account may perform automated actions.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class NotificationGroup(AttribAccessDict):
    """
    A group of related notifications, plus metadata for pagination.

    Example:

    .. code-block:: python

        # Returns a NotificationGroup object
        mastodon.grouped_notifications().notification_groups[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/GroupedNotificationsResults
    """

    group_key: "str"
    """
    Group key identifying the grouped notifications. Treated as opaque.

    Version history:
      * 4.3.0: added
    """

    notifications_count: "int"
    """
    Total number of individual notifications in this group.

    Version history:
      * 4.3.0: added
    """

    type: "str"
    """
    The type of event that resulted in the notifications.
    Should contain (as text): NotificationTypeEnum

    Version history:
      * 4.3.0: added
    """

    most_recent_notification_id: "str"
    """
    ID of the most recent notification in the group.

    Version history:
      * 4.3.0: added
    """

    page_min_id: "Optional[str]"
    """
    ID of the oldest notification in this group within the current page. (optional)

    Version history:
      * 4.3.0: added
    """

    page_max_id: "Optional[str]"
    """
    ID of the newest notification in this group within the current page. (optional)

    Version history:
      * 4.3.0: added
    """

    latest_page_notification_at: "Optional[datetime]"
    """
    Date at which the most recent notification within this group (in the current page) was created. (optional)

    Version history:
      * 4.3.0: added
    """

    sample_account_ids: "NonPaginatableList[str]"
    """
    IDs of some of the accounts who most recently triggered notifications in this group.

    Version history:
      * 4.3.0: added
    """

    status_id: "Optional[str]"
    """
    ID of the Status that was the object of the notification. (optional)

    Version history:
      * 4.3.0: added
    """

    report: "Optional[Report]"
    """
    Report that was the object of the notification. (optional)

    Version history:
      * 4.3.0: added
    """

    event: "Optional[RelationshipSeveranceEvent]"
    """
    Summary of the event that caused follow relationships to be severed. (optional)

    Version history:
      * 4.3.0: added
    """

    moderation_warning: "Optional[AccountWarning]"
    """
    Moderation warning that caused the notification. (optional)

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class AccountWarning(AttribAccessDict):
    """
    Moderation warning against a particular account.

    Example:

    .. code-block:: python

        # Returns a AccountWarning object
        # There isn't really a good way to get this manually - you get it if a moderator takes action.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/AccountWarning
    """

    id: "str"
    """
    The ID of the account warning in the database.

    Version history:
      * 4.3.0: added
    """

    action: "str"
    """
    Action taken against the account.

    Version history:
      * 4.3.0: added
    """

    text: "str"
    """
    Message from the moderator to the target account.

    Version history:
      * 4.3.0: added
    """

    status_ids: "Optional[NonPaginatableList[str]]"
    """
    List of status IDs relevant to the warning. May be null. (nullable)

    Version history:
      * 4.3.0: added
    """

    target_account: "Account"
    """
    Account against which a moderation decision has been taken.

    Version history:
      * 4.3.0: added
    """

    appeal: "Optional[Appeal]"
    """
    Appeal submitted by the target account, if any. (nullable)

    Version history:
      * 4.3.0: added
    """

    created_at: "datetime"
    """
    When the event took place.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class UnreadNotificationsCount(AttribAccessDict):
    """
    Rhe (capped) number of unread notifications for the current user.

    Example:

    .. code-block:: python

        # Returns a UnreadNotificationsCount object
        mastodon.notifications_unread_count()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/notifications/#unread-count
    """

    count: "int"
    """
    The capped number of unread notifications. The cap is not documented.

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class Appeal(AttribAccessDict):
    """
    Appeal against a moderation action.

    Example:

    .. code-block:: python

        # Returns a Appeal object
        # There isn't really a good way to get this manually - you get it if a moderator takes action.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Appeal/
    """

    text: "str"
    """
    Text of the appeal from the moderated account to the moderators..

    Version history:
      * 4.3.0: added
    """

    state: "str"
    """
    State of the appeal.
    Should contain (as text): AppealStateEnum

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class NotificationRequest(AttribAccessDict):
    """
    Represents a group of filtered notifications from a specific user.

    Example:

    .. code-block:: python

        # Returns a NotificationRequest object
        mastodon.notification_requests()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/NotificationRequest
    """

    id: "str"
    """
    The ID of the notification request in the database.

    Version history:
      * 4.3.0: added
    """

    created_at: "datetime"
    """
    When the first filtered notification from that user was created.

    Version history:
      * 4.3.0: added
    """

    updated_at: "datetime"
    """
    When the notification request was last updated.

    Version history:
      * 4.3.0: added
    """

    account: "Account"
    """
    The account that performed the action that generated the filtered notifications.

    Version history:
      * 4.3.0: added
    """

    notifications_count: "str"
    """
    How many of this account’s notifications were filtered.

    Version history:
      * 4.3.0: added
    """

    last_status: "Optional[Status]"
    """
    Most recent status associated with a filtered notification from that account. (optional)

    Version history:
      * 4.3.0: added
    """

    _version = "4.3.0"

class SupportedLocale(AttribAccessDict):
    """
    A locale supported by the instance.

    Example:

    .. code-block:: python

        # Returns a SupportedLocale object
        mastodon.instance_languages()[0]

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance
    """

    code: "str"
    """
    The locale code.

    Version history:
      * 4.2.0: added
    """

    name: "str"
    """
    The name of the locale.

    Version history:
      * 4.2.0: added
    """

    _version = "4.2.0"

class OAuthServerInfo(AttribAccessDict):
    """
    Information about the OAuth authorization server.

    Example:

    .. code-block:: python

        # Returns a OAuthServerInfo object
        mastodon.oauth_authorization_server_info()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/oauth/#authorization-server-metadata
    """

    issuer: "str"
    """
    The issuer of the OAuth server. Can be used to avoid accidentally getting replies from a wrong server by comparing it against the `iss`field. Not currently used by Mastodon.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    authorization_endpoint: "str"
    """
    The endpoint for authorization requests.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    token_endpoint: "str"
    """
    The endpoint for token requests.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    revocation_endpoint: "str"
    """
    The endpoint for revoking tokens.
    Should contain (as text): URL

    Version history:
      * 4.3.0: added
    """

    userinfo_endpoint: "str"
    """
    The endpoint for retrieving OAuth user information for the logged in user.
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    scopes_supported: "NonPaginatableList[str]"
    """
    List of scopes supported by the OAuth server.

    Version history:
      * 4.3.0: added
    """

    response_types_supported: "NonPaginatableList[str]"
    """
    List of response types (i.e. what kind of parameters can the server get back to your callback) supported by the OAuth server.

    Version history:
      * 4.3.0: added
    """

    response_modes_supported: "NonPaginatableList[str]"
    """
    List of response modes (i.e. how does the server get callback parameters back to you) supported by the OAuth server.

    Version history:
      * 4.3.0: added
    """

    grant_types_supported: "NonPaginatableList[str]"
    """
    List of grant types (i.e. authorization methods) supported by the OAuth server.

    Version history:
      * 4.3.0: added
    """

    token_endpoint_auth_methods_supported: "NonPaginatableList[str]"
    """
    List of authentication methods supported by the token endpoint.

    Version history:
      * 4.3.0: added
    """

    code_challenge_methods_supported: "NonPaginatableList[str]"
    """
    List of code challenge methods supported by the OAuth server.

    Version history:
      * 4.3.0: added
    """

    service_documentation: "Optional[str]"
    """
    URL to the service documentation (e.g. the Mastodon API reference). (optional)

    Version history:
      * 4.3.0: added
    """

    app_registration_endpoint: "Optional[str]"
    """
    Endpoint for registering applications. (optional)

    Version history:
      * 4.3.0: added
    """

    _version = "4.4.0"

class OAuthUserInfo(AttribAccessDict):
    """
    Information about the currently logged in user, returned by the OAuth userinfo endpoint.

    Example:

    .. code-block:: python

        # Returns a OAuthUserInfo object
        mastodon.oauth_userinfo()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/oauth/#userinfo
    """

    iss: "str"
    """
    The issuer of the OAuth server. Can be used to avoid accidentally getting replies from a wrong server by comparing it against the `issuer` field in OAuthServerInfo.
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    sub: "str"
    """
    The subject identifier of the user. For Mastodon, the URI of the ActivityPub Actor document.
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    name: "str"
    """
    The display name of the user.

    Version history:
      * 4.4.0: added
    """

    preferred_username: "str"
    """
    The preferred username of the user, i.e. the part after the first and before the second @ in their account name.

    Version history:
      * 4.4.0: added
    """

    profile : "str"
    """
    The URL of the user’s profile page.
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    picture: "str"
    """
    The URL of the user’s profile picture.
    Should contain (as text): URL

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

class TermsOfService(AttribAccessDict):
    """
    The terms of service for the instance.

    Example:

    .. code-block:: python

        # Returns a TermsOfService object
        mastodon.instance_terms_of_service()

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/#terms_of_service
    """

    effective_date: "datetime"
    """
    The date when the terms of service became effective.

    Version history:
      * 4.4.0: added
    """

    effective: "bool"
    """
    Whether the terms of service are currently in effect.

    Version history:
      * 4.4.0: added
    """

    content: "str"
    """
    The contents of the terms of service.
    Should contain (as text): HTML

    Version history:
      * 4.4.0: added
    """

    succeeded_by: "Optional[datetime]"
    """
    If there are newer terms of service, their effective date. (optional)

    Version history:
      * 4.4.0: added
    """

    _version = "4.4.0"

ENTITY_NAME_MAP = {
    "Account": Account,
    "AccountField": AccountField,
    "Role": Role,
    "CredentialAccountSource": CredentialAccountSource,
    "Status": Status,
    "Quote": Quote,
    "ShallowQuote": ShallowQuote,
    "StatusEdit": StatusEdit,
    "FilterResult": FilterResult,
    "StatusMention": StatusMention,
    "ScheduledStatus": ScheduledStatus,
    "ScheduledStatusParams": ScheduledStatusParams,
    "Poll": Poll,
    "PollOption": PollOption,
    "Conversation": Conversation,
    "Tag": Tag,
    "TagHistory": TagHistory,
    "CustomEmoji": CustomEmoji,
    "Application": Application,
    "Relationship": Relationship,
    "Filter": Filter,
    "FilterV2": FilterV2,
    "Notification": Notification,
    "Context": Context,
    "UserList": UserList,
    "MediaAttachment": MediaAttachment,
    "MediaAttachmentMetadataContainer": MediaAttachmentMetadataContainer,
    "MediaAttachmentImageMetadata": MediaAttachmentImageMetadata,
    "MediaAttachmentVideoMetadata": MediaAttachmentVideoMetadata,
    "MediaAttachmentAudioMetadata": MediaAttachmentAudioMetadata,
    "MediaAttachmentFocusPoint": MediaAttachmentFocusPoint,
    "MediaAttachmentColors": MediaAttachmentColors,
    "PreviewCard": PreviewCard,
    "TrendingLinkHistory": TrendingLinkHistory,
    "PreviewCardAuthor": PreviewCardAuthor,
    "Search": Search,
    "SearchV2": SearchV2,
    "Instance": Instance,
    "InstanceConfiguration": InstanceConfiguration,
    "InstanceURLs": InstanceURLs,
    "InstanceV2": InstanceV2,
    "InstanceIcon": InstanceIcon,
    "InstanceConfigurationV2": InstanceConfigurationV2,
    "InstanceVapidKey": InstanceVapidKey,
    "InstanceURLsV2": InstanceURLsV2,
    "InstanceThumbnail": InstanceThumbnail,
    "InstanceThumbnailVersions": InstanceThumbnailVersions,
    "InstanceStatistics": InstanceStatistics,
    "InstanceUsage": InstanceUsage,
    "InstanceUsageUsers": InstanceUsageUsers,
    "RuleTranslation": RuleTranslation,
    "Rule": Rule,
    "InstanceRegistrations": InstanceRegistrations,
    "InstanceContact": InstanceContact,
    "InstanceAccountConfiguration": InstanceAccountConfiguration,
    "InstanceStatusConfiguration": InstanceStatusConfiguration,
    "InstanceTranslationConfiguration": InstanceTranslationConfiguration,
    "InstanceMediaConfiguration": InstanceMediaConfiguration,
    "InstancePollConfiguration": InstancePollConfiguration,
    "Nodeinfo": Nodeinfo,
    "NodeinfoSoftware": NodeinfoSoftware,
    "NodeinfoServices": NodeinfoServices,
    "NodeinfoUsage": NodeinfoUsage,
    "NodeinfoUsageUsers": NodeinfoUsageUsers,
    "NodeinfoMetadata": NodeinfoMetadata,
    "Activity": Activity,
    "Report": Report,
    "AdminReport": AdminReport,
    "WebPushSubscription": WebPushSubscription,
    "WebPushSubscriptionAlerts": WebPushSubscriptionAlerts,
    "PushNotification": PushNotification,
    "Preferences": Preferences,
    "FeaturedTag": FeaturedTag,
    "Marker": Marker,
    "Announcement": Announcement,
    "Reaction": Reaction,
    "StreamReaction": StreamReaction,
    "FamiliarFollowers": FamiliarFollowers,
    "AdminAccount": AdminAccount,
    "AdminIp": AdminIp,
    "AdminMeasure": AdminMeasure,
    "AdminMeasureData": AdminMeasureData,
    "AdminDimension": AdminDimension,
    "AdminDimensionData": AdminDimensionData,
    "AdminRetention": AdminRetention,
    "AdminCohort": AdminCohort,
    "AdminDomainBlock": AdminDomainBlock,
    "AdminCanonicalEmailBlock": AdminCanonicalEmailBlock,
    "AdminDomainAllow": AdminDomainAllow,
    "AdminEmailDomainBlock": AdminEmailDomainBlock,
    "AdminEmailDomainBlockHistory": AdminEmailDomainBlockHistory,
    "AdminIpBlock": AdminIpBlock,
    "DomainBlock": DomainBlock,
    "ExtendedDescription": ExtendedDescription,
    "FilterKeyword": FilterKeyword,
    "FilterStatus": FilterStatus,
    "IdentityProof": IdentityProof,
    "StatusSource": StatusSource,
    "Suggestion": Suggestion,
    "Translation": Translation,
    "AccountCreationError": AccountCreationError,
    "AccountCreationErrorDetails": AccountCreationErrorDetails,
    "AccountCreationErrorDetailsField": AccountCreationErrorDetailsField,
    "NotificationPolicy": NotificationPolicy,
    "NotificationPolicySummary": NotificationPolicySummary,
    "RelationshipSeveranceEvent": RelationshipSeveranceEvent,
    "GroupedNotificationsResults": GroupedNotificationsResults,
    "PartialAccountWithAvatar": PartialAccountWithAvatar,
    "NotificationGroup": NotificationGroup,
    "AccountWarning": AccountWarning,
    "UnreadNotificationsCount": UnreadNotificationsCount,
    "Appeal": Appeal,
    "NotificationRequest": NotificationRequest,
    "SupportedLocale": SupportedLocale,
    "OAuthServerInfo": OAuthServerInfo,
    "OAuthUserInfo": OAuthUserInfo,
    "TermsOfService": TermsOfService,
}
__all__ = [
    "Account",
    "AccountField",
    "Role",
    "CredentialAccountSource",
    "Status",
    "Quote",
    "ShallowQuote",
    "StatusEdit",
    "FilterResult",
    "StatusMention",
    "ScheduledStatus",
    "ScheduledStatusParams",
    "Poll",
    "PollOption",
    "Conversation",
    "Tag",
    "TagHistory",
    "CustomEmoji",
    "Application",
    "Relationship",
    "Filter",
    "FilterV2",
    "Notification",
    "Context",
    "UserList",
    "MediaAttachment",
    "MediaAttachmentMetadataContainer",
    "MediaAttachmentImageMetadata",
    "MediaAttachmentVideoMetadata",
    "MediaAttachmentAudioMetadata",
    "MediaAttachmentFocusPoint",
    "MediaAttachmentColors",
    "PreviewCard",
    "TrendingLinkHistory",
    "PreviewCardAuthor",
    "Search",
    "SearchV2",
    "Instance",
    "InstanceConfiguration",
    "InstanceURLs",
    "InstanceV2",
    "InstanceIcon",
    "InstanceConfigurationV2",
    "InstanceVapidKey",
    "InstanceURLsV2",
    "InstanceThumbnail",
    "InstanceThumbnailVersions",
    "InstanceStatistics",
    "InstanceUsage",
    "InstanceUsageUsers",
    "RuleTranslation",
    "Rule",
    "InstanceRegistrations",
    "InstanceContact",
    "InstanceAccountConfiguration",
    "InstanceStatusConfiguration",
    "InstanceTranslationConfiguration",
    "InstanceMediaConfiguration",
    "InstancePollConfiguration",
    "Nodeinfo",
    "NodeinfoSoftware",
    "NodeinfoServices",
    "NodeinfoUsage",
    "NodeinfoUsageUsers",
    "NodeinfoMetadata",
    "Activity",
    "Report",
    "AdminReport",
    "WebPushSubscription",
    "WebPushSubscriptionAlerts",
    "PushNotification",
    "Preferences",
    "FeaturedTag",
    "Marker",
    "Announcement",
    "Reaction",
    "StreamReaction",
    "FamiliarFollowers",
    "AdminAccount",
    "AdminIp",
    "AdminMeasure",
    "AdminMeasureData",
    "AdminDimension",
    "AdminDimensionData",
    "AdminRetention",
    "AdminCohort",
    "AdminDomainBlock",
    "AdminCanonicalEmailBlock",
    "AdminDomainAllow",
    "AdminEmailDomainBlock",
    "AdminEmailDomainBlockHistory",
    "AdminIpBlock",
    "DomainBlock",
    "ExtendedDescription",
    "FilterKeyword",
    "FilterStatus",
    "IdentityProof",
    "StatusSource",
    "Suggestion",
    "Translation",
    "AccountCreationError",
    "AccountCreationErrorDetails",
    "AccountCreationErrorDetailsField",
    "NotificationPolicy",
    "NotificationPolicySummary",
    "RelationshipSeveranceEvent",
    "GroupedNotificationsResults",
    "PartialAccountWithAvatar",
    "NotificationGroup",
    "AccountWarning",
    "UnreadNotificationsCount",
    "Appeal",
    "NotificationRequest",
    "SupportedLocale",
    "OAuthServerInfo",
    "OAuthUserInfo",
    "TermsOfService",
]

