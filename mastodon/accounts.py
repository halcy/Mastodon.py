# accounts.py - account related endpoints

import collections

from .versions import _DICT_VERSION_ACCOUNT, _DICT_VERSION_STATUS, _DICT_VERSION_RELATIONSHIP, _DICT_VERSION_LIST, _DICT_VERSION_FAMILIAR_FOLLOWERS, _DICT_VERSION_HASHTAG
from .defaults import _DEFAULT_SCOPES, _SCOPE_SETS
from .errors import MastodonIllegalArgumentError, MastodonAPIError, MastodonNotFoundError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    @api_version("2.7.0", "2.7.0", "3.4.0")
    def create_account(self, username, password, email, agreement=False, reason=None, locale="en", scopes=_DEFAULT_SCOPES, to_file=None, return_detailed_error=False):
        """
        Creates a new user account with the given username, password and email. "agreement"
        must be set to true (after showing the user the instance's user agreement and having
        them agree to it), "locale" specifies the language for the confirmation email as an
        ISO 639-1 (two letter) or, if a language does not have one, 639-3 (three letter) language
        code. `reason` can be used to specify why a user would like to join if approved-registrations
        mode is on.

        Does not require an access token, but does require a client grant.

        By default, this method is rate-limited by IP to 5 requests per 30 minutes.

        Returns an access token (just like log_in), which it can also persist to to_file,
        and sets it internally so that the user is now logged in. Note that this token
        can only be used after the user has confirmed their email.

        By default, the function will throw if the account could not be created. Alternately,
        when `return_detailed_error` is passed, Mastodon.py will return the detailed error
        response that the API provides (Starting from version 3.4.0 - not checked here) as an dict with
        error details as the second return value and the token returned as `None` in case of error.
        The dict will contain a text `error` values as well as a `details` value which is a dict with
        one optional key for each potential field (`username`, `password`, `email` and `agreement`),
        each if present containing a dict with an `error` category and free text `description`.
        Valid error categories are:

            * ERR_BLOCKED - When e-mail provider is not allowed
            * ERR_UNREACHABLE - When e-mail address does not resolve to any IP via DNS (MX, A, AAAA)
            * ERR_TAKEN - When username or e-mail are already taken
            * ERR_RESERVED - When a username is reserved, e.g. "webmaster" or "admin"
            * ERR_ACCEPTED - When agreement has not been accepted
            * ERR_BLANK - When a required attribute is blank
            * ERR_INVALID - When an attribute is malformed, e.g. wrong characters or invalid e-mail address
            * ERR_TOO_LONG - When an attribute is over the character limit
            * ERR_TOO_SHORT - When an attribute is under the character requirement
            * ERR_INCLUSION - When an attribute is not one of the allowed values, e.g. unsupported locale
        """
        params = self.__generate_params(locals(), ['to_file', 'scopes'])
        params['client_id'] = self.client_id
        params['client_secret'] = self.client_secret

        if not agreement:
            del params['agreement']

        # Step 1: Get a user-free token via oauth
        try:
            oauth_params = {}
            oauth_params['scope'] = " ".join(scopes)
            oauth_params['client_id'] = self.client_id
            oauth_params['client_secret'] = self.client_secret
            oauth_params['grant_type'] = 'client_credentials'

            response = self.__api_request('POST', '/oauth/token', oauth_params, do_ratelimiting=False)
            temp_access_token = response['access_token']
        except Exception as e:
            raise MastodonIllegalArgumentError(f'Invalid request during oauth phase: {e}')

        # Step 2: Use that to create a user
        try:
            response = self.__api_request('POST', '/api/v1/accounts', params, do_ratelimiting=False, access_token_override=temp_access_token, skip_error_check=True)
            if "error" in response:
                if return_detailed_error:
                    return None, response
                raise MastodonIllegalArgumentError(f'Invalid request: {e}')
            self.access_token = response['access_token']
            self.__set_refresh_token(response.get('refresh_token'))
            self.__set_token_expired(int(response.get('expires_in', 0)))
        except Exception as e:
            raise MastodonIllegalArgumentError('Invalid request')

        # Step 3: Check scopes, persist, et cetera
        received_scopes = response["scope"].split(" ")
        for scope_set in _SCOPE_SETS.keys():
            if scope_set in received_scopes:
                received_scopes += _SCOPE_SETS[scope_set]

        if not set(scopes) <= set(received_scopes):
            raise MastodonAPIError(
                f'Granted scopes "{" ".join(received_scopes)}" '
                f'do not contain all of the requested scopes "{" ".join(scopes)}".'
            )

        if to_file is not None:
            with open(to_file, 'w') as token_file:
                token_file.write(response['access_token'] + "\n")
                token_file.write(self.api_base_url + "\n")

        self.__logged_in_id = None

        if return_detailed_error:
            return response['access_token'], {}
        else:
            return response['access_token']

    @api_version("3.4.0", "3.4.0", "3.4.0")
    def email_resend_confirmation(self):
        """
        Requests a re-send of the users confirmation mail for an unconfirmed logged in user.

        Only available to the app that the user originally signed up with.
        """
        self.__api_request('POST', '/api/v1/emails/confirmations')

    ###
    # Reading data: Accounts
    ###
    @api_version("1.0.0", "1.0.0", _DICT_VERSION_ACCOUNT)
    def account(self, id):
        """
        Fetch account information by user `id`.

        Does not require authentication for publicly visible accounts.

        Returns a :ref:`account dict <account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/accounts/{id}')

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def account_verify_credentials(self):
        """
        Fetch logged-in user's account information.

        Returns a :ref:`account dict <account dict>` (Starting from 2.1.0, with an additional "source" field).
        """
        return self.__api_request('GET', '/api/v1/accounts/verify_credentials')

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def me(self):
        """
        Get this user's account. Synonym for `account_verify_credentials()`, does exactly
        the same thing, just exists because `account_verify_credentials()` has a confusing
        name.
        """
        return self.account_verify_credentials()

    @api_version("1.0.0", "2.8.0", _DICT_VERSION_STATUS)
    def account_statuses(self, id, only_media=False, pinned=False, exclude_replies=False, exclude_reblogs=False, tagged=None, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch statuses by user `id`. Same options as :ref:`timeline() <timeline()>` are permitted.
        Returned toots are from the perspective of the logged-in user, i.e.
        all statuses visible to the logged-in user (including DMs) are
        included.

        If `only_media` is set, return only statuses with media attachments.
        If `pinned` is set, return only statuses that have been pinned. Note that
        as of Mastodon 2.1.0, this only works properly for instance-local users.
        If `exclude_replies` is set, filter out all statuses that are replies.
        If `exclude_reblogs` is set, filter out all statuses that are reblogs.
        If `tagged` is set, return only statuses that are tagged with `tagged`. Only a single tag without a '#' is valid.

        Does not require authentication for Mastodon versions after 2.7.0 (returns
        publicly visible statuses in that case), for publicly visible accounts.

        Returns a list of :ref:`status dicts <status dicts>`.
        """
        id = self.__unpack_id(id)
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        if not pinned:
            del params["pinned"]
        if not only_media:
            del params["only_media"]
        if not exclude_replies:
            del params["exclude_replies"]
        if not exclude_reblogs:
            del params["exclude_reblogs"]

        return self.__api_request('GET', f'/api/v1/accounts/{id}/statuses', params)

    @api_version("1.0.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def account_following(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch users the given user is following.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', f'/api/v1/accounts/{id}/following', params)

    @api_version("1.0.0", "2.6.0", _DICT_VERSION_ACCOUNT)
    def account_followers(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch users the given user is followed by.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        id = self.__unpack_id(id)
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', f'/api/v1/accounts/{id}/followers', params)

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_relationships(self, id):
        """
        Fetch relationship (following, followed_by, blocking, follow requested) of
        the logged in user to a given account. `id` can be a list.

        Returns a list of :ref:`relationship dicts <relationship dicts>`.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/relationships',
                                  params)

    @api_version("1.0.0", "2.3.0", _DICT_VERSION_ACCOUNT)
    def account_search(self, q, limit=None, following=False, resolve=False):
        """
        Fetch matching accounts. Will lookup an account remotely if the search term is
        in the username@domain format and not yet in the database. Set `following` to
        True to limit the search to users the logged-in user follows.

        Returns a list of :ref:`account dicts <account dicts>`.
        """
        params = self.__generate_params(locals())

        if params["following"] == False:
            del params["following"]

        return self.__api_request('GET', '/api/v1/accounts/search', params)

    @api_version("2.1.0", "2.1.0", _DICT_VERSION_LIST)
    def account_lists(self, id):
        """
        Get all of the logged-in user's lists which the specified user is
        a member of.

        Returns a list of :ref:`list dicts <list dicts>`.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', f'/api/v1/accounts/{id}/lists', params)

    @api_version("3.4.0", "3.4.0", _DICT_VERSION_ACCOUNT)
    def account_lookup(self, acct):
        """
        Look up an account from user@instance form (@instance allowed but not required for
        local accounts). Will only return accounts that the instance already knows about,
        and not do any webfinger requests. Use `account_search` if you need to resolve users
        through webfinger from remote.

        Returns an :ref:`account dict <account dict>`.
        """
        return self.__api_request('GET', '/api/v1/accounts/lookup', self.__generate_params(locals()))

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_FAMILIAR_FOLLOWERS)
    def account_familiar_followers(self, id):
        """
        Find followers for the account given by id (can be a list) that also follow the
        logged in account.

        Returns a list of :ref:`familiar follower dicts <familiar follower dicts>`
        """
        if not isinstance(id, list):
            id = [id]
        for i in range(len(id)):
            id[i] = self.__unpack_id(id[i])
        return self.__api_request('GET', '/api/v1/accounts/familiar_followers', {'id': id}, use_json=True)

    ###
    # Writing data: Accounts
    ###
    @api_version("1.0.0", "3.3.0", _DICT_VERSION_RELATIONSHIP)
    def account_follow(self, id, reblogs=True, notify=False):
        """
        Follow a user.

        Set `reblogs` to False to hide boosts by the followed user.
        Set `notify` to True to get a notification every time the followed user posts.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])

        if params["reblogs"] is None:
            del params["reblogs"]

        return self.__api_request('POST', f'/api/v1/accounts/{id}/follow', params)

    @api_version("1.0.0", "2.1.0", _DICT_VERSION_ACCOUNT)
    def follows(self, uri):
        """
        Follow a remote user with username given in username@domain form.

        Returns a :ref:`account dict <account dict>`.

        Deprecated - avoid using this. Currently uses a backwards compat implementation that may or may not work properly.
        """
        try:
            acct = self.account_search(uri)[0]
        except:
            raise MastodonNotFoundError("User not found")
        return self.account_follow(acct)

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_unfollow(self, id):
        """
        Unfollow a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unfollow')

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_RELATIONSHIP)
    def account_remove_from_followers(self, id):
        """
        Remove a user from the logged in users followers (i.e. make them unfollow the logged in
        user / "softblock" them).

        Returns a :ref:`relationship dict <relationship dict>` reflecting the updated following status.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/remove_from_followers')

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_block(self, id):
        """
        Block a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/block')

    @api_version("1.0.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_unblock(self, id):
        """
        Unblock a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unblock')

    @api_version("1.1.0", "2.4.3", _DICT_VERSION_RELATIONSHIP)
    def account_mute(self, id, notifications=True, duration=None):
        """
        Mute a user.

        Set `notifications` to False to receive notifications even though the user is
        muted from timelines. Pass a `duration` in seconds to have Mastodon automatically
        lift the mute after that many seconds.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('POST', f'/api/v1/accounts/{id}/mute', params)

    @api_version("1.1.0", "1.4.0", _DICT_VERSION_RELATIONSHIP)
    def account_unmute(self, id):
        """
        Unmute a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unmute')

    @api_version("1.1.1", "3.1.0", _DICT_VERSION_ACCOUNT)
    def account_update_credentials(self, display_name=None, note=None,
                                   avatar=None, avatar_mime_type=None,
                                   header=None, header_mime_type=None,
                                   locked=None, bot=None,
                                   discoverable=None, fields=None):
        """
        Update the profile for the currently logged-in user.

        `note` is the user's bio.

        `avatar` and 'header' are images. As with media uploads, it is possible to either
        pass image data and a mime type, or a filename of an image file, for either.

        `locked` specifies whether the user needs to manually approve follow requests.

        `bot` specifies whether the user should be set to a bot.

        `discoverable` specifies whether the user should appear in the user directory.

        `fields` can be a list of up to four name-value pairs (specified as tuples) to
        appear as semi-structured information in the user's profile.

        Returns the updated `account dict` of the logged-in user.
        """
        params_initial = collections.OrderedDict(locals())

        # Convert fields
        if fields is not None:
            if len(fields) > 4:
                raise MastodonIllegalArgumentError(
                    'A maximum of four fields are allowed.')

            fields_attributes = []
            for idx, (field_name, field_value) in enumerate(fields):
                params_initial[f'fields_attributes[{idx}][name]'] = field_name
                params_initial[f'fields_attributes[{idx}][value]'] = field_value

        # Clean up params
        for param in ["avatar", "avatar_mime_type", "header", "header_mime_type", "fields"]:
            if param in params_initial:
                del params_initial[param]

        # Create file info
        files = {}
        if avatar is not None:
            files["avatar"] = self.__load_media_file(avatar, avatar_mime_type)
        if header is not None:
            files["header"] = self.__load_media_file(header, header_mime_type)

        params = self.__generate_params(params_initial)
        return self.__api_request('PATCH', '/api/v1/accounts/update_credentials', params, files=files)

    @api_version("2.5.0", "2.5.0", _DICT_VERSION_RELATIONSHIP)
    def account_pin(self, id):
        """
        Pin / endorse a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/pin')

    @api_version("2.5.0", "2.5.0", _DICT_VERSION_RELATIONSHIP)
    def account_unpin(self, id):
        """
        Unpin / un-endorse a user.

        Returns a :ref:`relationship dict <relationship dict>` containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unpin')

    @api_version("3.2.0", "3.2.0", _DICT_VERSION_RELATIONSHIP)
    def account_note_set(self, id, comment):
        """
        Set a note (visible to the logged in user only) for the given account.

        Returns a :ref:`status dict <status dict>` with the `note` updated.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])
        return self.__api_request('POST', f'/api/v1/accounts/{id}/note', params)

    @api_version("3.3.0", "3.3.0", _DICT_VERSION_HASHTAG)
    def account_featured_tags(self, id):
        """
        Get an account's featured hashtags.

        Returns a list of :ref:`hashtag dicts <hashtag dicts>` (NOT `featured tag dicts`_).
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/accounts/{id}/featured_tags')
