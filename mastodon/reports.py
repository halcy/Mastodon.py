
# reports.py - report endpoints

from .versions import _DICT_VERSION_REPORT
from .errors import MastodonVersionError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Reports
    ###
    @api_version("1.1.0", "1.1.0", _DICT_VERSION_REPORT)
    def reports(self):
        """
        Fetch a list of reports made by the logged-in user.

        Returns a list of :ref:`report dicts <report dicts>`.

        Warning: This method has now finally been removed, and will not
        work on Mastodon versions 2.5.0 and above.
        """
        if self.verify_minimum_version("2.5.0", cached=True):
            raise MastodonVersionError("API removed in Mastodon 2.5.0")
        return self.__api_request('GET', '/api/v1/reports')

    ###
    # Writing data: Reports
    ###
    @api_version("1.1.0", "3.5.0", _DICT_VERSION_REPORT)
    def report(self, account_id, status_ids=None, comment=None, forward=False, category=None, rule_ids=None):
        """
        Report statuses to the instances administrators.

        Accepts a list of toot IDs associated with the report, and a comment.

        Starting with Mastodon 3.5.0, you can also pass a `category` (one out of
        "spam", "violation" or "other") and `rule_ids` (a list of rule IDs corresponding
        to the rules returned by the :ref:`instance() <instance()>` API).

        Set `forward` to True to forward a report of a remote user to that users
        instance as well as sending it to the instance local administrators.

        Returns a :ref:`report dict <report dict>`.
        """
        if category is not None and not category in ["spam", "violation", "other"]:
            raise MastodonIllegalArgumentError("Invalid report category (must be spam, violation or other)")

        account_id = self.__unpack_id(account_id)

        if status_ids is not None:
            if not isinstance(status_ids, list):
                status_ids = [status_ids]
            status_ids = [self.__unpack_id(x) for x in status_ids]

        params_initial = locals()
        if not forward:
            del params_initial['forward']

        params = self.__generate_params(params_initial)
        return self.__api_request('POST', '/api/v1/reports/', params)
