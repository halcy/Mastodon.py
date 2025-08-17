API relevant changes since last release / "to implement" list:

Refer to mastodon changelog and API docs for details when implementing, add or modify tests where needed

4.4.0 TODOs
-----------
* [x] Fix all the issues
* [ ] New endpoints for endorsements, replacing "pin" api, which is now deprecated: accounts_endorsements(id), account_endorse(id), account_unendorse(id)
* [ ] New endpoints for featured tags: tag_feature(name), tag_unfeature(name)
* [ ] New endpoint: instance_terms, with or without date (format?)
* [x] Some oauth stuff (userinfo? capability discovery? see issue for that)
* [x] status_delete now has a media delete param
* [ ] push_subscribe now has a "standard" parameter to switch between two versions. may also need to update crypto impls?
* [ ] account_register now has a date of birth param (as above: format?)
* [ ] update_credentials now has an attribution_domains param for link attribution (list)
* [x] Various updates to return values (automatable, hopefully, other than docs)
* [x] There is a "Deprecation" http header now, expose that to users?
