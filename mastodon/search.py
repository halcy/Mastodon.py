# search.py - search endpoints

from .versions import _DICT_VERSION_SEARCHRESULT
from .errors import MastodonVersionError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
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
            self.__ensure_search_params_acceptable(account_id, offset, min_id, max_id)
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
        self.__ensure_search_params_acceptable(account_id, offset, min_id, max_id)
        params = self.__generate_params(locals())

        if not resolve:
            del params["resolve"]

        if not exclude_unreviewed or not self.verify_minimum_version("3.0.0", cached=True):
            del params["exclude_unreviewed"]

        if "result_type" in params:
            params["type"] = params["result_type"]
            del params["result_type"]

        return self.__api_request('GET', '/api/v2/search', params)
