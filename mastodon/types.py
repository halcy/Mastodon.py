from __future__ import annotations # python< 3.9 compat
from datetime import datetime
from typing import Union, Optional, Tuple, List, IO, Dict
from mastodon.types_base import AttribAccessDict, IdType, MaybeSnowflakeIdType, PaginationInfo, PrimitiveIdType, EntityList, PaginatableList, NonPaginatableList, PathOrFile, WebpushCryptoParamsPubkey, WebpushCryptoParamsPrivkey, try_cast_recurse, try_cast, real_issubclass

class Account(AttribAccessDict):
    """
    A user acccount, local or remote.

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

    moved_to_account: "Optional[Account]"
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

    fields: "EntityList[AccountField]"
    """
    List of up to four (by default) AccountFields.

    Version history:
      * 2.4.0: added
    """

    emojis: "EntityList[CustomEmoji]"
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

    roles: "EntityList"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Deprecated. Was a list of strings with the users roles. Now just an empty list. Mastodon.py makes no attempt to fill it, and the field may be removed if Mastodon removes it. Use the `role` field instead.

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

    _version = "4.0.0"

class AccountField(AttribAccessDict):
    """
    A field, displayed on a users profile (e.g. "Pronouns", "Favorite color").

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

    language: "str"
    """
    The default posting language for new statuses.
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 2.4.2: added
    """

    fields: "EntityList[AccountField]"
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

    _version = "3.0.0"

class Status(AttribAccessDict):
    """
    A single status / toot / post.

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
    Descriptor for the status. Mastodon, for example, may use something like: 'tag:mastodon.social,2016-11-25:objectId=<id>:objectType=Status'.

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

    mentions: "EntityList[Account]"
    """
    A list Mentions this status includes.

    Version history:
      * 0.6.0: added
    """

    media_attachments: "EntityList[MediaAttachment]"
    """
    List files attached to this status.

    Version history:
      * 0.6.0: added
    """

    emojis: "EntityList[CustomEmoji]"
    """
    A list of CustomEmoji used in the status.

    Version history:
      * 2.0.0: added
    """

    tags: "EntityList[Tag]"
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

    filtered: "Optional[EntityList[FilterResult]]"
    """
    If present, a list of filter application results that indicate which of the users filters matched and what actions should be taken. (optional)

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class StatusEdit(AttribAccessDict):
    """
    An object representing a past version of an edited status.

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

    media_attachments: "EntityList[MediaAttachment]"
    """
    List of MediaAttachment objects with the attached media for this version of the status.

    Version history:
      * 3.5.0: added
    """

    emojis: "EntityList[CustomEmoji]"
    """
    List of custom emoji used in this version of the status.

    Version history:
      * 3.5.0: added
    """

    poll: "Poll"
    """
    The current state of the poll options at this revision. Note that edits changing the poll options will be collapsed together into one edit, since this action resets the poll.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class FilterResult(AttribAccessDict):
    """
    A filter action that should be taken on a status.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/FilterResult/
    """

    filter: "Union[Filter, FilterV2]"
    """
    The filter that was matched.

    Version history:
      * 4.0.0: added
    """

    keyword_matches: "Optional[EntityList[str]]"
    """
    The keyword within the filter that was matched. (nullable)

    Version history:
      * 4.0.0: added
    """

    status_matches: "Optional[EntityList]"
    """
    The status ID within the filter that was matched. (nullable)

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class StatusMention(AttribAccessDict):
    """
    A mention of a user within a status.

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

    media_attachments: "EntityList"
    """
    Array of MediaAttachment objects for the attachments to the scheduled status.

    Version history:
      * 2.7.0: added
    """

    _version = "2.7.0"

class ScheduledStatusParams(AttribAccessDict):
    """
    Parameters for a status / toot to be posted in the future.

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

    media_ids: "Optional[EntityList[str]]"
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

    visibility: "str"
    """
    Visibility of the status.

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

    allowed_mentions: "Optional[EntityList[str]]"
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

    _version = "2.8.0"

