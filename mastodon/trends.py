# trends.py - trend-related endpoints

from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Tag, Status, PreviewCard, NonPaginatableList
from typing import Optional, Union

class Mastodon(Internals):
    ###
    # Reading data: Trends
    ###
    @api_version("2.4.3", "3.5.0")
    def trends(self, limit: Optional[int] = None):
        """
        Old alias for :ref:`trending_tags() <trending_tags()>`

        Deprecated. Please use :ref:`trending_tags() <trending_tags()>` instead.
        """
        return self.trending_tags(limit=limit)

    @api_version("3.5.0", "3.5.0")
    def trending_tags(self, limit: Optional[int] = None, offset: Optional[int] = None, lang: Optional[str] = None) -> NonPaginatableList[Tag]:
        """
        Fetch trending-hashtag information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (default 10, the maximum
        number of results is 20).

        Specify `offset` to paginate results. Default 0.

        Does not require authentication unless locked down by the administrator.

        Important versioning note: This endpoint does not exist for Mastodon versions
        between 2.8.0 (inclusive) and 3.0.0 (exclusive).

        Pass `lang` to override the global locale parameter, which may affect trend ordering.

        The results are sorted by the instances's trending algorithm, descending.
        """
        params = self.__generate_params(locals())
        if "lang" in params:
            del params["lang"]
        if self.verify_minimum_version("3.5.0", cached=True):
            # Starting 3.5.0, old version is deprecated
            return self.__api_request('GET', '/api/v1/trends/tags', params, lang_override=lang)
        else:
            return self.__api_request('GET', '/api/v1/trends', params, lang_override=lang)

    @api_version("3.5.0", "3.5.0")
    def trending_statuses(self, limit: Optional[int] = None, offset: Optional[int] = None, lang: Optional[str] = None) -> NonPaginatableList[Status]:
        """
        Fetch trending-status information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (default 20, the maximum
        number of results is 40).

        Specify `offset` to paginate results. Default 0.

        Pass `lang` to override the global locale parameter, which may affect trend ordering.

        The results are sorted by the instances's trending algorithm, descending.
        """
        params = self.__generate_params(locals())
        if "lang" in params:
            del params["lang"]
        return self.__api_request('GET', '/api/v1/trends/statuses', params, lang_override=lang)

    @api_version("3.5.0", "3.5.0")
    def trending_links(self, limit: Optional[int] = None, offset: Optional[int] = None, lang: Optional[str] = None) -> NonPaginatableList[PreviewCard]:
        """
        Fetch trending-link information, if the instance provides such information.

        Specify `limit` to limit how many results are returned (default 10, the maximum
        number of results is 20).

        Specify `offset` to paginate results. Default 0.

        The results are sorted by the instances's trending algorithm, descending.
        """
        params = self.__generate_params(locals())
        if "lang" in params:
            del params["lang"]        
        return self.__api_request('GET', '/api/v1/trends/links', params, lang_override=lang)
