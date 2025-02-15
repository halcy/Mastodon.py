# conversations.py - conversation endpoints

from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from typing import Union, Optional
from mastodon.return_types import IdType, PaginatableList, Conversation

class Mastodon(Internals):
    ###
    # Reading data: Conversations
    ###
    @api_version("2.6.0", "2.6.0")
    def conversations(self, max_id: Optional[Union[Conversation, IdType]] = None, min_id: Optional[Union[Conversation, IdType]] = None, since_id: 
                      Optional[Union[Conversation, IdType]] = None, limit: Optional[int] = None) -> PaginatableList[Conversation]:
        """
        Fetches a user's conversations.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', "/api/v1/conversations/", params)

    ###
    # Writing data: Conversations
    ###
    @api_version("2.6.0", "2.6.0")
    def conversations_read(self, id: Union[Conversation, IdType]):
        """
        Marks a single conversation as read.

        The returned object reflects the conversation's new read status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/conversations/{id}/read')