class Poll(AttribAccessDict):
    """
    A poll attached to a status.

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

    options: "EntityList[PollOption]"
    """
    The poll options.

    Version history:
      * 2.8.0: added
    """

    emojis: "EntityList[CustomEmoji]"
    """
    List of CustomEmoji used in answer strings,.

    Version history:
      * 2.8.0: added
    """

    own_votes: "EntityList[int]"
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

    accounts: "EntityList[Account]"
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

    history: "Optional[EntityList[TagHistory]]"
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

    _version = "4.0.0"

class TagHistory(AttribAccessDict):
    """
    Usage history for a hashtag.

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

    category: "str"
    """
    The category to display the emoji under (not present if none is set).

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class Application(AttribAccessDict):
    """
    Information about an app (in terms of the API).

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Application/
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
    A vapid key that can be used in web applications.

    Version history:
      * 2.8.0: added
    """

    _version = "3.5.1"

class Relationship(AttribAccessDict):
    """
    Information about the relationship between two users.

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

    languages: "Optional[EntityList[str]]"
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

    context: "EntityList[str]"
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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Filter/
    """

    id: "IdType"
    """
    Id of the filter.

    Version history:
      * 4.0.0: added
    """

    context: "EntityList[str]"
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

    keywords: "EntityList[FilterKeyword]"
    """
    A list of keywords that will trigger this filter.

    Version history:
      * 4.0.0: added
    """

    statuses: "EntityList[FilterStatus]"
    """
    A list of statuses that will trigger this filter.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class Notification(AttribAccessDict):
    """
    A notification about some event, like a new reply or follower.

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

    status: "Status"
    """
    In case of "mention", the mentioning status In case of reblog / favourite, the reblogged / favourited status.

    Version history:
      * 0.9.9: added
    """

    _version = "4.0.0"

class Context(AttribAccessDict):
    """
    The conversation context for a given status, i.e. its predecessors (that it replies to) and successors (that reply to it).

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Context/
    """

    ancestors: "EntityList[Status]"
    """
    A list of Statuses that the Status with this Context is a reply to.

    Version history:
      * 0.6.0: added
    """

    descendants: "EntityList[Status]"
    """
    A list of Statuses that are replies to the Status with this Context.

    Version history:
      * 0.6.0: added
    """

    _version = "0.6.0"

class UserList(AttribAccessDict):
    """
    A list of users.

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

    _version = "3.3.0"

class MediaAttachment(AttribAccessDict):
    """
    A piece of media (like an image, video, or audio file) that can be or has been attached to a status.

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

    preview_url: "str"
    """
    The URL for the media preview.
    Should contain (as text): URL

    Version history:
      * 0.6.0: added
    """

    text_url: "str"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    Deprecated. The display text for the media (what shows up in text). May not be present in mastodon versions after 3.5.0.
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
    An object holding metadata about a media attachment and its thumbnail.

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

    colors: "MediaAttachmentColors"
    """
    Information about accent colors for the media.

    Version history:
      * 4.0.0: added
    """

    focus: "MediaAttachmentFocusPoint"
    """
    Information about the focus point for the media.

    Version history:
      * 3.3.0: added
    """

    _version = "4.0.0"

class MediaAttachmentImageMetadata(AttribAccessDict):
    """
    Metadata for an image media attachment.

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
    Metadata for a video or gifv media attachment.

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
    Name of the embedded contents author.

    Version history:
      * 1.3.0: added
    """

    author_url: "str"
    """
    URL pointing to the embedded contents author.
    Should contain (as text): URL

    Version history:
      * 1.3.0: added
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

    _version = "3.2.0"

class Search(AttribAccessDict):
    """
    A search result, with accounts, hashtags and statuses.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Search/
    """

    accounts: "EntityList[Account]"
    """
    List of Accounts resulting from the query.

    Version history:
      * 1.1.0: added
    """

    hashtags: "EntityList[str]"
    """
    THIS FIELD IS DEPRECATED. IT IS RECOMMENDED THAT YOU DO NOT USE IT.

    List of Tags resulting from the query.

    Version history:
      * 1.1.0: added
      * 2.4.1: v1 search deprecated because it returns a list of strings. v2 search added which returns a list of tags.
      * 3.0.0: v1 removed
    """

    statuses: "EntityList[Status]"
    """
    List of Statuses resulting from the query.

    Version history:
      * 1.1.0: added
    """

    _version = "3.0.0"

