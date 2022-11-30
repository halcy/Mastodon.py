from .defaults import _DEFAULT_SCOPES, _SCOPE_SETS
from .error import MastodonIllegalArgumentError, MastodonAPIError
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
            raise MastodonIllegalArgumentError('Invalid request during oauth phase: %s' % e)

        # Step 2: Use that to create a user
        try:
            response = self.__api_request('POST', '/api/v1/accounts', params, do_ratelimiting=False, access_token_override=temp_access_token, skip_error_check=True)
            if "error" in response:
                if return_detailed_error:
                    return None, response
                raise MastodonIllegalArgumentError('Invalid request: %s' % e)
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
            raise MastodonAPIError('Granted scopes "' + " ".join(received_scopes) + '" do not contain all of the requested scopes "' + " ".join(scopes) + '".')

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
