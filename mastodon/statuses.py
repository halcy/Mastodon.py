# statuses.py - status endpoints (regular and scheduled)

import collections

from .versions import _DICT_VERSION_STATUS, _DICT_VERSION_CARD, _DICT_VERSION_CONTEXT, _DICT_VERSION_ACCOUNT, _DICT_VERSION_SCHEDULED_STATUS, \
                        _DICT_VERSION_STATUS_EDIT
from .errors import MastodonIllegalArgumentError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Statuses
    ###
    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status(self, id):
        """
        Fetch information about a single toot.

        Does not require authentication for publicly visible statuses.

        Returns a :ref:`status dict <status dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}')

    @api_version("1.0.0", "3.0.0", _DICT_VERSION_CARD)
    def status_card(self, id):
        """
        Fetch a card associated with a status. A card describes an object (such as an
        external video or link) embedded into a status.

        Does not require authentication for publicly visible statuses.

        This function is deprecated as of 3.0.0 and the endpoint does not
        exist anymore - you should just use the "card" field of the status dicts
        instead. Mastodon.py will try to mimic the old behaviour, but this
        is somewhat inefficient and not guaranteed to be the case forever.

        Returns a :ref:`card dict <card dict>`.
        """
        if self.verify_minimum_version("3.0.0", cached=True):
            return self.status(id).card
        else:
            id = self.__unpack_id(id)
            return self.__api_request('GET', f'/api/v1/statuses/{id}/card')

    @api_version("1.0.0", "1.0.0", _DICT_VERSION_CONTEXT)
    def status_context(self, id):
        """
        Fetch information about ancestors and descendants of a toot.

        Does not require authentication for publicly visible statuses.

        Returns a :ref:`context dict <context dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}/context')

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def status_reblogged_by(self, id):
        """
        Fetch a list of users that have reblogged a status.

        Does not require authentication for publicly visible statuses.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}/reblogged_by')

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def status_favourited_by(self, id):
        """
        Fetch a list of users that have favourited a status.

        Does not require authentication for publicly visible statuses.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/statuses/{id}/favourited_by')

    ###
    # Reading data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0", _DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_statuses(self):
        """
        Fetch a list of scheduled statuses

        Returns a list of :ref:`scheduled status dicts <scheduled status dicts>`.
        """
        return self.__api_request('GET', '/api/v1/scheduled_statuses')

    @api_version("2.7.0", "2.7.0", _DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_status(self, id):
        """
        Fetch information about the scheduled status with the given id.

        Returns a :ref:`scheduled status dict <scheduled status dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/scheduled_statuses/{id}')

    ###
    # Writing data: Statuses
    ###
    def __status_internal(self, status, in_reply_to_id=None, media_ids=None,
                    sensitive=False, visibility=None, spoiler_text=None,
                    language=None, idempotency_key=None, content_type=None,
                    scheduled_at=None, poll=None, quote_id=None, edit=False):
        if quote_id is not None:
            if self.feature_set != "fedibird":
                raise MastodonIllegalArgumentError('quote_id is only available with feature set fedibird')
            quote_id = self.__unpack_id(quote_id)

        if content_type is not None:
            if self.feature_set != "pleroma":
                raise MastodonIllegalArgumentError('content_type is only available with feature set pleroma')
            # It would be better to read this from nodeinfo and cache, but this is easier
            if not content_type in ["text/plain", "text/html", "text/markdown", "text/bbcode"]:
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
            del [params_initial['sensitive']]

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
        if poll is not None:
            use_json = True

        params = self.__generate_params(params_initial, ['idempotency_key', 'edit'])
        if edit is None:
            # Post
            return self.__api_request('POST', '/api/v1/statuses', params, headers=headers, use_json=use_json)
        else:
            # Edit
            return self.__api_request('PUT', f'/api/v1/statuses/{self.__unpack_id(edit)}', params, headers=headers, use_json=use_json)

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def status_post(self, status, in_reply_to_id=None, media_ids=None,
                    sensitive=False, visibility=None, spoiler_text=None,
                    language=None, idempotency_key=None, content_type=None,
                    scheduled_at=None, poll=None, quote_id=None):
        """
        Post a status. Can optionally be in reply to another status and contain
        media.

        `media_ids` should be a list. (If it's not, the function will turn it
        into one.) It can contain up to four pieces of media (uploaded via
        :ref:`media_post() <media_post()>`). `media_ids` can also be the `media dicts`_ returned
        by :ref:`media_post() <media_post()>` - they are unpacked automatically.

        The `sensitive` boolean decides whether or not media attached to the post
        should be marked as sensitive, which hides it by default on the Mastodon
        web front-end.

        The visibility parameter is a string value and accepts any of:
        'direct' - post will be visible only to mentioned users
        'private' - post will be visible only to followers
        'unlisted' - post will be public but not appear on the public timeline
        'public' - post will be public

        If not passed in, visibility defaults to match the current account's
        default-privacy setting (starting with Mastodon version 1.6) or its
        locked setting - private if the account is locked, public otherwise
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
        status_post returns a :ref:`scheduled status dict <scheduled status dict>` instead.

        Pass `poll` to attach a poll to the status. An appropriate object can be
        constructed using :ref:`make_poll() <make_poll()>` . Note that as of Mastodon version
        2.8.2, you can only have either media or a poll attached, not both at
        the same time.

        **Specific to "pleroma" feature set:**: Specify `content_type` to set
        the content type of your post on Pleroma. It accepts 'text/plain' (default),
        'text/markdown', 'text/html' and 'text/bbcode'. This parameter is not
        supported on Mastodon servers, but will be safely ignored if set.

        **Specific to "fedibird" feature set:**: The `quote_id` parameter is
        a non-standard extension that specifies the id of a quoted status.

        Returns a :ref:`status dict <status dict>` with the new status.
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
            edit=None
        )

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def toot(self, status):
        """
        Synonym for :ref:`status_post() <status_post()>` that only takes the status text as input.

        Usage in production code is not recommended.

        Returns a :ref:`status dict <status dict>` with the new status.
        """
        return self.status_post(status)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS)
    def status_update(self, id, status=None, spoiler_text=None, sensitive=None, media_ids=None, poll=None):
        """
        Edit a status. The meanings of the fields are largely the same as in :ref:`status_post() <status_post()>`,
        though not every field can be edited.

        Note that editing a poll will reset the votes.
        """
        return self.__status_internal(
            status=status,
            media_ids=media_ids,
            sensitive=sensitive,
            spoiler_text=spoiler_text,
            poll=poll,
            edit=id
        )

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS_EDIT)
    def status_history(self, id):
        """
        Returns the edit history of a status as a list of :ref:`status edit dicts <status edit dicts>`, starting
        from the original form. Note that this means that a status that has been edited
        once will have *two* entries in this list, a status that has been edited twice
        will have three, and so on.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f"/api/v1/statuses/{id}/history")

    def status_source(self, id):
        """
        Returns the source of a status for editing.

        Return value is a dictionary containing exactly the parameters you could pass to
        :ref:`status_update() <status_update()>` to change nothing about the status, except `status` is `text`
        instead.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f"/api/v1/statuses/{id}/source")

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def status_reply(self, to_status, status, in_reply_to_id=None, media_ids=None,
                     sensitive=False, visibility=None, spoiler_text=None,
                     language=None, idempotency_key=None, content_type=None,
                     scheduled_at=None, poll=None, untag=False):
        """
        Helper function - acts like status_post, but prepends the name of all
        the users that are being replied to the status text and retains
        CW and visibility if not explicitly overridden.

        Note that `to_status` should be a :ref:`status dict <status dict>` and not an ID. 

        Set `untag` to True if you want the reply to only go to the user you
        are replying to, removing every other mentioned user from the
        conversation.
        """
        keyword_args = locals()
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

    @api_version("1.0.0", "1.0.0", "1.0.0")
    def status_delete(self, id):
        """
        Delete a status

        Returns the now-deleted status, with an added "source" attribute that contains
        the text that was used to compose this status (this can be used to power
        "delete and redraft" functionality)
        """
        id = self.__unpack_id(id)
        return self.__api_request('DELETE', f'/api/v1/statuses/{id}')

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_reblog(self, id, visibility=None):
        """
        Reblog / boost a status.

        The visibility parameter functions the same as in :ref:`status_post() <status_post()>` and
        allows you to reduce the visibility of a reblogged status.

        Returns a :ref:`status dict <status dict>` with a new status that wraps around the reblogged one.
        """
        params = self.__generate_params(locals(), ['id'])
        valid_visibilities = ['private', 'public', 'unlisted', 'direct']
        if 'visibility' in params:
            params['visibility'] = params['visibility'].lower()
            if params['visibility'] not in valid_visibilities:
                raise ValueError(f'Invalid visibility value! Acceptable values are {valid_visibilities}')

        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/reblog', params)

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_unreblog(self, id):
        """
        Un-reblog a status.

        Returns a :ref:`status dict <status dict>` with the status that used to be reblogged.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unreblog')

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_favourite(self, id):
        """
        Favourite a status.

        Returns a :ref:`status dict <status dict>` with the favourited status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/favourite')

    @api_version("1.0.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_unfavourite(self, id):
        """
        Un-favourite a status.

        Returns a :ref:`status dict <status dict>` with the un-favourited status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unfavourite')

    @api_version("1.4.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_mute(self, id):
        """
        Mute notifications for a status.

        Returns a :ref:`status dict <status dict>` with the now muted status
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/mute')

    @api_version("1.4.0", "2.0.0", _DICT_VERSION_STATUS)
    def status_unmute(self, id):
        """
        Unmute notifications for a status.

        Returns a :ref:`status dict <status dict>` with the status that used to be muted.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unmute')

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_STATUS)
    def status_pin(self, id):
        """
        Pin a status for the logged-in user.

        Returns a :ref:`status dict <status dict>` with the now pinned status
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/pin')

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_STATUS)
    def status_unpin(self, id):
        """
        Unpin a pinned status for the logged-in user.

        Returns a :ref:`status dict <status dict>` with the status that used to be pinned.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unpin')

    @api_version("3.1.0", "3.1.0", _DICT_VERSION_STATUS)
    def status_bookmark(self, id):
        """
        Bookmark a status as the logged-in user.

        Returns a :ref:`status dict <status dict>` with the now bookmarked status
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/bookmark')

    @api_version("3.1.0", "3.1.0", _DICT_VERSION_STATUS)
    def status_unbookmark(self, id):
        """
        Unbookmark a bookmarked status for the logged-in user.

        Returns a :ref:`status dict <status dict>` with the status that used to be bookmarked.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/statuses/{id}/unbookmark')

    ###
    # Writing data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0", _DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_status_update(self, id, scheduled_at):
        """
        Update the scheduled time of a scheduled status.

        New time must be at least 5 minutes into the future.

        Returns a :ref:`scheduled status dict <scheduled status dict>`
        """
        scheduled_at = self.__consistent_isoformat_utc(scheduled_at)
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', f'/api/v1/scheduled_statuses/{id}', params)

    @api_version("2.7.0", "2.7.0", "2.7.0")
    def scheduled_status_delete(self, id):
        """
        Deletes a scheduled status.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/scheduled_statuses/{id}')
