# favourites.py - favourites and also bookmarks

from .versions import _DICT_VERSION_STATUS
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Favourites
    ###
    @api_version("1.0.0", "2.6.0", _DICT_VERSION_STATUS)
    def favourites(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in user's favourited statuses.

        This endpoint uses internal ids for pagination, passing status ids to
        `max_id`, `min_id`, or `since_id` will not work. Pagination functions
        :ref:`fetch_next() <fetch_next()>`
        and :ref:`fetch_previous() <fetch_previous()>` should be used instead.

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
    # Reading data: Bookmarks
    ###
    @api_version("3.1.0", "3.1.0", _DICT_VERSION_STATUS)
    def bookmarks(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Get a list of statuses bookmarked by the logged-in user.

        This endpoint uses internal ids for pagination, passing status ids to
        `max_id`, `min_id`, or `since_id` will not work. Pagination functions
        :ref:`fetch_next() <fetch_next()>`
        and :ref:`fetch_previous() <fetch_previous()>` should be used instead.

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
