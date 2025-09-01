A note on versioning: This librarys major version will grow with the APIs 
version number. Breaking changes will be indicated by a change in the minor
(or major) version number, and will generally be avoided.  

v2.1.3
-------
* Fix the library throwing a deprecation warning during some internal operations due to the v1 version of the instance API being deprecated, add a fallback to the v1 API in case Mastodon actually removes the v1 endpoint in the future. (Thanks @andrew-codechimp
for the report)
* Fix "Everything" page in the docs

v2.1.2
-------
* Fix broken login when instance_v2 is present but has no api_versions attribute, such as on e.g. GoToSocial. (Thank you @bfordham for the report and fix!)

v2.1.1
------
* Fixed return type and docs for `account_set_note`.
* Improved documentation in various places.
* Added missing type annotations in `utility.py`.

v2.1.0
------
* Bumped support level to 4.4.3
* Fixed to_json breaking on python 3.14 (Thanks @limburgher for the report)
* Replaced pytest-vcr (deprecated) with pytest-recording (Thanks @CyberTailor)
* Improved timeline documentation (Thanks @adamse)
* Improved docs for stream_healthy (thanks @codl)
* Add offset parameter to trending_tags and trending_links (Thanks @ghost)
* Added support for retrieving API version and a warning for if it is not present despite the mastodon version suggesting it should be.
* Added support for retrieving OAuth authorization server info
* Added check for supported password grant type based on authorization server info (Thanks @thisismissem for the suggestion)
* Added support for alternate OAuth URLs based on the authorization server info
* Added pagination iteraton via `pagination_iterator` (Thanks @FredericoCeratto for the suggestion)
* Added a way to get pagination info out of lists that is slightly less digging-around-in-internals via `get_pagination_info` (Thanks @s427 for the inciting report)
* Added missing `replies_policy` and `exclusive` parameters to list creation and update methods.
* Add status length counter `get_status_length` (Thanks @yuletide for the suggestion and @cheeaun for the assistance)
* Fix `notifications` returning nonsense when passing a single `id` (Thanks @chinchalinchin for the report)
* Fix `moved` accidentally being named `moved_to_account` (Thanks @unusualevent for the report)
* Added a warning for deprecated endpoints if the "deprecation" header is present
* Added `oauth_userinfo` endpoint.
* Added `delete_media` parameter to `status_delete`.
* Added `standard` parameter to `push_subscription_set`.
* Added `attribution_domains` parameter to `account_update_credentials`.
* Added `date_of_birth` parameter to `create_account`.
* Added `account_endorse` and `account_unendorse` methods (replacing "pin" methods)
* Added `tag_feature` and `tag_unfeature` methods (replacing previous featured tag api)
* Added `instance_terms_of_service` method.

v2.0.1
------
Maintenance release. Fixes a few minor, but important, issues

* Remove spurious debug prints (Thanks aitorres)
* Fix pagination fetch_remaining being broken due to typing changes (Thanks jikamens)
* Fix pagination result parsing due to typing changes (Thanks hashier for the report)
* Fix pagination information not being saved with to/from_json functions

