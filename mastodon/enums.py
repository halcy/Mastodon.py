"""API enums for Mastodon.py. Manually maintained, for now.

Every enum derives from :class:`StringEnum`, so can be used interchangeably with strings.
"""

from mastodon.compat import StringEnum

class Visibility(StringEnum):
    """Visibility comparison domain; see :class:`PostVisibility`,
    :class:`StatusVisibility`, :class:`DefaultPostVisibility`, and
    :class:`ReblogVisibility`.
    """


class PostVisibility(Visibility):
    """Audience requested when publishing a post; see :class:`StatusVisibility`."""

    PUBLIC = "public"
    """Public and discoverable."""
    UNLISTED = "unlisted"
    """Public, but excluded from public discovery."""
    PRIVATE = "private"
    """Followers only."""
    DIRECT = "direct"
    """Mentioned accounts only."""


class StatusVisibility(Visibility):
    """Audience returned for a status, including known Pleroma extensions.

    See :class:`PostVisibility` for the standard publishing contract.
    """

    PUBLIC = "public"
    """Public and discoverable."""
    UNLISTED = "unlisted"
    """Public, but excluded from public discovery."""
    PRIVATE = "private"
    """Followers only."""
    DIRECT = "direct"
    """Mentioned accounts only."""
    LIST = "list"
    """A manually curated list (Pleroma extension)."""
    LOCAL = "local"
    """Local followers (Pleroma extension)."""


class DefaultPostVisibility(Visibility):
    """Saved default audience; see :class:`PostVisibility` for individual posts."""

    PUBLIC = "public"
    """Public and discoverable."""
    UNLISTED = "unlisted"
    """Public, but excluded from public discovery."""
    PRIVATE = "private"
    """Followers only."""
    DIRECT = "direct"
    """Mentioned accounts only."""


class ReblogVisibility(Visibility):
    """Audience of a boost, which cannot be direct; see :class:`PostVisibility`."""

    PUBLIC = "public"
    """Public and discoverable."""
    UNLISTED = "unlisted"
    """Public, but excluded from public discovery."""
    PRIVATE = "private"
    """Followers only."""


class QuotePolicy(StringEnum):
    """Quote-policy comparison domain; see :class:`PostQuotePolicy` and
    :class:`DefaultQuotePolicy`.
    """


class PostQuotePolicy(QuotePolicy):
    """Requested policy for quoting a post; see :class:`QuoteApprovalAudience`."""

    PUBLIC = "public"
    """Anyone except blocked accounts may quote."""
    FOLLOWERS = "followers"
    """Followers and the author may quote."""
    NOBODY = "nobody"
    """Only the author may quote."""


class DefaultQuotePolicy(QuotePolicy):
    """Saved default quote policy; see :class:`PostQuotePolicy`."""

    PUBLIC = "public"
    """Anyone except blocked accounts may quote."""
    FOLLOWERS = "followers"
    """Followers and the author may quote."""
    NOBODY = "nobody"
    """Only the author may quote."""


class QuoteState(StringEnum):
    """Authorization state shared by full and shallow quote responses."""

    PENDING = "pending"
    """Awaiting authorization by the quoted account."""
    ACCEPTED = "accepted"
    """Approved for display."""
    REJECTED = "rejected"
    """Explicitly rejected by the quoted account."""
    REVOKED = "revoked"
    """Previously granted permission was revoked."""
    DELETED = "deleted"
    """The quoted status was deleted."""
    UNAUTHORIZED = "unauthorized"
    """The current user cannot view the quoted status."""
    BLOCKED_ACCOUNT = "blocked_account"
    """The current user blocked the quoted account."""
    BLOCKED_DOMAIN = "blocked_domain"
    """The current user blocked the quoted domain."""
    MUTED_ACCOUNT = "muted_account"
    """The current user muted the quoted account."""


class ApprovalAudience(StringEnum):
    """Approval-audience comparison domain; see :class:`QuoteApprovalAudience`
    and :class:`FeatureApprovalAudience`.
    """


class QuoteApprovalAudience(ApprovalAudience):
    """Audience in a status's automatic/manual quote policy.

    Unlike :class:`PostQuotePolicy`, this describes the server's interpreted
    policy, including policies originating on other software.
    """

    PUBLIC = "public"
    """Anyone."""
    FOLLOWERS = "followers"
    """Followers of the author."""
    FOLLOWING = "following"
    """Accounts followed by the author."""
    UNSUPPORTED_POLICY = "unsupported_policy"
    """A policy Mastodon cannot interpret."""


class FeatureApprovalAudience(ApprovalAudience):
    """Audience in an account's automatic/manual featuring policy.

    See :class:`QuoteApprovalAudience` for the corresponding quote contract.
    """

    PUBLIC = "public"
    """Anyone."""
    FOLLOWERS = "followers"
    """Followers of the account."""
    FOLLOWING = "following"
    """Accounts followed by the account."""
    UNSUPPORTED_POLICY = "unsupported_policy"
    """A policy Mastodon cannot interpret."""


class ApprovalDecision(StringEnum):
    """Current-user approval comparison domain; see :class:`QuoteApprovalDecision`
    and :class:`FeatureApprovalDecision`.
    """


class QuoteApprovalDecision(ApprovalDecision):
    """Expected result of the current user requesting to quote a status."""

    AUTOMATIC = "automatic"
    """Expected to be accepted automatically."""
    MANUAL = "manual"
    """Expected to require manual review."""
    DENIED = "denied"
    """Not expected to be allowed."""
    UNKNOWN = "unknown"
    """Unsupported policy; treat as denied."""


class FeatureApprovalDecision(ApprovalDecision):
    """Expected result of featuring an account; see :class:`QuoteApprovalDecision`."""

    AUTOMATIC = "automatic"
    """Expected to be accepted automatically."""
    MANUAL = "manual"
    """Expected to require manual review."""
    DENIED = "denied"
    """Not expected to be allowed."""
    UNKNOWN = "unknown"
    """Unsupported policy; treat as denied."""
    MISSING = "missing"
    """No supported policy; treat as denied."""


class FilterContext(StringEnum):
    """Places where a filter applies, for both filter API versions."""

    HOME = "home"
    """Home timeline and lists."""
    NOTIFICATIONS = "notifications"
    """Notifications."""
    PUBLIC = "public"
    """Public timelines."""
    THREAD = "thread"
    """Expanded status threads."""
    ACCOUNT = "account"
    """Posts on account profiles."""


