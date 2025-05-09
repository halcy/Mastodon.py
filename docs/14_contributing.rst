Contributing
============

How to contribute
-----------------

Mastodon.py is incomplete a lot of the time because Mastodon has a very rich API with many functions, not all of which are implemented here.
Even when it is complete for a given Mastodon API version, there are forks and other Mastodon-API-compatible software that implement their own methods which Mastodon.py could in principle support.
And even when all of that work is done, it will inevitably have bugs, or places where the library could be made easier to use (which, really, are also bugs), missing tests that could catch bugs quicker, tooling to make updating everything faster, et cetera.

You can help get more of this done, and you should! This can take many forms: If you notice somtehing is missing, broken or confusing:

* You could file an issue on github, either with or without suggestions for how to fix the issue: https://github.com/halcy/Mastodon.py/issues
* You could, after filing an issue, do a PR that fixes that issue
* You could even just vaguely complain in my (https://icosahedron.website/@halcy) general direction on Mastodon

All of these help immensely, even if it's just "hey, I don't really get why X isn't working". We can't make the library better if we don't know what the actual issues people 
have are, so while I'm not going to implement every suggestion and do have some ideas of what does and does not make a good library, your feedback is, in fact, extremely valuable
and welcome.

If you're looking for some "starter issues" to address: Currently, we don't have support for much of any of the new 4.0.0 API endpoints implemented. Pick one and have a go,
especially from the admin API. Tests are somewhat annoying to set up, as they need to run against a live mastodon instance - great if you can write them, but feel free to
skip out on them, too, or just write them "in the dry" without actually running them and leaving that for someone else.

Tests
-----
Mastodon.py has an extensive suite of tests. The purpose of these is twofold:

* Make sure nothing is broken and that there aren't any regressions
* Where the official docs are unclear, verify assumptions we make about the Mastodon API and document the results

The tests use pytest and pytest-recording so that they can be ran even without a mastodon server, but new tests require
setting up a mastodon dev server. Further documentation can be found in the "tests" directory in the repository.
