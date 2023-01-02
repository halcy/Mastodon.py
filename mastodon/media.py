# admin.py - admin / moderation endpoints

import time

from .versions import _DICT_VERSION_MEDIA
from .errors import MastodonVersionError, MastodonAPIError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Media
    ###
    @api_version("3.1.4", "3.1.4", _DICT_VERSION_MEDIA)
    def media(self, id):
        """
        Get the updated JSON for one non-attached / in progress media upload belonging
        to the logged-in user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/media/{id}')

    ###
    # Writing data: Media
    ###
    @api_version("1.0.0", "3.2.0", _DICT_VERSION_MEDIA)
    def media_post(self, media_file, mime_type=None, description=None, focus=None, file_name=None, thumbnail=None, thumbnail_mime_type=None, synchronous=False):
        """
        Post an image, video or audio file. `media_file` can either be data or
        a file name. If data is passed directly, the mime type has to be specified
        manually, otherwise, it is determined from the file name. `focus` should be a tuple
        of floats between -1 and 1, giving the x and y coordinates of the images
        focus point for cropping (with the origin being the images center).

        Throws a `MastodonIllegalArgumentError` if the mime type of the
        passed data or file can not be determined properly.

        `file_name` can be specified to upload a file with the given name,
        which is ignored by Mastodon, but some other Fediverse server software
        will display it. If no name is specified, a random name will be generated.
        The filename of a file specified in media_file will be ignored.

        Starting with Mastodon 3.2.0, `thumbnail` can be specified in the same way as `media_file`
        to upload a custom thumbnail image for audio and video files.

        Returns a :ref:`media dict <media dict>`. This contains the id that can be used in
        status_post to attach the media file to a toot.

        When using the v2 API (post Mastodon version 3.1.4), the `url` in the
        returned dict will be `null`, since attachments are processed
        asynchronously. You can fetch an updated dict using `media`. Pass
        "synchronous" to emulate the old behaviour. Not recommended, inefficient
        and deprecated, will eat your API quota, you know the deal.
        """
        files = {'file': self.__load_media_file(
            media_file, mime_type, file_name)}

        if focus is not None:
            focus = f"{focus[0]},{focus[1]}"

        if thumbnail is not None:
            if not self.verify_minimum_version("3.2.0", cached=True):
                raise MastodonVersionError('Thumbnail requires version > 3.2.0')
            files["thumbnail"] = self.__load_media_file(
                thumbnail, thumbnail_mime_type)

        # Disambiguate URL by version
        if self.verify_minimum_version("3.1.4", cached=True):
            ret_dict = self.__api_request(
                'POST', '/api/v2/media', files=files, params={'description': description, 'focus': focus})
        else:
            ret_dict = self.__api_request(
                'POST', '/api/v1/media', files=files, params={'description': description, 'focus': focus})

        # Wait for processing?
        if synchronous:
            if self.verify_minimum_version("3.1.4"):
                while not "url" in ret_dict or ret_dict.url is None:
                    try:
                        ret_dict = self.media(ret_dict)
                        time.sleep(5.0)
                    except:
                        raise MastodonAPIError("Attachment could not be processed")
            else:
                # Old version always waits
                return ret_dict

        return ret_dict

    @api_version("2.3.0", "3.2.0", _DICT_VERSION_MEDIA)
    def media_update(self, id, description=None, focus=None, thumbnail=None, thumbnail_mime_type=None):
        """
        Update the metadata of the media file with the given `id`. `description` and
        `focus` and `thumbnail` are as in :ref:`media_post() <media_post()>` .

        Returns the updated :ref:`media dict <media dict>`.
        """
        id = self.__unpack_id(id)

        if focus is not None:
            focus = f"{focus[0]},{focus[1]}"

        params = self.__generate_params(
            locals(), ['id', 'thumbnail', 'thumbnail_mime_type'])

        if thumbnail is not None:
            if not self.verify_minimum_version("3.2.0", cached=True):
                raise MastodonVersionError('Thumbnail requires version > 3.2.0')
            files = {"thumbnail": self.__load_media_file(
                thumbnail, thumbnail_mime_type)}
            return self.__api_request('PUT', f'/api/v1/media/{id}', params, files=files)
        else:
            return self.__api_request('PUT', f'/api/v1/media/{id}', params)
