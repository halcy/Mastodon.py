# conversations.py - conversation endpoints

from mastodon.versions import _DICT_VERSION_CONVERSATION
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from typing import Union, Optional
from mastodon.types import IdType, PaginatableList, Conversation

class Mastodon(Internals):
    ###
    # Reading data: Conversations
    ###
    @api_version("2.6.0", "2.6.0", _DICT_VERSION_CONVERSATION)
    def conversations(self, max_id: Optional[Union[Conversation, IdType]] = None, min_id: Optional[Union[Conversation, IdType]] = None, since_id: 
                      Optional[Union[Conversation, IdType]] = None, limit: Optional[int] = None) -> PaginatableList[Conversation]:
        """
        Fetches a user's conversations.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id)

        if min_id is not None:
            min_id = self.__unpack_id(min_id)

        if since_id is not None:
            since_id = self.__unpack_id(since_id)

        params = self.__generate_params(locals())
        return self.__api_request('GET', "/api/v1/conversations/", params)

    ###
    # Writing data: Conversations
    ###
    @api_version("2.6.0", "2.6.0", _DICT_VERSION_CONVERSATION)
    def conversations_read(self, id: Union[Conversation, IdType]):
        """
        Marks a single conversation as read.

        The returned object reflects the conversation's new read status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/conversations/{id}/read')
