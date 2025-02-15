# list.py - list endpoints
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import NonPaginatableList, UserList, IdType, PaginatableList, Account

from typing import List, Union, Optional

class Mastodon(Internals):
    ###
    # Reading data: Lists
    ###
    @api_version("2.1.0", "2.1.0")
    def lists(self) -> NonPaginatableList[UserList]:
        """
        Fetch a list of all the Lists by the logged-in user.
        """
        return self.__api_request('GET', '/api/v1/lists')

    @api_version("2.1.0", "2.1.0")
    def list(self, id: Union[UserList, IdType]) -> UserList:
        """
        Fetch info about a specific list.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/lists/{id}')

    @api_version("2.1.0", "2.6.0")
    def list_accounts(self, id: Union[UserList, IdType], max_id: Optional[Union[UserList, IdType]] = None, 
                      min_id: Optional[Union[UserList, IdType]] = None, since_id: Optional[Union[UserList, IdType]] = None, 
                      limit: Optional[int] = None) -> PaginatableList[Account]:
        """
        Get the accounts that are on the given list.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'], dateconv=True)
        return self.__api_request('GET', f'/api/v1/lists/{id}/accounts', params)

    ###
    # Writing data: Lists
    ###
    @api_version("2.1.0", "2.1.0")
    def list_create(self, title: str) -> UserList:
        """
        Create a new list with the given `title`.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/lists', params)

    @api_version("2.1.0", "2.1.0")
    def list_update(self, id: Union[UserList, IdType], title: str) -> UserList:
        """
        Update info about a list, where "info" is really the lists `title`.

        The returned object reflects the updated list.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', f'/api/v1/lists/{id}', params)

    @api_version("2.1.0", "2.1.0")
    def list_delete(self, id: Union[UserList, IdType]):
        """
        Delete a list.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/lists/{id}')

    @api_version("2.1.0", "2.1.0")
    def list_accounts_add(self, id:  Union[UserList, IdType], account_ids: List[Union[Account, IdType]]):
        """
        Add the account(s) given in `account_ids` to the list.
        """
        id = self.__unpack_id(id)
        account_ids = self.__unpack_id(account_ids, listify = True)

        params = self.__generate_params(locals(), ['id'])
        self.__api_request('POST', f'/api/v1/lists/{id}/accounts', params)

    @api_version("2.1.0", "2.1.0")
    def list_accounts_delete(self, id: Union[UserList, IdType], account_ids: List[Union[Account, IdType]]):
        """
        Remove the account(s) given in `account_ids` from the list.
        """
        id = self.__unpack_id(id)
        account_ids = self.__unpack_id(account_ids, listify = True)
        params = self.__generate_params(locals(), ['id'])
        self.__api_request('DELETE', f'/api/v1/lists/{id}/accounts', params)
