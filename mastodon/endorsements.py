# notifications.py - endorsement endpoints

from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Account, NonPaginatableList

class Mastodon(Internals):
    ###
    # Reading data: Endorsements
    ###
    @api_version("2.5.0", "2.5.0")
    def endorsements(self) -> NonPaginatableList[Account]:
        """
        Fetch list of users endorsed by the logged-in user.
        """
        return self.__api_request('GET', '/api/v1/endorsements')
