Here's some general stuff to keep in mind, and some work that needs to be done:

* If you'd like to contribute, here's some suggestions:
  * Features are currently up to date and mostly tested, but there are some areas where tests could be 
    better. Check the codecov page and try to add tests those areas.
  * Nodeinfo is currently just documented by reference to the spec. It could be documented better.
  * Nodeinfo currently just retrieves the 2.0 spec version. It should likely attempt to retrieve other
    versions as well, trying to get the most recent one available.
  * There's some code duplication in places that could be lessened.
  * Other implementations of the Mastodon API as well as Mastodon forks exist - it may be good to try to support these:
    * Figure out what they do different and file issues / document it
    * Where code can be written to support alternate implementations or different features, write code to do this
    * Write tests specific to these features
    * We now have a "feature set" parameter to support these better.
    


