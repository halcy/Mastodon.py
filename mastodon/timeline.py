# timeline.py - endpoints for reading various different timelines

from mastodon.errors import MastodonIllegalArgumentError, MastodonNotFoundError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Status, IdType, PaginatableList, UserList
from typing import Union, Optional
from datetime import datetime

class Mastodon(Internals):
    ###
    # Reading data: Timelines
    ##
    @api_version("1.0.0", "3.1.4")
    def timeline(self, timeline: str = "home", max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None, only_media: bool = False, local: bool = False, 
                 remote: bool = False) -> PaginatableList[Status]:
        """ 
        Fetch statuses, most recent ones first. `timeline` can be 'home', 'local', 'public',
        'tag/<hashtag<', 'list/<id>' or 'link/<url>'. See the following functions documentation for what those do.

        The default timeline is the "home" timeline.

        Specify `only_media` to only get posts with attached media. Specify `local` to only get local statuses,
        and `remote` to only get remote statuses. Some options are mutually incompatible as dictated by logic.

        May or may not require authentication depending on server settings and what is specifically requested.

        See <https://docs.joinmastodon.org/methods/timelines/> for a description of the parameters.
        """
        params_initial = locals()

        if not local:
            del params_initial['local']

        if not remote:
            del params_initial['remote']

        if not only_media:
            del params_initial['only_media']

        if timeline == "local":
            timeline = "public"
            params_initial['local'] = True

        params = self.__generate_params(params_initial, ['timeline'], dateconv=True)
        return self.__api_request('GET', f'/api/v1/timelines/{timeline}', params)

    @api_version("1.0.0", "3.1.4")
    def timeline_home(self, max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None, only_media: bool = False, local: bool = False, 
                 remote: bool = False) -> PaginatableList[Status]:
        """
        Convenience method: Fetches the logged-in user's home timeline (i.e. followed users and self). Params as in `timeline()`.
        """
        return self.timeline('home', max_id=max_id, min_id=min_id, since_id=since_id, limit=limit, only_media=only_media, local=local, remote=remote)

    @api_version("1.0.0", "3.1.4")
    def timeline_local(self, max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None, only_media: bool = False) -> PaginatableList[Status]:
        """
        Convenience method: Fetches the local / instance-wide timeline, not including replies. Params as in `timeline()`.
        """
        return self.timeline('local', max_id=max_id, min_id=min_id, since_id=since_id, limit=limit, only_media=only_media)

    @api_version("1.0.0", "3.1.4")
    def timeline_public(self, max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None, only_media: bool = False, local: bool = False, 
                 remote: bool = False) -> PaginatableList[Status]:
        """
        Convenience method: Fetches the public / visible-network / federated timeline, not including replies. Params as in `timeline()`.
        """
        return self.timeline('public', max_id=max_id, min_id=min_id, since_id=since_id, limit=limit, only_media=only_media, local=local, remote=remote)

    @api_version("1.0.0", "3.1.4")
    def timeline_hashtag(self, hashtag: str, local: bool = False, max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None, only_media: bool = False,
                 remote: bool = False) -> PaginatableList[Status]:
        """
        Convenience method: Fetch a timeline of toots with a given hashtag. The hashtag parameter
        should not contain the leading #. Params as in `timeline()`.
        """
        if hashtag.startswith("#"):
            raise MastodonIllegalArgumentError("Hashtag parameter should omit leading #")
        hashtag = self.__unpack_id(hashtag, field="name")        
        return self.timeline(f'tag/{hashtag}', max_id=max_id, min_id=min_id, since_id=since_id, limit=limit, only_media=only_media, local=local, remote=remote)

    @api_version("2.1.0", "3.1.4")
    def timeline_list(self, id: Union[UserList, IdType], max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None, only_media: bool = False, local: bool = False, 
                 remote: bool = False) -> PaginatableList[Status]:
        """
        Convenience method: Fetches a timeline containing all the toots by users in a given list. Params as in `timeline()`.
        """
        id = self.__unpack_id(id)
        return self.timeline(f'list/{id}', max_id=max_id, min_id=min_id, since_id=since_id, limit=limit, only_media=only_media, local=local, remote=remote)

    def timeline_link(self, url: str, local: bool = False, max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None, only_media: bool = False,
                 remote: bool = False) -> PaginatableList[Status]:
        """
        Convenience method: Fetch a timeline of toots linking to a given trending URL. Params as in `timeline()`.

        Note: The URL must be *exactly* the same as one fron `trending_links()`, including the protocol and potentially trailing slash.

        Raises a MastodonNotFoundError if the URL is not currently trending.
        """
        return self.timeline(f'link?url={url}', max_id=max_id, min_id=min_id, since_id=since_id, limit=limit, only_media=only_media, local=local, remote=remote)