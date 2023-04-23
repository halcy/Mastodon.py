# conversations.py - conversation endpoints

from .versions import _DICT_VERSION_CONVERSATION
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Conversations
    ###
    @api_version("2.6.0", "2.6.0", _DICT_VERSION_CONVERSATION)
    def conversations(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches a user's conversations.

        Returns a list of :ref:`conversation dicts <conversation dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals())
        return self.__api_request('GET', "/api/v1/conversations/", params)

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
        return self.__api_request('POST', f'/api/v1/conversations/{id}/read')