class FilterAction(StringEnum):
    """How to handle a matching status. Unknown actions should behave as WARN."""

    WARN = "warn"
    """Show a filter warning and allow expansion."""
    HIDE = "hide"
    """Hide the status completely."""
    BLUR = "blur"
    """Hide or blur media with a filter warning."""


class NotificationType(StringEnum):
    """Notification comparison domain; see :class:`IndividualNotificationType`,
    :class:`GroupedNotificationType`, :class:`PushNotificationType`, and
    :class:`GroupableNotificationType`. Push admin values use underscores,
    whereas REST notification admin values use dots.
    """


class IndividualNotificationType(NotificationType):
    """Type of an individual REST notification; see :class:`GroupedNotificationType`."""

    MENTION = "mention"
    """An account mentioned the user."""
    STATUS = "status"
    """A watched account posted a status."""
    REBLOG = "reblog"
    """An account boosted the user's status."""
    FOLLOW = "follow"
    """An account followed the user."""
    FOLLOW_REQUEST = "follow_request"
    """An account requested to follow the user."""
    FAVOURITE = "favourite"
    """An account favourited the user's status."""
    POLL = "poll"
    """A poll created or voted in by the user ended."""
    UPDATE = "update"
    """A status the user interacted with was edited."""
    ADMIN_SIGN_UP = "admin.sign_up"
    """An account signed up; administrator notification."""
    ADMIN_REPORT = "admin.report"
    """A report was filed; administrator notification."""
    SEVERED_RELATIONSHIPS = "severed_relationships"
    """Moderation or blocking severed follow relationships."""
    MODERATION_WARNING = "moderation_warning"
    """A moderator warned the user or took action."""
    QUOTE = "quote"
    """An account quoted the user's status."""
    QUOTED_UPDATE = "quoted_update"
    """A status quoted by the user was edited."""
    ADDED_TO_COLLECTION = "added_to_collection"
    """An account added the user to a collection."""
    COLLECTION_UPDATE = "collection_update"
    """A collection featuring the user was updated."""


class GroupedNotificationType(NotificationType):
    """Type of a grouped notification; see :class:`IndividualNotificationType`."""

    MENTION = "mention"
    """An account mentioned the user."""
    STATUS = "status"
    """A watched account posted a status."""
    REBLOG = "reblog"
    """An account boosted the user's status."""
    FOLLOW = "follow"
    """An account followed the user."""
    FOLLOW_REQUEST = "follow_request"
    """An account requested to follow the user."""
    FAVOURITE = "favourite"
    """An account favourited the user's status."""
    POLL = "poll"
    """A poll created or voted in by the user ended."""
    UPDATE = "update"
    """A status the user interacted with was edited."""
    ADMIN_SIGN_UP = "admin.sign_up"
    """An account signed up; administrator notification."""
    ADMIN_REPORT = "admin.report"
    """A report was filed; administrator notification."""
    SEVERED_RELATIONSHIPS = "severed_relationships"
    """Moderation or blocking severed follow relationships."""
    MODERATION_WARNING = "moderation_warning"
    """A moderator warned the user or took action."""
    QUOTE = "quote"
    """An account quoted the user's status."""
    QUOTED_UPDATE = "quoted_update"
    """A status quoted by the user was edited."""
    ANNUAL_REPORT = "annual_report"
    """The user's annual report is ready."""
    ADDED_TO_COLLECTION = "added_to_collection"
    """An account added the user to a collection."""
    COLLECTION_UPDATE = "collection_update"
    """A collection featuring the user was updated."""


class PushNotificationType(NotificationType):
    """Type sent in push payloads; see :class:`IndividualNotificationType`.

    Administrator notification wire values intentionally use underscores.
    """

    FOLLOW = "follow"
    """An account followed the user."""
    FAVOURITE = "favourite"
    """An account favourited the user's status."""
    REBLOG = "reblog"
    """An account boosted the user's status."""
    MENTION = "mention"
    """An account mentioned the user."""
    POLL = "poll"
    """A poll created or voted in by the user ended."""
    FOLLOW_REQUEST = "follow_request"
    """An account requested to follow the user."""
    STATUS = "status"
    """A watched account posted a status."""
    UPDATE = "update"
    """A boosted status was edited."""
    ADMIN_SIGN_UP = "admin_sign_up"
    """An account signed up; administrator notification."""
    ADMIN_REPORT = "admin_report"
    """A report was filed; administrator notification."""
    QUOTE = "quote"
    """An account quoted the user's status."""
    QUOTED_UPDATE = "quoted_update"
    """A status quoted by the user was edited."""


class GroupableNotificationType(NotificationType):
    """Types supported by notification grouping; see :class:`GroupedNotificationType`."""

    FAVOURITE = "favourite"
    """Group favourites."""
    FOLLOW = "follow"
    """Group new followers."""
    REBLOG = "reblog"
    """Group boosts."""


class ListRepliesPolicy(StringEnum):
    """Which replies appear in a user list."""

    FOLLOWED = "followed"
    """Replies to any followed account."""
    LIST = "list"
    """Replies to accounts on the list."""
    NONE = "none"
    """No replies."""


class MediaAttachmentType(StringEnum):
    """Kind of an attached media file, not its MIME type."""

    UNKNOWN = "unknown"
    """Unsupported or unrecognized media."""
    IMAGE = "image"
    """Static image."""
    GIFV = "gifv"
    """Looping silent animation."""
    VIDEO = "video"
    """Video clip."""
    AUDIO = "audio"
    """Audio track."""


class PreviewCardType(StringEnum):
    """OEmbed kind of a preview card."""

    LINK = "link"
    """Link preview."""
    PHOTO = "photo"
    """Photo embed."""
    VIDEO = "video"
    """Video embed."""
    RICH = "rich"
    """Rich iframe embed; not currently accepted by Mastodon."""


class CollectionItemState(StringEnum):
    """Consent state of a featured collection entry."""

    PENDING = "pending"
    """Awaiting the account's consent."""
    ACCEPTED = "accepted"
    """The account consented."""
    REJECTED = "rejected"
    """The account rejected the request."""
    REVOKED = "revoked"
    """The account revoked earlier consent."""


class TimelineAccess(StringEnum):
    """Access requirement advertised for a local or remote instance feed.

    See :class:`TimelineAccessType` for the feed selector parameter.
    """

    PUBLIC = "public"
    """Available to visitors and authenticated users."""
    AUTHENTICATED = "authenticated"
    """Authentication is required."""
    DISABLED = "disabled"
    """Only users with the View live and topic feeds permission have access."""


