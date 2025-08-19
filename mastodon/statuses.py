# statuses.py - status endpoints (regular and scheduled)

import collections
from datetime import datetime
import base64

from mastodon.errors import MastodonIllegalArgumentError, MastodonVersionError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Status, IdType, ScheduledStatus, PreviewCard, Context, NonPaginatableList, Account,\
                MediaAttachment, Poll, StatusSource, StatusEdit, PaginatableList, PathOrFile, Translation

from typing import Union, Optional, List, Dict, Any, Tuple

class Mastodon(Internals):
    ###
    # Reading data: Statuses
    ###
    @api_version("1.0.0", "2.0.0")
    def status(self, id: Union[Status, IdType]) -> Status:
        """
        Fetch information about a single toot.

        Does not require authentication for publicly visible statuses.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}')

    @api_version("4.3.0", "4.3.0")
    def statuses(self, ids: List[Union[Status, IdType]]) -> List[Status]:
        """
        Fetch information from multiple statuses by a list of status `id`.

        Does not require authentication for publicly visible accounts.
        """
        ids = [self.__unpack_id(id, dateconv=True) for id in ids]
        return self.__api_request('GET', '/api/v1/statuses', {"id[]": ids})

    @api_version("1.0.0", "3.0.0")
    def status_card(self, id: Union[Status, IdType]) -> PreviewCard:
        """
        Fetch a card associated with a status. A card describes an object (such as an
        external video or link) embedded into a status.

        Does not require authentication for publicly visible statuses.

        This function is deprecated as of 3.0.0 and the endpoint does not
        exist anymore - you should just use the "card" field of the status
        instead. Mastodon.py will try to mimic the old behaviour, but this
        is somewhat inefficient and not guaranteed to be the case forever.
        """
        if self.verify_minimum_version("3.0.0", cached=True):
            return self.status(id).card
        else:
            id = self.__unpack_id(id)
            return self.__api_request('GET', f'/api/v1/statuses/{id}/card')

    @api_version("1.0.0", "1.0.0")
    def status_context(self, id: Union[Status, IdType]) -> Context:
        """
        Fetch information about ancestors and descendants of a toot.

        Does not require authentication for publicly visible statuses.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}/context')

    @api_version("1.0.0", "2.1.0")
    def status_reblogged_by(self, id: Union[Status, IdType]) -> NonPaginatableList[Account]:
        """
        Fetch a list of users that have reblogged a status.

        Does not require authentication for publicly visible statuses.

        Interesting caveat: If you self-reblog a status with private
        visibility, this endpoint will not return your account as having
        reblogged it.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}/reblogged_by')

    @api_version("1.0.0", "2.1.0")
    def status_favourited_by(self, id: Union[Status, IdType]) -> NonPaginatableList[Account]:
        """
        Fetch a list of users that have favourited a status.

        Does not require authentication for publicly visible statuses.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}/favourited_by')

    ###
    # Reading data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0")
    def scheduled_statuses(self, max_id: Optional[Union[Status, IdType, datetime]] = None, min_id: Optional[Union[Status, IdType, datetime]] = None, 
                 since_id: Optional[Union[Status, IdType, datetime]] = None, limit: Optional[int] = None) -> PaginatableList[ScheduledStatus]:
        """
        Fetch a list of scheduled statuses
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/scheduled_statuses', params)

    @api_version("2.7.0", "2.7.0")
    def scheduled_status(self, id: Union[ScheduledStatus, IdType]) -> ScheduledStatus:
        """
        Fetch information about the scheduled status with the given id.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/scheduled_statuses/{id}')

    ###
    # Writing data: Statuses
    ###
    def __status_internal(self, status: Optional[str], in_reply_to_id: Optional[Union[Status, IdType]] = None, media_ids: Optional[List[Union[MediaAttachment, IdType]]] = None,
                    sensitive: Optional[bool] = False, visibility: Optional[str] = None, spoiler_text: Optional[str] = None, language: Optional[str] = None, 
                    idempotency_key: Optional[str] = None, content_type: Optional[str] = None, scheduled_at: Optional[datetime] = None, 
                    poll: Optional[Union[Poll, IdType]] = None, quote_id: Optional[Union[Status, IdType]] = None, edit: bool = False,
                    strict_content_type: bool = False, media_attributes: Optional[List[Dict[str, Any]]] = None) -> Union[Status, ScheduledStatus]:
        """
        Internal statuses poster helper
        """
        if quote_id is not None:
            if self.feature_set != "fedibird":
                raise MastodonIllegalArgumentError('quote_id is only available with feature set fedibird')
            quote_id = self.__unpack_id(quote_id)

        if content_type is not None:
            if self.feature_set != "pleroma":
                if strict_content_type:
                    raise MastodonIllegalArgumentError('content_type is only available with feature set pleroma')
                
            # It would be better to read this from nodeinfo and cache, but this is easier
            if not content_type in ["text/plain", "text/html", "text/markdown", "text/bbcode"]:
                if strict_content_type:
                    raise MastodonIllegalArgumentError('Invalid content type specified')

        if in_reply_to_id is not None:
            in_reply_to_id = self.__unpack_id(in_reply_to_id)

        if scheduled_at is not None:
            scheduled_at = self.__consistent_isoformat_utc(scheduled_at)

        params_initial = locals()

        # Validate poll/media exclusivity
        if poll is not None:
            if media_ids is not None and len(media_ids) != 0:
                raise ValueError(
                    'Status can have media or poll attached - not both.')

        # Validate visibility parameter
        valid_visibilities = ['private', 'public', 'unlisted', 'direct']
        if params_initial['visibility'] is None:
            del params_initial['visibility']
        else:
            params_initial['visibility'] = params_initial['visibility'].lower()
            if params_initial['visibility'] not in valid_visibilities:
                raise ValueError(f'Invalid visibility value! Acceptable values are {valid_visibilities}')

        if params_initial['language'] is None:
            del params_initial['language']

        if params_initial['sensitive'] is False:
            del params_initial['sensitive']

        headers = {}
        if idempotency_key is not None:
            headers['Idempotency-Key'] = idempotency_key

        if media_ids is not None:
            try:
                media_ids_proper = []
                if not isinstance(media_ids, (list, tuple)):
                    media_ids = [media_ids]
                for media_id in media_ids:
                    media_ids_proper.append(self.__unpack_id(media_id))
            except Exception as e:
                raise MastodonIllegalArgumentError(f"Invalid media dict: {e}")

            params_initial["media_ids"] = media_ids_proper

        if params_initial['content_type'] is None:
            del params_initial['content_type']

        use_json = False
        if poll is not None or media_attributes is not None:
            use_json = True

        # If media_attributes is set, make sure that media_ids contains at least all the IDs of the media from media_attributes
        if media_attributes is not None:
            if "media_ids" in params_initial and params_initial["media_ids"] is not None:
                params_initial["media_ids"] = list(set(params_initial["media_ids"]) + set([x["id"] for x in media_attributes]))
            else:
                params_initial["media_ids"] = [x["id"] for x in media_attributes]

        params = self.__generate_params(params_initial, ['idempotency_key', 'edit', 'strict_content_type'], for_json = use_json)
        cast_type = Status
        if scheduled_at is not None:
            cast_type = ScheduledStatus
        if edit is None:
            # Post
            return self.__api_request('POST', '/api/v1/statuses', params, headers=headers, use_json=use_json, override_type=cast_type)
        else:
            # Edit
            return self.__api_request('PUT', f'/api/v1/statuses/{self.__unpack_id(edit)}', params, headers=headers, use_json=use_json, override_type=cast_type)

    @api_version("1.0.0", "2.8.0")
    def status_post(self, status: str, in_reply_to_id: Optional[Union[Status, IdType]] = None, media_ids: Optional[List[Union[MediaAttachment, IdType]]] = None,
                    sensitive: bool = False, visibility: Optional[str] = None, spoiler_text: Optional[str] = None, language: Optional[str] = None, 
                    idempotency_key: Optional[str] = None, content_type: Optional[str] = None, scheduled_at: Optional[datetime] = None, 
                    poll: Optional[Union[Poll, IdType]] = None, quote_id: Optional[Union[Status, IdType]] = None, strict_content_type: bool = False) -> Union[Status, ScheduledStatus]:
        """
        Post a status. Can optionally be in reply to another status and contain
        media.

        `media_ids` should be a list. (If it's not, the function will turn it
        into one.) It can contain up to four pieces of media (uploaded via
        :ref:`media_post() <media_post()>`). `media_ids` can also be the objects returned
        by :ref:`media_post() <media_post()>` - they are unpacked automatically.

        The `sensitive` boolean decides whether or not media attached to the post
        should be marked as sensitive, which hides it by default on the Mastodon
        web front-end.

        The `visibility` parameter is a string value and accepts any of:
        
        * ``'direct'`` - post will be visible only to **mentioned users**, known in Mastodon's UI as "Mentioned users only"
        * ``'private'`` - post will be visible only to **followers**, known in Mastodon's UI as "Followers only"
        * ``'unlisted'`` - post will be public but **will not appear** on the public timelines
        * ``'public'`` - post will be public and **will appear** on public timelines

\
        If not passed in, `visibility` defaults to match the current account's
        default-privacy setting (starting with Mastodon version 1.6) or its
        locked setting - ``'private'`` if the account is locked, ``'public'`` otherwise
        (for Mastodon versions lower than 1.6).

        The `spoiler_text` parameter is a string to be shown as a warning before
        the text of the status.  If no text is passed in, no warning will be
        displayed.

        Specify `language` to override automatic language detection. The parameter
        accepts all valid ISO 639-1 (2-letter) or for languages where that do not
        have one, 639-3 (three letter) language codes.

        You can set `idempotency_key` to a value to uniquely identify an attempt
        at posting a status. Even if you call this function more than once,
        if you call it with the same `idempotency_key`, only one status will
        be created.

        Pass a datetime as `scheduled_at` to schedule the toot for a specific time
        (the time must be at least 5 minutes into the future). If this is passed,
        status_post returns a `ScheduledStatus` instead.

        Pass `poll` to attach a poll to the status. An appropriate object can be
        constructed using :ref:`make_poll() <make_poll()>` . Note that as of Mastodon version
        2.8.2, you can only have either media or a poll attached, not both at
        the same time.

        You can use :ref:`get_status_length() <get_status_length()>` to count how many
        characters a status you want to post would take up in terms of Mastodons character
        limit. The limits can be retrieved from the instance information (`instance_v2()`).

        **Specific to "pleroma" feature set:**: Specify `content_type` to set
        the content type of your post on Pleroma. It accepts 'text/plain' (default),
        'text/markdown', 'text/html' and 'text/bbcode'. This parameter is not
        supported on Mastodon servers, but will be safely ignored if set.
        If you want to throw an error if the content type is not known
        to work on the server, set `strict_content_type` to True.

        **Specific to "fedibird" feature set:**: The `quote_id` parameter is
        a non-standard extension that specifies the id of a quoted status.

        Returns the new status.
        """
        return self.__status_internal(
            status,
            in_reply_to_id,
            media_ids,
            sensitive,
            visibility,
            spoiler_text,
            language,
            idempotency_key,
            content_type,
            scheduled_at,
            poll,
            quote_id,
            edit=None,
            strict_content_type=strict_content_type
        )

    @api_version("1.0.0", "2.8.0")
    def toot(self, status: str) -> Status:
        """
        Synonym for :ref:`status_post() <status_post()>` that only takes the status text as input.

        Usage in production code is not recommended.
        """
        return self.status_post(status)


    def generate_media_edit_attributes(self, id: Union[MediaAttachment, IdType], description: Optional[str] = None, 
                                      focus: Optional[Tuple[float, float]] = None, 
                                      thumbnail: Optional[PathOrFile] = None, thumb_mimetype: Optional[str] = None) -> Dict[str, Any]:
        """
        Helper function to generate a single media edit attribute dictionary.
        
        Parameters:
        - `id` (str): The ID of the media attachment (mandatory).
        - `description` (Optional[str]): A new description for the media.
        - `focus` (Optional[Tuple[float, float]]): The focal point of the media.
        - `thumbnail` (Optional[PathOrFile]): The thumbnail to be used.
        """
        media_edit = {"id": self.__unpack_id(id)}
        
        if description is not None:
            media_edit["description"] = description
        
        if focus is not None:
            if isinstance(focus, tuple) and len(focus) == 2:
                media_edit["focus"] = f"{focus[0]},{focus[1]}"
            else:
                raise MastodonIllegalArgumentError("Focus must be a tuple of two floats between -1 and 1")
        
        if thumbnail is not None:
            if not self.verify_minimum_version("3.2.0", cached=True):
                raise MastodonVersionError('Thumbnail requires version > 3.2.0')
            _, thumb_file, thumb_mimetype = self.__load_media_file(thumbnail, thumb_mimetype)
            media_edit["thumbnail"] =  f"data:{thumb_mimetype};base64,{base64.b64encode(thumb_file.read()).decode()}"
        
        return media_edit

    @api_version("3.5.0", "4.1.0")
    def status_update(self, id: Union[Status, IdType], status: str, spoiler_text: Optional[str] = None, 
                      sensitive: Optional[bool] = None, media_ids: Optional[List[Union[MediaAttachment, IdType]]] = None, 
                      poll: Optional[Union[Poll, IdType]] = None, media_attributes: Optional[List[Dict[str, Any]]] = None) -> Status:
        """
        Edit a status. The meanings of the fields are largely the same as in :ref:`status_post() <status_post()>`,
        though not every field can be edited. The `status` parameter is mandatory.

        Note that editing a poll will reset the votes.

        To edit media metadata, generate a list of dictionaries with the following keys:
        """
        return self.__status_internal(
            status=status,
            media_ids=media_ids,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
            poll=poll,
            edit=id,
            media_attributes=media_attributes
        )

    @api_version("3.5.0", "3.5.0")
    def status_history(self, id: Union[StatusEdit, IdType]) -> NonPaginatableList[StatusEdit]:
        """
        Returns the edit history of a status as a list of StatusEdit objects, starting
        from the original form. Note that this means that a status that has been edited
        once will have *two* entries in this list, a status that has been edited twice
        will have three, and so on.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f"/api/v1/statuses/{id}/history")

    def status_source(self, id: Union[Status, IdType]) -> StatusSource:
        """
        Returns the source of a status for editing.

        Return value is a dictionary containing exactly the parameters you could pass to
        :ref:`status_update() <status_update()>` to change nothing about the status, except `status` is `text`
        instead.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f"/api/v1/statuses/{id}/source")

    @api_version("1.0.0", "2.8.0")
    def status_reply(self, to_status: Union[Status, IdType], status: str, media_ids: Optional[List[Union[MediaAttachment, IdType]]] = None,
                    sensitive: bool = False, visibility: Optional[str] = None, spoiler_text: Optional[str] = None, language: Optional[str] = None, 
                    idempotency_key: Optional[str] = None, content_type: Optional[str] = None, scheduled_at: Optional[datetime] = None, 
                    poll: Optional[Union[Poll, IdType]] = None, quote_id: Optional[Union[Status, IdType]] = None, untag: bool = False, 
                    strict_content_type: bool = False) -> Status:
        """
        Helper function - acts like status_post, but prepends the name of all
        the users that are being replied to the status text and retains
        CW and visibility if not explicitly overridden.

        Note that `to_status` must be a `Status` and not just an ID. 

        Set `untag` to True if you want the reply to only go to the user you
        are replying to, removing every other mentioned user from the
        conversation.
        """
        keyword_args = locals().copy()
        del keyword_args["self"]
        del keyword_args["to_status"]
        del keyword_args["untag"]

        user_id = self.__get_logged_in_id()

        # Determine users to mention
        mentioned_accounts = collections.OrderedDict()
        try:
            mentioned_accounts[to_status.account.id] = to_status.account.acct
        except AttributeError as e:
            raise TypeError("to_status must specify a status dict!") from e

        if not untag:
            for account in to_status.mentions:
                if account.id != user_id and not account.id in mentioned_accounts.keys():
                    mentioned_accounts[account.id] = account.acct

        # Join into one piece of text. The space is added inside because of self-replies.
        status = " ".join(f"@{x}" for x in mentioned_accounts.values()) + " " + status

        # Retain visibility / cw
        if visibility is None and 'visibility' in to_status:
            visibility = to_status.visibility
        if spoiler_text is None and 'spoiler_text' in to_status:
            spoiler_text = to_status.spoiler_text

        keyword_args["status"] = status
        keyword_args["visibility"] = visibility
        keyword_args["spoiler_text"] = spoiler_text
        keyword_args["in_reply_to_id"] = to_status.id
        return self.status_post(**keyword_args)

    @api_version("1.0.0", "1.0.0")
    def status_delete(self, id: Union[Status, IdType], delete_media: bool = None) -> Status:
        """
        Delete a status

        Returns the now-deleted status, with an added "text" attribute that contains
        the text that was used to compose this status (this can be used to power
        "delete and redraft" functionality) as well as either poll or media_attachments
        set in the same way. Note that when reattaching media, you have to wait up to several
        seconds for the media to be un-attached from the original status - that operation is
        not synchronous with the delete.

        Pass `delete_media=True` to delete the media attachments of the status immediately,
        instead of just scheduling them for deletion as part of the next media cleanup. If you
        set this, you will not be able to reuse them in a new status (so if you're delete-redrafting,
        you should not set this).
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('DELETE', f'/api/v1/statuses/{id}', params)

    @api_version("1.0.0", "2.0.0")
    def status_reblog(self, id: Union[Status, IdType], visibility: Optional[str] = None) -> Status:
        """
        Reblog / boost a status.

        The visibility parameter functions the same as in :ref:`status_post() <status_post()>` and
        allows you to reduce the visibility of a reblogged status.

        Returns a new Status that wraps around the reblogged status.
        """
        params = self.__generate_params(locals(), ['id'])
        valid_visibilities = ['private', 'public', 'unlisted', 'direct']
        if 'visibility' in params:
            params['visibility'] = params['visibility'].lower()
            if params['visibility'] not in valid_visibilities:
                raise ValueError(f'Invalid visibility value! Acceptable values are {valid_visibilities}')

        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/reblog', params)

    @api_version("1.0.0", "2.0.0")
    def status_unreblog(self, id: Union[Status, IdType]) -> Status:
        """
        Un-reblog a status.

        Returns the status that used to be reblogged.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unreblog')

    @api_version("1.0.0", "2.0.0")
    def status_favourite(self, id: Union[Status, IdType]) -> Status:
        """
        Favourite a status.

        Returns the favourited status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/favourite')

    @api_version("1.0.0", "2.0.0")
    def status_unfavourite(self, id: Union[Status, IdType]) -> Status: 
        """
        Un-favourite a status.

        Returns the un-favourited status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unfavourite')

    @api_version("1.4.0", "2.0.0")
    def status_mute(self, id: Union[Status, IdType]) -> Status:
        """
        Mute notifications for a status.

        Returns the now muted status
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/mute')

    @api_version("1.4.0", "2.0.0")
    def status_unmute(self, id: Union[Status, IdType]) -> Status:
        """
        Unmute notifications for a status.

        Returns the status that used to be muted.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unmute')

    @api_version("2.1.0", "2.1.0")
    def status_pin(self, id: Union[Status, IdType]) -> Status:
        """
        Pin a status for the logged-in user.

        Returns the now pinned status
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/pin')

    @api_version("2.1.0", "2.1.0")
    def status_unpin(self, id: Union[Status, IdType]) -> Status:
        """
        Unpin a pinned status for the logged-in user.

        Returns the status that used to be pinned.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unpin')

    @api_version("3.1.0", "3.1.0")
    def status_bookmark(self, id: Union[Status, IdType]) -> Status:
        """
        Bookmark a status as the logged-in user.

        Returns the now bookmarked status
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/bookmark')

    @api_version("3.1.0", "3.1.0")
    def status_unbookmark(self, id: Union[Status, IdType]) -> Status:
        """
        Unbookmark a bookmarked status for the logged-in user.

        Returns the status that used to be bookmarked.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unbookmark')

    ###
    # Writing data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0")
    def scheduled_status_update(self, id: Union[Status, IdType], scheduled_at: datetime) -> ScheduledStatus:
        """
        Update the scheduled time of a scheduled status.

        New time must be at least 5 minutes into the future.

        Returned object reflects the updates to the scheduled status.
        """
        scheduled_at = self.__consistent_isoformat_utc(scheduled_at)
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', f'/api/v1/scheduled_statuses/{id}', params)

    @api_version("2.7.0", "2.7.0")
    def scheduled_status_delete(self, id: Union[Status, IdType]):
        """
        Deletes a scheduled status.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/scheduled_statuses/{id}')

    ##
    # Translation
    ##
    @api_version("4.0.0", "4.0.0")
    def status_translate(self, id: Union[Status, IdType], lang: Optional[str] = None) -> Translation:
        """
        Translate the status content into some language.

        Raises a MastodonAPIError if the server can't perform the requested translation, for any
        reason (doesn't support translation, unsupported language pair, etc.).
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])

        return self.__api_request('POST', f'/api/v1/statuses/{id}/translate', params)
