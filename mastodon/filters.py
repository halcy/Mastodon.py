# filters.py - Filter-related endpoints

import re

from mastodon.errors import MastodonIllegalArgumentError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Filter, FilterV2, Status, Notification
from mastodon.types_base import PaginatableList, NonPaginatableList, IdType

from typing import Union, Optional


class Mastodon(Internals):
    ###
    # Reading data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3")
    def filters(self) -> Union[NonPaginatableList[Filter], NonPaginatableList[FilterV2]]:
        """
        Fetch all of the logged-in user's filters.
        """
        return self.__api_request('GET', '/api/v1/filters')

    @api_version("2.4.3", "2.4.3")
    def filter(self, id: Union[Filter, FilterV2, IdType]) -> Union[Filter, FilterV2]:
        """
        Fetches information about the filter with the specified `id`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/filters/{id}')

    # TODO: Add v2 filter support
    # TODO: test this properly
    @api_version("2.4.3", "2.4.3")
    def filters_apply(self, objects: Union[PaginatableList[Status], PaginatableList[Notification]], filters: Union[NonPaginatableList[Filter], NonPaginatableList[FilterV2]], context: str) -> Union[PaginatableList[Status], PaginatableList[Notification]]:
        """
        Helper function: Applies a list of filters to a list of either statuses
        or notifications and returns only those matched by none. This function will
        apply all filters that match the context provided in `context`, i.e.
        if you want to apply only notification-relevant filters, specify
        'notifications'. Valid contexts are 'home', 'notifications', 'public' and 'thread'.
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
    def filter_create(self, phrase: str, context: str, irreversible: bool = False, whole_word: bool = True, expires_in: Optional[int] = None) -> Union[Filter, FilterV2]:
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
    def filter_update(self, id: Union[Filter, FilterV2, IdType], phrase: Optional[str] = None, context: Optional[str] = None, irreversible: Optional[bool] = None, whole_word: Optional[bool] = None, expires_in: Optional[int] = None) -> Union[Filter, FilterV2]:
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
