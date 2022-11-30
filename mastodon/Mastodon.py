# coding: utf-8

import json
import base64
import os
import os.path
import time
import datetime
import collections
from contextlib import closing
import requests
from requests.models import urlencode
import dateutil
import dateutil.parser
import re
import copy


from .compat import IMPL_HAS_CRYPTO, IMPL_HAS_ECE, IMPL_HAS_BLURHASH
from .compat import cryptography, default_backend, ec, serialization
from .compat import http_ece
from .compat import blurhash
from .compat import urlparse

from .utility import parse_version_string, max_version, api_version
from .utility import AttribAccessDict, AttribAccessDict
from .utility import Mastodon as Utility

from .error import *
from .versions import _DICT_VERSION_APPLICATION, _DICT_VERSION_MENTION, _DICT_VERSION_MEDIA, _DICT_VERSION_ACCOUNT, _DICT_VERSION_POLL, \
                        _DICT_VERSION_STATUS, _DICT_VERSION_INSTANCE, _DICT_VERSION_HASHTAG, _DICT_VERSION_EMOJI, _DICT_VERSION_RELATIONSHIP, \
                        _DICT_VERSION_NOTIFICATION, _DICT_VERSION_CONTEXT, _DICT_VERSION_LIST, _DICT_VERSION_CARD, _DICT_VERSION_SEARCHRESULT, \
                        _DICT_VERSION_ACTIVITY, _DICT_VERSION_REPORT, _DICT_VERSION_PUSH, _DICT_VERSION_PUSH_NOTIF, _DICT_VERSION_FILTER, \
                        _DICT_VERSION_CONVERSATION, _DICT_VERSION_SCHEDULED_STATUS, _DICT_VERSION_PREFERENCES, _DICT_VERSION_ADMIN_ACCOUNT, \
                        _DICT_VERSION_FEATURED_TAG, _DICT_VERSION_MARKER, _DICT_VERSION_REACTION, _DICT_VERSION_ANNOUNCEMENT, _DICT_VERSION_STATUS_EDIT, \
                        _DICT_VERSION_FAMILIAR_FOLLOWERS, _DICT_VERSION_ADMIN_DOMAIN_BLOCK, _DICT_VERSION_ADMIN_MEASURE, _DICT_VERSION_ADMIN_DIMENSION, \
                        _DICT_VERSION_ADMIN_RETENTION

from .defaults import _DEFAULT_TIMEOUT, _DEFAULT_SCOPES, _DEFAULT_STREAM_TIMEOUT, _DEFAULT_STREAM_RECONNECT_WAIT_SEC
from .defaults import _SCOPE_SETS

from .internals import Mastodon as Internals
from .authentication import Mastodon as Authentication
from .accounts import Mastodon as Accounts
from .instance import Mastodon as Instance
from .timeline import Mastodon as Timeline
from .statuses import Mastodon as Statuses

