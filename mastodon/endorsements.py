# notifications.py - endorsement endpoints

from .versions import _DICT_VERSION_ACCOUNT
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Endorsements
    ###
    @api_version("2.5.0", "2.5.0", _DICT_VERSION_ACCOUNT)
    def endorsements(self):
        """
        Fetch list of users endorsed by the logged-in user.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        return self.__api_request('GET', '/api/v1/endorsements')