v2.0.0
------
* Absolutely massive rework of entities and typing. There are now proper classes for all entities, and typing is now used throughout the library. There is an attempt here to be backwards compatible, and none of my *tests* break.
* Documentation fixes based on the new entities and typing.
* Added information that streaming API access is now auth mandatory (Thanks @leahoswald)
* Removed six dependency, since we don't care about 2.x anymore (Thanks @a-detiste)
* Support level is now 4.3.0
* Note that logging in with passwords is deprecated and to be removed in 4.4.0
* Clarify the use of `code`  (Thanks @lasseedfast)
* Improved docstring for visibility (Thanks @ashwinvis)
* Added `offset` parameter to `trending_statuses` (Thanks @Teqed)
* We're now using space age technology (pyproject.toml - thanks @codl)
* Add py.typed marker (Thanks @ZeeD for the suggestion)
* Added CITATION.cff (Thanks @hauschke for the suggestion)
* Fixed a potential issue with modification to locals (Thanks Konano)
* Added support for 4.3.0 `accounts` endpoint (Thanks AlexKalopsia)
* Fix version parsing for GoToSocial (Thanks gmemstr)
* Updated docs to reflect the fact that startign with 4.4.0, the password grant type is no longer supported.
* Added support for following tags (`followed_tags`, `tag_follow`, `tag_unfollow`, `tag`)
* Fix library not working with -O2 (Thanks mirabilos for the report)
* Version check mode now defaults to "none", since it keeps causing more problems than it solves.
* Document `media` (Thanks LunarLambda for the report)
* Added json serialization and deserialization for returned entities
* Added missing event types and a catch-all event for streaming API
* Add v1 and v2 variants for `instance`
* Add canonical domain block support (`admin_canonical_email_blocks`, `admin_canonical_email_block`, `admin_canonical_email_block_create`, `admin_canonical_email_block_delete`)
* Add trending link timeline (`timeline_link`)
* Update suggestions endpoint and return value
* Add with_suspended parameter to account_relationships
* Add forward_to_domains parameter to reports
* Add `account_delete_avatar` and `account_delete_header`
* Add `statuses` method to retrieve multiple statuses at once
* Add automatic conversion of datetime objects to flake IDs for min/max/since_id fields where appropriate
* Add `notifications_unread_count`
* Add media attachment editing
* Add email domain blocking support (`admin_email_domain_blocks`, `admin_email_domain_block`, `admin_email_domain_block_create`, `admin_email_domain_block_delete`)
* Add `instance_extended_description`
* Add `instance_translation_languages`, translation support (`status_translate`)
* Add trend admin functions (`admin_trending_tags`, `admin_trending_statuses`, `admin_trending_links`, `admin_approve_trending_link`, `admin_reject_trending_link`, `admin_approve_trending_status`, `admin_reject_trending_status`, `admin_approve_trending_tag`, `admin_reject_trending_tag`)
* Add admin IP block functions (`admin_ip_blocks`, `admin_ip_block`, `admin_ip_block_create`, `admin_ip_block_delete`)
* Add `instance_domain_blocks`
* Add notification policy and requests (`notifications_policy`, `update_notifications_policy`, `notifications_requests`, `notification_request`, `accept_notification_request`, `reject_notification_request`, `notifications_merged`, `accept_multiple_notification_requests`, `dismiss_multiple_notification_requests`)
* Add `instance_languages`
* Add notification grouping (`grouped_notifications`, `grouped_notification`, `dismiss_grouped_notification`, `grouped_notification_accounts`, `unread_grouped_notifications_count`)
* Add v2 filer API (`filters_v2`, `filter_v2`, `create_filter_v2`, `update_filter_v2`, `delete_filter_v2`, `filter_keywords_v2`, `add_filter_keyword_v2`, `delete_filter_keyword_v2`, `filter_statuses_v2`, `add_filter_status_v2`, `filter_status_v2`, `delete_filter_status_v2`)

v1.8.1
------
* Replace some lambdas with list comprenehsions (thanks eumiro)
* Add `resolve` keyword to `account_search` (thanks zevaryx)
* Add support for user agent header in `create_app` (thanks jkawamoto)
* Update tox.ini for newer versions (thanks jkawamoto)
* Various doc and argument check fixes (thanks cnotin, codl, alexmshepherd, RedactedCode)
* Fix magic not working on windows (thanks xloem)
* Add readme to PyPi page (thanks hugovk)
* Fix `list_accounts` to actually include request parameters (thanks leoncowle)
* Small formatting changes (thanks amaargiru)
* Add link to examples to docs and readme.
* Add `local` and `remote` parameter to `stream_public` (thank you for the report jeafreezy)
* Fix `limit` and `lang` parameters on trend related functions not present or working (thanks for the report pdeitel)
* Fix some issues with stream reconnect handling (thanks for the report ianh)
* Added an example for how to receive webpush notifications (thanks JesseWeinstein)
* Replaced `follows` with a backwards compatibility stub.
* Added pagination parameters to `admin_domain_blocks` (thanks for the report defnull)

