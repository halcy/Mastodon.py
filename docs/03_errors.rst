Error handling
==============
.. py:module:: mastodon
    :no-index:
.. py:class: Mastodon

When Mastodon.py encounters an error, it will raise an exception, generally with
some text included to tell you what went wrong.

The base class that all Mastodon exceptions inherit from is `MastodonError`.
If you are only interested in the fact an error was raised somewhere in
Mastodon.py, and not the details, this is the exception you can catch.

`MastodonIllegalArgumentError` is generally a programming problem - you asked the
API to do something obviously invalid (i.e. specify a privacy option that does
not exist).

`MastodonFileNotFoundError` and `MastodonNetworkError` are IO errors - could be you
specified a wrong URL, could be the internet is down or your hard drive is
dying. They inherit from `MastodonIOError`, for easy catching. There is a sub-error
of `MastodonNetworkError`, `MastodonReadTimeout`, which is thrown when a streaming
API stream times out during reading.

`MastodonAPIError` is an error returned from the Mastodon instance - the server
has decided it can't fulfil your request (i.e. you requested info on a user that
does not exist). It is further split into `MastodonNotFoundError` (API returned 404)
and `MastodonUnauthorizedError` (API returned 401). Different error codes might exist,
but are not currently handled separately.

`MastodonMalformedEventError` is raised when a streaming API listener receives an
invalid event. There have been reports that this can sometimes happen after prolonged
operation due to an upstream problem in the requests/urllib libraries.

`MastodonRatelimitError` is raised when you hit an API rate limit. You should try
again after a while (see the rate limiting section above).

`MastodonServerError` is raised when the server throws an internal error, likely due
to server misconfiguration.

`MastodonVersionError` is raised when a version check for an API call fails.

`MastodonDeprecationWarning` is raised when a deprecated API call is used. This is based
on the `deprecation` HTTP header returned by the server.
