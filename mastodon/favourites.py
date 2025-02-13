# favourites.py - favourites and also bookmarks

from mastodon.versions import _DICT_VERSION_STATUS
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Status, IdType, PaginatableList

from typing import Optional, Union

class Mastodon(Internals):
    ###
    # Reading data: Favourites
    ###
    @api_version("1.0.0", "2.6.0", _DICT_VERSION_STATUS)
    def favourites(self, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None, 
                   since_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[Status]:
        """
        Fetch the logged-in user's favourited statuses.

        This endpoint uses internal ids for pagination, passing status ids to
        `max_id`, `min_id`, or `since_id` will not work.

        Returns a list of :ref:`status dicts <status dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id)

        if min_id is not None:
            min_id = self.__unpack_id(min_id)

        if since_id is not None:
            since_id = self.__unpack_id(since_id)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/favourites', params)

    ###
    # Reading data: Bookmarks
    ###
    @api_version("3.1.0", "3.1.0", _DICT_VERSION_STATUS)
    def bookmarks(self, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None, 
                   since_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[Status]:
        """
        Get a list of statuses bookmarked by the logged-in user.

        This endpoint uses internal ids for pagination, passing status ids to
        `max_id`, `min_id`, or `since_id` will not work.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id)

        if min_id is not None:
            min_id = self.__unpack_id(min_id)

        if since_id is not None:
            since_id = self.__unpack_id(since_id)

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/bookmarks', params)