v1.8.0
------
* Overall: Support level is now 3.5.5 (last before 4.0.0)
* BREAKING CHANGE: Switch the base URL to None, throw an error when no base url is passed. Having mastosoc as default was sensible when there were only three mastodon servers. It is not sensible now and trips people up constantly.
* GENERAL WARNING: Currently, Mastodon.py does not support the "new" filter system. In the future, it will, and it will respect filters by default (i.e. remove filtered posts).
* Fixed an issue with the fix for the Pleroma date bug (thanks adbenitez)
* Added trending APIs (`trending_tags`, `trending_statuses`, `trending_links`, `admin_trending_tags`, `admin_trending_statuses`, `admin_trending_links`)
* Added `lang` parameter and document what it does properly.
* Added `category` and `rule_ids` to `reports`
* Made the documentation a bit neater (thanks dieseltravis)
* Added the domain blocking admin API (`admin_domain_blocks`, `admin_domain_block`, `admin_update_domain_block`, `admin_delete_domain_block` - thanks catgoat)
* Added the stats admin APIs (`admin_measures`, `admin_dimensions`, `admin_retention`)
* Added client auth data to access token file.
* Added `account_familiar_followers` API
* Added `account_remove_from_followers` API
* Added `admin_accounts_v2` API
* FUTURE BREAKING CHANGE WARNING: For now, `admin_accounts` still calls v1, but this may change in the future. You are encouraged to use v2 instead.
* Made the version comparisons a bit nicer (thanks eumiro)
* Switch to more recent modules for datetime and timezone stuff (thanks eumiro)
* Made the documentation a bit more consistent (thanks dieseltravis)
* Substantially restructured the documentation, making it a lot nicer to read
* Substantially restructured the code, making it hopefully a lot easier to maintain
    * This SHOULD NOT break anything. If this breaks your code, please let me know.
* This too isn't really a changelog entry but in the same vein as the last post, thank you Claire and Gargron for clarifying many things about the API when asked.

v1.7.0
------
* Cleaned code up a bit (thanks eumiro)
* Fixed some Pleroma related issues (thanks aveao, taraletti, adbenitez)
* Added post editing (`status_update`, `status_source`, `status_history`)
* Added missing streaming events
* Added missing parameters on directory endpoint (thanks heharkon)
* This isn't somehing I changed but thank you a / triggerofsol for answering Many questions I had about specifics of what the API does that are not documented
* Fixed search ignoring `exclude_unreviewed` (Thanks acidghost)
* Added support for using pathlib paths when loading media files (Thanks reagle)
* Removed blocklist with long dead instances
* Added `types` parameter to notifications.
* Documented additional notification types
* Made version parsing more robust against varions things that Mastodon-compatible APIs might throw at it.
* TECHNICALLY BREAKING CHANGE, but I would be quite surprised if this actually breaks anyone: Date parsing will now, when the date string is empty, return Jan. 1st, 1970 instead. This is to work around what I assume is a bug in Pleroma.

v1.6.3
------
* Add server rules API (`instance_rules`)
* Add confirmation email resend API (`email_resend_confirmation`)
* Add account lookup API (`account_lookup`)
* Add `policy` param to control notification sources for `push_subscription_set`
* Add ability to get detailed signup error to `create_account`
* Fix version check for limited federation instances (Thanks to ulysseus-eu for the report)

v1.6.2
------
* Fix some issues with datetime conversion (thanks to various people for reporting it)

v1.6.1
------
* BREAKING CHANGE: Change behaviour of streaming api handlers to no longer raise an exception when an unknown event is received and change the contract of the unknown event handler to explicitly state that it will not receive events once Mastodon.py updates.
* 3.1.3 support
    * Added v2 media_post api
* 3.1.4 support
    * Added "remote", "local" and "only_media" parameter for timelines more broadly
    * Documented updates to instance information api return value
* 3.2.0 support
    * Added account notes API
    * Added thumbnail support to media_post / media_update
    * Documented new keys in media API
* 3.3.0 support
    * Added "notify" parameter for following.
    * Added support for timed mutes
    * Added support for getting an accounts features tags via account_featured_tags
* Miscelaneous additions
    * Added support for paginating by date via converting dates to snowflake IDs (on Mastodon only - thanks to edent for the suggestion)
    * Added a method to revoke oauth tokens (thanks fluffy-critter)
* Fixes
    * Various small and big fixes, improving reliablity and test coverage
    * Changed health APIs to work with newer Mastodon versions
    * Changed URLs from "tootsuite" to "mastodon" in several places (thanks andypiper)
    * Fixed some fields not converting to datetimes (thanks SouthFox-D)
    * Improved oauth web flow support
    * Improved documentation consistency (thanks andypiper)

