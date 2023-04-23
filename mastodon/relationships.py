# relationships.py - endpoints for user and domain blocks and mutes as well as follow requests

from .versions import _DICT_VERSION_ACCOUNT, _DICT_VERSION_RELATIONSHIP
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
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
    # Writing data: Follow requests
    ###
    @api_version("1.0.0", "3.0.0", _DICT_VERSION_RELATIONSHIP)
    def follow_request_authorize(self, id):
        """
        Accept an incoming follow request.

        Returns the updated :ref:`relationship dict <relationship dict>` for the requesting account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/follow_requests/{id}/authorize')

    @api_version("1.0.0", "3.0.0", _DICT_VERSION_RELATIONSHIP)
    def follow_request_reject(self, id):
        """
        Reject an incoming follow request.

        Returns the updated :ref:`relationship dict <relationship dict>` for the requesting account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/follow_requests/{id}/reject')

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
