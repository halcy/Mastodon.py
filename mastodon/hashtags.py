# hashtags.py - hashtag and featured-hashtag endpoints

from .versions import _DICT_VERSION_FEATURED_TAG, _DICT_VERSION_HASHTAG
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tags(self):
        """
        Return the hashtags the logged-in user has set to be featured on
        their profile as a list of :ref:`featured tag dicts <featured tag dicts>`.

        Returns a list of :ref:`featured tag dicts <featured tag dicts>`.
        """
        return self.__api_request('GET', '/api/v1/featured_tags')

    @api_version("3.0.0", "3.0.0", _DICT_VERSION_HASHTAG)
    def featured_tag_suggestions(self):
        """
        Returns the logged-in user's 10 most commonly-used hashtags.

        Returns a list of :ref:`hashtag dicts <hashtag dicts>`.
        """
        return self.__api_request('GET', '/api/v1/featured_tags/suggestions')

    ###
    # Writing data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tag_create(self, name):
        """
        Creates a new featured hashtag displayed on the logged-in user's profile.

        Returns a :ref:`featured tag dict <featured tag dict>` with the newly featured tag.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/featured_tags', params)

    @api_version("3.0.0", "3.0.0", _DICT_VERSION_FEATURED_TAG)
    def featured_tag_delete(self, id):
        """
        Deletes one of the logged-in user's featured hashtags.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/featured_tags/{id}')
