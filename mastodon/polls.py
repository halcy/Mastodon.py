# polls.py - poll related endpoints and tooling
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Poll, IdType
from typing import Union, List

class Mastodon(Internals):
    ###
    # Reading data: Polls
    ###
    @api_version("2.8.0", "2.8.0")
    def poll(self, id: Union[Poll, IdType]) -> Poll:
        """
        Fetch information about the poll with the given id
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/polls/{id}')

    ###
    # Writing data: Polls
    ###
    @api_version("2.8.0", "2.8.0")
    def poll_vote(self, id: Union[Poll, IdType], choices: Union[int, List[int]]) -> Poll:
        """
        Vote in the given poll.

        `choices` is the index of the choice you wish to register a vote for
        (i.e. its index in the corresponding polls `options` field. In case
        of a poll that allows selection of more than one option, a list of
        indices can be passed.

        You can only submit choices for any given poll once in case of
        single-option polls, or only once per option in case of multi-option
        polls.

        The returned object will reflect the updated votes.
        """
        id = self.__unpack_id(id)
        if not isinstance(choices, list):
            choices = [choices]
        params = self.__generate_params(locals(), ['id'])

        return self.__api_request('POST', f'/api/v1/polls/{id}/votes', params)

    @api_version("2.8.0", "2.8.0")
    def make_poll(self, options: List[str], expires_in: int, multiple: bool = False, hide_totals: bool = False) -> Poll:
        """
        Generate a poll object that can be passed as the `poll` option when posting a status.

        `options` is an array of strings with the poll options (Maximum, by default: 4 - see
        the instance configuration for the actual value on any given instance, if stated).
        `expires_in` is the time in seconds for which the poll should be open.
        Set multiple to True to allow people to choose more than one answer. Set
        hide_totals to True to hide the results of the poll until it has expired.
        """
        poll_params = locals().copy()
        del poll_params["self"]
        return poll_params