class ReportCategory(StringEnum):
    """Generic reason for a user or administrator report."""

    SPAM = "spam"
    """Unwanted or repetitive content."""
    LEGAL = "legal"
    """Illegal content."""
    VIOLATION = "violation"
    """Violation of a specific server rule."""
    OTHER = "other"
    """Another reason."""


class PushSubscriptionPolicy(StringEnum):
    """Sources permitted to generate push notifications."""

    ALL = "all"
    """All sources."""
    NONE = "none"
    """Do not send pushes."""
    FOLLOWER = "follower"
    """Accounts following the user."""
    FOLLOWED = "followed"
    """Accounts followed by the user."""


class MediaExpansion(StringEnum):
    """Saved reading preference for expanding media."""

    DEFAULT = "default"
    """Hide sensitive media."""
    SHOW_ALL = "show_all"
    """Show all media."""
    HIDE_ALL = "hide_all"
    """Hide all media."""


class AdminMeasureKey(StringEnum):
    """Quantitative administrator metric; see :class:`AdminDimensionKey`."""

    ACTIVE_USERS = "active_users"
    """Active users in the period."""
    NEW_USERS = "new_users"
    """New users in the period."""
    INTERACTIONS = "interactions"
    """Interactions with local statuses."""
    OPENED_REPORTS = "opened_reports"
    """Reports filed."""
    RESOLVED_REPORTS = "resolved_reports"
    """Reports resolved."""
    TAG_ACCOUNTS = "tag_accounts"
    """Accounts using a tag."""
    TAG_USES = "tag_uses"
    """Statuses using a tag."""
    TAG_SERVERS = "tag_servers"
    """Servers using a tag."""
    INSTANCE_ACCOUNTS = "instance_accounts"
    """Accounts originating from a domain."""
    INSTANCE_MEDIA_ATTACHMENTS = "instance_media_attachments"
    """Storage consumed by a domain's media."""
    INSTANCE_REPORTS = "instance_reports"
    """Reports against a domain's accounts."""
    INSTANCE_STATUSES = "instance_statuses"
    """Statuses originating from a domain."""
    INSTANCE_FOLLOWS = "instance_follows"
    """Accounts on a domain followed by local users."""
    INSTANCE_FOLLOWERS = "instance_followers"
    """Local accounts followed by a domain's users."""


class AdminDimensionKey(StringEnum):
    """Qualitative administrator metric; see :class:`AdminMeasureKey`.

    Data-item keys are not this enum: depending on the dimension they are
    arbitrary languages, domains, usernames, client names, or software names.
    """

    LANGUAGES = "languages"
    """Languages of local statuses."""
    SOURCES = "sources"
    """Clients used to author local statuses."""
    SERVERS = "servers"
    """Remote servers by status count."""
    SPACE_USAGE = "space_usage"
    """Storage usage by component."""
    SOFTWARE_VERSIONS = "software_versions"
    """Versions of server software components."""
    TAG_SERVERS = "tag_servers"
    """Servers using a tag."""
    TAG_LANGUAGES = "tag_languages"
    """Languages of statuses using a tag."""
    INSTANCE_ACCOUNTS = "instance_accounts"
    """Popular accounts from a domain."""
    INSTANCE_LANGUAGES = "instance_languages"
    """Languages of statuses from a domain."""


class RetentionFrequency(StringEnum):
    """Bucket frequency of administrator retention cohorts."""

    DAY = "day"
    """Daily cohorts."""
    MONTH = "month"
    """Monthly cohorts."""


class DomainBlockSeverity(StringEnum):
    """Domain-moderation comparison domain; see :class:`AdminDomainBlockSeverity`
    and :class:`PublicDomainBlockSeverity`.
    """


class AdminDomainBlockSeverity(DomainBlockSeverity):
    """Administrator domain-block action, including no-op blocks.

    See :class:`PublicDomainBlockSeverity` for public responses.
    """

    SILENCE = "silence"
    """Hide users except when followed."""
    SUSPEND = "suspend"
    """Reject incoming messages from the domain."""
    NOOP = "noop"
    """No status action; media or report rejection can still apply."""


class PublicDomainBlockSeverity(DomainBlockSeverity):
    """Publicly reported domain-block action; see :class:`AdminDomainBlockSeverity`."""

    SILENCE = "silence"
    """Hide users except when followed."""
    SUSPEND = "suspend"
    """Reject incoming messages from the domain."""


class IpBlockSeverity(StringEnum):
    """Administrator restriction applied to an IP range."""

    SIGN_UP_REQUIRES_APPROVAL = "sign_up_requires_approval"
    """Signups require approval."""
    SIGN_UP_BLOCK = "sign_up_block"
    """Reject signups."""
    NO_ACCESS = "no_access"
    """Reject all activity."""


class SuggestionReason(StringEnum):
    """Suggestion-reason comparison domain; see :class:`SuggestionSource` and
    :class:`LegacySuggestionSource`.
    """


class SuggestionSource(SuggestionReason):
    """Reasons in the current suggestion sources array.

    See :class:`LegacySuggestionSource` for the deprecated scalar field.
    """

    FEATURED = "featured"
    """Recommended by server staff."""
    MOST_FOLLOWED = "most_followed"
    """Many active local followers."""
    MOST_INTERACTIONS = "most_interactions"
    """Many boosts and favourites recently."""
    SIMILAR_TO_RECENTLY_FOLLOWED = "similar_to_recently_followed"
    """Similar profile to recently followed accounts."""
    FRIENDS_OF_FRIENDS = "friends_of_friends"
    """Followed by accounts the user follows."""


class LegacySuggestionSource(SuggestionReason):
    """Deprecated scalar suggestion reason; see :class:`SuggestionSource`."""

    STAFF = "staff"
    """Recommended by server staff."""
    PAST_INTERACTIONS = "past_interactions"
    """The user previously interacted with the account."""
    GLOBAL = "global"
    """Many recent interactions and active local followers."""


class AccountCreationErrorCode(StringEnum):
    """Machine-readable validation failure while registering an account."""

    ERR_BLOCKED = "ERR_BLOCKED"
    """Email provider is blocked."""
    ERR_UNREACHABLE = "ERR_UNREACHABLE"
    """Email domain has no reachable DNS address."""
    ERR_TAKEN = "ERR_TAKEN"
    """Username or email is already taken."""
    ERR_RESERVED = "ERR_RESERVED"
    """Username is reserved."""
    ERR_ACCEPTED = "ERR_ACCEPTED"
    """Required agreement was not accepted."""
    ERR_BLANK = "ERR_BLANK"
    """Required value is blank."""
    ERR_INVALID = "ERR_INVALID"
    """Value is malformed."""
    ERR_TOO_LONG = "ERR_TOO_LONG"
    """Value is too long."""
    ERR_TOO_SHORT = "ERR_TOO_SHORT"
    """Value is too short."""
    ERR_INCLUSION = "ERR_INCLUSION"
    """Value is not an allowed choice."""


