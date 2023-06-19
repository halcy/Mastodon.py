# notifications.py - endorsement endpoints

from mastodon.versions import _DICT_VERSION_ACCOUNT
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.types import Account, NonPaginatableList

class Mastodon(Internals):
    ###
    # Reading data: Endorsements
    ###
    @api_version("2.5.0", "2.5.0", _DICT_VERSION_ACCOUNT)
    def endorsements(self) -> NonPaginatableList[Account]:
        """
        Fetch list of users endorsed by the logged-in user.
        """
        return self.__api_request('GET', '/api/v1/endorsements')
