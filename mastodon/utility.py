# utility.py - utility functions, externally usable

from typing import TypeVar
import re
import dateutil
import datetime
import copy
import warnings

from mastodon.errors import MastodonAPIError, MastodonIllegalArgumentError, MastodonNotFoundError, MastodonVersionError
from mastodon.compat import IMPL_HAS_BLURHASH, blurhash, IMPL_HAS_GRAPHEME, grapheme
from mastodon.internals import Mastodon as Internals

from mastodon.versions import parse_version_string, max_version, api_version

from typing import Optional, Union, Dict, Iterator, Tuple, List
from mastodon.return_types import PaginatableList, PaginationInfo, PaginatableList, MediaAttachment
from mastodon.types_base import Entity, try_cast

from ._url_regex import url_regex
import unicodedata

_T = TypeVar("_T", bound=Entity)

class Mastodon(Internals):
    def set_language(self, lang: str):
        """
        Set the locale Mastodon will use to generate responses. Valid parameters are all ISO 639-1 (two letter) or, for languages that do
        not have one, 639-3 (three letter) language codes. This affects some error messages (those related to validation) and trends.
        """
        self.lang = lang

    def retrieve_mastodon_version(self) -> str:
        """
        Determine installed Mastodon version and set major, minor and patch (not including RC info) accordingly.

        Returns the version string, possibly including rc info.
        """
        try:
            version_str = self.__normalize_version_string(
                self.__instance()["version"])
            self.__version_check_worked = True
        except Exception as e:
            # instance() was added in 1.1.0, so our best guess is 1.0.0.
            version_str = "1.0.0"
            self.__version_check_worked = False
        self.mastodon_major, self.mastodon_minor, self.mastodon_patch = parse_version_string(
            version_str)

        # If the instance has an API version, we store that as well.
        # If we have a version >= 4.3.0 but no API version, we throw a warning that this is a Weird Implementation,
        # which might help with adoption of the API versioning or at least give us a better picture of how it is going.
        found_api_version = False
        try:
            instance_v2_info = self.__instance_v2()
            if "api_versions" in instance_v2_info and instance_v2_info["api_versions"]:
                if "mastodon" in instance_v2_info["api_versions"]:
                    self.mastodon_api_version = int(
                        instance_v2_info["api_versions"]["mastodon"])
                    found_api_version = True
        except MastodonNotFoundError:
            pass
        except MastodonVersionError:
            pass

        self.__version_check_tried = True
        if not found_api_version and self.verify_minimum_version("4.3.0", cached=True):
            warnings.warn(
                "Mastodon version is detected as >= 4.3.0, but no API version found. Please report this.")
        return version_str

    def verify_minimum_version(self, version_str: str, cached: bool = False) -> bool:
        """
        Update version info from server and verify that at least the specified version is present.

        If you specify "cached", the version info update part is skipped.

        Returns True if version requirement is satisfied, False if not.
        """
        if not cached or not self.__version_check_tried or not self.__version_check_worked:
            self.retrieve_mastodon_version()
        major, minor, patch = parse_version_string(version_str)
        if major > self.mastodon_major:
            return False
        elif major == self.mastodon_major and minor > self.mastodon_minor:
            return False
        elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
            return False
        return True

    def get_approx_server_time(self) -> datetime:
        """
        Retrieve the approximate server time

        We parse this from the hopefully present "Date" header, but make no effort to compensate for latency.
        """
        response = self.__api_request("HEAD", "/", return_response_object=True)
        if 'Date' in response.headers:
            server_time_datetime = dateutil.parser.parse(
                response.headers['Date'])

            # Make sure we're in local time
            epoch_time = self.__datetime_to_epoch(server_time_datetime)
            return datetime.datetime.fromtimestamp(epoch_time)
        else:
            raise MastodonAPIError("No server time in response.")

    ###
    # Blurhash utilities
    ###
    def decode_blurhash(self, media_dict: MediaAttachment, out_size: Tuple[int, int] = (16, 16), size_per_component: bool = True, return_linear: bool = True) -> List[List[List[float]]]:
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
        decode_components_x, decode_components_y = blurhash.components(
            media_dict["blurhash"])
        if size_per_component:
            decode_size_x = decode_components_x * out_size[0]
            decode_size_y = decode_components_y * out_size[1]
        else:
            decode_size_x = out_size[0]
            decode_size_y = out_size[1]

        # Decode
        decoded_image = blurhash.decode(
            media_dict["blurhash"], decode_size_x, decode_size_y, linear=return_linear)

        # And that's pretty much it.
        return decoded_image

    ###
    # Pagination
    ###
    def fetch_next(self, previous_page: Union[PaginatableList[_T], _T, PaginationInfo]) -> Optional[Union[PaginatableList[_T], _T]]:
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
            raise MastodonIllegalArgumentError(
                "The passed object is not paginatable")

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

    def fetch_previous(self, next_page: Union[PaginatableList[_T], _T, PaginationInfo]) -> Optional[Union[PaginatableList[_T], _T]]:
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
            raise MastodonIllegalArgumentError(
                "The passed object is not paginatable")

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

    def fetch_remaining(self, first_page: PaginatableList[_T]) -> PaginatableList[_T]:
        """
        Fetches all the remaining pages of a paginated request starting from a
        first page and returns the entire set of results (including the first page
        that was passed in) as a big list.

        Be careful, as this might generate a lot of requests, depending on what you are
        fetching, and might cause you to run into rate limits very quickly.

        Does not work with grouped notifications, since they use a somewhat weird, inside-out
        pagination scheme. If you need to access these in a paginated way, use fetch_next and fetch_previous
        directly.
        """
        first_page = copy.deepcopy(first_page)

        all_pages = []
        current_page = first_page
        while current_page is not None and len(current_page) > 0:
            all_pages.extend(current_page)
            current_page = self.fetch_next(current_page)

        return all_pages

    def get_pagination_info(self, page: PaginatableList[Entity], pagination_direction: str) -> Optional[PaginationInfo]:
        """
        Extracts pagination information from a paginated response.

        Returns a PaginationInfo dictionary containing pagination information, or None if not available.

        The resulting PaginationInfo is best treated as opaque, though is unlikely to change.
        """
        if hasattr(page, "_pagination_next") and pagination_direction == "next":
            return try_cast(PaginationInfo, page._pagination_next)
        elif hasattr(page, "_pagination_prev") and pagination_direction == "previous":
            return try_cast(PaginationInfo, page._pagination_prev)
        else:
            return None

    def pagination_iterator(self, start_page: Union[PaginatableList[_T], PaginationInfo], direction: str = "next", return_pagination_info: bool = False) -> Iterator[_T]:
        """
        Returns an iterator that will yield all entries in a paginated request,
        starting from the given start_page (can also be just the PaginationInfo, in which case the
        first returned thing will be the result of fetch_next or fetch_previous, depending on the direction).
        and fetching new pages as needed, and breaks when no more pages are available.

        Set direction to "next" to iterate forward, or "previous" to iterate backwards.

        If return_pagination_info is True, the iterator will instead yield tuples of (Entity, PaginationInfo),
        where PaginationInfo is a dictionary containing pagination information for the current page and direction.

        Does not work with grouped notifications, since they use a somewhat weird, inside-out
        pagination scheme. If you need to access these in a paginated way, use fetch_next and fetch_previous
        directly.
        """
        if direction not in ["next", "previous"]:
            raise MastodonIllegalArgumentError(
                "Invalid pagination direction: {}".format(direction))

        # Don't rely on python type info here, this is a Danger Zone. Instead, check for
        # _pagination_endpoint
        if hasattr(start_page, "_pagination_endpoint") or (isinstance(start_page, dict) and '_pagination_endpoint' in start_page):
            current_page = self.fetch_next(
                start_page) if direction == "next" else self.fetch_previous(start_page)
        else:
            current_page = start_page

        while current_page is not None and len(current_page) > 0:
            for entry in current_page:
                if return_pagination_info:
                    yield (entry, self.get_pagination_info(current_page, direction))
                else:
                    print("CURRENT PAGE IS", current_page)
                    print("YIELDING ENTRY: ", entry)
                    yield entry

            if direction == "next":
                current_page = self.fetch_next(current_page)
            else:
                current_page = self.fetch_previous(current_page)

    @staticmethod
    def get_status_length(text: str, spoiler_text: str = "") -> int:
        """
        For a given status `text` and `spoiler_text`, return how many characters this status counts as
        when computing the status length and comparing it against the limit.

        Note that there are other limits you may run into, such as the maximum length of a URL, or the
        maximum length of a usernames domain part. But as long as you do *normal* things, this function
        will return the correct length for the status text.
        """
        if not IMPL_HAS_GRAPHEME:
            raise NotImplementedError(
                'To use the get_status_length function, please install the grapheme Python module.')

        username_regex = re.compile(
            r'(^|[^/\w])@(([a-z0-9_]+)@[a-z0-9\.\-]+[a-z0-9]+)', re.IGNORECASE)

        def countable_text(input_text: str) -> str:
            # Transform text such that it has the correct length for counting
            # post text lengths against the limit
            def _url_repl(m: re.Match) -> str:
                return m.group(2) + ("x" * 23)
            text = url_regex.sub(_url_repl, input_text)
            text = username_regex.sub(r'\1@\3', text)
            return text

        return grapheme.length(countable_text(text)) + grapheme.length(spoiler_text)

