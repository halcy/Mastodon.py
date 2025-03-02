# utility.py - utility functions, externally usable

import re
import dateutil
import datetime
import copy

from mastodon.errors import MastodonAPIError, MastodonIllegalArgumentError
from mastodon.compat import IMPL_HAS_BLURHASH, blurhash
from mastodon.internals import Mastodon as Internals

from mastodon.versions import parse_version_string, max_version, api_version

from typing import Optional, Union, Dict
from mastodon.return_types import PaginatableList, PaginationInfo, PaginatableList
from mastodon.types_base import Entity

# Class level:
class Mastodon(Internals):
    def set_language(self, lang):
        """
        Set the locale Mastodon will use to generate responses. Valid parameters are all ISO 639-1 (two letter) or, for languages that do
        not have one, 639-3 (three letter) language codes. This affects some error messages (those related to validation) and trends.
        """
        self.lang = lang

    def retrieve_mastodon_version(self):
        """
        Determine installed Mastodon version and set major, minor and patch (not including RC info) accordingly.

        Returns the version string, possibly including rc info.
        """
        try:
            version_str = self.__normalize_version_string(self.__instance()["version"])
            self.version_check_worked = True
        except Exception as e:
            # instance() was added in 1.1.0, so our best guess is 1.0.0.
            version_str = "1.0.0"
            self.version_check_worked = False
        self.mastodon_major, self.mastodon_minor, self.mastodon_patch = parse_version_string(version_str)
        self.version_check_tried = True
        return version_str

    def verify_minimum_version(self, version_str, cached=False):
        """
        Update version info from server and verify that at least the specified version is present.

        If you specify "cached", the version info update part is skipped.

        Returns True if version requirement is satisfied, False if not.
        """
        if not cached or not self.version_check_tried:
            self.retrieve_mastodon_version()
        major, minor, patch = parse_version_string(version_str)
        if major > self.mastodon_major:
            return False
        elif major == self.mastodon_major and minor > self.mastodon_minor:
            return False
        elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
            return False
        return True

    def get_approx_server_time(self):
        """
        Retrieve the approximate server time

        We parse this from the hopefully present "Date" header, but make no effort to compensate for latency.
        """
        response = self.__api_request("HEAD", "/", return_response_object=True)
        if 'Date' in response.headers:
            server_time_datetime = dateutil.parser.parse(response.headers['Date'])

            # Make sure we're in local time
            epoch_time = self.__datetime_to_epoch(server_time_datetime)
            return datetime.datetime.fromtimestamp(epoch_time)
        else:
            raise MastodonAPIError("No server time in response.")

    ###
    # Blurhash utilities
    ###
    def decode_blurhash(self, media_dict, out_size=(16, 16), size_per_component=True, return_linear=True):
        """
        Basic media-dict blurhash decoding.

        out_size is the desired result size in pixels, either absolute or per blurhash
        component (this is the default).

        By default, this function will return the image as linear RGB, ready for further
        scaling operations. If you want to display the image directly, set return_linear
        to False.

        Returns the decoded blurhash image as a three-dimensional list: [height][width][3],
        with the last dimension being RGB colours.

        For further info and tips for advanced usage, refer to the documentation for the
        blurhash module: https://github.com/halcy/blurhash-python
        """
        if not IMPL_HAS_BLURHASH:
            raise NotImplementedError(
                'To use the blurhash functions, please install the blurhash Python module.')

        # Figure out what size to decode to
        decode_components_x, decode_components_y = blurhash.components(media_dict["blurhash"])
        if size_per_component:
            decode_size_x = decode_components_x * out_size[0]
            decode_size_y = decode_components_y * out_size[1]
        else:
            decode_size_x = out_size[0]
            decode_size_y = out_size[1]

        # Decode
        decoded_image = blurhash.decode(media_dict["blurhash"], decode_size_x, decode_size_y, linear=return_linear)

        # And that's pretty much it.
        return decoded_image

    ###
    # Pagination
    ###
    def fetch_next(self, previous_page: Union[PaginatableList[Entity], Entity, Dict]) -> Optional[Union[PaginatableList[Entity], Entity]]:
        """
        Fetches the next page of results of a paginated request. Pass in the
        previous page in its entirety, or the pagination information dict
        returned as a part of that pages last status ('_pagination_next').

        Returns the next page or None if no further data is available.
        """
        # Duck typing to keep compat with potentially persisted pagination info
        if hasattr(previous_page, "_pagination_next"):
            params = copy.deepcopy(previous_page._pagination_next)
        elif isinstance(previous_page, dict) and '_pagination_next' in previous_page:
            params = copy.deepcopy(previous_page['_pagination_next'])
        else:
            params = copy.deepcopy(previous_page)

        if params is None:
            return None

        is_pagination_dict = False
        if isinstance(previous_page, dict):
            if all(key in ['_pagination_method', '_pagination_endpoint', 'min_id', 'max_id', 'since_id', 'limit'] for key in previous_page):
                is_pagination_dict = True

        if not "_pagination_method" in params and not "_pagination_endpoint" in params:
            raise MastodonIllegalArgumentError("The passed object is not paginatable")

        method = params['_pagination_method']
        del params['_pagination_method']

        endpoint = params['_pagination_endpoint']
        del params['_pagination_endpoint']

        response_type = None
        if '_mastopy_type' in params:
            response_type = params['_mastopy_type']
            del params['_mastopy_type']

        force_pagination = False
        if not isinstance(previous_page, list):
            force_pagination = True

        if not is_pagination_dict:
            return self.__api_request(method, endpoint, params, force_pagination=force_pagination, override_type=response_type)
        else:
            return self.__api_request(method, endpoint, params, override_type=response_type)

    def fetch_previous(self, next_page: Union[PaginatableList[Entity], Entity, Dict]) -> Optional[Union[PaginatableList[Entity], Entity]]:
        """
        Fetches the previous page of results of a paginated request. Pass in the
        previous page in its entirety, or the pagination information dict
        returned as a part of that pages first status ('_pagination_prev').

        Returns the previous page or None if no further data is available.
        """
        # Duck typing to keep compat with potentially persisted pagination info
        if hasattr(next_page, "_pagination_prev"):
            params = copy.deepcopy(next_page._pagination_prev)
        elif isinstance(next_page, dict) and '_pagination_prev' in next_page:
            params = copy.deepcopy(next_page['_pagination_prev'])
        else:
            params = copy.deepcopy(next_page)

        if params is None:
            return None

        is_pagination_dict = False
        if isinstance(next_page, dict):
            if all(key in ['_pagination_method', '_pagination_endpoint', 'min_id', 'max_id', 'since_id', 'limit'] for key in next_page):
                is_pagination_dict = True

        if not "_pagination_method" in params and not "_pagination_endpoint" in params:
            raise MastodonIllegalArgumentError("The passed object is not paginatable")
        
        method = params['_pagination_method']
        del params['_pagination_method']

        endpoint = params['_pagination_endpoint']
        del params['_pagination_endpoint']

        response_type = None
        if '_mastopy_type' in params:
            response_type = params['_mastopy_type']
            del params['_mastopy_type']

        force_pagination = False
        if not isinstance(next_page, list):
            force_pagination = True
        
        if not is_pagination_dict:
            return self.__api_request(method, endpoint, params, force_pagination=force_pagination, override_type=response_type)
        else:
            return self.__api_request(method, endpoint, params, override_type=response_type)

    def fetch_remaining(self, first_page: PaginatableList[Entity]) -> PaginatableList[Entity]:
        """
        Fetches all the remaining pages of a paginated request starting from a
        first page and returns the entire set of results (including the first page
        that was passed in) as a big list.

        Be careful, as this might generate a lot of requests, depending on what you are
        fetching, and might cause you to run into rate limits very quickly.

        Does not currently work with grouped notifications, please deal with those
        yourself, for now.
        """
        first_page = copy.deepcopy(first_page)

        all_pages = []
        current_page = first_page
        while current_page is not None and len(current_page) > 0:
            all_pages.extend(current_page)
            current_page = self.fetch_next(current_page)

        return all_pages
