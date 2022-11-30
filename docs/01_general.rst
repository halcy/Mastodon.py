General information
===================
.. py:module:: mastodon
.. py:class: Mastodon

Rate limiting
-------------
Mastodon's API rate limits per user account. By default, the limit is 300 requests
per 5 minute time slot. This can differ from instance to instance and is subject to change.
Mastodon.py has three modes for dealing with rate limiting that you can pass to
the constructor, "throw", "wait" and "pace", "wait" being the default.

In "throw" mode, Mastodon.py makes no attempt to stick to rate limits. When
a request hits the rate limit, it simply throws a `MastodonRateLimitError`. This is
for applications that need to handle all rate limiting themselves (i.e. interactive apps),
or applications wanting to use Mastodon.py in a multi-threaded context ("wait" and "pace"
modes are not thread safe).

.. note::
   Rate limit information is available on the `Mastodon` object for applications that
   implement their own rate limit handling.

   .. attribute:: Mastodon.ratelimit_remaining

      Number of requests allowed until the next reset.

   .. attribute:: Mastodon.ratelimit_reset

      Time at which the rate limit will next be reset, as a POSIX timestamp.

   .. attribute:: Mastodon.ratelimit_limit

      Total number of requests allowed between resets. Typically 300.

   .. attribute:: Mastodon.ratelimit_lastcall

      Time at which these values have last been seen and updated, as a POSIX timestamp.

In "wait" mode, once a request hits the rate limit, Mastodon.py will wait until
the rate limit resets and then try again, until the request succeeds or an error
is encountered. This mode is for applications that would rather just not worry about rate limits
much, don't poll the API all that often, and are okay with a call sometimes just taking
a while.

In "pace" mode, Mastodon.py will delay each new request after the first one such that,
if requests were to continue at the same rate, only a certain fraction (set in the
constructor as `ratelimit_pacefactor`) of the rate limit will be used up. The fraction can
be (and by default, is) greater than one. If the rate limit is hit, "pace" behaves like
"wait". This mode is probably the most advanced one and allows you to just poll in
a loop without ever sleeping at all yourself. It is for applications that would rather
just pretend there is no such thing as a rate limit and are fine with sometimes not
being very interactive.

In addition to the per-user limit, there is a per-IP limit of 7500 requests per 5
minute time slot, and tighter limits on logins. Mastodon.py does not make any effort
to respect these.

If your application requires many hits to endpoints that are available without logging
in, do consider using Mastodon.py without authenticating to get the full per-IP limit.

Pagination
----------
Many of Mastodon's API endpoints are paginated. What this means is that if you request
data from them, you might not get all the data at once - instead, you might only get the
first few results.

All endpoints that are paginated have four parameters: `since_id`, `max_id`, `min_id` and
`limit`. `since_id` allows you to specify the smallest id you want in the returned data, but
you will still always get the newest data, so if there are too many statuses between
the newest one and `since_id`, some will not be returned. `min_id`, on the other hand, gives
you statuses with that minimum id and newer, starting at the given id. `max_id`, similarly,
allows you to specify the largest id you want. By specifying either min_id or `max_id`
(generally, only one, not both, though specifying both is supported starting with Mastodon
version 3.3.0) of them you can go through pages forwards and backwards.

On Mastodon mainline, you can, pass datetime objects as IDs when fetching posts,
since the IDs used are Snowflake IDs and dates can be approximately converted to those.
This is guaranteed to work on mainline Mastodon servers and very likely to work on all
forks, but will **not** work on other servers implementing the API, like Pleroma, Misskey
or Gotosocial. You should not use this if you want your application to be universally
compatible. It's also relatively coarse-grained.

`limit` allows you to specify how many results you would like returned. Note that an
instance may choose to return less results than you requested - by default, Mastodon
will return no more than 40 statuses and no more than 80 accounts no matter how high
you set the limit.

The responses returned by paginated endpoints contain a "link" header that specifies
which parameters to use to get the next and previous pages. Mastodon.py parses these
and stores them (if present) in the first (for the previous page) and last (for the
next page) item of the returned list as _pagination_prev and _pagination_next. They
are accessible only via attribute-style access. Note that this means that if you
want to persist pagination info with your data, you'll have to take care of that
manually (or persist objects, not just dicts).

There are convenience functions available for fetching the previous and next page of
a paginated request as well as for fetching all pages starting from a first page.
For details, see :ref:`fetch_next() <fetch_next()>`, :ref:`fetch_previous() <fetch_previous()>`. 
and :ref:`fetch_remaining() <fetch_remaining()>`.

IDs and unpacking
-----------------
Mastodon's API uses IDs in several places: User IDs, Toot IDs, ...

While debugging, it might be tempting to copy-paste IDs from the
web interface into your code. This will not work, as the IDs on the web
interface and in the URLs are not the same as the IDs used internally
in the API, so don't do that.

ID unpacking
~~~~~~~~~~~~
Wherever Mastodon.py expects an ID as a parameter, you can also pass a
dict that contains an id - this means that, for example, instead of writing

.. code-block:: python

    mastodon.status_post("@somebody wow!", in_reply_to_id = toot["id"])

you can also just write

.. code-block:: python

    mastodon.status_post("@somebody wow!", in_reply_to_id = toot)

and everything will work as intended.

Snowflake IDs
~~~~~~~~~~~~~
Some IDs in Mastodon (such as those for statuses) are Snowflake IDs. These broadly
correspond to times, with a low resolution, so it is possible to convert a time to
a Snowflake ID and search for posts between two dates. Mastodon.py will do the
conversion for you automatically when you pass a `datetime` object as the id.

Note that this functionality will *not* work on anything but Mastodon and forks,
and that it is somewhat inexact due to the relatively low resolution.

Versioning
----------
Mastodon.py will check if a certain endpoint is available before doing API
calls. By default, it checks against the version of Mastodon retrieved on
init(), or the version you specified. Mastodon.py can be set (in the
constructor) to either check if an endpoint is available at all (this is the
default) or to check if the endpoint is available and behaves as in the newest
Mastodon version (with regards to parameters as well as return values).
Version checking can also be disabled altogether. If a version check fails,
Mastodon.py throws a `MastodonVersionError`.

Some functions need to check what version of Mastodon they are talking to.
These will generally use a cached version to avoid sending a lot of pointless
requests.

Many non-mainline forks have various different formats for their versions and
they have different, incompatible ideas about how to report version. Mastodon.py
tries its best to figure out what is going on, but success is not guaranteed.

With the following functions, you can make Mastodon.py re-check the server
version or explicitly determine if a specific minimum Version is available.
Long-running applications that aim to support multiple Mastodon versions
should do this from time to time in case a server they are running against
updated.

.. automethod:: Mastodon.retrieve_mastodon_version
.. automethod:: Mastodon.verify_minimum_version

A brief note on block lists
---------------------------
Mastodon.py used to block three instances because these were particularly notorious for
harassing trans people and I don't feel like I have an obligation to let software I 
distribute help people who want my friends to die. I don't want to be associated with 
that, at all. 

Those instances are now all gone, any point that could have been has been made, and 
there is no list anymore.

.. note::
   Trans rights are human rights. 