class CredentialAccountErrorCode(StringEnum):
    """Reason why the authenticated account is not functional."""

    PENDING_CONFIRMATION = "pending_confirmation"
    """Email confirmation is pending."""
    PENDING_APPROVAL = "pending_approval"
    """Moderator approval is pending."""
    ACCOUNT_DELETED = "account_deleted"
    """The account was deleted."""
    ACCOUNT_SUSPENDED = "account_suspended"
    """The account was suspended."""
    MEMORIAL = "memorial"
    """The account is a memorial."""
    LOGIN_DISABLED = "login_disabled"
    """Login was disabled."""
    TWO_FACTOR_AUTHENTICATION_REQUIRED = "2fa_required"
    """Two-factor authentication is required."""


class NotificationPolicyAction(StringEnum):
    """Treatment of notifications from an account category."""

    ACCEPT = "accept"
    """Accept notifications."""
    FILTER = "filter"
    """Mark notifications as filtered."""
    DROP = "drop"
    """Do not create notification objects."""


class RelationshipSeveranceType(StringEnum):
    """Cause of a relationship-severance event."""

    DOMAIN_BLOCK = "domain_block"
    """A moderator suspended a domain."""
    USER_DOMAIN_BLOCK = "user_domain_block"
    """The user blocked a domain."""
    ACCOUNT_SUSPENSION = "account_suspension"
    """A moderator suspended an account."""


class ModerationAction(StringEnum):
    """Account-moderation comparison domain; see :class:`AdminAccountAction`
    and :class:`AccountWarningAction`.
    """


class AdminAccountAction(ModerationAction):
    """Action requested by an administrator; see :class:`AccountWarningAction`."""

    NONE = "none"
    """Send a warning without another action."""
    DISABLE = "disable"
    """Disable login."""
    SILENCE = "silence"
    """Limit the account."""
    SUSPEND = "suspend"
    """Suspend the account."""
    SENSITIVE = "sensitive"
    """Mark all posts sensitive."""


class AccountWarningAction(ModerationAction):
    """Action recorded in a moderation warning; see :class:`AdminAccountAction`."""

    NONE = "none"
    """Warning only."""
    DISABLE = "disable"
    """The account was disabled."""
    MARK_STATUSES_AS_SENSITIVE = "mark_statuses_as_sensitive"
    """Specific posts were marked sensitive."""
    DELETE_STATUSES = "delete_statuses"
    """Specific posts were deleted."""
    SENSITIVE = "sensitive"
    """All posts were marked sensitive."""
    SILENCE = "silence"
    """The account was limited."""
    SUSPEND = "suspend"
    """The account was suspended."""


class AppealState(StringEnum):
    """Review state of a moderation appeal."""

    APPROVED = "approved"
    """Approved by a moderator."""
    REJECTED = "rejected"
    """Rejected by a moderator."""
    PENDING = "pending"
    """Awaiting review."""


class AsyncRefreshStatus(StringEnum):
    """Progress of an asynchronous refresh."""

    RUNNING = "running"
    """The background job is still running."""
    FINISHED = "finished"
    """The background job has finished."""


class AnnualReportStatus(StringEnum):
    """Availability of an annual report (the response entity is AnnualReportState)."""

    AVAILABLE = "available"
    """Generated and available."""
    GENERATING = "generating"
    """Currently being generated."""
    ELIGIBLE = "eligible"
    """Can be generated."""
    INELIGIBLE = "ineligible"
    """Cannot be generated."""


class AnnualReportArchetype(StringEnum):
    """Posting archetype shared by annual report schema versions."""

    LURKER = "lurker"
    """Posted, replied, and boosted less than the yearly average."""
    BOOSTER = "booster"
    """Boosted more than twice as often as posting standalone statuses."""
    POLLSTER = "pollster"
    """At least ten percent of standalone statuses contained polls."""
    REPLIER = "replier"
    """Replied more than twice as often as posting standalone statuses."""
    ORACLE = "oracle"
    """Does not match another archetype."""


