    
from .versions import _DICT_VERSION_STATUS, _DICT_VERSION_CARD, _DICT_VERSION_CONTEXT, _DICT_VERSION_ACCOUNT, _DICT_VERSION_SCHEDULED_STATUS
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):    
    ###
    # Reading data: Statuses
    ###
    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status(self, id):
        """
        Fetch information about a single toot.

        Does not require authentication for publicly visible statuses.

        Returns a :ref:`status dict <status dict>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("1.0.0", "3.0.0", _DICT_VERSION_CARD)
    def status_card(self, id):
        """
        Fetch a card associated with a status. A card describes an object (such as an
        external video or link) embedded into a status.

        Does not require authentication for publicly visible statuses.

        This function is deprecated as of 3.0.0 and the endpoint does not
        exist anymore - you should just use the "card" field of the status dicts
        instead. Mastodon.py will try to mimic the old behaviour, but this
        is somewhat inefficient and not guaranteed to be the case forever.

        Returns a :ref:`card dict <card dict>`.
        """
        if self.verify_minimum_version("3.0.0", cached=True):
            return self.status(id).card
        else:
            id = self.__unpack_id(id)
            url = '/api/v1/statuses/{0}/card'.format(str(id))
            return self.__api_request('GET', url)

    @api_version("1.0.0", "1.0.0", _DICT_VERSION_CONTEXT)
    def status_context(self, id):
        """
        Fetch information about ancestors and descendants of a toot.

        Does not require authentication for publicly visible statuses.

        Returns a :ref:`context dict <context dict>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/context'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def status_reblogged_by(self, id):
        """
        Fetch a list of users that have reblogged a status.

        Does not require authentication for publicly visible statuses.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/reblogged_by'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def status_favourited_by(self, id):
        """
        Fetch a list of users that have favourited a status.

        Does not require authentication for publicly visible statuses.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/favourited_by'.format(str(id))
        return self.__api_request('GET', url)

    ###
    # Reading data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0", _DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_statuses(self):
        """
        Fetch a list of scheduled statuses

        Returns a list of :ref:`scheduled status dicts <scheduled status dicts>`.
        """
        return self.__api_request('GET', '/api/v1/scheduled_statuses')

    @api_version("2.7.0", "2.7.0", _DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_status(self, id):
        """
        Fetch information about the scheduled status with the given id.

        Returns a :ref:`scheduled status dict <scheduled status dict>`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/scheduled_statuses/{0}'.format(str(id))
        return self.__api_request('GET', url)
        