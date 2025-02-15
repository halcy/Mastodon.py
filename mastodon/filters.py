# filters.py - Filter-related endpoints

import re

from mastodon.errors import MastodonIllegalArgumentError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Filter, FilterV2, Status, Notification, FilterKeyword, FilterStatus
from mastodon.types_base import PaginatableList, NonPaginatableList, IdType

from typing import Union, Optional, List, Dict


class Mastodon(Internals):
    ###
    # Reading data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3")
    def filters(self) -> NonPaginatableList[Filter]:
        """
        Fetch all of the logged-in user's filters.
        """
        return self.__api_request('GET', '/api/v1/filters')

    @api_version("2.4.3", "2.4.3")
    def filter(self, id: Union[Filter, IdType]) -> Filter:
        """
        Fetches information about the filter with the specified `id`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/filters/{id}')

    @api_version("2.4.3", "2.4.3")
    def filters_apply(self, objects: Union[PaginatableList[Status], PaginatableList[Notification]], filters: Union[NonPaginatableList[Filter], NonPaginatableList[FilterV2]], context: str) -> Union[PaginatableList[Status], PaginatableList[Notification]]:
        """
        Helper function: Applies a list of filters to a list of either statuses
        or notifications and returns only those matched by none. This function will
        apply all filters that match the context provided in `context`, i.e.
        if you want to apply only notification-relevant filters, specify
        'notifications'. Valid contexts are 'home', 'notifications', 'public' and 'thread'.

        NB: This is for v1 filters. v2 filters are applied by the server, which adds the "filtered"
        attribute to filtered statuses.
        """
        # Build filter regex
        filter_strings = []
        for keyword_filter in filters:
            if not context in keyword_filter["context"]:
                continue

            filter_string = re.escape(keyword_filter["phrase"])
            if keyword_filter["whole_word"]:
                filter_string = "\\b" + filter_string + "\\b"
            filter_strings.append(filter_string)
        filter_re = re.compile("|".join(filter_strings), flags=re.IGNORECASE)

        # Apply
        filter_results = []
        for filter_object in objects:
            filter_status = filter_object
            if "status" in filter_object:
                filter_status = filter_object["status"]
            filter_text = filter_status["content"]
            filter_text = re.sub(r"<.*?>", " ", filter_text)
            filter_text = re.sub(r"\s+", " ", filter_text).strip()
            if not filter_re.search(filter_text):
                filter_results.append(filter_object)
        return filter_results

    ###
    # Writing data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3")
    def filter_create(self, phrase: str, context: str, irreversible: bool = False, whole_word: bool = True, expires_in: Optional[int] = None) -> Filter:
        """
        Creates a new keyword filter. `phrase` is the phrase that should be
        filtered out, `context` specifies from where to filter the keywords.
        Valid contexts are 'home', 'notifications', 'public' and 'thread'.

        Set `irreversible` to True if you want the filter to just delete statuses
        server side. This works only for the 'home' and 'notifications' contexts.

        Set `whole_word` to False if you want to allow filter matches to
        start or end within a word, not only at word boundaries.

        Set `expires_in` to specify for how many seconds the filter should be
        kept around.

        Returns the newly created filter.
        """
        params = self.__generate_params(locals())

        for context_val in context:
            if not context_val in ['home', 'notifications', 'public', 'thread']:
                raise MastodonIllegalArgumentError('Invalid filter context.')

        return self.__api_request('POST', '/api/v1/filters', params)

    @api_version("2.4.3", "2.4.3")
    def filter_update(self, id: Union[Filter, IdType], phrase: Optional[str] = None, context: Optional[str] = None, irreversible: Optional[bool] = None, whole_word: Optional[bool] = None, expires_in: Optional[int] = None) -> Filter:
        """
        Updates the filter with the given `id`. Parameters are the same
        as in `filter_create()`.

        Returns the updated filter.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', f'/api/v1/filters/{id}', params)

    @api_version("2.4.3", "2.4.3")
    def filter_delete(self, id: Union[Filter, FilterV2, IdType]):
        """
        Deletes the filter with the given `id`.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/filters/{id}')

    ###
    # Filters v2 api
    ###
    @api_version("4.0.0", "4.0.0")
    def filters_v2(self) -> NonPaginatableList[FilterV2]:
        """
        Fetch all filters for the authenticated user.
        """
        return self.__api_request('GET', '/api/v2/filters')

    @api_version("4.0.0", "4.0.0")
    def filter_v2(self, filter_id: Union[Filter, IdType]) -> Filter:
        """
        Fetch a specific filter by its ID.
        """
        filter_id = self.__unpack_id(filter_id)
        return self.__api_request('GET', f'/api/v2/filters/{filter_id}')

    @api_version("4.0.0", "4.0.0")
    def create_filter_v2(
        self,
        title: str,
        context: List[str],
        filter_action: str,
        expires_in: Optional[int] = None,
        keywords_attributes: Optional[List[Dict[str, Union[str, bool]]]] = None
    ) -> FilterV2:
        """
        Create a new filter with the given parameters.

        `title` is a human readable name for the filter. 
        
        `context` is list of contexts where the filter should apply. Valid values are:
            - "home": Filter applies to the home timeline.
            - "notifications": Filter applies to notifications. Filtered notifications land in notification requests.
            - "public": Filter applies to the public timelines.
            - "thread": Filter applies to conversations.
            - "account": Filter applies to account timelines.

        `filter_action` gives the policy to be applied when the filter is matched. Valid values are:
            - "warn": The user is warned if the content matches the filter.
            - "hide": The content is completely hidden if it matches the filter.

        NB: Even if you specify "hide", the status will still be returned - it will just have the "filtered" attribute set.
        
        pass a number of seconds as `expires_in` to make the filter expire in that many seconds. Use None for no expiration.
            
        pass a list of keyword dicts to initially as `keywords_attributes`, each with the following values:
            - "keyword": The term to filter on.
            - "whole_word": Whether word boundaries should be considered.
            
        """
        params = self.__generate_params(locals(), for_json=True)
        return self.__api_request('POST', '/api/v2/filters', params, use_json=True)

    @api_version("4.0.0", "4.0.0")
    def update_filter_v2(
        self,
        filter_id: Union[FilterV2, IdType],
        title: Optional[str] = None,
        context: Optional[List[str]] = None,
        filter_action: Optional[str] = None,
        expires_in: Optional[int] = None,
        keywords_attributes: Optional[List[Dict[str, Union[str, bool, int]]]] = None
    ) -> FilterV2:
        """
        Update an existing filter with the given parameters.

        Parameters are as in `create_filter_v2()`. Only the parameters you want to update need to be provided.
        """
        filter_id = self.__unpack_id(filter_id)
        params = self.__generate_params(locals(), for_json=True)
        return self.__api_request('PUT', f'/api/v2/filters/{filter_id}', params, use_json=True)

    @api_version("4.0.0", "4.0.0")
    def delete_filter_v2(self, filter_id: Union[FilterV2, IdType]) -> None:
        """
        Delete an existing filter.
        """
        filter_id = self.__unpack_id(filter_id)
        self.__api_request('DELETE', f'/api/v2/filters/{filter_id}')

    @api_version("4.0.0", "4.0.0")
    def filter_keywords_v2(self, filter_id: Union[FilterV2, IdType]) -> NonPaginatableList[FilterKeyword]:
        """
        Fetch all keywords associated with a given filter.
        """
        filter_id = self.__unpack_id(filter_id)
        return self.__api_request('GET', f'/api/v2/filters/{filter_id}/keywords')

    @api_version("4.0.0", "4.0.0")
    def add_filter_keyword_v2(
        self,
        filter_id: Union[FilterV2, IdType],
        keyword: str,
        whole_word: bool = False
    ) -> FilterKeyword:
        """
        Add a single keyword to an existing filter.

        Parameters are as in `create_filter_v2()` `keywords_attributes`.
        """
        filter_id = self.__unpack_id(filter_id)
        params = self.__generate_params(locals())
        return self.__api_request('POST', f'/api/v2/filters/{filter_id}/keywords', params)

    @api_version("4.0.0", "4.0.0")
    def delete_filter_keyword_v2(self, keyword_id: Union[FilterKeyword, IdType]) -> None:
        """
        Delete a single keyword from any filter.
        """
        keyword_id = self.__unpack_id(keyword_id)
        self.__api_request('DELETE', f'/api/v2/filters/keywords/{keyword_id}')

    @api_version("4.0.0", "4.0.0")
    def filter_statuses_v2(self, filter_id: Union[FilterV2, IdType]) -> List[FilterStatus]:
        """
        Retrieve all status-based filters for a FilterV2.
        """
        filter_id = self.__unpack_id(filter_id)
        return self.__api_request('GET', f'/api/v2/filters/{filter_id}/statuses')

    @api_version("4.0.0", "4.0.0")
    def add_filter_status_v2(self, filter_id: Union[FilterV2, IdType], status_id: Union[Status, IdType]) -> FilterStatus:
        """
        Add a status to a filter, which will then match on that status in addition to any keywords.
        Includes reblogs, does not include replies.
        """
        filter_id = self.__unpack_id(filter_id)
        status_id = self.__unpack_id(status_id)
        params = self.__generate_params({"status_id": status_id})
        return self.__api_request('POST', f'/api/v2/filters/{filter_id}/statuses', params)

    @api_version("4.0.0", "4.0.0")
    def filter_status_v2(self, filter_status_id: Union[FilterStatus, IdType]) -> FilterStatus:
        """
        Fetch a single status-based filter by its ID.
        """
        filter_status_id = self.__unpack_id(filter_status_id)
        return self.__api_request('GET', f'/api/v2/filters/statuses/{filter_status_id}')

    @api_version("4.0.0", "4.0.0")
    def delete_filter_status_v2(self, filter_status_id: Union[FilterStatus, IdType]) -> None:
        """
        Remove a status filter from a FilterV2.
        """
        filter_status_id = self.__unpack_id(filter_status_id)
        self.__api_request('DELETE', f'/api/v2/filters/statuses/{filter_status_id}')