class OAuthScope(StringEnum):
    """Known Mastodon OAuth scopes, including legacy scopes.

    Prefer granular permissions. Server extensions remain plain strings.
    See https://docs.joinmastodon.org/api/oauth-scopes/.
    """

    READ = "read"
    """Read access, including granular read scopes."""
    WRITE = "write"
    """Write access, including granular write scopes."""
    FOLLOW = "follow"
    """Legacy relationship-management scope."""
    PUSH = "push"
    """Manage push subscriptions."""
    PROFILE = "profile"
    """Read the authenticated user's minimal profile."""
    READ_ACCOUNTS = "read:accounts"
    """Read accounts."""
    READ_BLOCKS = "read:blocks"
    """Read account blocks."""
    READ_BOOKMARKS = "read:bookmarks"
    """Read bookmarks."""
    READ_COLLECTIONS = "read:collections"
    """Read featured collections."""
    READ_FAVOURITES = "read:favourites"
    """Read favourites."""
    READ_FILTERS = "read:filters"
    """Read filters."""
    READ_FOLLOWS = "read:follows"
    """Read follow relationships."""
    READ_LISTS = "read:lists"
    """Read lists."""
    READ_MUTES = "read:mutes"
    """Read mutes."""
    READ_NOTIFICATIONS = "read:notifications"
    """Read notifications."""
    READ_REPORTS = "read:reports"
    """Deprecated, unused report-read scope."""
    READ_SEARCH = "read:search"
    """Search."""
    READ_STATUSES = "read:statuses"
    """Read statuses."""
    WRITE_ACCOUNTS = "write:accounts"
    """Update accounts."""
    WRITE_BLOCKS = "write:blocks"
    """Manage account blocks."""
    WRITE_BOOKMARKS = "write:bookmarks"
    """Manage bookmarks."""
    WRITE_COLLECTIONS = "write:collections"
    """Manage featured collections."""
    WRITE_CONVERSATIONS = "write:conversations"
    """Manage conversations."""
    WRITE_FAVOURITES = "write:favourites"
    """Manage favourites."""
    WRITE_FILTERS = "write:filters"
    """Manage filters."""
    WRITE_FOLLOWS = "write:follows"
    """Manage follow relationships."""
    WRITE_LISTS = "write:lists"
    """Manage lists."""
    WRITE_MEDIA = "write:media"
    """Upload and update media."""
    WRITE_MUTES = "write:mutes"
    """Manage mutes."""
    WRITE_NOTIFICATIONS = "write:notifications"
    """Manage notifications."""
    WRITE_REPORTS = "write:reports"
    """Submit reports."""
    WRITE_STATUSES = "write:statuses"
    """Publish and manage statuses."""
    ADMIN_READ = "admin:read"
    """Read administrator data."""
    ADMIN_READ_ACCOUNTS = "admin:read:accounts"
    """Read administrator account data."""
    ADMIN_READ_REPORTS = "admin:read:reports"
    """Read administrator reports."""
    ADMIN_READ_DOMAIN_ALLOWS = "admin:read:domain_allows"
    """Read domain allows."""
    ADMIN_READ_DOMAIN_BLOCKS = "admin:read:domain_blocks"
    """Read domain blocks."""
    ADMIN_READ_IP_BLOCKS = "admin:read:ip_blocks"
    """Read IP blocks."""
    ADMIN_READ_EMAIL_DOMAIN_BLOCKS = "admin:read:email_domain_blocks"
    """Read email-domain blocks."""
    ADMIN_READ_CANONICAL_EMAIL_BLOCKS = "admin:read:canonical_email_blocks"
    """Read canonical-email blocks."""
    ADMIN_WRITE = "admin:write"
    """Manage administrator data."""
    ADMIN_WRITE_ACCOUNTS = "admin:write:accounts"
    """Manage administrator account data."""
    ADMIN_WRITE_REPORTS = "admin:write:reports"
    """Manage administrator reports."""
    ADMIN_WRITE_DOMAIN_ALLOWS = "admin:write:domain_allows"
    """Manage domain allows."""
    ADMIN_WRITE_DOMAIN_BLOCKS = "admin:write:domain_blocks"
    """Manage domain blocks."""
    ADMIN_WRITE_IP_BLOCKS = "admin:write:ip_blocks"
    """Manage IP blocks."""
    ADMIN_WRITE_EMAIL_DOMAIN_BLOCKS = "admin:write:email_domain_blocks"
    """Manage email-domain blocks."""
    ADMIN_WRITE_CANONICAL_EMAIL_BLOCKS = "admin:write:canonical_email_blocks"
    """Manage canonical-email blocks."""
    CRYPTO = "crypto"
    """Removed experimental encryption scope, present on older servers."""


class OAuthResponseType(StringEnum):
    """OAuth authorization response types advertised by Mastodon."""

    CODE = "code"
    """Return an authorization code."""


class OAuthResponseMode(StringEnum):
    """OAuth authorization response transport."""

    QUERY = "query"
    """URI query parameters."""
    FRAGMENT = "fragment"
    """URI fragment parameters."""
    FORM_POST = "form_post"
    """HTML form POST."""


class OAuthGrantType(StringEnum):
    """OAuth token grants advertised by Mastodon."""

    AUTHORIZATION_CODE = "authorization_code"
    """Exchange an authorization code."""
    CLIENT_CREDENTIALS = "client_credentials"
    """Obtain an application token."""
    PASSWORD = "password"
    """Legacy resource-owner password grant."""


class OAuthTokenEndpointAuthMethod(StringEnum):
    """Authentication methods advertised for the OAuth token endpoint."""

    CLIENT_SECRET_BASIC = "client_secret_basic"
    """HTTP Basic client authentication."""
    CLIENT_SECRET_POST = "client_secret_post"
    """Client credentials in the POST body."""


class OAuthCodeChallengeMethod(StringEnum):
    """PKCE challenge methods advertised by Mastodon."""

    S256 = "S256"
    """Base64url-encoded SHA-256 challenge."""


class FederationProtocol(StringEnum):
    """Federation protocols in the NodeInfo 2.0 schema.

    See https://nodeinfo.diaspora.software/schema.html.
    """

    ACTIVITYPUB = "activitypub"
    """ActivityPub."""
    BUDDYCLOUD = "buddycloud"
    """Buddycloud."""
    DFRN = "dfrn"
    """Distributed Friends and Relations Network."""
    DIASPORA = "diaspora"
    """Diaspora."""
    LIBERTREE = "libertree"
    """Libertree."""
    OSTATUS = "ostatus"
    """OStatus."""
    PUMPIO = "pumpio"
    """pump.io."""
    TENT = "tent"
    """Tent."""
    XMPP = "xmpp"
    """XMPP."""
    ZOT = "zot"
    """Zot."""


class NodeInfoService(StringEnum):
    """NodeInfo service comparison domain; see :class:`NodeInfoInboundService`
    and :class:`NodeInfoOutboundService`.
    """


class NodeInfoInboundService(NodeInfoService):
    """Message sources defined by NodeInfo 2.0; see :class:`NodeInfoOutboundService`."""

    ATOM = "atom1.0"
    """Atom 1.0."""
    GNUSOCIAL = "gnusocial"
    """GNU social."""
    IMAP = "imap"
    """IMAP mail."""
    PNUT = "pnut"
    """pnut.io."""
    POP3 = "pop3"
    """POP3 mail."""
    PUMPIO = "pumpio"
    """pump.io."""
    RSS = "rss2.0"
    """RSS 2.0."""
    TWITTER = "twitter"
    """Twitter."""


class NodeInfoOutboundService(NodeInfoService):
    """Publishing destinations defined by NodeInfo 2.0.

    See :class:`NodeInfoInboundService` for message sources.
    """

    ATOM = "atom1.0"
    """Atom 1.0."""
    BLOGGER = "blogger"
    """Blogger."""
    BUDDYCLOUD = "buddycloud"
    """Buddycloud."""
    DIASPORA = "diaspora"
    """Diaspora."""
    DREAMWIDTH = "dreamwidth"
    """Dreamwidth."""
    DRUPAL = "drupal"
    """Drupal."""
    FACEBOOK = "facebook"
    """Facebook."""
    FRIENDICA = "friendica"
    """Friendica."""
    GNUSOCIAL = "gnusocial"
    """GNU social."""
    GOOGLE = "google"
    """Google."""
    INSANEJOURNAL = "insanejournal"
    """InsaneJournal."""
    LIBERTREE = "libertree"
    """Libertree."""
    LINKEDIN = "linkedin"
    """LinkedIn."""
    LIVEJOURNAL = "livejournal"
    """LiveJournal."""
    MEDIAGOBLIN = "mediagoblin"
    """MediaGoblin."""
    MYSPACE = "myspace"
    """Myspace."""
    PINTEREST = "pinterest"
    """Pinterest."""
    PNUT = "pnut"
    """pnut.io."""
    POSTEROUS = "posterous"
    """Posterous."""
    PUMPIO = "pumpio"
    """pump.io."""
    REDMATRIX = "redmatrix"
    """RedMatrix."""
    RSS = "rss2.0"
    """RSS 2.0."""
    SMTP = "smtp"
    """SMTP mail."""
    TENT = "tent"
    """Tent."""
    TUMBLR = "tumblr"
    """Tumblr."""
    TWITTER = "twitter"
    """Twitter."""
    WORDPRESS = "wordpress"
    """WordPress."""
    XMPP = "xmpp"
    """XMPP."""


