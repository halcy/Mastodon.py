# preferences.py - user preferences, markers

import collections

from .versions import _DICT_VERSION_PREFERENCES, _DICT_VERSION_MARKER
from .errors import MastodonIllegalArgumentError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Preferences
    ###
    @api_version("2.8.0", "2.8.0", _DICT_VERSION_PREFERENCES)
    def preferences(self):
        """
        Fetch the user's preferences, which can be used to set some default options.
        As of 2.8.0, apps can only fetch, not update preferences.

        Returns a :ref:`preference dict <preference dict>`.
        """
        return self.__api_request('GET', '/api/v1/preferences')

    ##
    # Reading data: Read markers
    ##
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_MARKER)
    def markers_get(self, timeline=["home"]):
        """
        Get the last-read-location markers for the specified timelines. Valid timelines
        are the same as in :ref:`timeline() <timeline()>`

        Note that despite the singular name, `timeline` can be a list.

        Returns a dict of :ref:`read marker dicts <read marker dicts>`, keyed by timeline name.
        """
        if not isinstance(timeline, (list, tuple)):
            timeline = [timeline]
        params = self.__generate_params(locals())

        return self.__api_request('GET', '/api/v1/markers', params)

    ##
    # Writing data: Read markers
    ##
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_MARKER)
    def markers_set(self, timelines, last_read_ids):
        """
        Set the "last read" marker(s) for the given timeline(s) to the given id(s)

        Note that if you give an invalid timeline name, this will silently do nothing.

        Returns a dict with the updated :ref:`read marker dicts <read marker dicts>`, keyed by timeline name.
        """
        if not isinstance(timelines, (list, tuple)):
            timelines = [timelines]

        if not isinstance(last_read_ids, (list, tuple)):
            last_read_ids = [last_read_ids]

        if len(last_read_ids) != len(timelines):
            raise MastodonIllegalArgumentError("Number of specified timelines and ids must be the same")

        params = collections.OrderedDict()
        for timeline, last_read_id in zip(timelines, last_read_ids):
            params[timeline] = collections.OrderedDict()
            params[timeline]["last_read_id"] = self.__unpack_id(last_read_id)

        return self.__api_request('POST', '/api/v1/markers', params, use_json=True)
