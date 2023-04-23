# suggestions.py - follow suggestion endpoints

from .versions import _DICT_VERSION_ACCOUNT
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_ACCOUNT)
    def suggestions(self):
        """
        Fetch follow suggestions for the logged-in user.

        Returns a list of :ref:`account dicts <account dicts>`.

        """
        return self.__api_request('GET', '/api/v1/suggestions')

    ###
    # Writing data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_ACCOUNT)
    def suggestion_delete(self, account_id):
        """
        Remove the user with the given `account_id` from the follow suggestions.
        """
        account_id = self.__unpack_id(account_id)
        self.__api_request('DELETE', f'/api/v1/suggestions/{account_id}')