class SearchResultType(StringEnum):
    """Search result category."""

    ACCOUNTS = "accounts"
    """Accounts."""
    HASHTAGS = "hashtags"
    """Hashtags."""
    STATUSES = "statuses"
    """Statuses."""
    COLLECTIONS = "collections"
    """Featured collections."""


class AdminAccountOrigin(StringEnum):
    """Origin filter for administrator account searches."""

    LOCAL = "local"
    """Local accounts."""
    REMOTE = "remote"
    """Remote accounts."""


class AdminAccountStatus(StringEnum):
    """Account-state filter for administrator account searches."""

    ACTIVE = "active"
    """Active accounts."""
    PENDING = "pending"
    """Accounts awaiting approval."""
    DISABLED = "disabled"
    """Accounts with login disabled."""
    SILENCED = "silenced"
    """Limited accounts."""
    SUSPENDED = "suspended"
    """Suspended accounts."""


class AdminAccountPermission(StringEnum):
    """Permission filter for administrator account searches."""

    STAFF = "staff"
    """Accounts with staff permissions."""


class NotificationAccountExpansion(StringEnum):
    """Account detail included with grouped notifications."""

    FULL = "full"
    """Full account entities."""
    PARTIAL_AVATARS = "partial_avatars"
    """Partial account entities including avatars."""


class StatusContentType(StringEnum):
    """Known post input formats supported by Mastodon-compatible servers.

    MIME types advertised by a server are extensible; plain strings are accepted.
    """

    PLAIN = "text/plain"
    """Plain text."""
    HTML = "text/html"
    """HTML (server extension)."""
    MARKDOWN = "text/markdown"
    """Markdown (server extension)."""
    BBCODE = "text/bbcode"
    """BBCode (server extension)."""


class RateLimitMethod(StringEnum):
    """Local-library rate limit strategy, not a server API value."""

    THROW = "throw"
    """Raise on rate limits."""
    WAIT = "wait"
    """Wait until the rate limit resets."""
    PACE = "pace"
    """Space requests to avoid exhausting the rate limit."""


class VersionCheckMode(StringEnum):
    """Local-library API version checking strategy."""

    NONE = "none"
    """Disable version checks."""
    CREATED = "created"
    """Check when a method was introduced."""
    CHANGED = "changed"
    """Check when a method was last changed."""


class FeatureSet(StringEnum):
    """Local-library server feature family."""

    MAINLINE = "mainline"
    """Mainline Mastodon."""
    PLEROMA = "pleroma"
    """Pleroma extensions."""
    FEDIBIRD = "fedibird"
    """Fedibird extensions."""


class PaginationDirection(StringEnum):
    """Local-library direction when following pagination links."""

    NEXT = "next"
    """Fetch the next page."""
    PREVIOUS = "previous"
    """Fetch the previous page."""


class Timeline(StringEnum):
    """Common timeline selector; dynamic tag/list/link selectors remain strings.

    See :class:`MarkerTimeline` for stored reading-position keys.
    """

    HOME = "home"
    """The authenticated user's home timeline."""
    LOCAL = "local"
    """Public statuses originating locally."""
    PUBLIC = "public"
    """Public statuses from all servers."""


class MarkerTimeline(StringEnum):
    """Timelines with stored reading positions; see :class:`Timeline`."""

    HOME = "home"
    """Home timeline."""
    NOTIFICATIONS = "notifications"
    """Notifications."""


class TimelineAccessType(StringEnum):
    """Feed selector for timeline access checks; see :class:`TimelineAccess`."""

    PUBLIC = "public"
    """Live public feed."""
    HASHTAG = "hashtag"
    """Hashtag feed."""
    TRENDING_LINKS = "trending_links"
    """Trending link feed."""


class DirectoryOrder(StringEnum):
    """Ordering of the profile directory."""

    ACTIVE = "active"
    """Most recently active accounts first."""
    NEW = "new"
    """Most recently registered accounts first."""


class NodeinfoSchema(StringEnum):
    """NodeInfo discovery schema relation URIs, not document version strings.

    See https://nodeinfo.diaspora.software/schema.html.
    """

    V1_0 = "http://nodeinfo.diaspora.software/ns/schema/1.0"
    """NodeInfo 1.0."""
    V1_1 = "http://nodeinfo.diaspora.software/ns/schema/1.1"
    """NodeInfo 1.1."""
    V2_0 = "http://nodeinfo.diaspora.software/ns/schema/2.0"
    """NodeInfo 2.0."""
    V2_1 = "http://nodeinfo.diaspora.software/ns/schema/2.1"
    """NodeInfo 2.1."""


class NodeinfoVersion(StringEnum):
    """Version in a NodeInfo document; see :class:`NodeinfoSchema` for discovery URIs."""

    V1_0 = "1.0"
    """NodeInfo 1.0."""
    V1_1 = "1.1"
    """NodeInfo 1.1."""
    V2_0 = "2.0"
    """NodeInfo 2.0."""
    V2_1 = "2.1"
    """NodeInfo 2.1."""


class StreamEventType(StringEnum):
    """Event names delivered to streaming listeners, including legacy events."""

    UPDATE = "update"
    """A new status."""
    NOTIFICATION = "notification"
    """A new notification."""
    DELETE = "delete"
    """A status was deleted."""
    FILTERS_CHANGED = "filters_changed"
    """The user's filters changed."""
    CONVERSATION = "conversation"
    """A direct conversation changed."""
    ANNOUNCEMENT = "announcement"
    """An announcement was created or updated."""
    ANNOUNCEMENT_REACTION = "announcement.reaction"
    """An announcement's reactions changed."""
    ANNOUNCEMENT_REACTION_LEGACY = "announcement_reaction"
    """Legacy underscore spelling of an announcement reaction event."""
    ANNOUNCEMENT_DELETE = "announcement.delete"
    """An announcement was deleted."""
    ANNOUNCEMENT_DELETE_LEGACY = "announcement_delete"
    """Legacy underscore spelling of an announcement deletion event."""
    STATUS_UPDATE = "status.update"
    """A status was edited."""
    STATUS_UPDATE_LEGACY = "status_update"
    """Legacy underscore spelling of a status edit event."""
    ENCRYPTED_MESSAGE = "encrypted_message"
    """A legacy experimental encrypted message."""
    NOTIFICATIONS_MERGED = "notifications_merged"
    """Notification groups were merged."""


