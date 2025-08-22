
# If you'd like to contribute to Mastodon.py, here's some concrete areas that need work:

* Features are currently up to date and mostly tested, but there are some areas where tests could be better, especially for all the wrong-argument and error state checks. Check the codecov page and try to add tests those areas.
* Nodeinfo is currently just documented by reference to the spec. It could be documented better.
* Nodeinfo currently just retrieves the 2.0 spec version. It should likely attempt to retrieve other versions as well, trying to get the most recent one available.
* We currently don't use OAuth Proof Key for Code Exchange - that should be implemented at some point (for servers that support it).
* Other implementations of the Mastodon API as well as Mastodon forks exist - it may be good to try to support these:
  * Figure out what they do different and file issues / document it
  * Where code can be written to support alternate implementations or different features, write code to do this
  * Write tests specific to these features
  * We now have a "feature set" parameter to support these better.
* You can also check TODO.md for any open TODOs that have been added.
  
# General guidelines

* If you've discovered what you think is a bug, or are even just unclear on whether something is a bug, or about how to do some specific thing - just open an issue, we'll try to respond.
* If you're contributing code, while it'd be great if you could provide tests, if setting up a mastodon server to test against is too much, feel free to go without - we can always add those later.
* There is a .githooks directory that you can start using by running "$ git config --local core.hooksPath .githooks/". Right now, there is only a hook that checks whether you're trying to commit a credential.
* We don't generally accept purely cosmetic changes, please avoid patches that only apply formatting.
* If you have any questions about contributing or the library, you can either open up a discussion in the github discussions section, open an issue, or directly talk to @halcy@icosahedron.website on the Fediverse or .halcy on discord.
  