class SearchV2(AttribAccessDict):
    """
    A search result, with accounts, hashtags and statuses.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Search/
    """

    accounts: "EntityList[Account]"
    """
    List of Accounts resulting from the query.

    Version history:
      * 1.1.0: added
    """

    hashtags: "EntityList[Tag]"
    """
    List of Tags resulting from the query.

    Version history:
      * 2.4.1: added
    """

    statuses: "EntityList[Status]"
    """
    List of Statuses resulting from the query.

    Version history:
      * 1.1.0: added
    """

    _version = "2.4.1"

class Instance(AttribAccessDict):
    """
    Information about an instance. V1 API version.

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

    languages: "EntityList[str]"
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

    rules: "EntityList[Rule]"
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

    languages: "EntityList[str]"
    """
    Array of ISO 639-1 (two-letter) language codes the instance has chosen to advertise.
    Should contain (as text): TwoLetterLanguageCodeEnum

    Version history:
      * 4.0.0: added
    """

    configuration: "InstanceConfiguration"
    """
    Various instance configuration settings - especially various limits (character counts, media upload sizes, ...).

    Version history:
      * 3.1.4: added
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

    rules: "EntityList[Rule]"
    """
    List of Rules with `id` and `text` fields, one for each server rule set by the admin.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class InstanceConfigurationV2(AttribAccessDict):
    """
    Configuration values for this instance, especially limits and enabled features.

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

    _version = "4.0.0"

class InstanceURLsV2(AttribAccessDict):
    """
    A list of URLs related to an instance.

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

    _version = "4.0.0"

class InstanceThumbnail(AttribAccessDict):
    """
    Extended information about an instances thumbnail.

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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Instance/
    """

    active_month: "int"
    """
    This instances most recent monthly active user count.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class Rule(AttribAccessDict):
    """
    A rule that instance staff has specified users must follow on this instance.

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
    The rule to be followed.

    Version history:
      * 3.4.0: added
    """

    _version = "3.4.0"

class InstanceRegistrations(AttribAccessDict):
    """
    Registration information for this instance, like whether registrations are open and whether they require approval.

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
    Presumably, a registration related URL. It is unclear what this is for. (nullable)
    Should contain (as text): URL

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class InstanceContact(AttribAccessDict):
    """
    Contact information for this instances' staff.

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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    max_featured_tags: "int"
    """
    The maximum number of featured tags that can be displayed on a profile.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class InstanceStatusConfiguration(AttribAccessDict):
    """
    Configuration values relating to statuses.

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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/instance/
    """

    supported_mime_types: "EntityList[str]"
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

    _version = "3.4.2"

class InstancePollConfiguration(AttribAccessDict):
    """
    Configuration values relating to polls.

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

    protocols: "EntityList[str]"
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
    Additional node metadata. On Mastodon, typically an empty object with no fields.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class NodeinfoSoftware(AttribAccessDict):
    """
    NodeInfo software-related information.

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

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    outbound: "EntityList"
    """
    List of services that this instance can send messages to. On Mastodon, typically an empty list.

    Version history:
      * 3.0.0: added
    """

    inbound: "EntityList"
    """
    List of services that this instance can retrieve messages from. On Mastodon, typically an empty list.

    Version history:
      * 3.0.0: added
    """

    _version = "3.0.0"

class NodeinfoUsage(AttribAccessDict):
    """
    Nodeinfo usage-related information.

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
    Nodeinfo extra metadata.

    See also (Mastodon API documentation): https://github.com/jhass/nodeinfo
    """

    _version = "0.0.0"

class Activity(AttribAccessDict):
    """
    Information about recent activity on an instance.

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

    status_ids: "EntityList[IdType]"
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

    rules_ids: "EntityList[IdType]"
    """
    IDs of the rules selected for this report.

    Version history:
      * 3.5.0: added
    """

    _version = "4.0.0"

