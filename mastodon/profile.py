# profile.py - profile endpoints
import collections

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import PathOrFile, Profile
from mastodon.utility import api_version

from typing import List, Optional, Tuple


class Mastodon(Internals):
    @api_version("4.6.0", "4.6.0")
    def profile(self) -> Profile:
        """
        Retrieve the logged-in user's editable profile.
        """
        return self.__api_request('GET', '/api/v1/profile')

    @api_version("4.6.0", "4.6.0")
    def profile_update(self, display_name: Optional[str] = None, note: Optional[str] = None,
                       avatar: Optional[PathOrFile] = None, avatar_mime_type: Optional[str] = None,
                       header: Optional[PathOrFile] = None, header_mime_type: Optional[str] = None,
                       locked: Optional[bool] = None, bot: Optional[bool] = None,
                       discoverable: Optional[bool] = None, hide_collections: Optional[bool] = None,
                       indexable: Optional[bool] = None, show_media: Optional[bool] = None,
                       show_media_replies: Optional[bool] = None, show_featured: Optional[bool] = None,
                       attribution_domains: Optional[List[str]] = None,
                       fields: Optional[List[Tuple[str, str]]] = None) -> Profile:
        """
        Update the logged-in user's editable profile and return the updated profile.

        `avatar` and `header` may be filenames or file-like objects. Direct file data
        requires the corresponding MIME type.

        `locked` indicates whether the account is private (requiring follow approvals
        for all accounts). 
        
        `bot` indicates whether the account is marked as being a bot (taking automated actions). 
        
        `discoverable` indicates whether the account is publicly discoverable via the 
        discovery features, while `indexable` indicates whether the account is indexable
        for search.

        `show_media` indicates whether the account wants to show a media tab, while `show_media_replies`
        indicates whether the account wants to show media attached to replies in the media tab.

        `show_featured` indicates whether the account wants to show a featured tab.

        `attribution_domains` is a list of domains of websites allowed to credit the account
        as an author.

        `fields` is a list of custom profile fields, each represented as a tuple of the field name and value.

        Returns the updated Profile object.
        """
        params = collections.OrderedDict(locals())
        if fields is not None:
            for idx, (field_name, field_value) in enumerate(fields):
                params[f'fields_attributes[{idx}][name]'] = field_name
                params[f'fields_attributes[{idx}][value]'] = field_value

        for param in ["avatar", "avatar_mime_type", "header", "header_mime_type", "fields"]:
            del params[param]

        files = {}
        if avatar is not None:
            files["avatar"] = self.__load_media_file(avatar, avatar_mime_type)
        if header is not None:
            files["header"] = self.__load_media_file(header, header_mime_type)

        return self.__api_request('PATCH', '/api/v1/profile', self.__generate_params(params), files=files)