v1.5.2
------
* BREAKING CHANGE (but to a representation that was intended to be internal): Greatly improve how pagination info is stored (arittner)
* Added "unknown event" handler for streaming (arittner)
* Added support for exclude_types in notifications api (MicroCheapFx)
* Added pagination to bookmarks (arittner)
* Made connecting for streaming more resilient (arittner)
* Allowed specifying a user agent header (arittner)
* Addeded support for tagged and exclude_reblogs on account_statuses api (arittner)
* Added support for reports without attached statuses (arittner)
* General fixes
    * Fixed a typo in __json_fruefalse_parse (zen-tools)
* Some non-mastodon related fixes
    * Fixed a typo in error message for content_type (rinpatch
    * Added support for specifying file name when uploading (animeavi)
    * Fixed several crashes related to gotosocials version string (fwaggle)
    * Fixed an issue related to hometowns version string

v1.5.1
------
* 3.1 support
    * Added `discoverable` parameter to account_update_credentials (Thanks gdunstone)
    * Added new notification type "follow_request"
    * Added bookmarks support: 
        * New functions: `status_bookmark`, `status_unbookmark`, `bookmarks`
        * New fine-grained oauth scopes: read:bookmarks and write:bookmarks.
    * Added announcement support
        * New functions: `announcements`, `announcement_dismiss`
    * Added announcement reaction support
        * New functions: `announcement_reaction_create`, `announcement_reaction_delete`
* Fixed missing notification type "poll" in push notification API and documentation.´
* Fixed a token loading bug
* Fix header upload in account_update_credentials (Thanks gdunstone)
* Commented blocklist code (Thanks marnanel for the report)
* Added fallback for when magic is not available (Thanks limburgher)
* Added missing "mentions_only" parameter to notifications (Thanks adbenitez for the report)
* Moved "content_type" parameter into "pleroma" feature set. This is a breaking change.

v1.5.0
------
* BREAKING CHANGE: the search_v1 API is now gone from Mastodon, Mastodon.py will still let you use it where available / use it where needed if you call search()
* Support for new 3.0.0 features
    * Added profile directory API: directory()
    * Added featured and suggested tags API: featured_tags(), featured_tag_suggestions(), featured_tag_create(), featured_tag_delete() (Thanks Gargron for the advice)
    * Added read-markers API: markers_get(), markers_set()
    * Re-added trends API: trends()
    * Added health api: instance_health()
    * Added nodeinfo support: instance_nodeinfo()
    * Added new parameters to search (exclude_unreviewed) and create_account (reason)
* Added ability to persist base URLs together with access token and client id / secret files
* Documented that status_card endpoint has been removed, switched to alternate method of retrieving cards if function is still used
* Added blurhash as a core dependency, since it is now licensed permissively again
* Added me() function as synonym for account_verify_credentials() to lessen confusion
* Fixed notification-dismiss to use new API endpoint where the old one is not available (Thanks kensanata)
* Fixed status_reply to match status_post
* Add basic support for non-mainline features via the feature_set parameter
    * Added support for fedibirds quote_id parameter in status_post
* Future-proofed webpush cryptography api while trying to remain very backwards compatible so that it can hopefully in the future become part of the core
* Clarified and updated the documentation and improved the tests in various ways

v1.4.6
------
* Fix documentation for list_accounts()
* Add note about block lists to documentation
* Add note that 2.7 support is being sunset

v1.4.5
------
* Small fix to be friendlier to hosted apps

v1.4.4
------
* Added support for moderation API (Thanks Gargron for the clarifications and dotUser for helping with testing)
* Made status_delete return the deleted status (With "source" attribute)
* Added account_id parameter to notifications
* Added streaming_health
* Added support for local hashtag streams
* Made blurhash an optional dependency (Thanks limburgher)
* Fixed some things related to error handling (Thanks lefherz)
* Fixed various small documentation issues (Thanks lefherz)

v1.4.3
------
* BREAKING BUT ONLY FOR YOUR DEPLOY, POTENTIALLY: http_ece and cryptography are now optional dependencies, if you need full webpush crypto support add the "webpush" feature to your Mastodon.py requirements or require one or both manually in your own setup.py.
* Fixed a bug in create_account (Thanks csmall for the report)
* Allowed and documented non-authenticated access to streaming API (Thanks webwurst)
* Fixed MastodonServerError not being exported (Thanks lefherz)
* Fixed various small documentation issues (Thanks julianaito)

v1.4.2
------
* Fixed date parsing in hashtag dicts.

v1.4.1
------
* Fixed search not working on Mastodon versions before 2.8.0. search now dynamically selects search_v1 or search_v2 and adjusts valid parameters depending on the detected Mastodon version.
* Added blurhash decoding.

v1.4.0
------
There are some breaking changes in this release, though less than you might think, considering
this goes all the way from version 2.4.3 to 2.8.0.

* BREAKING CHANGE: Changed streaming API behaviour to make the initial connection asynchronous (Thanks to Shura0 for the detailed report)
    * Old behaviour: The initial connection could fail, the stream functions would then throw an exception.
    * New behaviour: The initial connection function just returns immediately. If there is a connection error, the listeners on_abort handler is called to inform the user and the connection is retried.
* BREAKING CHANGE: search() now calls through to search_v2. The old behaviour is available as search_v1.
* Added support for polls (Added in 2.8.0)
* Added support for preferences API (Added in 2.8.0)
* Added support for the boost visibility parameter (Added in 2.8.0)
* Added support for type, limit, offset, min_id, max_id, account_id on the search API (Added in 2.8.0)
* Added support for scheduled statuses (Added in 2.7.0)
* Added support for account creation via the API (Thanks gargron for clarifying many things here and in other places. Added in 2.7.0)
* Added support for conversation streaming / stream_direct (Added in 2.6.0)
* Added support for conversations (Added in 2.6.0)
* Added support for report forwarding (Added in 2.5.0)
* Added support for multiple OAuth redirect URIs and forcing the user to re-login in OAuth flows.
* Added support for app_verify_credentials endpoint (Added in 2.7.2).
* Added support for min_id based backwards pagination (Added in 2.6.0). The old method is still supported for older installs.
* Added support for account pins / endorsements (Added in 2.5.0).
* Updated documentation for changes to entities.
* Added the ability to access non-authenticated endpoints with no app credentials (Thanks to cerisara for the report and codl).
* Fixed the streaming API not working with gzip encoding (Thanks to bitleks for the report).
* Added more explicitly caught error classes (Thanks to lefherz).
* Improved Pleroma support including content-type and pagination fixes (Thanks to jfmcbrayer for the report and codl).
* Added better session support (Thanks to jrabbit).
* Fixed dependencies (Thanks to jrabbit).
* Fixed variousmime type issues (Thanks to errbufferoverfl and jfmcbrayer).
* Improved the example code (Thanks to MarkEEaton).
* Fixed various small documentation issues (Thanks to allo-).

v1.3.1
------
* Mastodon v2.4.3 compatibility:
   * Keyword filter support: filters(), filter(), filters_apply(), filter_create(), filter_update(), filter_delete()
   * Follow suggestions support: suggestions(), suggestion_delete()
   * account_follow() now has "reblogs" parameter
   * account_mute() now has "notifications" parameter
   * Support for granular scopes
* Added status_reply() convenience function
* First attempt at basic Pleroma compatibility (Thanks deeunderscore)
* Several small fixes

v1.3.0
------
!!!!! There are several potentially breaking changes in here, and a lot
of things changed, since this release covers two Mastodon versions and 
then some !!!!!

* Several small bug fixes (Thanks goldensuneur, bowlercaptain, joyeusenoelle)
* Improved stream error handling (thanks @codl)
* Improvements to streaming:
    * Added on_abort() handler to streams
    * Added automatic reconnecting
    * POTENTIALLY BREAKING CHANGE: Added better error catching to make sure 
      streaming functions do not just crash
* Mastodon v2.3 compatibility (sorry for the late release)
    * only_media parameter in timeline functions 
    * focus support for media_upload()
    * Added media_update()
* Mastodon v2.4 compatibility
    * Added fields to account_update_credentials()
    * WebPush support:
        * Added push_subscription(), push_subscription_set(), push_subscription_update(),
          push_subscription_delete()
        * Added webpush crypto utilities: push_subscription_generate_keys(), 
          push_subscription_decrypt_push()
* Added support for pinned toots, an oversight from 2.1.0: status_pin(), status_unpin()
* POTENTIALLY BREAKING CHANGE: Changed pagination attributes to not be part of the dict keys
  of paginated return values.
* Many internal improvements, more tests

v1.2.2
------
* Several small bugfixes (thanks @codl)
* Mastodon v2.1.2 compatibility
    * Added instance_activity()
    * Added instance_peers()    
* Fixed StreamListener breaking when listening to more than one stream (again thanks, codl)
    * POTENTIALLY BREAKING CHANGE: Remvoved handle_line, which should have been an internal helper to begin with

v1.2.1 
------
* Internal stability changes and fixes to streaming code
* Fixed async parameter being ignored in two streaming methods

v1.2.0
------
* BREAKING CHANGE: Renamed streaming functions to be more in line with the rest
* POTENTIALLY BREAKING CHANGE: Added attribute-style access for returned dicts
* Mastodon v2.1.0 compatibility
    * Added custom_emojis()
    * Added list(), lists(), list_accounts()
    * Added list_create(), list_update(), list_delete()
    * Added list_accounts_add(), list_accounts_delete()
    * Added account_lists()
    * Added timeline_list()
    * Added stream_list()
* Added automatic id unpacking    
* Added api versioning
* Added a large amount of tests (MASSIVE thanks to codl)
* Added asynchronous mode to streaming api (Thanks Kjwon15)
* Added CallbackStreamListener
* Improved documentation for the streaming API
* Various fixes, clarifications, et cetera (Thanks Dryusdan, codl)  

v1.1.2
------
* 2.0 id compatibility (thanks @codl)
* Added emoji support
* Media alt-text support (thanks foozmeat)
* Python2 fixes (thanks ragingscholar)
* General code cleanup and small fixes (thanks @codl)
* Beginnings of better error handling (thanks Elizafox)
* Various documentation updates

v1.1.1
------
* Emergency fix to allow logging in to work (thanks @codl)

v1.1.0
------
* BREAKING CHANGE: Added date parsing to the response parser
* Added notification dismissal
* Added conversation muting
* Updated documentation
* Added asynchronous mode for the streaming API
* Fixed several bugs (thanks ng-0, LogalDeveloper, Chronister, Elizafox, codl, lambadalambda)
* Improved code style (thanks foxmask)

v1.0.8
------
* Added support for domain blocks
* Updated the documentation to reflect API changes
* Added support for pagination (Thanks gled-rs, azillion)
* Fixed various bugs (Thanks brrzap, fumi-san)

v1.0.7
------
* Added support for OAuth2 (Thanks to azillon)
* Added support for several new endpoints (Thanks phryk, aeonofdiscord, naoyat)
* Fixed various bugs (Thanks EliotBerriot, csu, edsu)
* Added support for streaming API (Thanks wjt)

v1.0.6
------
* Fixed several bugs (Thanks to Psycojoker, wjt and wxcafe)
* Added support for spoiler text (Thanks to Erin Congden)
* Added support for mute functionality (Thanks to Erin Congden)
* Added support for getting favourites (Thanks to Erin Congden)
* Added support for follow requests (Thanks to Erin Congden, again)
* Added MANIFEST.in to allow for conda packaging (Thanks, pmlandwehr)

v1.0.5
------
* Fixed previous fix (Thank you, @tylerb@mastodon.social)

v1.0.4
------
* Fixed an app creation bug (Thank you, @tylerb@mastodon.social)

v1.0.3
------
* Added support for toot privacy (thanks fpietsche)

v1.0.2
------
* Removed functions and documentation for APIs that have been removed
* Documentation is now vastly improved thanks to @lydia@mastodon.social / girlsim
* Rate limiting code - Mastodon.py can now attempt to respect rate limits
* Several small bug fixes, consistency fixes, quality-of-life improvements

v.1.0.1
-------
* Added timeline_*() functions for consistency. timeline() functions as before.
* Clarified documentation in various places.
* Added previously-undocumented notifications() - API that gets a users notifications.
  
v.1.0.0
-------
* Initial Release

