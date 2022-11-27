API relevant changes since last release / "to implement" list:

Refer to mastodon changelog and API docs for details when implementing, add or modify tests where needed

3.1.3
-----
* [x] POST /api/v1/media → POST /api/v2/media (v1 deprecated)

3.1.4
-----
* [x] Add ability to exclude local content from federated timeline
* [x] Add ability to exclude remote content from hashtag timelines in web UI
* [x] Add invites_enabled attribute to GET /api/v1/instance in REST API

3.2.0
-----
* [x] Add personal notes for accounts
* [x] Add customizable thumbnails for audio and video attachments
* [x] Add color extraction for thumbnails

3.3.0
-----
* [x] Add option to be notified when a followed user posts
* [x] Add duration option to the mute function
* [postponed to 4.0 because that's when the official docs say it starts existing as an API] Add ability to block access or limit sign-ups from chosen IPs
* [postponed - need websocket support first] Add support for managing multiple stream subscriptions in a single connection
* [x] Add support for limiting results by both min_id and max_id at the same time in REST API
* [x] Add GET /api/v1/accounts/:id/featured_tags to REST API

3.4.0
-----
* [x] Add server rules
* [x] Add POST /api/v1/emails/confirmations to REST API
* [x] Add GET /api/v1/accounts/lookup to REST API
* [x] Add policy param to POST /api/v1/push/subscriptions in REST API
* [x] Add details to error response for POST /api/v1/accounts in REST API

3.4.2
-----
* [postpone to later] Add configuration attribute to GET /api/v1/instance

3.5.0
-----
* [x] Add support for incoming edited posts
* [x] Add notifications for posts deleted by moderators <- by email. not actually API relevant.
* [x] Add explore page with trending posts and links
* [x] Add graphs and retention metrics to admin dashboard
* [ ] Add GET /api/v1/accounts/familiar_followers to REST API
* [ ] Add POST /api/v1/accounts/:id/remove_from_followers to REST API
* [x] Add category and rule_ids params to POST /api/v1/reports IN REST API
* [x] Add global lang param to REST API
* [x] Add types param to GET /api/v1/notifications in REST API
* [x] Add notifications for moderators about new sign-ups
* [ ] v2 admin account api

3.5.3
-----
* [later with tool to update dicts] Add limited attribute to accounts in REST API

4.0.0 and beyond
----------------
? ? ? ?

General improvements that would be good to do before doing another release:
* [ ] Split mastodon.py into parts in some way that makes sense, it's getting very unwieldy
* [x] Fix the CI
* [ ] Get test coverage like, real high
* [x] Add all those streaming events??
* [ ] Document return values (skipping this for a bit to then do it at the end with tooling)
