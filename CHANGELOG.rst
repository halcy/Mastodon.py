A note on versioning: This librarys major version will grow with the APIs 
version number. Breaking changes will be indicated by a change in the minor
(or major) version number, and will generally be avoided. 

v1.2.2
------
* Several small bugfixes (thanks codl)
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
* 2.0 id compatibility (thanks codl)
* Added emoji support
* Media alt-text support (thanks foozmeat)
* Python2 fixes (thanks ragingscholar)
* General code cleanup and small fixes (thanks codl)
* Beginnings of better error handling (thanks Elizafox)
* Various documentation updates

v1.1.1
------
* Emergency fix to allow logging in to work (thanks codl)

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