class AdminReport(AttribAccessDict):
    """
    Information about a report that has been filed against a user.

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

    statuses: "EntityList[Status]"
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

    forwarded: "bool"
    """
    Whether a report was forwarded to a remote instance.

    Version history:
      * 4.0.0: added
    """

    rules: "EntityList[Rule]"
    """
    Rules attached to the report, for context.

    Version history:
      * 3.5.0: added
    """

    _version = "4.0.0"

class WebPushSubscription(AttribAccessDict):
    """
    Information about the logged-in users web push subscription for the authenticated application.

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

    _version = "4.0.0"

class WebPushSubscriptionAlerts(AttribAccessDict):
    """
    Information about alerts as part of a push subscription.

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/WebPushSubscription/
    """

    follow: "bool"
    """
    True if push subscriptions for follow events have been requested, false or not present otherwise.

    Version history:
      * 2.4.0: added
    """

    favourite: "bool"
    """
    True if push subscriptions for favourite events have been requested, false or not present otherwise.

    Version history:
      * 2.4.0: added
    """

    reblog: "bool"
    """
    True if push subscriptions for reblog events have been requested, false or not present otherwise.

    Version history:
      * 2.4.0: added
    """

    mention: "bool"
    """
    True if push subscriptions for mention events have been requested, false or not present otherwise.

    Version history:
      * 2.4.0: added
    """

    poll: "bool"
    """
    True if push subscriptions for poll events have been requested, false or not present otherwise.

    Version history:
      * 2.8.0: added
    """

    follow_request: "bool"
    """
    True if push subscriptions for follow request events have been requested, false or not present otherwise.

    Version history:
      * 2.4.0: added
    """

    status: "bool"
    """
    True if push subscriptions for status creation (watched users only) events have been requested, false or not present otherwise.

    Version history:
      * 3.1.0: added
    """

    update: "bool"
    """
    True if push subscriptions for status update (edit) events have been requested, false or not present otherwise.

    Version history:
      * 3.3.0: added
    """

    admin_sign_up: "bool"
    """
    True if push subscriptions for sign up events have been requested, false or not present otherwise. Admins only.

    Version history:
      * 3.5.0: added
    """

    admin_report: "bool"
    """
    True if push subscriptions for report creation events have been requested, false or not present otherwise. Admins only.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class PushNotification(AttribAccessDict):
    """
    A single Mastodon push notification received via WebPush, after decryption.

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

    last_status_at: "datetime"
    """
    The last time a public status containing this hashtag was added to this instance's database (can be None if there are none).

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

    mentions: "EntityList[StatusMention]"
    """
    Users mentioned in the annoucement.

    Version history:
      * 3.1.0: added
    """

    tags: "EntityList"
    """
    Hashtags mentioned in the announcement.

    Version history:
      * 3.1.0: added
    """

    emojis: "EntityList"
    """
    Custom emoji used in the annoucement.

    Version history:
      * 3.1.0: added
    """

    reactions: "EntityList[Reaction]"
    """
    Reactions to the annoucement.

    Version history:
      * 3.1.0: added
    """

    statuses: "EntityList"
    """
    Statuses linked in the announcement text.

    Version history:
      * 3.1.0: added
    """

    _version = "3.1.0"

class Reaction(AttribAccessDict):
    """
    A reaction to an announcement.

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

    url: "str"
    """
    URL for the custom emoji image.
    Should contain (as text): URL

    Version history:
      * 3.1.0: added
    """

    static_url: "str"
    """
    URL for a never-animated version of the custom emoji image.
    Should contain (as text): URL

    Version history:
      * 3.1.0: added
    """

    _version = "3.1.0"

