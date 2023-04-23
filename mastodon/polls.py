# polls.py - poll related endpoints and tooling

from .versions import _DICT_VERSION_POLL
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Polls
    ###
    @api_version("2.8.0", "2.8.0", _DICT_VERSION_POLL)
    def poll(self, id):
        """
        Fetch information about the poll with the given id

        Returns a :ref:`poll dict <poll dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/polls/{id}')

    ###
    # Writing data: Polls
    ###
    @api_version("2.8.0", "2.8.0", _DICT_VERSION_POLL)
    def poll_vote(self, id, choices):
        """
        Vote in the given poll.

        `choices` is the index of the choice you wish to register a vote for
        (i.e. its index in the corresponding polls `options` field. In case
        of a poll that allows selection of more than one option, a list of
        indices can be passed.

        You can only submit choices for any given poll once in case of
        single-option polls, or only once per option in case of multi-option
        polls.

        Returns the updated :ref:`poll dict <poll dict>`
        """
        id = self.__unpack_id(id)
        if not isinstance(choices, list):
            choices = [choices]
        params = self.__generate_params(locals(), ['id'])

        self.__api_request('POST', f'/api/v1/polls/{id}/votes', params)

    def make_poll(self, options, expires_in, multiple=False, hide_totals=False):
        """
        Generate a poll object that can be passed as the `poll` option when posting a status.

        options is an array of strings with the poll options (Maximum, by default: 4),
        expires_in is the time in seconds for which the poll should be open.
        Set multiple to True to allow people to choose more than one answer. Set
        hide_totals to True to hide the results of the poll until it has expired.
        """
        poll_params = locals()
        del poll_params["self"]
        return poll_params
