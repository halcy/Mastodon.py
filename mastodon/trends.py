# trends.py - trend-related endpoints

from .versions import _DICT_VERSION_HASHTAG, _DICT_VERSION_STATUS, _DICT_VERSION_CARD
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Trends
    ###
    @api_version("2.4.3", "3.5.0", _DICT_VERSION_HASHTAG)
    def trends(self, limit=None):
        """
        Old alias for :ref:`trending_tags() <trending_tags()>`

        Deprecated. Please use :ref:`trending_tags() <trending_tags()>` instead.
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
        if "lang" in params:
            del params["lang"]
        if self.verify_minimum_version("3.5.0", cached=True):
            # Starting 3.5.0, old version is deprecated
            return self.__api_request('GET', '/api/v1/trends/tags', params, lang_override=lang)
        else:
            return self.__api_request('GET', '/api/v1/trends', params, lang_override=lang)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS)
    def trending_statuses(self, limit=None, lang=None):
        """
        Fetch trending-status information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (the maximum number
        of results is 10, the endpoint is not paginated).

        Pass `lang` to override the global locale parameter, which may affect trend ordering.

        Returns a list of :ref:`status dicts <status dicts>`, sorted by the instances's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        if "lang" in params:
            del params["lang"]
        return self.__api_request('GET', '/api/v1/trends/statuses', params, lang_override=lang)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_CARD)
    def trending_links(self, limit=None, lang=None):
        """
        Fetch trending-link information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (the maximum number
        of results is 10, the endpoint is not paginated).

        Returns a list of :ref:`card dicts <card dicts>`, sorted by the instances's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        if "lang" in params:
            del params["lang"]        
        return self.__api_request('GET', '/api/v1/trends/links', params, lang_override=lang)
