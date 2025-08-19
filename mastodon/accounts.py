# accounts.py - account related endpoints

import collections

from mastodon.defaults import _DEFAULT_SCOPES, _SCOPE_SETS
from mastodon.errors import MastodonIllegalArgumentError, MastodonAPIError, MastodonNotFoundError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals

from typing import Union, Optional, Tuple, List
from mastodon.return_types import AccountCreationError, Account, IdType, Status, PaginatableList, NonPaginatableList, UserList, Relationship, FamiliarFollowers, Tag, IdType, PathOrFile, AttribAccessDict, try_cast_recurse
from datetime import datetime

class Mastodon(Internals):
    @api_version("2.7.0", "2.7.0")
    def create_account(self, username: str, password: str, email: str, agreement: bool = False, reason: Optional[str] = None, 
                        locale: str = "en", scopes: List[str] = _DEFAULT_SCOPES, to_file: Optional[str] = None, 
                        return_detailed_error: bool = False, date_of_birth: Optional[datetime] = None) -> Union[Optional[str], Tuple[Optional[str], AccountCreationError]]:
        """
        Creates a new user account with the given username, password and email. "agreement"
        must be set to true (after showing the user the instance's user agreement and having
        them agree to it), "locale" specifies the language for the confirmation email as an
        ISO 639-1 (two letter) or, if a language does not have one, 639-3 (three letter) language
        code. `reason` can be used to specify why a user would like to join if approved-registrations
        mode is on. date_of_birth can be used to specify the date of birth of the user, which is required
        if the server has a minimum age requirement set.

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
        # Do we have a date of birth? If so, add it to a string in YYYY-MM-DD format.
        if date_of_birth is not None:
            if not isinstance(date_of_birth, datetime):
                raise MastodonIllegalArgumentError("date_of_birth must be a datetime object")
            date_of_birth = date_of_birth.strftime("%Y-%m-%d")

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

            response = self.__api_request('POST', '/oauth/token', oauth_params, do_ratelimiting=False, override_type=AttribAccessDict)
            temp_access_token = response['access_token']
        except Exception as e:
            raise MastodonIllegalArgumentError(f'Invalid request during oauth phase: {e}')

        # Step 2: Use that to create a user
        response = self.__api_request('POST', '/api/v1/accounts', params, do_ratelimiting=False, access_token_override=temp_access_token, skip_error_check=True, override_type=dict)
        if "error" in response:
            if return_detailed_error:
                return None, try_cast_recurse(AccountCreationError, response)
            raise MastodonIllegalArgumentError(f'Invalid request: {response["error"]}')
        self.access_token = response['access_token']
        self.__set_refresh_token(response.get('refresh_token'))
        self.__set_token_expired(int(response.get('expires_in', 0)))

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
            return response['access_token'], AccountCreationError()
        else:
            return response['access_token']

    @api_version("3.4.0", "3.4.0")
    def email_resend_confirmation(self):
        """
        Requests a re-send of the users confirmation mail for an unconfirmed logged in user.

        Only available to the app that the user originally signed up with.
        """
        self.__api_request('POST', '/api/v1/emails/confirmations')

    ###
    # Reading data: Accounts
    ###
    @api_version("1.0.0", "1.0.0")
    def account(self, id: Union[Account, IdType]) -> Account:
        """
        Fetch account information by user `id`.

        Does not require authentication for publicly visible accounts.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/accounts/{id}')

    @api_version("4.3.0", "4.3.0")
    def accounts(self, ids: List[Union[Account, IdType]]) -> List[Account]:
        """
        Fetch information from multiple accounts by a list of user `id`.

        Does not require authentication for publicly visible accounts.
        """
        ids = [self.__unpack_id(id, dateconv=True) for id in ids]
        return self.__api_request('GET', '/api/v1/accounts', {"id[]": ids})

    @api_version("1.0.0", "2.1.0")
    def account_verify_credentials(self) -> Account:
        """
        Fetch logged-in user's account information. Returns the version of the Account object with `source` field.
        """
        return self.__api_request('GET', '/api/v1/accounts/verify_credentials')

    @api_version("1.0.0", "2.1.0")
    def me(self) -> Account:
        """
        Get this user's account. Synonym for `account_verify_credentials()`, does exactly
        the same thing, just exists because `account_verify_credentials()` has a confusing
        name.
        """
        return self.account_verify_credentials()

    @api_version("1.0.0", "2.8.0")
    def account_statuses(self, id: Union[Account, IdType], only_media: bool = False, pinned: bool = False, exclude_replies: bool = False, 
                         exclude_reblogs: bool = False, tagged: Optional[str] = None, max_id: Optional[Union[Status, IdType, datetime]] = None, 
                         min_id: Optional[Union[Status, IdType, datetime]] = None, since_id: Optional[Union[Status, IdType, datetime]] = None, 
                         limit: Optional[int] = None) -> PaginatableList[Status]:
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

    @api_version("1.0.0", "2.6.0")
    def account_following(self, id: Union[Account, IdType], max_id: Optional[Union[Account, IdType]] = None, 
                          min_id: Optional[Union[Account, IdType]] = None, since_id: Optional[Union[Account, IdType]] = None, 
                          limit: Optional[int] = None) -> PaginatableList[Account]:
        """
        Fetch users the given user is following.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'], dateconv=True)
        return self.__api_request('GET', f'/api/v1/accounts/{id}/following', params)

    @api_version("1.0.0", "2.6.0")
    def account_followers(self, id: Union[Account, IdType], max_id: Optional[Union[Account, IdType]] = None, 
                          min_id: Optional[Union[Account, IdType]] = None, since_id: Optional[Union[Account, IdType]] = None, 
                          limit: Optional[int] = None) -> PaginatableList[Account]:
        """
        Fetch users the given user is followed by.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'], dateconv=True)
        return self.__api_request('GET', f'/api/v1/accounts/{id}/followers', params)

    @api_version("1.0.0", "1.4.0")
    def account_relationships(self, id: Union[List[Union[Account, IdType]], Union[Account, IdType]], with_suspended: Optional[bool] = None) -> NonPaginatableList[Relationship]:
        """
        Fetch relationship (following, followed_by, blocking, follow requested) of
        the logged in user to a given account. `id` can be a list.

        Pass `with_suspended = True` to include relationships with suspended accounts.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/relationships',
                                  params)

    @api_version("1.0.0", "2.8.0")
    def account_search(self, q: str, limit: Optional[int] = None, following: bool = False, resolve: bool = False, offset: Optional[int] = None) -> NonPaginatableList[Account]:
        """
        Fetch matching accounts. Will lookup an account remotely if the search term is
        in the username@domain format and not yet in the database. Set `following` to
        True to limit the search to users the logged-in user follows.

        Paginated in a weird way ("limit" / "offset"), if you want to fetch all results
        here please do it yourself for now.
        """
        params = self.__generate_params(locals())

        if params["following"] == False:
            del params["following"]

        return self.__api_request('GET', '/api/v1/accounts/search', params)

    @api_version("2.1.0", "2.1.0")
    def account_lists(self, id: Union[Account, IdType]) -> NonPaginatableList[UserList]:
        """
        Get all of the logged-in user's lists which the specified user is
        a member of.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', f'/api/v1/accounts/{id}/lists', params)

    @api_version("3.4.0", "3.4.0")
    def account_lookup(self, acct: str) -> Account:
        """
        Look up an account from user@instance form (@instance allowed but not required for
        local accounts). Will only return accounts that the instance already knows about,
        and not do any webfinger requests. Use `account_search` if you need to resolve users
        through webfinger from remote.
        """
        return self.__api_request('GET', '/api/v1/accounts/lookup', self.__generate_params(locals()))

    @api_version("3.5.0", "3.5.0")
    def account_familiar_followers(self, id: Union[List[Union[Account, IdType]], Union[Account, IdType]]) -> NonPaginatableList[FamiliarFollowers]:
        """
        Find followers for the account given by id (can be a list) that also follow the
        logged in account.
        """
        id = self.__unpack_id(id, listify = True)
        return self.__api_request('GET', '/api/v1/accounts/familiar_followers', {'id': id}, use_json=True)

    ###
    # Writing data: Accounts
    ###
    @api_version("1.0.0", "3.3.0")
    def account_follow(self, id: Union[Account, IdType], reblogs: bool =True, notify: bool = False) -> Relationship:
        """
        Follow a user.

        Set `reblogs` to False to hide boosts by the followed user.
        Set `notify` to True to get a notification every time the followed user posts.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])

        if params["reblogs"] is None:
            del params["reblogs"]

        return self.__api_request('POST', f'/api/v1/accounts/{id}/follow', params)

    @api_version("1.0.0", "2.1.0")
    def follows(self, uri: str) -> Relationship:
        """
        Follow a remote user with username given in username@domain form.

        Deprecated - avoid using this. Currently uses a backwards compat implementation that may or may not work properly.
        """
        try:
            acct = self.account_search(uri)[0]
        except:
            raise MastodonNotFoundError("User not found")
        return self.account_follow(acct)

    @api_version("1.0.0", "1.4.0")
    def account_unfollow(self, id: Union[Account, IdType]) -> Relationship:
        """
        Unfollow a user.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unfollow')

    @api_version("3.5.0", "3.5.0")
    def account_remove_from_followers(self, id: Union[Account, IdType]) -> Relationship:
        """
        Remove a user from the logged in users followers (i.e. make them unfollow the logged in
        user / "softblock" them).

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/remove_from_followers')

    @api_version("1.0.0", "1.4.0")
    def account_block(self, id: Union[Account, IdType]) -> Relationship:
        """
        Block a user.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/block')

    @api_version("1.0.0", "1.4.0")
    def account_unblock(self, id: Union[Account, IdType]) -> Relationship:
        """
        Unblock a user.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unblock')

    @api_version("1.1.0", "2.4.3")
    def account_mute(self, id: Union[Account, IdType], notifications: bool = True, duration: Optional[int] = None) -> Relationship:
        """
        Mute a user.

        Set `notifications` to False to receive notifications even though the user is
        muted from timelines. Pass a `duration` in seconds to have Mastodon automatically
        lift the mute after that many seconds.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('POST', f'/api/v1/accounts/{id}/mute', params)

    @api_version("1.1.0", "1.4.0")
    def account_unmute(self, id: Union[Account, IdType]) -> Relationship:
        """
        Unmute a user.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unmute')

    @api_version("1.1.1", "3.1.0")
    def account_update_credentials(self, display_name: Optional[str] = None, note: Optional[str] = None,
                                   avatar: Optional[PathOrFile] = None, avatar_mime_type: Optional[str] = None,
                                   header: Optional[PathOrFile] = None, header_mime_type: Optional[str] = None,
                                   locked: Optional[bool] = None, bot: Optional[bool] = None,
                                   discoverable: Optional[bool] = None, fields: Optional[List[Tuple[str, str]]] = None,
                                   attribution_domains: Optional[List[str]] = None) -> Account:
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

        `attribution_domains` can be a list of domains that the user wants to allow to
        attribute content to them.

        The returned object reflects the updated account.
        """
        params_initial = collections.OrderedDict(locals())

        # Convert fields
        if fields is not None:
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

    @api_version("2.5.0", "2.5.0")
    def account_pin(self, id: Union[Account, IdType]) -> Relationship:
        """
        Pin / endorse a user.

        The returned object reflects the updated relationship with the user.

        Deprecated, use `account_endorse` instead.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/pin')

    @api_version("2.5.0", "2.5.0")
    def account_unpin(self, id: Union[Account, IdType]) -> Relationship:
        """
        Unpin / un-endorse a user.

        The returned object reflects the updated relationship with the user.

        Deprecated, use `account_unendorse` instead.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unpin')

    @api_version("4.4.0", "4.4.0")
    def account_endorse(self, id: Union[Account, IdType]) -> Relationship:
        """
        Endorse a user.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/endorse')
    
    @api_version("4.4.0", "4.4.0")
    def account_unendorse(self, id: Union[Account, IdType]) -> Relationship:
        """
        Unendorse a user.

        The returned object reflects the updated relationship with the user.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/accounts/{id}/unendorse')

    @api_version("3.2.0", "3.2.0")
    def account_note_set(self, id: Union[Account, IdType], comment: str) -> Relationship:
        """
        Set a note (visible to the logged in user only) for the given account.

        The returned object contains the updated note.

        nb: To retrieve the current note for an account, use `account_relationships`.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])
        return self.__api_request('POST', f'/api/v1/accounts/{id}/note', params)

    @api_version("3.3.0", "3.3.0")
    def account_featured_tags(self, id: Union[Account, IdType]) -> NonPaginatableList[Tag]:
        """
        Get an account's featured hashtags.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/accounts/{id}/featured_tags')

    @api_version("4.2.0", "4.2.0")
    def account_delete_avatar(self):
        """
        Delete the logged-in user's avatar.
        """
        self.__api_request('DELETE', '/api/v1/profile/avatar')
    
    @api_version("4.2.0", "4.2.0")
    def account_delete_header(self):
        """
        Delete the logged-in user's header.
        """

        self.__api_request('DELETE', '/api/v1/profile/header')