class StreamType(StringEnum):
    """WebSocket subscription channel; tag and list identifiers are separate parameters."""

    USER = "user"
    """The user's home timeline and notifications."""
    USER_NOTIFICATION = "user:notification"
    """Only the user's notifications."""
    PUBLIC = "public"
    """All public statuses."""
    PUBLIC_MEDIA = "public:media"
    """Public statuses with media."""
    PUBLIC_LOCAL = "public:local"
    """Local public statuses."""
    PUBLIC_LOCAL_MEDIA = "public:local:media"
    """Local public statuses with media."""
    PUBLIC_REMOTE = "public:remote"
    """Remote public statuses."""
    PUBLIC_REMOTE_MEDIA = "public:remote:media"
    """Remote public statuses with media."""
    HASHTAG = "hashtag"
    """Public statuses containing a selected hashtag."""
    HASHTAG_LOCAL = "hashtag:local"
    """Local public statuses containing a selected hashtag."""
    LIST = "list"
    """Statuses in a selected user list."""
    DIRECT = "direct"
    """Direct conversations."""


class Language(StringEnum):
    """All 184 ISO 639-1 two-letter language codes, with English names.

    Standard: https://www.loc.gov/standards/iso639-2/php/code_list.php

    ISO 639-3 codes (such as ``und``), regional tags (such as ``pt-BR``), and
    server-specific language identifiers remain accepted as ordinary strings.
    Member names use the uppercase code rather than a potentially ambiguous
    English language name.
    """

    AA = "aa"
    """Afar."""
    AB = "ab"
    """Abkhazian."""
    AE = "ae"
    """Avestan."""
    AF = "af"
    """Afrikaans."""
    AK = "ak"
    """Akan."""
    AM = "am"
    """Amharic."""
    AN = "an"
    """Aragonese."""
    AR = "ar"
    """Arabic."""
    AS = "as"
    """Assamese."""
    AV = "av"
    """Avaric."""
    AY = "ay"
    """Aymara."""
    AZ = "az"
    """Azerbaijani."""
    BA = "ba"
    """Bashkir."""
    BE = "be"
    """Belarusian."""
    BG = "bg"
    """Bulgarian."""
    BH = "bh"
    """Bihari languages."""
    BI = "bi"
    """Bislama."""
    BM = "bm"
    """Bambara."""
    BN = "bn"
    """Bengali."""
    BO = "bo"
    """Tibetan."""
    BR = "br"
    """Breton."""
    BS = "bs"
    """Bosnian."""
    CA = "ca"
    """Catalan; Valencian."""
    CE = "ce"
    """Chechen."""
    CH = "ch"
    """Chamorro."""
    CO = "co"
    """Corsican."""
    CR = "cr"
    """Cree."""
    CS = "cs"
    """Czech."""
    CU = "cu"
    """Church Slavic; Old Slavonic."""
    CV = "cv"
    """Chuvash."""
    CY = "cy"
    """Welsh."""
    DA = "da"
    """Danish."""
    DE = "de"
    """German."""
    DV = "dv"
    """Divehi; Dhivehi; Maldivian."""
    DZ = "dz"
    """Dzongkha."""
    EE = "ee"
    """Ewe."""
    EL = "el"
    """Greek, Modern (1453-)."""
    EN = "en"
    """English."""
    EO = "eo"
    """Esperanto."""
    ES = "es"
    """Spanish; Castilian."""
    ET = "et"
    """Estonian."""
    EU = "eu"
    """Basque."""
    FA = "fa"
    """Persian."""
    FF = "ff"
    """Fulah."""
    FI = "fi"
    """Finnish."""
    FJ = "fj"
    """Fijian."""
    FO = "fo"
    """Faroese."""
    FR = "fr"
    """French."""
    FY = "fy"
    """Western Frisian."""
    GA = "ga"
    """Irish."""
    GD = "gd"
    """Gaelic; Scottish Gaelic."""
    GL = "gl"
    """Galician."""
    GN = "gn"
    """Guarani."""
    GU = "gu"
    """Gujarati."""
    GV = "gv"
    """Manx."""
    HA = "ha"
    """Hausa."""
    HE = "he"
    """Hebrew."""
    HI = "hi"
    """Hindi."""
    HO = "ho"
    """Hiri Motu."""
    HR = "hr"
    """Croatian."""
    HT = "ht"
    """Haitian; Haitian Creole."""
    HU = "hu"
    """Hungarian."""
    HY = "hy"
    """Armenian."""
    HZ = "hz"
    """Herero."""
    IA = "ia"
    """Interlingua (International Auxiliary Language Association)."""
    ID = "id"
    """Indonesian."""
    IE = "ie"
    """Interlingue; Occidental."""
    IG = "ig"
    """Igbo."""
    II = "ii"
    """Sichuan Yi; Nuosu."""
    IK = "ik"
    """Inupiaq."""
    IO = "io"
    """Ido."""
    IS = "is"
    """Icelandic."""
    IT = "it"
    """Italian."""
    IU = "iu"
    """Inuktitut."""
    JA = "ja"
    """Japanese."""
    JV = "jv"
    """Javanese."""
    KA = "ka"
    """Georgian."""
    KG = "kg"
    """Kongo."""
    KI = "ki"
    """Kikuyu; Gikuyu."""
    KJ = "kj"
    """Kuanyama; Kwanyama."""
    KK = "kk"
    """Kazakh."""
    KL = "kl"
    """Kalaallisut; Greenlandic."""
    KM = "km"
    """Central Khmer."""
    KN = "kn"
    """Kannada."""
    KO = "ko"
    """Korean."""
    KR = "kr"
    """Kanuri."""
    KS = "ks"
    """Kashmiri."""
    KU = "ku"
    """Kurdish."""
    KV = "kv"
    """Komi."""
    KW = "kw"
    """Cornish."""
    KY = "ky"
    """Kirghiz; Kyrgyz."""
    LA = "la"
    """Latin."""
    LB = "lb"
    """Luxembourgish; Letzeburgesch."""
    LG = "lg"
    """Ganda."""
    LI = "li"
    """Limburgan; Limburger; Limburgish."""
    LN = "ln"
    """Lingala."""
    LO = "lo"
    """Lao."""
    LT = "lt"
    """Lithuanian."""
    LU = "lu"
    """Luba-Katanga."""
    LV = "lv"
    """Latvian."""
    MG = "mg"
    """Malagasy."""
    MH = "mh"
    """Marshallese."""
    MI = "mi"
    """Maori."""
    MK = "mk"
    """Macedonian."""
    ML = "ml"
    """Malayalam."""
    MN = "mn"
    """Mongolian."""
    MR = "mr"
    """Marathi."""
    MS = "ms"
    """Malay."""
    MT = "mt"
    """Maltese."""
    MY = "my"
    """Burmese."""
    NA = "na"
    """Nauru."""
    NB = "nb"
    """Bokmal, Norwegian."""
    ND = "nd"
    """Ndebele, North."""
    NE = "ne"
    """Nepali."""
    NG = "ng"
    """Ndonga."""
    NL = "nl"
    """Dutch; Flemish."""
    NN = "nn"
    """Norwegian Nynorsk."""
    NO = "no"
    """Norwegian."""
    NR = "nr"
    """Ndebele, South."""
    NV = "nv"
    """Navajo; Navaho."""
    NY = "ny"
    """Chichewa; Chewa; Nyanja."""
    OC = "oc"
    """Occitan (post 1500)."""
    OJ = "oj"
    """Ojibwa."""
    OM = "om"
    """Oromo."""
    OR = "or"
    """Oriya; Odia."""
    OS = "os"
    """Ossetian; Ossetic."""
    PA = "pa"
    """Panjabi; Punjabi."""
    PI = "pi"
    """Pali."""
    PL = "pl"
    """Polish."""
    PS = "ps"
    """Pushto; Pashto."""
    PT = "pt"
    """Portuguese."""
    QU = "qu"
    """Quechua."""
    RM = "rm"
    """Romansh."""
    RN = "rn"
    """Rundi."""
    RO = "ro"
    """Romanian; Moldavian; Moldovan."""
    RU = "ru"
    """Russian."""
    RW = "rw"
    """Kinyarwanda."""
    SA = "sa"
    """Sanskrit."""
    SC = "sc"
    """Sardinian."""
    SD = "sd"
    """Sindhi."""
    SE = "se"
    """Northern Sami."""
    SG = "sg"
    """Sango."""
    SI = "si"
    """Sinhala; Sinhalese."""
    SK = "sk"
    """Slovak."""
    SL = "sl"
    """Slovenian."""
    SM = "sm"
    """Samoan."""
    SN = "sn"
    """Shona."""
    SO = "so"
    """Somali."""
    SQ = "sq"
    """Albanian."""
    SR = "sr"
    """Serbian."""
    SS = "ss"
    """Swati."""
    ST = "st"
    """Sotho, Southern."""
    SU = "su"
    """Sundanese."""
    SV = "sv"
    """Swedish."""
    SW = "sw"
    """Swahili."""
    TA = "ta"
    """Tamil."""
    TE = "te"
    """Telugu."""
    TG = "tg"
    """Tajik."""
    TH = "th"
    """Thai."""
    TI = "ti"
    """Tigrinya."""
    TK = "tk"
    """Turkmen."""
    TL = "tl"
    """Tagalog."""
    TN = "tn"
    """Tswana."""
    TO = "to"
    """Tonga (Tonga Islands)."""
    TR = "tr"
    """Turkish."""
    TS = "ts"
    """Tsonga."""
    TT = "tt"
    """Tatar."""
    TW = "tw"
    """Twi."""
    TY = "ty"
    """Tahitian."""
    UG = "ug"
    """Uighur; Uyghur."""
    UK = "uk"
    """Ukrainian."""
    UR = "ur"
    """Urdu."""
    UZ = "uz"
    """Uzbek."""
    VE = "ve"
    """Venda."""
    VI = "vi"
    """Vietnamese."""
    VO = "vo"
    """Volapuk."""
    WA = "wa"
    """Walloon."""
    WO = "wo"
    """Wolof."""
    XH = "xh"
    """Xhosa."""
    YI = "yi"
    """Yiddish."""
    YO = "yo"
    """Yoruba."""
    ZA = "za"
    """Zhuang; Chuang."""
    ZH = "zh"
    """Chinese."""
    ZU = "zu"
    """Zulu."""


