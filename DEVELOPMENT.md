Here's some general stuff to keep in mind, and some work that needs to be done

* Mastodon.py tries to work for python2 as well as python3, so avoid things like annotations,
  use requests over urllib, et cetera.

* Unimplemented methods:
    * GET /api/v1/instance
    * GET /api/v1/reports
    * POST /api/v1/reports
    * GET /api/v1/statuses/:id/card
    * PATCH /api/v1/accounts/update_credentials
    
* Documentation that needs to be updated:
    * Toot dicts are missing some fields (cards, applications, visibility)
    * Some others probably are missing stuff also
    
* Other things missing:
    * Transparent as well as explicit pagination support
    * Tests (long-term goal)