class StreamReaction(AttribAccessDict):
    """
    A reaction to an announcement.

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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/FamiliarFollowers/
    """

    id: "IdType"
    """
    ID of the account for which the familiar followers are being returned.

    Version history:
      * 3.5.0: added
    """

    accounts: "EntityList[Account]"
    """
    List of Accounts of the familiar followers.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminAccount(AttribAccessDict):
    """
    Admin variant of the Account entity, with some additional information.

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
      * 3.5.0: return type changed from String to [AdminIp]({{< relref "entities/Admin_Ip" >}}) due to a bug
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
    Undocumented. If you know what this means, please let me know.

    Version history:
      * 2.9.1: added
    """

    ips: "EntityList[AdminIp]"
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

    invited_by_account_id : "Optional[IdType]"
    """
    Present if the user was created via invite and set to the inviting users id. (optional)

    Version history:
      * 2.9.1: added
    """

    _version = "4.0.0"

class AdminIp(AttribAccessDict):
    """
    An IP address used by some user or other instance, visible as part of some admin APIs.

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

    human_value: "str"
    """
    Human readable variant of the measure returned.

    Version history:
      * 3.5.0: added
    """

    previous_total: "Optional[str]"
    """
    Previous measurement period value of the measure returned, if available. (nullable)

    Version history:
      * 3.5.0: added
    """

    data: "EntityList[AdminMeasureData]"
    """
    A list of AdminMeasureData with the measure broken down by date.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminMeasureData(AttribAccessDict):
    """
    A single row of data for an admin reporting api measurement.

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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Admin_Dimension/
    """

    key: "str"
    """
    Name of the dimension returned.

    Version history:
      * 3.5.0: added
    """

    data: "EntityList[AdminDimensionData]"
    """
    A list of data AdminDimensionData objects.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminDimensionData(AttribAccessDict):
    """
    A single row of data for qualitative measurements about the server, as returned by the admin reporting api.

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

    data: "EntityList[AdminCohort]"
    """
    List of AdminCohort objects.

    Version history:
      * 3.5.0: added
    """

    _version = "3.5.0"

class AdminCohort(AttribAccessDict):
    """
    A single data point regarding user retention for a given cohort, as returned by the admin reporting api.

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

    _version = "4.0.0"

class AdminCanonicalEmailBlock(AttribAccessDict):
    """
    An e-mail block that has been set up to prevent certain e-mails to be used when signing up, via hash matching.

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

    history: "EntityList[AdminEmailDomainBlockHistory]"
    """
    Usage statistics for given days (typically the past week).

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class AdminEmailDomainBlockHistory(AttribAccessDict):
    """
    Historic data about attempted signups using e-mails from a given domain.

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

    comment: "str"
    """
    An optional reason for the domain block.

    Version history:
      * 4.0.0: added
    """

    _version = "4.0.0"

class ExtendedDescription(AttribAccessDict):
    """
    An extended instance description that can contain HTML.

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
    A cryptographic proof-of-identity.

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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/entities/Suggestion
    """

    source: "str"
    """
    The reason this account is being suggested.

    Version history:
      * 3.4.0: added
    """

    account: "Account"
    """
    The account being recommended to follow.

    Version history:
      * 3.4.0: added
    """

    _version = "3.4.0"

class Translation(AttribAccessDict):
    """
    A translation of a status.

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

    See also (Mastodon API documentation): https://docs.joinmastodon.org/methods/accounts/#create
    """

    username: "Optional[AccountCreationErrorDetailsField]"
    """
    An object giving more details about an error caused by the username. (optional)

    Version history:
      * 3.4.0: added
    """

    password: "Optional[AccountCreationErrorDetailsField]"
    """
    An object giving more details about an error caused by the password. (optional)

    Version history:
      * 3.4.0: added
    """

    email: "Optional[AccountCreationErrorDetailsField]"
    """
    An object giving more details about an error caused by the e-mail. (optional)

    Version history:
      * 3.4.0: added
    """

    agreement: "Optional[AccountCreationErrorDetailsField]"
    """
    An object giving more details about an error caused by the usage policy agreement. (optional)

    Version history:
      * 3.4.0: added
    """

    locale: "Optional[AccountCreationErrorDetailsField]"
    """
    An object giving more details about an error caused by the locale. (optional)

    Version history:
      * 3.4.0: added
    """

    reason: "Optional[AccountCreationErrorDetailsField]"
    """
    An object giving more details about an error caused by the registration reason. (optional)

    Version history:
      * 3.4.0: added
    """

    _version = "3.4.0"

class AccountCreationErrorDetailsField(AttribAccessDict):
    """
    An object giving details about what specifically is wrong with a given field in an account registration attempt.

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
