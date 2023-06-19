# suggestions.py - follow suggestion endpoints

from mastodon.versions import _DICT_VERSION_ACCOUNT
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.types import NonPaginatableList, Account, IdType
from typing import Union

class Mastodon(Internals):
    ###
    # Reading data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_ACCOUNT)
    def suggestions(self) -> NonPaginatableList[Account]:
        """
        Fetch follow suggestions for the logged-in user.
        """
        return self.__api_request('GET', '/api/v1/suggestions')

    ###
    # Writing data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_ACCOUNT)
    def suggestion_delete(self, account_id: Union[Account, IdType]):
        """
        Remove the user with the given `account_id` from the follow suggestions.
        """
        account_id = self.__unpack_id(account_id)
        self.__api_request('DELETE', f'/api/v1/suggestions/{account_id}')
