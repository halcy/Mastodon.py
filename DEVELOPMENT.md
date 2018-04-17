Here's some general stuff to keep in mind, and some work that needs to be done

* Mastodon.py tries to work for python2 as well as python3, so avoid things like annotations,
  use requests over urllib, et cetera.

* Current TODOs (2.3 support):
    * Add support for media updating
    * Add support for focal points
    * Add support for idempotency keys
    * Document error handling better
    * Update tests
    * Decide what to do about frame_rate values specified as fractions (7/20 etc.)
    
