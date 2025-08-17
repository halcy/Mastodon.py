# hashtags.py - hashtag and featured-hashtag endpoints
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Tag, NonPaginatableList, PaginatableList, FeaturedTag, IdType
from mastodon.errors import MastodonIllegalArgumentError

from typing import Union, Optional
from datetime import datetime

class Mastodon(Internals):
    ###
    # Reading data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0")
    def featured_tags(self) -> NonPaginatableList[FeaturedTag]:
        """
        Return the hashtags the logged-in user has set to be featured on
        their profile.
        """
        return self.__api_request('GET', '/api/v1/featured_tags')

    @api_version("3.0.0", "3.0.0")
    def featured_tag_suggestions(self) -> NonPaginatableList[FeaturedTag]:
        """
        Returns the logged-in user's 10 most commonly-used hashtags.
        """
        return self.__api_request('GET', '/api/v1/featured_tags/suggestions')

    ###
    # Writing data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0")
    def featured_tag_create(self, name: str) -> FeaturedTag:
        """
        Creates a new featured hashtag displayed on the logged-in user's profile.

        The returned object is the newly featured tag.

        Obsoleted by `tag_feature` / `tag_unfeature`.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/featured_tags', params)

    @api_version("3.0.0", "3.0.0")
    def featured_tag_delete(self, id: Union[FeaturedTag, IdType]):
        """
        Deletes one of the logged-in user's featured hashtags.

        Obsoleted by `tag_feature` / `tag_unfeature`.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/featured_tags/{id}')

    @api_version("4.4.0", "4.4.0")
    def tag_feature(self, name: str) -> Tag:
        """
        Creates a new featured hashtag displayed on the logged-in user's profile.

        Same effect as above, but newer. Likely obsoletes `featured_tag_create`.
        """
        name = self.__unpack_id(name, field="name")
        if name.startswith("#"):
            raise MastodonIllegalArgumentError("Hashtag parameter should omit leading #")
        return self.__api_request('POST', f'/api/v1/tags/{name}/feature')
    
    @api_version("4.4.0", "4.4.0")
    def tag_unfeature(self, name: str) -> Tag:
        """
        Deletes one of the logged-in user's featured hashtags.

        Same effect as above, but newer. Likely obsoletes `featured_tag_delete`.
        """
        name = self.__unpack_id(name, field="name")
        if name.startswith("#"):
            raise MastodonIllegalArgumentError("Hashtag parameter should omit leading #")
        return self.__api_request('POST', f'/api/v1/tags/{name}/unfeature')

    ###
    # Reading data: Followed tags
    ###
    @api_version("4.0.0", "4.0.0")
    def followed_tags(self, max_id: Optional[Union[Tag, IdType, datetime]] = None, 
                      min_id: Optional[Union[Tag, IdType, datetime]] = None, since_id: Optional[Union[Tag, IdType, datetime]] = None, 
                      limit: Optional[int] = None) -> PaginatableList[Tag]:
        """
        Returns the logged-in user's followed tags.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/followed_tags', params)
    
    
    @api_version("4.0.0", "4.0.0")
    def tag(self, hashtag: Union[Tag, str]) -> Tag:
        """
        Get information about a single tag.
        """
        hashtag = self.__unpack_id(hashtag, field="name")
        if hashtag.startswith("#"):
            raise MastodonIllegalArgumentError("Hashtag parameter should omit leading #")        
        return self.__api_request('GET', f'/api/v1/tags/{hashtag}')
    
    ###
    # Writing data: Followed tags
    ###
    @api_version("4.0.0", "4.0.0")
    def tag_follow(self, hashtag: Union[Tag, str]) -> Tag:
        """
        Follow a tag.

        Returns the newly followed tag.
        """
        hashtag = self.__unpack_id(hashtag, field="name")
        if hashtag.startswith("#"):
            raise MastodonIllegalArgumentError("Hashtag parameter should omit leading #")        
        return self.__api_request('POST', f'/api/v1/tags/{hashtag}/follow')
    
    @api_version("4.0.0", "4.0.0")
    def tag_unfollow(self, hashtag: Union[Tag, str]) -> Tag:
        """
        Unfollow a tag.

        Returns the previously followed tag.
        """
        hashtag = self.__unpack_id(hashtag, field="name")
        if hashtag.startswith("#"):
            raise MastodonIllegalArgumentError("Hashtag parameter should omit leading #")        
        return self.__api_request('POST', f'/api/v1/tags/{hashtag}/unfollow')
    
