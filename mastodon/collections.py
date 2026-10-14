# collections.py - collection endpoints
from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Account, Collection, CollectionItem, CollectionWithAccounts, Collections, \
    IdType, WrappedCollection, WrappedCollectionItem
from mastodon.types_base import EmptyResponse
from mastodon.utility import api_version

from typing import List, Optional, Union


class Mastodon(Internals):
    @api_version("4.6.0", "4.6.0")
    def collection_create(self, name: str, description: Optional[str] = None,
                          language: Optional[str] = None, tag_name: Optional[str] = None,
                          sensitive: Optional[bool] = None, discoverable: Optional[bool] = None,
                          account_ids: Optional[List[Union[Account, IdType]]] = None) -> WrappedCollection:
        """
        Create a Collection of accounts for follow recommendation purposes, optionally 
        including the accounts in `account_ids`.
        
        `name` is the name of the new collection, and `description` is an optional description.
        `language` is the optional associated language for the new collection as a ISO 639-1 two-letter or
        if a two letter code isn't available, 639-3 three-letter language code. `tag_name` gives an optional
        hashtag to associated with the Collection.

        `sensitive` indicates whether the new collection contains sensitive content, `discoverable` indicates
        whether the new collection is discoverable by other users through discovery functionality (or otherwise,
        only visible by direct link).
        """
        if account_ids is not None:
            account_ids = self.__unpack_id(account_ids, listify=True)
        return self.__api_request('POST', '/api/v1/collections', self.__generate_params(locals()))

    @api_version("4.6.0", "4.6.0")
    def collection(self, id: Union[Collection, IdType]) -> CollectionWithAccounts:
        """
        Retrieve a Collection and the accounts referenced by it.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/collections/{id}')

    @api_version("4.6.0", "4.6.0")
    def account_collections(self, id: Union[Account, IdType], limit: Optional[int] = None,
                            offset: Optional[int] = None) -> Collections:
        """
        Retrieve Collections owned by an account.

        Paginated via limit/offset instead of via normal cursor-based pagination, which is currently
        not supported by Mastodon.py pagination helpers.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', f'/api/v1/accounts/{id}/collections', params)

    @api_version("4.6.0", "4.6.0")
    def account_in_collections(self, id: Optional[Union[Account, IdType]], limit: Optional[int] = None,
                               offset: Optional[int] = None) -> Collections:
        """
        Retrieve Collections featuring the logged-in account.

        A different accounts id can be specified as the `id` parameter, however, this will currently 
        lead to Mastodon throwing an error.

        Paginated via limit/offset instead of via normal cursor-based pagination, which is currently
        not supported by Mastodon.py pagination helpers.
        """
        if id is None:
            id = self.me()
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', f'/api/v1/accounts/{id}/in_collections', params)

    @api_version("4.6.0", "4.6.0")
    def collection_update(self, id: Union[Collection, IdType], name: Optional[str] = None,
                          description: Optional[str] = None, language: Optional[str] = None,
                          tag_name: Optional[str] = None, sensitive: Optional[bool] = None,
                          discoverable: Optional[bool] = None) -> WrappedCollection:
        """
        Update a Collection.

        Parameters are the same as in `collection_create`, less `account_ids`.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PATCH', f'/api/v1/collections/{id}', params)

    @api_version("4.6.0", "4.6.0")
    def collection_delete(self, id: Union[Collection, IdType]) -> EmptyResponse:
        """
        Delete a Collection.
        """
        id = self.__unpack_id(id)
        return self.__api_request('DELETE', f'/api/v1/collections/{id}')

    @api_version("4.6.0", "4.6.0")
    def collection_item_add(self, id: Union[Collection, IdType], account_id: Union[Account, IdType]) -> WrappedCollectionItem:
        """
        Add an account to a Collection.
        """
        id = self.__unpack_id(id)
        account_id = self.__unpack_id(account_id)
        return self.__api_request(
            'POST', f'/api/v1/collections/{id}/items', {'account_id': account_id})

    @api_version("4.6.0", "4.6.0")
    def collection_item_delete(self, collection_id: Union[Collection, IdType], item_id: Union[CollectionItem, IdType]) -> EmptyResponse:
        """
        Remove a Collection item from a Collection owned by the logged-in user.
        """
        collection_id = self.__unpack_id(collection_id)
        item_id = self.__unpack_id(item_id)
        return self.__api_request('DELETE', f'/api/v1/collections/{collection_id}/items/{item_id}')

    @api_version("4.6.0", "4.6.0")
    def collection_item_revoke(self, collection_id: Union[Collection, IdType], item_id: Union[CollectionItem, IdType]) -> EmptyResponse:
        """
        Revoke the logged-in account's inclusion in a Collection.
        """
        collection_id = self.__unpack_id(collection_id)
        item_id = self.__unpack_id(item_id)
        return self.__api_request('POST', f'/api/v1/collections/{collection_id}/items/{item_id}/revoke')
