
# reports.py - report endpoints

from mastodon.errors import MastodonVersionError, MastodonIllegalArgumentError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import NonPaginatableList, Report, Account, IdType, Status, Rule
from typing import Union, Optional, List

class Mastodon(Internals):
    ###
    # Reading data: Reports
    ###
    @api_version("1.1.0", "1.1.0")
    def reports(self) -> NonPaginatableList[Report]:
        """
        Fetch a list of reports made by the logged-in user.

        Warning: This method has now finally been removed, and will not
        work on Mastodon versions 2.5.0 and above.
        """
        if self.verify_minimum_version("2.5.0", cached = True):
            raise MastodonVersionError("API removed in Mastodon 2.5.0")
        return self.__api_request('GET', '/api/v1/reports')

    ###
    # Writing data: Reports
    ###
    @api_version("1.1.0", "3.5.0")
    def report(self, account_id: Union[Account, IdType], status_ids: Optional[Union[Status, IdType]] = None, comment: Optional[str] = None, 
               forward: bool = False, category: Optional[str] = None, rule_ids: Optional[List[Union[Rule, IdType]]] = None, forward_to_domains: Optional[List[str]] = None) -> Report:
        """
        Report statuses to the instances administrators.

        Accepts a list of toot IDs associated with the report, and a comment.

        Starting with Mastodon 3.5.0, you can also pass a `category` (one out of
        "spam", "violation" or "other") and `rule_ids` (a list of rule IDs corresponding
        to the rules returned by the :ref:`instance() <instance()>` API).

        Set `forward` to True to forward a report of a remote user to that users
        instance as well as sending it to the instance local administrators. Set
        forward_to_domains to a list of domains to forward the report to (only domains of
        people mentioned in the status), or omitto forward to the domain of the reported status.
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