__all__ = [
    "StringEnum", "Visibility", "PostVisibility", "StatusVisibility",
    "DefaultPostVisibility", "ReblogVisibility", "QuotePolicy", "PostQuotePolicy",
    "DefaultQuotePolicy", "QuoteState", "ApprovalAudience", "QuoteApprovalAudience",
    "FeatureApprovalAudience", "ApprovalDecision", "QuoteApprovalDecision",
    "FeatureApprovalDecision", "FilterContext", "FilterAction", "NotificationType",
    "IndividualNotificationType", "GroupedNotificationType", "PushNotificationType",
    "GroupableNotificationType", "ListRepliesPolicy", "MediaAttachmentType",
    "PreviewCardType", "CollectionItemState", "TimelineAccess", "ReportCategory",
    "PushSubscriptionPolicy", "MediaExpansion", "AdminMeasureKey", "AdminDimensionKey",
    "RetentionFrequency", "DomainBlockSeverity", "AdminDomainBlockSeverity",
    "PublicDomainBlockSeverity", "IpBlockSeverity", "SuggestionReason",
    "SuggestionSource", "LegacySuggestionSource", "AccountCreationErrorCode",
    "CredentialAccountErrorCode", "NotificationPolicyAction", "RelationshipSeveranceType",
    "ModerationAction", "AdminAccountAction", "AccountWarningAction", "AppealState",
    "AsyncRefreshStatus", "AnnualReportStatus", "AnnualReportArchetype", "OAuthScope",
    "OAuthResponseType", "OAuthResponseMode", "OAuthGrantType",
    "OAuthTokenEndpointAuthMethod", "OAuthCodeChallengeMethod", "FederationProtocol",
    "NodeInfoService", "NodeInfoInboundService", "NodeInfoOutboundService",
    "SearchResultType", "AdminAccountOrigin", "AdminAccountStatus",
    "AdminAccountPermission", "NotificationAccountExpansion", "StatusContentType",
    "RateLimitMethod", "VersionCheckMode", "FeatureSet", "PaginationDirection",
    "Timeline", "MarkerTimeline", "TimelineAccessType", "DirectoryOrder",
    "NodeinfoSchema", "NodeinfoVersion", "StreamEventType", "StreamType", "Language",
]
