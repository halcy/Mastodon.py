# suggestions.py - follow suggestion endpoints

from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import NonPaginatableList, Account, IdType, Suggestion
from typing import Union

class Mastodon(Internals):
    ###
    # Reading data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3")
    def suggestions_v1(self) -> NonPaginatableList[Account]:
        """
        Fetch follow suggestions for the logged-in user.
        """
        return self.__api_request('GET', '/api/v1/suggestions')

    @api_version("3.4.0", "3.4.0")
    def suggestions_v2(self) -> NonPaginatableList[Suggestion]:
        """
        Fetch follow suggestions for the logged-in user.
        """
        return self.__api_request('GET', '/api/v2/suggestions')

    def suggestions(self) -> Union[NonPaginatableList[Suggestion], NonPaginatableList[Account]]:
        """
        Fetch follow suggestions for the logged-in user.

        Will use the v1 endpoint if the server is below 3.4.0, otherwise will use the v2 endpoint
        and unpack the account dicts.
        """
        if self.verify_minimum_version("3.4.0", cached=True):
            suggestions = self.suggestions_v2()
            return [s.account for s in suggestions]
        else:
            return self.suggestions_v1()

    ###
    # Writing data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3")
    def suggestion_delete(self, account_id: Union[Account, IdType]):
        """
        Remove the user with the given `account_id` from the follow suggestions.
        """
        account_id = self.__unpack_id(account_id)
        self.__api_request('DELETE', f'/api/v1/suggestions/{account_id}')
