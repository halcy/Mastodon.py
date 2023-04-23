# list.py - list endpoints

from .versions import _DICT_VERSION_LIST, _DICT_VERSION_ACCOUNT
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Lists
    ###
    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def lists(self):
        """
        Fetch a list of all the Lists by the logged-in user.

        Returns a list of :ref:`list dicts <list dicts>`.
        """
        return self.__api_request('GET', '/api/v1/lists')

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def list(self, id):
        """
        Fetch info about a specific list.

        Returns a :ref:`list dict <list dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/lists/{id}')

    @api_version("2.1.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def list_accounts(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Get the accounts that are on the given list.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)

        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', f'/api/v1/lists/{id}/accounts', params)

    ###
    # Writing data: Lists
    ###
    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def list_create(self, title):
        """
        Create a new list with the given `title`.

        Returns the :ref:`list dict <list dict>` of the created list.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/lists', params)

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def list_update(self, id, title):
        """
        Update info about a list, where "info" is really the lists `title`.

        Returns the :ref:`list dict <list dict>` of the modified list.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', f'/api/v1/lists/{id}', params)

    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_delete(self, id):
        """
        Delete a list.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/lists/{id}')

    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_accounts_add(self, id, account_ids):
        """
        Add the account(s) given in `account_ids` to the list.
        """
        id = self.__unpack_id(id)

        if not isinstance(account_ids, list):
            account_ids = [account_ids]
        account_ids = [self.__unpack_id(x) for x in account_ids]

        params = self.__generate_params(locals(), ['id'])
        self.__api_request('POST', f'/api/v1/lists/{id}/accounts', params)

    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_accounts_delete(self, id, account_ids):
        """
        Remove the account(s) given in `account_ids` from the list.
        """
        id = self.__unpack_id(id)

        if not isinstance(account_ids, list):
            account_ids = [account_ids]
        account_ids = [self.__unpack_id(x) for x in account_ids]

        params = self.__generate_params(locals(), ['id'])
        self.__api_request('DELETE', f'/api/v1/lists/{id}/accounts', params)