##
# The actual Mastodon class
###
class Mastodon(Utility, Authentication, Accounts, Instance, Timeline, Statuses):
    """
    Thorough and easy to use Mastodon
    API wrapper in Python.

    Main class, imports most things from modules
    """
    # Support level
    __SUPPORTED_MASTODON_VERSION = "3.5.5"

    @staticmethod
    def get_supported_version():
        """
        Retrieve the maximum version of Mastodon supported by this version of Mastodon.py
        """
        return Mastodon.__SUPPORTED_MASTODON_VERSION

    ###
    # Reading data: Polls
    ###
    @api_version("2.8.0", "2.8.0", _DICT_VERSION_POLL)
    def poll(self, id):
        """
        Fetch information about the poll with the given id

        Returns a :ref:`poll dict <poll dict>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/polls/{0}'.format(str(id))
        return self.__api_request('GET', url)

    ###
    # Reading data: Notifications
    ###
    @api_version("1.0.0", "3.5.0", _DICT_VERSION_NOTIFICATION)
    def notifications(self, id=None, account_id=None, max_id=None, min_id=None, since_id=None, limit=None, exclude_types=None, types=None, mentions_only=None):
        """
        Fetch notifications (mentions, favourites, reblogs, follows) for the logged-in
        user. Pass `account_id` to get only notifications originating from the given account.

        There are different types of notifications: 
            * `follow` - A user followed the logged in user
            * `follow_request` - A user has requested to follow the logged in user (for locked accounts)
            * `favourite` - A user favourited a post by the logged in user
            * `reblog` - A user reblogged a post by the logged in user
            * `mention` - A user mentioned the logged in user
            * `poll` - A poll the logged in user created or voted in has ended
            * `update` - A status the logged in user has reblogged (and only those, as of 4.0.0) has been edited
            * `status` - A user that the logged in user has enabned notifications for has enabled `notify` (see :ref:`account_follow() <account_follow()>`)
            * `admin.sign_up` - For accounts with appropriate permissions (TODO: document which those are when adding the permission API): A new user has signed up
            * `admin.report` - For accounts with appropriate permissions (TODO: document which those are when adding the permission API): A new report has been received
        Parameters `exclude_types` and `types` are array of these types, specifying them will in- or exclude the
        types of notifications given. It is legal to give both parameters at the same tine, the result will then
        be the intersection of the results of both filters. Specifying `mentions_only` is a deprecated way to set 
        `exclude_types` to all but mentions.

        Can be passed an `id` to fetch a single notification.

        Returns a list of :ref:`notification dicts <notification dicts>`.
        """
        if mentions_only is not None:
            if exclude_types is None and types is None:
                if mentions_only:
                    if self.verify_minimum_version("3.5.0", cached=True):
                        types = ["mention"]
                    else:
                        exclude_types = ["follow", "favourite", "reblog", "poll", "follow_request"]
            else:
                raise MastodonIllegalArgumentError('Cannot specify exclude_types/types when mentions_only is present')
            del mentions_only

        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        if account_id is not None:
            account_id = self.__unpack_id(account_id)

        if id is None:
            params = self.__generate_params(locals(), ['id'])
            return self.__api_request('GET', '/api/v1/notifications', params)
        else:
            id = self.__unpack_id(id)
            url = '/api/v1/notifications/{0}'.format(str(id))
            return self.__api_request('GET', url)

    ###
    # Reading data: Accounts
    ###
    @api_version("1.0.0", "1.0.0", _DICT_VERSION_ACCOUNT)
    def account(self, id):
        """
        Fetch account information by user `id`.

        Does not require authentication for publicly visible accounts.

        Returns a :ref:`account dict <account dict>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def account_verify_credentials(self):
        """
        Fetch logged-in user's account information.

        Returns a :ref:`account dict <account dict>` (Starting from 2.1.0, with an additional "source" field).
        """
        return self.__api_request('GET', '/api/v1/accounts/verify_credentials')

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def me(self):
        """
        Get this user's account. Synonym for `account_verify_credentials()`, does exactly
        the same thing, just exists becase `account_verify_credentials()` has a confusing
        name.
        """
        return self.account_verify_credentials()

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def account_statuses(self, id, only_media=False, pinned=False, exclude_replies=False, exclude_reblogs=False, tagged=None, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch statuses by user `id`. Same options as :ref:`timeline() <timeline()>` are permitted.
        Returned toots are from the perspective of the logged-in user, i.e.
        all statuses visible to the logged-in user (including DMs) are
        included.

        If `only_media` is set, return only statuses with media attachments.
        If `pinned` is set, return only statuses that have been pinned. Note that
        as of Mastodon 2.1.0, this only works properly for instance-local users.
        If `exclude_replies` is set, filter out all statuses that are replies.
        If `exclude_reblogs` is set, filter out all statuses that are reblogs.
        If `tagged` is set, return only statuses that are tagged with `tagged`. Only a single tag without a '#' is valid.

        Does not require authentication for Mastodon versions after 2.7.0 (returns
        publicly visible statuses in that case), for publicly visible accounts.

        Returns a list of :ref:`status dicts <status dicts>`.
        """
        id = self.__unpack_id(id)
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        if not pinned:
            del params["pinned"]
        if not only_media:
            del params["only_media"]
        if not exclude_replies:
            del params["exclude_replies"]
        if not exclude_reblogs:
            del params["exclude_reblogs"]

        url = '/api/v1/accounts/{0}/statuses'.format(str(id))
        return self.__api_request('GET', url, params)

    @api_version("1.0.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def account_following(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch users the given user is following.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/following'.format(str(id))
        return self.__api_request('GET', url, params)

    @api_version("1.0.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def account_followers(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch users the given user is followed by.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/followers'.format(str(id))
        return self.__api_request('GET', url, params)

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_relationships(self, id):
        """
        Fetch relationship (following, followed_by, blocking, follow requested) of
        the logged in user to a given account. `id` can be a list.

        Returns a list of :ref:`relationship dicts <relationship dicts>`.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/relationships',
                                  params)

    @api_version("1.0.0", "2.3.0", _DICT_VERSION_ACCOUNT)
    def account_search(self, q, limit=None, following=False):
        """
        Fetch matching accounts. Will lookup an account remotely if the search term is
        in the username@domain format and not yet in the database. Set `following` to
        True to limit the search to users the logged-in user follows.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        params = self.__generate_params(locals())

        if params["following"] == False:
            del params["following"]

        return self.__api_request('GET', '/api/v1/accounts/search', params)

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def account_lists(self, id):
        """
        Get all of the logged-in user's lists which the specified user is
        a member of.

        Returns a list of :ref:`list dicts <list dicts>`.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/lists'.format(str(id))
        return self.__api_request('GET', url, params)

    @api_version("3.4.0", "3.4.0", _DICT_VERSION_ACCOUNT)
    def account_lookup(self, acct):
        """
        Look up an account from user@instance form (@instance allowed but not required for
        local accounts). Will only return accounts that the instance already knows about, 
        and not do any webfinger requests. Use `account_search` if you need to resolve users 
        through webfinger from remote.

        Returns an :ref:`account dict <account dict>`.
        """
        return self.__api_request('GET', '/api/v1/accounts/lookup', self.__generate_params(locals()))
    
    @api_version("3.5.0", "3.5.0", _DICT_VERSION_FAMILIAR_FOLLOWERS)
    def account_familiar_followers(self, id):
        """
        Find followers for the account given by id (can be a list) that also follow the
        logged in account.

        Returns a list of :ref:`familiar follower dicts <familiar follower dicts>`
        """
        if not isinstance(id, list):
            id = [id]
        for i in range(len(id)):
            id[i] = self.__unpack_id(id[i])
        return self.__api_request('GET', '/api/v1/accounts/familiar_followers', {'id': id}, use_json=True)

    ###
    # Reading data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tags(self):
        """
        Return the hashtags the logged-in user has set to be featured on
        their profile as a list of :ref:`featured tag dicts <featured tag dicts>`.

        Returns a list of :ref:`featured tag dicts <featured tag dicts>`.
        """
        return self.__api_request('GET', '/api/v1/featured_tags')

    @api_version("3.0.0", "3.0.0", _DICT_VERSION_HASHTAG)
    def featured_tag_suggestions(self):
        """
        Returns the logged-in user's 10 most commonly-used hashtags.

        Returns a list of :ref:`hashtag dicts <hashtag dicts>`.
        """
        return self.__api_request('GET', '/api/v1/featured_tags/suggestions')

    ###
    # Reading data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filters(self):
        """
        Fetch all of the logged-in user's filters.

        Returns a list of :ref:`filter dicts <filter dicts>`. Not paginated.
        """
        return self.__api_request('GET', '/api/v1/filters')

    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filter(self, id):
        """
        Fetches information about the filter with the specified `id`.

        Returns a :ref:`filter dict <filter dict>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/filters/{0}'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filters_apply(self, objects, filters, context):
        """
        Helper function: Applies a list of filters to a list of either statuses
        or notifications and returns only those matched by none. This function will
        apply all filters that match the context provided in `context`, i.e.
        if you want to apply only notification-relevant filters, specify
        'notifications'. Valid contexts are 'home', 'notifications', 'public' and 'thread'.
        """

        # Build filter regex
        filter_strings = []
        for keyword_filter in filters:
            if not context in keyword_filter["context"]:
                continue

            filter_string = re.escape(keyword_filter["phrase"])
            if keyword_filter["whole_word"]:
                filter_string = "\\b" + filter_string + "\\b"
            filter_strings.append(filter_string)
        filter_re = re.compile("|".join(filter_strings), flags=re.IGNORECASE)

        # Apply
        filter_results = []
        for filter_object in objects:
            filter_status = filter_object
            if "status" in filter_object:
                filter_status = filter_object["status"]
            filter_text = filter_status["content"]
            filter_text = re.sub(r"<.*?>", " ", filter_text)
            filter_text = re.sub(r"\s+", " ", filter_text).strip()
            if not filter_re.search(filter_text):
                filter_results.append(filter_object)
        return filter_results

    ###
    # Reading data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_ACCOUNT)
    def suggestions(self):
        """
        Fetch follow suggestions for the logged-in user.

        Returns a list of :ref:`account dicts <account dicts>`.

        """
        return self.__api_request('GET', '/api/v1/suggestions')

    ###
    # Reading data: Follow suggestions
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_ACCOUNT)
    def directory(self, offset=None, limit=None, order=None, local=None):
        """
        Fetch the contents of the profile directory, if enabled on the server.

        `offset` how many accounts to skip before returning results. Default 0.

        `limit` how many accounts to load. Default 40.

        `order` "active" to sort by most recently posted statuses (default) or
                "new" to sort by most recently created profiles.

        `local` True to return only local accounts.

        Returns a list of :ref:`account dicts <account dicts>`.

        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/directory', params)

    ###
    # Reading data: Endorsements
    ###
    @api_version("2.5.0", "2.5.0", _DICT_VERSION_ACCOUNT)
    def endorsements(self):
        """
        Fetch list of users endorsed by the logged-in user.

        Returns a list of :ref:`account dicts <account dicts>`.

        """
        return self.__api_request('GET', '/api/v1/endorsements')

    ###
    # Reading data: Searching
    ###

    def __ensure_search_params_acceptable(self, account_id, offset, min_id, max_id):
        """
        Internal Helper: Throw a MastodonVersionError if version is < 2.8.0 but parameters
        for search that are available only starting with 2.8.0 are specified.
        """
        if any(item is not None for item in (account_id, offset, min_id, max_id)):
            if not self.verify_minimum_version("2.8.0", cached=True):
                raise MastodonVersionError("Advanced search parameters require Mastodon 2.8.0+")

    @api_version("1.1.0", "2.8.0", _DICT_VERSION_SEARCHRESULT)
    def search(self, q, resolve=True, result_type=None, account_id=None, offset=None, min_id=None, max_id=None, exclude_unreviewed=True):
        """
        Fetch matching hashtags, accounts and statuses. Will perform webfinger
        lookups if resolve is True. Full-text search is only enabled if
        the instance supports it, and is restricted to statuses the logged-in
        user wrote or was mentioned in.

        `result_type` can be one of "accounts", "hashtags" or "statuses", to only
        search for that type of object.

        Specify `account_id` to only get results from the account with that id.

        `offset`, `min_id` and `max_id` can be used to paginate.

        `exclude_unreviewed` can be used to restrict search results for hashtags to only
        those that have been reviewed by moderators. It is on by default. When using the
        v1 search API (pre 2.4.1), it is ignored.

        Will use search_v1 (no tag dicts in return values) on Mastodon versions before
        2.4.1), search_v2 otherwise. Parameters other than resolve are only available
        on Mastodon 2.8.0 or above - this function will throw a MastodonVersionError
        if you try to use them on versions before that. Note that the cached version
        number will be used for this to avoid uneccesary requests.

        Returns a :ref:`search result dict <search result dict>`, with tags as `hashtag dicts`_.
        """
        if self.verify_minimum_version("2.4.1", cached=True):
            return self.search_v2(q, resolve=resolve, result_type=result_type, account_id=account_id, offset=offset, min_id=min_id, max_id=max_id, exclude_unreviewed=exclude_unreviewed)
        else:
            self.__ensure_search_params_acceptable(
                account_id, offset, min_id, max_id)
            return self.search_v1(q, resolve=resolve)

    @api_version("1.1.0", "2.1.0", "2.1.0")
    def search_v1(self, q, resolve=False):
        """
        Identical to `search_v2()`, except in that it does not return
        tags as :ref:`hashtag dicts <hashtag dicts>`.

        Returns a :ref:`search result dict <search result dict>`.
        """
        params = self.__generate_params(locals())
        if not resolve:
            del params['resolve']
        return self.__api_request('GET', '/api/v1/search', params)

    @api_version("2.4.1", "2.8.0", _DICT_VERSION_SEARCHRESULT)
    def search_v2(self, q, resolve=True, result_type=None, account_id=None, offset=None, min_id=None, max_id=None, exclude_unreviewed=True):
        """
        Identical to `search_v1()`, except in that it returns tags as
        :ref:`hashtag dicts <hashtag dicts>`, has more parameters, and resolves by default.

        For more details documentation, please see `search()`

        Returns a :ref:`search result dict <search result dict>`.
        """
        self.__ensure_search_params_acceptable(
            account_id, offset, min_id, max_id)
        params = self.__generate_params(locals())

        if not resolve:
            del params["resolve"]

        if not exclude_unreviewed or not self.verify_minimum_version("3.0.0", cached=True):
            del params["exclude_unreviewed"]

        if "result_type" in params:
            params["type"] = params["result_type"]
            del params["result_type"]

        return self.__api_request('GET', '/api/v2/search', params)

    ###
    # Reading data: Trends
    ###
    @api_version("2.4.3", "3.5.0", _DICT_VERSION_HASHTAG)
    def trends(self, limit=None):
        """
        Alias for :ref:`trending_tags() <trending_tags()>`
        """
        return self.trending_tags(limit=limit) 

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_HASHTAG)
    def trending_tags(self, limit=None, lang=None):
        """
        Fetch trending-hashtag information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (the maximum number
        of results is 10, the endpoint is not paginated).

        Does not require authentication unless locked down by the administrator.

        Important versioning note: This endpoint does not exist for Mastodon versions
        between 2.8.0 (inclusive) and 3.0.0 (exclusive). 

        Pass `lang` to override the global locale parameter, which may affect trend ordering.

        Returns a list of :ref:`hashtag dicts <hashtag dicts>`, sorted by the instance's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        if self.verify_minimum_version("3.5.0", cached=True):
            # Starting 3.5.0, old version is deprecated
            return self.__api_request('GET', '/api/v1/trends/tags', params)
        else:
            return self.__api_request('GET', '/api/v1/trends', params)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS)
    def trending_statuses(self):
        """
        Fetch trending-status information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (the maximum number
        of results is 10, the endpoint is not paginated).

        Pass `lang` to override the global locale parameter, which may affect trend ordering.

        Returns a list of :ref:`status dicts <status dicts>`, sorted by the instances's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/trends/statuses', params)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_CARD)
    def trending_links(self):
        """
        Fetch trending-link information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (the maximum number
        of results is 10, the endpoint is not paginated).

        Returns a list of :ref:`card dicts <card dicts>`, sorted by the instances's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/trends/links', params)

    ###
    # Reading data: Lists
    ###
    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def lists(self):
        """
        Fetch a list of all the Lists by the logged-in user.

        Returns a list of :ref:`list dicts <list dicts>`.
        """
        return self.__api_request('GET', '/api/v1/lists')

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def list(self, id):
        """
        Fetch info about a specific list.

        Returns a :ref:`list dict <list dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', '/api/v1/lists/{0}'.format(id))

    @api_version("2.1.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def list_accounts(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Get the accounts that are on the given list.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)

        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', '/api/v1/lists/{0}/accounts'.format(id))

    ###
    # Reading data: Mutes and Blocks
    ###
    @api_version("1.1.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def mutes(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch a list of users muted by the logged-in user.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/mutes', params)

    @api_version("1.0.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def blocks(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch a list of users blocked by the logged-in user.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/blocks', params)

    ###
    # Reading data: Reports
    ###
    @api_version("1.1.0", "1.1.0", _DICT_VERSION_REPORT)
    def reports(self):
        """
        Fetch a list of reports made by the logged-in user.

        Returns a list of :ref:`report dicts <report dicts>`.

        Warning: This method has now finally been removed, and will not
        work on Mastodon versions 2.5.0 and above.
        """
        if self.verify_minimum_version("2.5.0", cached=True):
            raise MastodonVersionError("API removed in Mastodon 2.5.0")
        return self.__api_request('GET', '/api/v1/reports')

    ###
    # Reading data: Favourites
    ###
    @api_version("1.0.0", "2.6.0", _DICT_VERSION_STATUS)
    def favourites(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in user's favourited statuses.

        Returns a list of :ref:`status dicts <status dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/favourites', params)

    ###
    # Reading data: Follow requests
    ###
    @api_version("1.0.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def follow_requests(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in user's incoming follow requests.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/follow_requests', params)

    ###
    # Reading data: Domain blocks
    ###
    @api_version("1.4.0", "2.6.0", "1.4.0")
    def domain_blocks(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in user's blocked domains.

        Returns a list of blocked domain URLs (as strings, without protocol specifier).
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/domain_blocks', params)

    ###
    # Reading data: Emoji
    ###
    @api_version("2.1.0", "2.1.0", _DICT_VERSION_EMOJI)
    def custom_emojis(self):
        """
        Fetch the list of custom emoji the instance has installed.

        Does not require authentication unless locked down by the administrator.

        Returns a list of :ref:`emoji dicts <emoji dicts>`.
        """
        return self.__api_request('GET', '/api/v1/custom_emojis')

    ###
    # Reading data: Apps
    ###
    @api_version("2.0.0", "2.7.2", _DICT_VERSION_APPLICATION)
    def app_verify_credentials(self):
        """
        Fetch information about the current application.

        Returns an :ref:`application dict <application dict>`.
        """
        return self.__api_request('GET', '/api/v1/apps/verify_credentials')

    ###
    # Reading data: Webpush subscriptions
    ###
    @api_version("2.4.0", "2.4.0", _DICT_VERSION_PUSH)
    def push_subscription(self):
        """
        Fetch the current push subscription the logged-in user has for this app.

        Returns a :ref:`push subscription dict <push subscription dict>`.
        """
        return self.__api_request('GET', '/api/v1/push/subscription')

    ###
    # Reading data: Preferences
    ###
    @api_version("2.8.0", "2.8.0", _DICT_VERSION_PREFERENCES)
    def preferences(self):
        """
        Fetch the user's preferences, which can be used to set some default options.
        As of 2.8.0, apps can only fetch, not update preferences.

        Returns a :ref:`preference dict <preference dict>`.
        """
        return self.__api_request('GET', '/api/v1/preferences')

    ##
    # Reading data: Announcements
    ##

    # /api/v1/announcements
    @api_version("3.1.0", "3.1.0", _DICT_VERSION_ANNOUNCEMENT)
    def announcements(self):
        """
        Fetch currently active announcements.

        Returns a list of :ref:`announcement dicts <announcement dicts>`.
        """
        return self.__api_request('GET', '/api/v1/announcements')

    ##
    # Reading data: Read markers
    ##
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_MARKER)
    def markers_get(self, timeline=["home"]):
        """
        Get the last-read-location markers for the specified timelines. Valid timelines
        are the same as in :ref:`timeline() <timeline()>`

        Note that despite the singular name, `timeline` can be a list.

        Returns a dict of :ref:`read marker dicts <read marker dicts>`, keyed by timeline name.
        """
        if not isinstance(timeline, (list, tuple)):
            timeline = [timeline]
        params = self.__generate_params(locals())

        return self.__api_request('GET', '/api/v1/markers', params)

    ###
    # Reading data: Bookmarks
    ###
    @api_version("3.1.0", "3.1.0", _DICT_VERSION_STATUS)
    def bookmarks(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Get a list of statuses bookmarked by the logged-in user.

        Returns a list of :ref:`status dicts <status dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/bookmarks', params)

    ###
    # Writing data: Statuses
    ###
    def __status_internal(self, status, in_reply_to_id=None, media_ids=None,
                    sensitive=False, visibility=None, spoiler_text=None,
                    language=None, idempotency_key=None, content_type=None,
                    scheduled_at=None, poll=None, quote_id=None, edit=False):
        if quote_id is not None:
            if self.feature_set != "fedibird":
                raise MastodonIllegalArgumentError('quote_id is only available with feature set fedibird')
            quote_id = self.__unpack_id(quote_id)

        if content_type is not None:
            if self.feature_set != "pleroma":
                raise MastodonIllegalArgumentError('content_type is only available with feature set pleroma')
            # It would be better to read this from nodeinfo and cache, but this is easier
            if not content_type in ["text/plain", "text/html", "text/markdown", "text/bbcode"]:
                raise MastodonIllegalArgumentError('Invalid content type specified')

        if in_reply_to_id is not None:
            in_reply_to_id = self.__unpack_id(in_reply_to_id)

        if scheduled_at is not None:
            scheduled_at = self.__consistent_isoformat_utc(scheduled_at)

        params_initial = locals()

        # Validate poll/media exclusivity
        if poll is not None:
            if media_ids is not None and len(media_ids) != 0:
                raise ValueError(
                    'Status can have media or poll attached - not both.')

        # Validate visibility parameter
        valid_visibilities = ['private', 'public', 'unlisted', 'direct']
        if params_initial['visibility'] is None:
            del params_initial['visibility']
        else:
            params_initial['visibility'] = params_initial['visibility'].lower()
            if params_initial['visibility'] not in valid_visibilities:
                raise ValueError('Invalid visibility value! Acceptable values are %s' % valid_visibilities)

        if params_initial['language'] is None:
            del params_initial['language']

        if params_initial['sensitive'] is False:
            del [params_initial['sensitive']]

        headers = {}
        if idempotency_key is not None:
            headers['Idempotency-Key'] = idempotency_key

        if media_ids is not None:
            try:
                media_ids_proper = []
                if not isinstance(media_ids, (list, tuple)):
                    media_ids = [media_ids]
                for media_id in media_ids:
                    media_ids_proper.append(self.__unpack_id(media_id))
            except Exception as e:
                raise MastodonIllegalArgumentError("Invalid media dict: %s" % e)

            params_initial["media_ids"] = media_ids_proper

        if params_initial['content_type'] is None:
            del params_initial['content_type']

        use_json = False
        if poll is not None:
            use_json = True

        params = self.__generate_params(params_initial, ['idempotency_key', 'edit'])
        if edit is None:
            # Post
            return self.__api_request('POST', '/api/v1/statuses', params, headers=headers, use_json=use_json)
        else:
            # Edit
            return self.__api_request('PUT', '/api/v1/statuses/{0}'.format(str(self.__unpack_id(edit))), params, headers=headers, use_json=use_json)

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def status_post(self, status, in_reply_to_id=None, media_ids=None,
                    sensitive=False, visibility=None, spoiler_text=None,
                    language=None, idempotency_key=None, content_type=None,
                    scheduled_at=None, poll=None, quote_id=None):
        """
        Post a status. Can optionally be in reply to another status and contain
        media.

        `media_ids` should be a list. (If it's not, the function will turn it
        into one.) It can contain up to four pieces of media (uploaded via
        :ref:`media_post() <media_post()>`). `media_ids` can also be the `media dicts`_ returned
        by :ref:`media_post() <media_post()>` - they are unpacked automatically.

        The `sensitive` boolean decides whether or not media attached to the post
        should be marked as sensitive, which hides it by default on the Mastodon
        web front-end.

        The visibility parameter is a string value and accepts any of:
        'direct' - post will be visible only to mentioned users
        'private' - post will be visible only to followers
        'unlisted' - post will be public but not appear on the public timeline
        'public' - post will be public

        If not passed in, visibility defaults to match the current account's
        default-privacy setting (starting with Mastodon version 1.6) or its
        locked setting - private if the account is locked, public otherwise
        (for Mastodon versions lower than 1.6).

        The `spoiler_text` parameter is a string to be shown as a warning before
        the text of the status.  If no text is passed in, no warning will be
        displayed.

        Specify `language` to override automatic language detection. The parameter
        accepts all valid ISO 639-1 (2-letter) or for languages where that do not
        have one, 639-3 (three letter) language codes.

        You can set `idempotency_key` to a value to uniquely identify an attempt
        at posting a status. Even if you call this function more than once,
        if you call it with the same `idempotency_key`, only one status will
        be created.

        Pass a datetime as `scheduled_at` to schedule the toot for a specific time
        (the time must be at least 5 minutes into the future). If this is passed,
        status_post returns a :ref:`scheduled status dict <scheduled status dict>` instead.

        Pass `poll` to attach a poll to the status. An appropriate object can be
        constructed using :ref:`make_poll() <make_poll()>` . Note that as of Mastodon version
        2.8.2, you can only have either media or a poll attached, not both at
        the same time.

        **Specific to "pleroma" feature set:**: Specify `content_type` to set
        the content type of your post on Pleroma. It accepts 'text/plain' (default),
        'text/markdown', 'text/html' and 'text/bbcode'. This parameter is not
        supported on Mastodon servers, but will be safely ignored if set.

        **Specific to "fedibird" feature set:**: The `quote_id` parameter is
        a non-standard extension that specifies the id of a quoted status.

        Returns a :ref:`status dict <status dict>` with the new status.
        """
        return self.__status_internal( 
            status, 
            in_reply_to_id, 
            media_ids, 
            sensitive, 
            visibility, 
            spoiler_text, 
            language, 
            idempotency_key, 
            content_type, 
            scheduled_at, 
            poll, 
            quote_id, 
            edit=None
        )

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def toot(self, status):
        """
        Synonym for :ref:`status_post() <status_post()>` that only takes the status text as input.

        Usage in production code is not recommended.

        Returns a :ref:`status dict <status dict>` with the new status.
        """
        return self.status_post(status)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS)
    def status_update(self, id, status = None, spoiler_text = None, sensitive = None, media_ids = None, poll = None):
        """
        Edit a status. The meanings of the fields are largely the same as in :ref:`status_post() <status_post()>`,
        though not every field can be edited.

        Note that editing a poll will reset the votes.
        """
        return self.__status_internal(
            status = status, 
            media_ids = media_ids, 
            sensitive = sensitive, 
            spoiler_text = spoiler_text, 
            poll = poll, 
            edit = id
        ) 

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS_EDIT)
    def status_history(self, id):
        """
        Returns the edit history of a status as a list of :ref:`status edit dicts <status edit dicts>`, starting
        from the original form. Note that this means that a status that has been edited
        once will have *two* entries in this list, a status that has been edited twice
        will have three, and so on.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', "/api/v1/statuses/{0}/history".format(str(id)))

    def status_source(self, id):
        """
        Returns the source of a status for editing.

        Return value is a dictionary containing exactly the parameters you could pass to
        :ref:`status_update() <status_update()>` to change nothing about the status, except `status` is `text`
        instead.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', "/api/v1/statuses/{0}/source".format(str(id)))

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def status_reply(self, to_status, status, in_reply_to_id=None, media_ids=None,
                     sensitive=False, visibility=None, spoiler_text=None,
                     language=None, idempotency_key=None, content_type=None,
                     scheduled_at=None, poll=None, untag=False):
        """
        Helper function - acts like status_post, but prepends the name of all
        the users that are being replied to to the status text and retains
        CW and visibility if not explicitly overridden.

        Set `untag` to True if you want the reply to only go to the user you
        are replying to, removing every other mentioned user from the
        conversation.
        """
        keyword_args = locals()
        del keyword_args["self"]
        del keyword_args["to_status"]
        del keyword_args["untag"]

        user_id = self.__get_logged_in_id()

        # Determine users to mention
        mentioned_accounts = collections.OrderedDict()
        mentioned_accounts[to_status.account.id] = to_status.account.acct

        if not untag:
            for account in to_status.mentions:
                if account.id != user_id and not account.id in mentioned_accounts.keys():
                    mentioned_accounts[account.id] = account.acct

        # Join into one piece of text. The space is added inside because of self-replies.
        status = "".join(map(lambda x: "@" + x + " ",
                         mentioned_accounts.values())) + status

        # Retain visibility / cw
        if visibility is None and 'visibility' in to_status:
            visibility = to_status.visibility
        if spoiler_text is None and 'spoiler_text' in to_status:
            spoiler_text = to_status.spoiler_text

        keyword_args["status"] = status
        keyword_args["visibility"] = visibility
        keyword_args["spoiler_text"] = spoiler_text
        keyword_args["in_reply_to_id"] = to_status.id
        return self.status_post(**keyword_args)

    @api_version("2.8.0", "2.8.0", _DICT_VERSION_POLL)
    def make_poll(self, options, expires_in, multiple=False, hide_totals=False):
        """
        Generate a poll object that can be passed as the `poll` option when posting a status.

        options is an array of strings with the poll options (Maximum, by default: 4),
        expires_in is the time in seconds for which the poll should be open.
        Set multiple to True to allow people to choose more than one answer. Set
        hide_totals to True to hide the results of the poll until it has expired.
        """
        poll_params = locals()
        del poll_params["self"]
        return poll_params

    @api_version("1.0.0", "1.0.0", "1.0.0")
    def status_delete(self, id):
        """
        Delete a status

        Returns the now-deleted status, with an added "source" attribute that contains
        the text that was used to compose this status (this can be used to power
        "delete and redraft" functionality)
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}'.format(str(id))
        return self.__api_request('DELETE', url)

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_reblog(self, id, visibility=None):
        """
        Reblog / boost a status.

        The visibility parameter functions the same as in :ref:`status_post() <status_post()>` and
        allows you to reduce the visibility of a reblogged status.

        Returns a :ref:`status dict <status dict>` with a new status that wraps around the reblogged one.
        """
        params = self.__generate_params(locals(), ['id'])
        valid_visibilities = ['private', 'public', 'unlisted', 'direct']
        if 'visibility' in params:
            params['visibility'] = params['visibility'].lower()
            if params['visibility'] not in valid_visibilities:
                raise ValueError('Invalid visibility value! Acceptable '
                                 'values are %s' % valid_visibilities)

        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/reblog'.format(str(id))
        return self.__api_request('POST', url, params)

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_unreblog(self, id):
        """
        Un-reblog a status.

        Returns a :ref:`status dict <status dict>` with the status that used to be reblogged.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unreblog'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_favourite(self, id):
        """
        Favourite a status.

        Returns a :ref:`status dict <status dict>` with the favourited status.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/favourite'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_unfavourite(self, id):
        """
        Un-favourite a status.

        Returns a :ref:`status dict <status dict>` with the un-favourited status.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unfavourite'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.4.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_mute(self, id):
        """
        Mute notifications for a status.

        Returns a :ref:`status dict <status dict>` with the now muted status
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/mute'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.4.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_unmute(self, id):
        """
        Unmute notifications for a status.

        Returns a :ref:`status dict <status dict>` with the status that used to be muted.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unmute'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_STATUS)
    def status_pin(self, id):
        """
        Pin a status for the logged-in user.

        Returns a :ref:`status dict <status dict>` with the now pinned status
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/pin'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_STATUS)
    def status_unpin(self, id):
        """
        Unpin a pinned status for the logged-in user.

        Returns a :ref:`status dict <status dict>` with the status that used to be pinned.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unpin'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("3.1.0", "3.1.0", _DICT_VERSION_STATUS)
    def status_bookmark(self, id):
        """
        Bookmark a status as the logged-in user.

        Returns a :ref:`status dict <status dict>` with the now bookmarked status
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/bookmark'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("3.1.0", "3.1.0", _DICT_VERSION_STATUS)
    def status_unbookmark(self, id):
        """
        Unbookmark a bookmarked status for the logged-in user.

        Returns a :ref:`status dict <status dict>` with the status that used to be bookmarked.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unbookmark'.format(str(id))
        return self.__api_request('POST', url)

    ###
    # Writing data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0", _DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_status_update(self, id, scheduled_at):
        """
        Update the scheduled time of a scheduled status.

        New time must be at least 5 minutes into the future.

        Returns a :ref:`scheduled status dict <scheduled status dict>`
        """
        scheduled_at = self.__consistent_isoformat_utc(scheduled_at)
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/scheduled_statuses/{0}'.format(str(id))
        return self.__api_request('PUT', url, params)

    @api_version("2.7.0", "2.7.0", "2.7.0")
    def scheduled_status_delete(self, id):
        """
        Deletes a scheduled status.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/scheduled_statuses/{0}'.format(str(id))
        self.__api_request('DELETE', url)

    ###
    # Writing data: Polls
    ###
    @api_version("2.8.0", "2.8.0", _DICT_VERSION_POLL)
    def poll_vote(self, id, choices):
        """
        Vote in the given poll.

        `choices` is the index of the choice you wish to register a vote for
        (i.e. its index in the corresponding polls `options` field. In case
        of a poll that allows selection of more than one option, a list of
        indices can be passed.

        You can only submit choices for any given poll once in case of
        single-option polls, or only once per option in case of multi-option
        polls.

        Returns the updated :ref:`poll dict <poll dict>`
        """
        id = self.__unpack_id(id)
        if not isinstance(choices, list):
            choices = [choices]
        params = self.__generate_params(locals(), ['id'])

        url = '/api/v1/polls/{0}/votes'.format(id)
        self.__api_request('POST', url, params)

    ###
    # Writing data: Notifications
    ###

    @api_version("1.0.0", "1.0.0", "1.0.0")
    def notifications_clear(self):
        """
        Clear out a user's notifications
        """
        self.__api_request('POST', '/api/v1/notifications/clear')

    @api_version("1.3.0", "2.9.2", "2.9.2")
    def notifications_dismiss(self, id):
        """
        Deletes a single notification
        """
        id = self.__unpack_id(id)

        if self.verify_minimum_version("2.9.2", cached=True):
            url = '/api/v1/notifications/{0}/dismiss'.format(str(id))
            self.__api_request('POST', url)
        else:
            params = self.__generate_params(locals())
            self.__api_request('POST', '/api/v1/notifications/dismiss', params)

    ###
    # Writing data: Conversations
    ###
    @api_version("2.6.0", "2.6.0", _DICT_VERSION_CONVERSATION)
    def conversations_read(self, id):
        """
        Marks a single conversation as read.

        Returns the updated :ref:`conversation dict <conversation dict>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/conversations/{0}/read'.format(str(id))
        return self.__api_request('POST', url)

    ###
    # Writing data: Accounts
    ###
    @api_version("1.0.0", "3.3.0", _DICT_VERSION_RELATIONSHIP)
    def account_follow(self, id, reblogs=True, notify=False):
        """
        Follow a user.

        Set `reblogs` to False to hide boosts by the followed user.
        Set `notify` to True to get a notification every time the followed user posts.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])

        if params["reblogs"] is None:
            del params["reblogs"]

        url = '/api/v1/accounts/{0}/follow'.format(str(id))
        return self.__api_request('POST', url, params)

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def follows(self, uri):
        """
        Follow a remote user by uri (username@domain).

        Returns a :ref:`account dict <account dict>`.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/follows', params)

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_unfollow(self, id):
        """
        Unfollow a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/accounts/{0}/unfollow'.format(str(id)))

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_RELATIONSHIP)
    def account_remove_from_followers(self, id):
        """
        Remove a user from the logged in users followers (i.e. make them unfollow the logged in
        user / "softblock" them).

        Returns a :ref:`relationship dict <relationship dict>` reflecting the updated following status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/accounts/{0}/remove_from_followers'.format(str(id)))
    

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_block(self, id):
        """
        Block a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/block'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_unblock(self, id):
        """
        Unblock a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/unblock'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.1.0", "2.4.3", _DICT_VERSION_RELATIONSHIP)
    def account_mute(self, id, notifications=True, duration=None):
        """
        Mute a user.

        Set `notifications` to False to receive notifications even though the user is
        muted from timelines. Pass a `duration` in seconds to have Mastodon automatically
        lift the mute after that many seconds.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/mute'.format(str(id))
        return self.__api_request('POST', url, params)

    @api_version("1.1.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_unmute(self, id):
        """
        Unmute a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/unmute'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.1.1", "3.1.0", _DICT_VERSION_ACCOUNT)
    def account_update_credentials(self, display_name=None, note=None,
                                   avatar=None, avatar_mime_type=None,
                                   header=None, header_mime_type=None,
                                   locked=None, bot=None,
                                   discoverable=None, fields=None):
        """
        Update the profile for the currently logged-in user.

        `note` is the user's bio.

        `avatar` and 'header' are images. As with media uploads, it is possible to either
        pass image data and a mime type, or a filename of an image file, for either.

        `locked` specifies whether the user needs to manually approve follow requests.

        `bot` specifies whether the user should be set to a bot.

        `discoverable` specifies whether the user should appear in the user directory.

        `fields` can be a list of up to four name-value pairs (specified as tuples) to
        appear as semi-structured information in the user's profile.

        Returns the updated `account dict` of the logged-in user.
        """
        params_initial = collections.OrderedDict(locals())

        # Convert fields
        if fields is not None:
            if len(fields) > 4:
                raise MastodonIllegalArgumentError(
                    'A maximum of four fields are allowed.')

            fields_attributes = []
            for idx, (field_name, field_value) in enumerate(fields):
                params_initial['fields_attributes[' +
                               str(idx) + '][name]'] = field_name
                params_initial['fields_attributes[' +
                               str(idx) + '][value]'] = field_value

        # Clean up params
        for param in ["avatar", "avatar_mime_type", "header", "header_mime_type", "fields"]:
            if param in params_initial:
                del params_initial[param]

        # Create file info
        files = {}
        if avatar is not None:
            files["avatar"] = self.__load_media_file(avatar, avatar_mime_type)
        if header is not None:
            files["header"] = self.__load_media_file(header, header_mime_type)

        params = self.__generate_params(params_initial)
        return self.__api_request('PATCH', '/api/v1/accounts/update_credentials', params, files=files)

    @api_version("2.5.0", "2.5.0", _DICT_VERSION_RELATIONSHIP)
    def account_pin(self, id):
        """
        Pin / endorse a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/pin'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("2.5.0", "2.5.0", _DICT_VERSION_RELATIONSHIP)
    def account_unpin(self, id):
        """
        Unpin / un-endorse a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/unpin'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("3.2.0", "3.2.0", _DICT_VERSION_RELATIONSHIP)
    def account_note_set(self, id, comment):
        """
        Set a note (visible to the logged in user only) for the given account.

        Returns a :ref:`status dict <status dict>` with the `note` updated.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])
        return self.__api_request('POST', '/api/v1/accounts/{0}/note'.format(str(id)), params)

    @api_version("3.3.0", "3.3.0", _DICT_VERSION_HASHTAG)
    def account_featured_tags(self, id):
        """
        Get an account's featured hashtags.

        Returns a list of :ref:`hashtag dicts <hashtag dicts>` (NOT `featured tag dicts`_).
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', '/api/v1/accounts/{0}/featured_tags'.format(str(id)))

    ###
    # Writing data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tag_create(self, name):
        """
        Creates a new featured hashtag displayed on the logged-in user's profile.

        Returns a :ref:`featured tag dict <featured tag dict>` with the newly featured tag.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/featured_tags', params)

    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tag_delete(self, id):
        """
        Deletes one of the logged-in user's featured hashtags.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/featured_tags/{0}'.format(str(id))
        self.__api_request('DELETE', url)

    ###
    # Writing data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filter_create(self, phrase, context, irreversible=False, whole_word=True, expires_in=None):
        """
        Creates a new keyword filter. `phrase` is the phrase that should be
        filtered out, `context` specifies from where to filter the keywords.
        Valid contexts are 'home', 'notifications', 'public' and 'thread'.

        Set `irreversible` to True if you want the filter to just delete statuses
        server side. This works only for the 'home' and 'notifications' contexts.

        Set `whole_word` to False if you want to allow filter matches to
        start or end within a word, not only at word boundaries.

        Set `expires_in` to specify for how many seconds the filter should be
        kept around.

        Returns the :ref:`filter dict <filter dict>` of the newly created filter.
        """
        params = self.__generate_params(locals())

        for context_val in context:
            if not context_val in ['home', 'notifications', 'public', 'thread']:
                raise MastodonIllegalArgumentError('Invalid filter context.')

        return self.__api_request('POST', '/api/v1/filters', params)

    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filter_update(self, id, phrase=None, context=None, irreversible=None, whole_word=None, expires_in=None):
        """
        Updates the filter with the given `id`. Parameters are the same
        as in `filter_create()`.

        Returns the :ref:`filter dict <filter dict>` of the updated filter.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/filters/{0}'.format(str(id))
        return self.__api_request('PUT', url, params)

    @api_version("2.4.3", "2.4.3", "2.4.3")
    def filter_delete(self, id):
        """
        Deletes the filter with the given `id`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/filters/{0}'.format(str(id))
        self.__api_request('DELETE', url)

    ###
    # Writing data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_ACCOUNT)
    def suggestion_delete(self, account_id):
        """
        Remove the user with the given `account_id` from the follow suggestions.
        """
        account_id = self.__unpack_id(account_id)
        url = '/api/v1/suggestions/{0}'.format(str(account_id))
        self.__api_request('DELETE', url)

    ###
    # Writing data: Lists
    ###
    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def list_create(self, title):
        """
        Create a new list with the given `title`.

        Returns the :ref:`list dict <list dict>` of the created list.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/lists', params)

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def list_update(self, id, title):
        """
        Update info about a list, where "info" is really the lists `title`.

        Returns the :ref:`list dict <list dict>` of the modified list.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', '/api/v1/lists/{0}'.format(id), params)

    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_delete(self, id):
        """
        Delete a list.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', '/api/v1/lists/{0}'.format(id))

    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_accounts_add(self, id, account_ids):
        """
        Add the account(s) given in `account_ids` to the list.
        """
        id = self.__unpack_id(id)

        if not isinstance(account_ids, list):
            account_ids = [account_ids]
        account_ids = list(map(lambda x: self.__unpack_id(x), account_ids))

        params = self.__generate_params(locals(), ['id'])
        self.__api_request(
            'POST', '/api/v1/lists/{0}/accounts'.format(id), params)

    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_accounts_delete(self, id, account_ids):
        """
        Remove the account(s) given in `account_ids` from the list.
        """
        id = self.__unpack_id(id)

        if not isinstance(account_ids, list):
            account_ids = [account_ids]
        account_ids = list(map(lambda x: self.__unpack_id(x), account_ids))

        params = self.__generate_params(locals(), ['id'])
        self.__api_request(
            'DELETE', '/api/v1/lists/{0}/accounts'.format(id), params)

    ###
    # Writing data: Reports
    ###
    @api_version("1.1.0", "3.5.0", _DICT_VERSION_REPORT)
    def report(self, account_id, status_ids=None, comment=None, forward=False, category=None, rule_ids=None):
        """
        Report statuses to the instances administrators.

        Accepts a list of toot IDs associated with the report, and a comment.

        Starting with Mastodon 3.5.0, you can also pass a `category` (one out of
        "spam", "violation" or "other") and `rule_ids` (a list of rule IDs corresponding
        to the rules returned by the :ref:`instance() <instance()>` API).

        Set `forward` to True to forward a report of a remote user to that users
        instance as well as sending it to the instance local administrators.

        Returns a :ref:`report dict <report dict>`.
        """
        if category is not None and not category in ["spam", "violation", "other"]:
            raise MastodonIllegalArgumentError("Invalid report category (must be spam, violation or other)")

        account_id = self.__unpack_id(account_id)

        if status_ids is not None:
            if not isinstance(status_ids, list):
                status_ids = [status_ids]
            status_ids = list(map(lambda x: self.__unpack_id(x), status_ids))

        params_initial = locals()
        if not forward:
            del params_initial['forward']

        params = self.__generate_params(params_initial)
        return self.__api_request('POST', '/api/v1/reports/', params)

    ###
    # Writing data: Follow requests
    ###
    @api_version("1.0.0", "3.0.0", _DICT_VERSION_RELATIONSHIP)
    def follow_request_authorize(self, id):
        """
        Accept an incoming follow request.

        Returns the updated :ref:`relationship dict <relationship dict>` for the requesting account.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/follow_requests/{0}/authorize'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "3.0.0", _DICT_VERSION_RELATIONSHIP)
    def follow_request_reject(self, id):
        """
        Reject an incoming follow request.

        Returns the updated :ref:`relationship dict <relationship dict>` for the requesting account.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/follow_requests/{0}/reject'.format(str(id))
        return self.__api_request('POST', url)

    ###
    # Writing data: Media
    ###
    @api_version("1.0.0", "3.2.0", _DICT_VERSION_MEDIA)
    def media_post(self, media_file, mime_type=None, description=None, focus=None, file_name=None, thumbnail=None, thumbnail_mime_type=None, synchronous=False):
        """
        Post an image, video or audio file. `media_file` can either be data or
        a file name. If data is passed directly, the mime type has to be specified
        manually, otherwise, it is determined from the file name. `focus` should be a tuple
        of floats between -1 and 1, giving the x and y coordinates of the images
        focus point for cropping (with the origin being the images center).

        Throws a `MastodonIllegalArgumentError` if the mime type of the
        passed data or file can not be determined properly.

        `file_name` can be specified to upload a file with the given name,
        which is ignored by Mastodon, but some other Fediverse server software
        will display it. If no name is specified, a random name will be generated.
        The filename of a file specified in media_file will be ignored.

        Starting with Mastodon 3.2.0, `thumbnail` can be specified in the same way as `media_file`
        to upload a custom thumbnail image for audio and video files.

        Returns a :ref:`media dict <media dict>`. This contains the id that can be used in
        status_post to attach the media file to a toot.

        When using the v2 API (post Mastodon version 3.1.4), the `url` in the
        returned dict will be `null`, since attachments are processed
        asynchronously. You can fetch an updated dict using `media`. Pass
        "synchronous" to emulate the old behaviour. Not recommended, inefficient
        and deprecated, you know the deal.
        """
        files = {'file': self.__load_media_file(
            media_file, mime_type, file_name)}

        if focus is not None:
            focus = str(focus[0]) + "," + str(focus[1])

        if thumbnail is not None:
            if not self.verify_minimum_version("3.2.0", cached=True):
                raise MastodonVersionError(
                    'Thumbnail requires version > 3.2.0')
            files["thumbnail"] = self.__load_media_file(
                thumbnail, thumbnail_mime_type)

        # Disambiguate URL by version
        if self.verify_minimum_version("3.1.4", cached=True):
            ret_dict = self.__api_request(
                'POST', '/api/v2/media', files=files, params={'description': description, 'focus': focus})
        else:
            ret_dict = self.__api_request(
                'POST', '/api/v1/media', files=files, params={'description': description, 'focus': focus})

        # Wait for processing?
        if synchronous:
            if self.verify_minimum_version("3.1.4"):
                while not "url" in ret_dict or ret_dict.url is None:
                    try:
                        ret_dict = self.media(ret_dict)
                        time.sleep(1.0)
                    except:
                        raise MastodonAPIError(
                            "Attachment could not be processed")
            else:
                # Old version always waits
                return ret_dict

        return ret_dict

    @api_version("2.3.0", "3.2.0", _DICT_VERSION_MEDIA)
    def media_update(self, id, description=None, focus=None, thumbnail=None, thumbnail_mime_type=None):
        """
        Update the metadata of the media file with the given `id`. `description` and
        `focus` and `thumbnail` are as in :ref:`media_post() <media_post()>` .

        Returns the updated :ref:`media dict <media dict>`.
        """
        id = self.__unpack_id(id)

        if focus is not None:
            focus = str(focus[0]) + "," + str(focus[1])

        params = self.__generate_params(
            locals(), ['id', 'thumbnail', 'thumbnail_mime_type'])

        if thumbnail is not None:
            if not self.verify_minimum_version("3.2.0", cached=True):
                raise MastodonVersionError(
                    'Thumbnail requires version > 3.2.0')
            files = {"thumbnail": self.__load_media_file(
                thumbnail, thumbnail_mime_type)}
            return self.__api_request('PUT', '/api/v1/media/{0}'.format(str(id)), params, files=files)
        else:
            return self.__api_request('PUT', '/api/v1/media/{0}'.format(str(id)), params)

    @api_version("3.1.4", "3.1.4", _DICT_VERSION_MEDIA)
    def media(self, id):
        """
        Get the updated JSON for one non-attached / in progress media upload belonging
        to the logged-in user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', '/api/v1/media/{0}'.format(str(id)))

    ###
    # Writing data: Domain blocks
    ###
    @api_version("1.4.0", "1.4.0", "1.4.0")
    def domain_block(self, domain=None):
        """
        Add a block for all statuses originating from the specified domain for the logged-in user.
        """
        params = self.__generate_params(locals())
        self.__api_request('POST', '/api/v1/domain_blocks', params)

    @api_version("1.4.0", "1.4.0", "1.4.0")
    def domain_unblock(self, domain=None):
        """
        Remove a domain block for the logged-in user.
        """
        params = self.__generate_params(locals())
        self.__api_request('DELETE', '/api/v1/domain_blocks', params)

    ##
    # Writing data: Read markers
    ##
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_MARKER)
    def markers_set(self, timelines, last_read_ids):
        """
        Set the "last read" marker(s) for the given timeline(s) to the given id(s)

        Note that if you give an invalid timeline name, this will silently do nothing.

        Returns a dict with the updated :ref:`read marker dicts <read marker dicts>`, keyed by timeline name.
        """
        if not isinstance(timelines, (list, tuple)):
            timelines = [timelines]

        if not isinstance(last_read_ids, (list, tuple)):
            last_read_ids = [last_read_ids]

        if len(last_read_ids) != len(timelines):
            raise MastodonIllegalArgumentError(
                "Number of specified timelines and ids must be the same")

        params = collections.OrderedDict()
        for timeline, last_read_id in zip(timelines, last_read_ids):
            params[timeline] = collections.OrderedDict()
            params[timeline]["last_read_id"] = self.__unpack_id(last_read_id)

        return self.__api_request('POST', '/api/v1/markers', params, use_json=True)

    ###
    # Writing data: Push subscriptions
    ###
    @api_version("2.4.0", "2.4.0", _DICT_VERSION_PUSH)
    def push_subscription_set(self, endpoint, encrypt_params, follow_events=None,
                              favourite_events=None, reblog_events=None,
                              mention_events=None, poll_events=None,
                              follow_request_events=None, status_events=None, policy='all'):
        """
        Sets up or modifies the push subscription the logged-in user has for this app.

        `endpoint` is the endpoint URL mastodon should call for pushes. Note that mastodon
        requires https for this URL. `encrypt_params` is a dict with key parameters that allow
        the server to encrypt data for you: A public key `pubkey` and a shared secret `auth`.
        You can generate this as well as the corresponding private key using the
        :ref:`push_subscription_generate_keys() <push_subscription_generate_keys()>` function.

        `policy` controls what sources will generate webpush events. Valid values are
        `all`, `none`, `follower` and `followed`.

        The rest of the parameters controls what kind of events you wish to subscribe to.

        Returns a :ref:`push subscription dict <push subscription dict>`.
        """
        if not policy in ['all', 'none', 'follower', 'followed']:
            raise MastodonIllegalArgumentError("Valid values for policy are 'all', 'none', 'follower' or 'followed'.")

        endpoint = Mastodon.__protocolize(endpoint)

        push_pubkey_b64 = base64.b64encode(encrypt_params['pubkey'])
        push_auth_b64 = base64.b64encode(encrypt_params['auth'])

        params = {
            'subscription[endpoint]': endpoint,
            'subscription[keys][p256dh]': push_pubkey_b64,
            'subscription[keys][auth]': push_auth_b64,
            'policy': policy
        }

        if follow_events is not None:
            params['data[alerts][follow]'] = follow_events

        if favourite_events is not None:
            params['data[alerts][favourite]'] = favourite_events

        if reblog_events is not None:
            params['data[alerts][reblog]'] = reblog_events

        if mention_events is not None:
            params['data[alerts][mention]'] = mention_events

        if poll_events is not None:
            params['data[alerts][poll]'] = poll_events

        if follow_request_events is not None:
            params['data[alerts][follow_request]'] = follow_request_events

        if follow_request_events is not None:
            params['data[alerts][status]'] = status_events

        # Canonicalize booleans
        params = self.__generate_params(params)

        return self.__api_request('POST', '/api/v1/push/subscription', params)

    @api_version("2.4.0", "2.4.0", _DICT_VERSION_PUSH)
    def push_subscription_update(self, follow_events=None,
                                 favourite_events=None, reblog_events=None,
                                 mention_events=None, poll_events=None,
                                 follow_request_events=None):
        """
        Modifies what kind of events the app wishes to subscribe to.

        Returns the updated :ref:`push subscription dict <push subscription dict>`.
        """
        params = {}

        if follow_events is not None:
            params['data[alerts][follow]'] = follow_events

        if favourite_events is not None:
            params['data[alerts][favourite]'] = favourite_events

        if reblog_events is not None:
            params['data[alerts][reblog]'] = reblog_events

        if mention_events is not None:
            params['data[alerts][mention]'] = mention_events

        if poll_events is not None:
            params['data[alerts][poll]'] = poll_events

        if follow_request_events is not None:
            params['data[alerts][follow_request]'] = follow_request_events

        # Canonicalize booleans
        params = self.__generate_params(params)

        return self.__api_request('PUT', '/api/v1/push/subscription', params)

    @api_version("2.4.0", "2.4.0", "2.4.0")
    def push_subscription_delete(self):
        """
        Remove the current push subscription the logged-in user has for this app.
        """
        self.__api_request('DELETE', '/api/v1/push/subscription')

    ###
    # Writing data: Annoucements
    ###
    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_dismiss(self, id):
        """
        Set the given annoucement to read.
        """
        id = self.__unpack_id(id)

        url = '/api/v1/announcements/{0}/dismiss'.format(str(id))
        self.__api_request('POST', url)

    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_reaction_create(self, id, reaction):
        """
        Add a reaction to an announcement. `reaction` can either be a unicode emoji
        or the name of one of the instances custom emoji.

        Will throw an API error if the reaction name is not one of the allowed things
        or when trying to add a reaction that the user has already added (adding a
        reaction that a different user added is legal and increments the count).
        """
        id = self.__unpack_id(id)

        url = '/api/v1/announcements/{0}/reactions/{1}'.format(
            str(id), reaction)
        self.__api_request('PUT', url)

    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_reaction_delete(self, id, reaction):
        """
        Remove a reaction to an announcement.

        Will throw an API error if the reaction does not exist.
        """
        id = self.__unpack_id(id)

        url = '/api/v1/announcements/{0}/reactions/{1}'.format(
            str(id), reaction)
        self.__api_request('DELETE', url)

    ###
    # Moderation API
    ###
    @api_version("2.9.1", "4.0.0", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_accounts_v2(self, origin=None, by_domain=None, status=None, username=None, display_name=None, email=None, ip=None, 
                            permissions=None, invited_by=None, role_ids=None, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches a list of accounts that match given criteria. By default, local accounts are returned.

        * Set `origin` to "local" or "remote" to get only local or remote accounts.
        * Set `by_domain` to a domain to get only accounts from that domain.
        * Set `status` to one of "active", "pending", "disabled", "silenced" or "suspended" to get only accounts with that moderation status (default: active)
        * Set `username` to a string to get only accounts whose username contains this string.
        * Set `display_name` to a string to get only accounts whose display name contains this string.
        * Set `email` to an email to get only accounts with that email (this only works on local accounts).
        * Set `ip` to an ip (as a string, standard v4/v6 notation) to get only accounts whose last active ip is that ip (this only works on local accounts).
        * Set `permissions` to "staff" to only get accounts with staff permissions.
        * Set `invited_by` to an account id to get only accounts invited by this user.
        * Set `role_ids` to a list of role IDs to get only accounts with those roles.

        Returns a list of :ref:`admin account dicts <admin account dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        if role_ids is not None:
            if not isinstance(role_ids, list):
                role_ids = [role_ids]
            role_ids = list(map(self.__unpack_id, role_ids))

        if invited_by is not None:
            invited_by = self.__unpack_id(invited_by)

        if permissions is not None and not permissions in ["staff"]:
            raise MastodonIllegalArgumentError("Permissions must be staff if passed")

        if origin is not None and not origin in ["local", "remote"]:
            raise MastodonIllegalArgumentError("Origin must be local or remote")

        if status is not None and not status in ["active", "pending", "disabled", "silenced", "suspended"]:
            raise MastodonIllegalArgumentError("Status must be local or active, pending, disabled, silenced or suspended")

        if not by_domain is None:
            by_domain = self.__deprotocolize(by_domain)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v2/admin/accounts', params)

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_accounts(self, remote=False, by_domain=None, status='active', username=None, display_name=None, email=None, ip=None, staff_only=False, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Currently a synonym for admin_accounts_v1, now deprecated. You are strongly encouraged to use admin_accounts_v2 instead, since this one is kind of bad. 
        
        !!!!! This function may be switched to calling the v2 API in the future. This is your warning. If you want to keep using v1, use it explicitly. !!!!!
        """
        return self.admin_accounts_v1(
            remote=remote,
            by_domain=by_domain,
            status=status,
            username=username,
            display_name=display_name,
            email=email,
            ip=ip,
            staff_only=staff_only,
            max_id=max_id,
            min_id=min_id,
            since_id=since_id
        )

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_accounts_v1(self, remote=False, by_domain=None, status='active', username=None, display_name=None, email=None, ip=None, staff_only=False, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches a list of accounts that match given criteria. By default, local accounts are returned.

        * Set `remote` to True to get remote accounts, otherwise local accounts are returned (default: local accounts)
        * Set `by_domain` to a domain to get only accounts from that domain.
        * Set `status` to one of "active", "pending", "disabled", "silenced" or "suspended" to get only accounts with that moderation status (default: active)
        * Set `username` to a string to get only accounts whose username contains this string.
        * Set `display_name` to a string to get only accounts whose display name contains this string.
        * Set `email` to an email to get only accounts with that email (this only works on local accounts).
        * Set `ip` to an ip (as a string, standard v4/v6 notation) to get only accounts whose last active ip is that ip (this only works on local accounts).
        * Set `staff_only` to True to only get staff accounts (this only works on local accounts).

        Note that setting the boolean parameters to False does not mean "give me users to which this does not apply" but
        instead means "I do not care if users have this attribute".

        Deprecated in Mastodon version 3.5.0.

        Returns a list of :ref:`admin account dicts <admin account dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['remote', 'status', 'staff_only'])

        if remote:
            params["remote"] = True

        mod_statuses = ["active", "pending", "disabled", "silenced", "suspended"]
        if not status in mod_statuses:
            raise ValueError("Invalid moderation status requested.")

        if staff_only:
            params["staff"] = True

        for mod_status in mod_statuses:
            if status == mod_status:
                params[status] = True

        if not by_domain is None:
            by_domain = self.__deprotocolize(by_domain)

        return self.__api_request('GET', '/api/v1/admin/accounts', params)

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account(self, id):
        """
        Fetches a single :ref:`admin account dict <admin account dict>` for the user with the given id.

        Returns that dict.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', '/api/v1/admin/accounts/{0}'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_enable(self, id):
        """
        Reenables login for a local account for which login has been disabled.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/enable'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_approve(self, id):
        """
        Approves a pending account.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/approve'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_reject(self, id):
        """
        Rejects and deletes a pending account.

        Returns the updated :ref:`admin account dict <admin account dict>` for the account that is now gone.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/reject'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsilence(self, id):
        """
        Unsilences an account.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/unsilence'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsuspend(self, id):
        """
        Unsuspends an account.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/unsuspend'.format(id))

    @api_version("3.3.0", "3.3.0", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_delete(self, id):
        """
        Delete a local user account.

        The deleted accounts :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('DELETE', '/api/v1/admin/accounts/{0}'.format(id))

    @api_version("3.3.0", "3.3.0", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsensitive(self, id):
        """
        Unmark an account as force-sensitive.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/unsensitive'.format(id))

    @api_version("2.9.1", "2.9.1", "2.9.1")
    def admin_account_moderate(self, id, action=None, report_id=None, warning_preset_id=None, text=None, send_email_notification=True):
        """
        Perform a moderation action on an account.

        Valid actions are:
            * "disable" - for a local user, disable login.
            * "silence" - hide the users posts from all public timelines.
            * "suspend" - irreversibly delete all the user's posts, past and future.
            * "sensitive" - forcce an accounts media visibility to always be sensitive.

        If no action is specified, the user is only issued a warning.

        Specify the id of a report as `report_id` to close the report with this moderation action as the resolution.
        Specify `warning_preset_id` to use a warning preset as the notification text to the user, or `text` to specify text directly.
        If both are specified, they are concatenated (preset first). Note that there is currently no API to retrieve or create
        warning presets.

        Set `send_email_notification` to False to not send the user an email notification informing them of the moderation action.
        """
        if action is None:
            action = "none"

        if not send_email_notification:
            send_email_notification = None

        id = self.__unpack_id(id)
        if report_id is not None:
            report_id = self.__unpack_id(report_id)

        params = self.__generate_params(locals(), ['id', 'action'])

        params["type"] = action

        self.__api_request(
            'POST', '/api/v1/admin/accounts/{0}/action'.format(id), params)

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_reports(self, resolved=False, account_id=None, target_account_id=None, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches the list of reports.

        Set `resolved` to True to search for resolved reports. `account_id` and `target_account_id`
        can be used to get reports filed by or about a specific user.

        Returns a list of :ref:`report dicts <report dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        if account_id is not None:
            account_id = self.__unpack_id(account_id)

        if target_account_id is not None:
            target_account_id = self.__unpack_id(target_account_id)

        if not resolved:
            resolved = None

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/reports', params)

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report(self, id):
        """
        Fetches the report with the given id.

        Returns a :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', '/api/v1/admin/reports/{0}'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_assign(self, id):
        """
        Assigns the given report to the logged-in user.

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/assign_to_self'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_unassign(self, id):
        """
        Unassigns the given report from the logged-in user.

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/unassign'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_reopen(self, id):
        """
        Reopens a closed report.

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/reopen'.format(id))

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_resolve(self, id):
        """
        Marks a report as resolved (without taking any action).

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/resolve'.format(id))

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_HASHTAG)
    def admin_trending_tags(self, limit=None):
        """
        Admin version of :ref:`trending_tags() <trending_tags()>`. Includes unapproved tags.

        Returns a list of :ref:`hashtag dicts <hashtag dicts>`, sorted by the instance's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/tags', params)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS)
    def admin_trending_statuses(self):
        """
        Admin version of :ref:`trending_statuses() <trending_statuses()>`. Includes unapproved tags.

        Returns a list of :ref:`status dicts <status dicts>`, sorted by the instance's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/statuses', params)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_CARD)
    def admin_trending_links(self):
        """
        Admin version of :ref:`trending_links() <trending_links()>`. Includes unapproved tags.

        Returns a list of :ref:`card dicts <card dicts>`, sorted by the instance's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/links', params)

    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_domain_blocks(self, id=None, limit:int=None):
        """
        Fetches a list of blocked domains. Requires scope `admin:read:domain_blocks`.

        Provide an `id` to fetch a specific domain block based on its database id.

        Returns a list of :ref:`admin domain block dicts <admin domain block dicts>`, raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is not None:
            id = self.__unpack_id(id)
            return self.__api_request('GET', '/api/v1/admin/domain_blocks/{0}'.format(id))
        else:
            params = self.__generate_params(locals(),['limit'])
            return self.__api_request('GET', '/api/v1/admin/domain_blocks/', params)
    
    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_create_domain_block(self, domain:str, severity:str=None, reject_media:bool=None, reject_reports:bool=None, private_comment:str=None, public_comment:str=None, obfuscate:bool=None):
        """
        Perform a moderation action on a domain. Requires scope `admin:write:domain_blocks`.

        Valid severities are:
            * "silence" - hide all posts from federated timelines and do not show notifications to local users from the remote instance's users unless they are following the remote user. 
            * "suspend" - deny interactions with this instance going forward. This action is reversible.
            * "limit" - generally used with reject_media=true to force reject media from an instance without silencing or suspending..

        If no action is specified, the domain is only silenced.
        `domain` is the domain to block. Note that using the top level domain will also imapct all subdomains. ie, example.com will also impact subdomain.example.com.
        `reject_media` will not download remote media on to your local instance media storage.
        `reject_reports` ignores all reports from the remote instance.
        `private_comment` sets a private admin comment for the domain.
        `public_comment` sets a publicly available comment for this domain, which will be available to local users and may be available to everyone depending on your settings.
        `obfuscate` censors some part of the domain name. Useful if the domain name contains unwanted words like slurs.

        Returns the new domain block as an :ref:`admin domain block dict <admin domain block dict>`.
        """
        if domain is None:
            raise AttributeError("Must provide a domain to block a domain")
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/admin/domain_blocks/', params)

    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_update_domain_block(self, id, severity:str=None, reject_media:bool=None, reject_reports:bool=None, private_comment:str=None, public_comment:str=None, obfuscate:bool=None):
        """
        Modify existing moderation action on a domain. Requires scope `admin:write:domain_blocks`.

        Valid severities are:
            * "silence" - hide all posts from federated timelines and do not show notifications to local users from the remote instance's users unless they are following the remote user. 
            * "suspend" - deny interactions with this instance going forward. This action is reversible.
            * "limit" - generally used with reject_media=true to force reject media from an instance without silencing or suspending.

        If no action is specified, the domain is only silenced.
        `domain` is the domain to block. Note that using the top level domain will also imapct all subdomains. ie, example.com will also impact subdomain.example.com.
        `reject_media` will not download remote media on to your local instance media storage.
        `reject_reports` ignores all reports from the remote instance.
        `private_comment` sets a private admin comment for the domain.
        `public_comment` sets a publicly available comment for this domain, which will be available to local users and may be available to everyone depending on your settings.
        `obfuscate` censors some part of the domain name. Useful if the domain name contains unwanted words like slurs.

        Returns the modified domain block as an :ref:`admin domain block dict <admin domain block dict>`, raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is None:
            raise AttributeError("Must provide an id to modify the existing moderation actions on a given domain.")
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])
        return self.__api_request('PUT', '/api/v1/admin/domain_blocks/{0}'.format(id), params)

    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_delete_domain_block(self, id=None):
        """
        Removes moderation action against a given domain. Requires scope `admin:write:domain_blocks`.

        Provide an `id` to remove a specific domain block based on its database id.

        Raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is not None:
            id = self.__unpack_id(id)
            self.__api_request('DELETE', '/api/v1/admin/domain_blocks/{0}'.format(id))
        else:
            raise AttributeError("You must provide an id of an existing domain block to remove it.")

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_ADMIN_MEASURE)
    def admin_measures(self, start_at, end_at, active_users=False, new_users=False, interactions=False, opened_reports = False, resolved_reports=False,
                        tag_accounts=None, tag_uses=None, tag_servers=None, instance_accounts=None, instance_media_attachments=None, instance_reports=None,
                        instance_statuses=None, instance_follows=None, instance_followers=None):
        """
        Retrieves numerical instance information for the time period (at day granularity) between `start_at` and `end_at`.

            * `active_users`: Pass true to retrieve the number of active users on your instance within the time period
            * `new_users`: Pass true to retrieve the number of users who joined your instance within the time period
            * `interactions`: Pass true to retrieve the number of interactions (favourites, boosts, replies) on local statuses within the time period
            * `opened_reports`: Pass true to retrieve the number of reports filed within the time period
            * `resolved_reports` = Pass true to retrieve the number of reports resolved within the time period
            * `tag_accounts`: Pass a tag ID to get the number of accounts which used that tag in at least one status within the time period
            * `tag_uses`: Pass a tag ID to get the number of statuses which used that tag within the time period
            * `tag_servers`: Pass a tag ID to to get the number of remote origin servers for statuses which used that tag within the time period
            * `instance_accounts`: Pass a domain to get the number of accounts originating from that remote domain within the time period
            * `instance_media_attachments`: Pass a domain to get the amount of space used by media attachments from that remote domain within the time period
            * `instance_reports`: Pass a domain to get the number of reports filed against accounts from that remote domain within the time period
            * `instance_statuses`: Pass a domain to get the number of statuses originating from that remote domain within the time period
            * `instance_follows`: Pass a domain to get the number of accounts from a remote domain followed by that local user within the time period
            * `instance_followers`: Pass a domain to get the number of local accounts followed by accounts from that remote domain within the time period

        This API call is relatively expensive - watch your servers load if you want to get a lot of statistical data. Especially the instance_statuses stats
        might take a long time to compute and, in fact, time out.

        There is currently no way to get tag IDs implemented in Mastodon.py, because the Mastodon public API does not implement one. This will be fixed in a future
        release.

        Returns a list of :ref:`admin measure dicts <admin measure dicts>`.
        """
        params_init = locals()
        keys = []
        for key in ["active_users", "new_users", "interactions", "opened_reports", "resolved_reports"]:
            if params_init[key] == True:
                keys.append(key)
        
        params = {}
        for key in ["tag_accounts", "tag_uses", "tag_servers"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"id": self.__unpack_id(params_init[key])}
        for key in ["instance_accounts", "instance_media_attachments", "instance_reports", "instance_statuses", "instance_follows", "instance_followers"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"domain": Mastodon.__deprotocolize(params_init[key]).split("/")[0]}

        if len(keys) == 0:
            raise MastodonIllegalArgumentError("Must request at least one metric.")

        params["keys"] = keys
        params["start_at"] = self.__consistent_isoformat_utc(start_at)
        params["end_at"] = self.__consistent_isoformat_utc(end_at)
        
        return self.__api_request('POST', '/api/v1/admin/measures', params, use_json=True)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_ADMIN_DIMENSION)
    def admin_dimensions(self, start_at, end_at, limit=None, languages=False, sources=False, servers=False, space_usage=False, software_versions=False,
                            tag_servers=None, tag_languages=None, instance_accounts=None, instance_languages=None):
        """
        Retrieves primarily categorical instance information for the time period (at day granularity) between `start_at` and `end_at`.

            * `languages`: Pass true to get the most-used languages on this server
            * `sources`: Pass true to get the most-used client apps on this server
            * `servers`: Pass true to get the remote servers with the most statuses
            * `space_usage`: Pass true to get the how much space is used by different components your software stack
            * `software_versions`: Pass true to get the version numbers for your software stack
            * `tag_servers`: Pass a tag ID to get the most-common servers for statuses including a trending tag
            * `tag_languages`: Pass a tag ID to get the most-used languages for statuses including a trending tag
            * `instance_accounts`: Pass a domain to get the most-followed accounts from a remote server
            * `instance_languages`: Pass a domain to get the most-used languages from a remote server

        Pass `limit` to set how many results you want on queries where that makes sense.

        This API call is relatively expensive - watch your servers load if you want to get a lot of statistical data.

        There is currently no way to get tag IDs implemented in Mastodon.py, because the Mastodon public API does not implement one. This will be fixed in a future
        release.

        Returns a list of :ref:`admin dimension dicts <admin dimension dicts>`.
        """
        params_init = locals()
        keys = []
        for key in ["languages", "sources", "servers", "space_usage", "software_versions"]:
            if params_init[key] == True:
                keys.append(key)
        
        params = {}
        for key in ["tag_servers", "tag_languages"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"id": self.__unpack_id(params_init[key])}
        for key in ["instance_accounts", "instance_languages"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"domain": Mastodon.__deprotocolize(params_init[key]).split("/")[0]}

        if len(keys) == 0:
            raise MastodonIllegalArgumentError("Must request at least one dimension.")

        params["keys"] = keys
        if limit is not None:
            params["limit"] = limit
        params["start_at"] = self.__consistent_isoformat_utc(start_at)
        params["end_at"] = self.__consistent_isoformat_utc(end_at)
        
        return self.__api_request('POST', '/api/v1/admin/dimensions', params, use_json=True)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_ADMIN_RETENTION)
    def admin_retention(self, start_at, end_at, frequency="day"):
        """
        Gets user retention statistics (at `frequency` - "day" or "month" - granularity) between `start_at` and `end_at`.

        Returns a list of :ref:`admin retention dicts <admin retention dicts>`
        """
        if not frequency in ["day", "month"]:
            raise MastodonIllegalArgumentError("Frequency must be day or month")

        params = {
            "start_at": self.__consistent_isoformat_utc(start_at),
            "end_at": self.__consistent_isoformat_utc(end_at),
            "frequency": frequency
        }
        return self.__api_request('POST', '/api/v1/admin/retention', params)

    ###
    # Push subscription crypto utilities
    ###
    def push_subscription_generate_keys(self):
        """
        Generates a private key, public key and shared secret for use in webpush subscriptions.

        Returns two dicts: One with the private key and shared secret and another with the
        public key and shared secret.
        """
        if not IMPL_HAS_CRYPTO:
            raise NotImplementedError(
                'To use the crypto tools, please install the webpush feature dependencies.')

        push_key_pair = ec.generate_private_key(ec.SECP256R1(), default_backend())
        push_key_priv = push_key_pair.private_numbers().private_value
        try: 
            push_key_pub = push_key_pair.public_key().public_bytes(
                serialization.Encoding.X962,
                serialization.PublicFormat.UncompressedPoint,
            )
        except:
            push_key_pub = push_key_pair.public_key().public_numbers().encode_point()
            
        push_shared_secret = os.urandom(16)

        priv_dict = {
            'privkey': push_key_priv,
            'auth': push_shared_secret
        }

        pub_dict = {
            'pubkey': push_key_pub,
            'auth': push_shared_secret
        }

        return priv_dict, pub_dict

    @api_version("2.4.0", "2.4.0", _DICT_VERSION_PUSH_NOTIF)
    def push_subscription_decrypt_push(self, data, decrypt_params, encryption_header, crypto_key_header):
        """
        Decrypts `data` received in a webpush request. Requires the private key dict
        from :ref:`push_subscription_generate_keys() <push_subscription_generate_keys()>` (`decrypt_params`) as well as the
        Encryption and server Crypto-Key headers from the received webpush

        Returns the decoded webpush as a :ref:`push notification dict <push notification dict>`.
        """
        if (not IMPL_HAS_ECE) or (not IMPL_HAS_CRYPTO):
            raise NotImplementedError(
                'To use the crypto tools, please install the webpush feature dependencies.')

        salt = self.__decode_webpush_b64(encryption_header.split("salt=")[1].strip())
        dhparams = self.__decode_webpush_b64(crypto_key_header.split("dh=")[1].split(";")[0].strip())
        p256ecdsa = self.__decode_webpush_b64(crypto_key_header.split("p256ecdsa=")[1].strip())
        dec_key = ec.derive_private_key(decrypt_params['privkey'], ec.SECP256R1(), default_backend())
        decrypted = http_ece.decrypt(
            data,
            salt=salt,
            key=p256ecdsa,
            private_key=dec_key,
            dh=dhparams,
            auth_secret=decrypt_params['auth'],
            keylabel="P-256",
            version="aesgcm"
        )

        return json.loads(decrypted.decode('utf-8'), object_hook=Mastodon.__json_hooks)

    ###
    # Blurhash utilities
    ###
    def decode_blurhash(self, media_dict, out_size=(16, 16), size_per_component=True, return_linear=True):
        """
        Basic media-dict blurhash decoding.

        out_size is the desired result size in pixels, either absolute or per blurhash
        component (this is the default).

        By default, this function will return the image as linear RGB, ready for further
        scaling operations. If you want to display the image directly, set return_linear
        to False.

        Returns the decoded blurhash image as a three-dimensional list: [height][width][3],
        with the last dimension being RGB colours.

        For further info and tips for advanced usage, refer to the documentation for the
        blurhash module: https://github.com/halcy/blurhash-python
        """
        if not IMPL_HAS_BLURHASH:
            raise NotImplementedError(
                'To use the blurhash functions, please install the blurhash Python module.')

        # Figure out what size to decode to
        decode_components_x, decode_components_y = blurhash.components(media_dict["blurhash"])
        if size_per_component:
            decode_size_x = decode_components_x * out_size[0]
            decode_size_y = decode_components_y * out_size[1]
        else:
            decode_size_x = out_size[0]
            decode_size_y = out_size[1]

        # Decode
        decoded_image = blurhash.decode(media_dict["blurhash"], decode_size_x, decode_size_y, linear=return_linear)

        # And that's pretty much it.
        return decoded_image

    ###
    # Pagination
    ###
    def fetch_next(self, previous_page):
        """
        Fetches the next page of results of a paginated request. Pass in the
        previous page in its entirety, or the pagination information dict
        returned as a part of that pages last status ('_pagination_next').

        Returns the next page or None if no further data is available.
        """
        if isinstance(previous_page, list) and len(previous_page) != 0:
            if hasattr(previous_page, '_pagination_next'):
                params = copy.deepcopy(previous_page._pagination_next)
            else:
                return None
        else:
            params = copy.deepcopy(previous_page)

        method = params['_pagination_method']
        del params['_pagination_method']

        endpoint = params['_pagination_endpoint']
        del params['_pagination_endpoint']

        return self.__api_request(method, endpoint, params)

    def fetch_previous(self, next_page):
        """
        Fetches the previous page of results of a paginated request. Pass in the
        previous page in its entirety, or the pagination information dict
        returned as a part of that pages first status ('_pagination_prev').

        Returns the previous page or None if no further data is available.
        """
        if isinstance(next_page, list) and len(next_page) != 0:
            if hasattr(next_page, '_pagination_prev'):
                params = copy.deepcopy(next_page._pagination_prev)
            else:
                return None
        else:
            params = copy.deepcopy(next_page)

        method = params['_pagination_method']
        del params['_pagination_method']

        endpoint = params['_pagination_endpoint']
        del params['_pagination_endpoint']

        return self.__api_request(method, endpoint, params)

    def fetch_remaining(self, first_page):
        """
        Fetches all the remaining pages of a paginated request starting from a
        first page and returns the entire set of results (including the first page
        that was passed in) as a big list.

        Be careful, as this might generate a lot of requests, depending on what you are
        fetching, and might cause you to run into rate limits very quickly.
        """
        first_page = copy.deepcopy(first_page)

        all_pages = []
        current_page = first_page
        while current_page is not None and len(current_page) > 0:
            all_pages.extend(current_page)
            current_page = self.fetch_next(current_page)

        return all_pages

    ###
    # Streaming
    ###
    @api_version("1.1.0", "1.4.2", _DICT_VERSION_STATUS)
    def stream_user(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams events that are relevant to the authorized user, i.e. home
        timeline and notifications.
        """
        return self.__stream('/api/v1/streaming/user', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2", _DICT_VERSION_STATUS)
    def stream_public(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams public events.
        """
        return self.__stream('/api/v1/streaming/public', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2", _DICT_VERSION_STATUS)
    def stream_local(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams local public events.
        """
        return self.__stream('/api/v1/streaming/public/local', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2", _DICT_VERSION_STATUS)
    def stream_hashtag(self, tag, listener, local=False, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Stream for all public statuses for the hashtag 'tag' seen by the connected
        instance.

        Set local to True to only get local statuses.
        """
        if tag.startswith("#"):
            raise MastodonIllegalArgumentError(
                "Tag parameter should omit leading #")
        base = '/api/v1/streaming/hashtag'
        if local:
            base += '/local'
        return self.__stream("{}?tag={}".format(base, tag), listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_STATUS)
    def stream_list(self, id, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Stream events for the current user, restricted to accounts on the given
        list.
        """
        id = self.__unpack_id(id)
        return self.__stream("/api/v1/streaming/list?list={}".format(id), listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("2.6.0", "2.6.0", _DICT_VERSION_STATUS)
    def stream_direct(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams direct message events for the logged-in user, as conversation events.
        """
        return self.__stream('/api/v1/streaming/direct', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("2.5.0", "2.5.0", "2.5.0")
    def stream_healthy(self):
        """
        Returns without True if streaming API is okay, False or raises an error otherwise.
        """
        api_okay = self.__api_request('GET', '/api/v1/streaming/health', base_url_override=self.__get_streaming_base(), parse=False)
        if api_okay in [b'OK', b'success']:
            return True
        return False
