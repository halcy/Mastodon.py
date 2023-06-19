# hashtags.py - hashtag and featured-hashtag endpoints

from mastodon.versions import _DICT_VERSION_FEATURED_TAG, _DICT_VERSION_HASHTAG
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.types import Tag, NonPaginatableList, FeaturedTag, IdType

from typing import Union

class Mastodon(Internals):
    ###
    # Reading data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tags(self) -> NonPaginatableList[Tag]:
        """
        Return the hashtags the logged-in user has set to be featured on
        their profile as a list of :ref:`featured tag dicts <featured tag dicts>`.
        """
        return self.__api_request('GET', '/api/v1/featured_tags')

    @api_version("3.0.0", "3.0.0", _DICT_VERSION_HASHTAG)
    def featured_tag_suggestions(self) -> NonPaginatableList[Tag]:
        """
        Returns the logged-in user's 10 most commonly-used hashtags.
        """
        return self.__api_request('GET', '/api/v1/featured_tags/suggestions')

    ###
    # Writing data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tag_create(self, name: str) -> FeaturedTag:
        """
        Creates a new featured hashtag displayed on the logged-in user's profile.

        The returned object is the newly featured tag.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/featured_tags', params)

    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tag_delete(self, id: Union[FeaturedTag, IdType]):
        """
        Deletes one of the logged-in user's featured hashtags.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/featured_tags/{id}')
