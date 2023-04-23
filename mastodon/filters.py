# filters.py - Filter-related endpoints

import re

from .versions import _DICT_VERSION_FILTER
from .errors import MastodonIllegalArgumentError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filters(self):
        """
        Fetch all of the logged-in user's filters.

        Returns a list of :ref:`filter dicts <filter dicts>`. Not paginated.
        """
        return self.__api_request('GET', '/api/v1/filters')

    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filter(self, id):
        """
        Fetches information about the filter with the specified `id`.

        Returns a :ref:`filter dict <filter dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/filters/{id}')

    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filters_apply(self, objects, filters, context):
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
    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filter_create(self, phrase, context, irreversible=False, whole_word=True, expires_in=None):
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

        Returns the :ref:`filter dict <filter dict>` of the newly created filter.
        """
        params = self.__generate_params(locals())

        for context_val in context:
            if not context_val in ['home', 'notifications', 'public', 'thread']:
                raise MastodonIllegalArgumentError('Invalid filter context.')

        return self.__api_request('POST', '/api/v1/filters', params)

    @api_version("2.4.3", "2.4.3", _DICT_VERSION_FILTER)
    def filter_update(self, id, phrase=None, context=None, irreversible=None, whole_word=None, expires_in=None):
        """
        Updates the filter with the given `id`. Parameters are the same
        as in `filter_create()`.

        Returns the :ref:`filter dict <filter dict>` of the updated filter.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', f'/api/v1/filters/{id}', params)

    @api_version("2.4.3", "2.4.3", "2.4.3")
    def filter_delete(self, id):
        """
        Deletes the filter with the given `id`.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/filters/{id}')
