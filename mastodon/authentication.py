# authentication.py - app and user creation, login, oauth, getting app info, and the constructor

import requests
from requests.models import urlencode
import datetime
import os
import time
import collections

from .errors import MastodonIllegalArgumentError, MastodonNetworkError, MastodonVersionError, MastodonAPIError
from .versions import _DICT_VERSION_APPLICATION
from .defaults import _DEFAULT_SCOPES, _SCOPE_SETS, _DEFAULT_TIMEOUT, _DEFAULT_USER_AGENT
from .utility import parse_version_string, api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Registering apps
    ###
    @staticmethod
    def create_app(client_name, scopes=_DEFAULT_SCOPES, redirect_uris=None, website=None, to_file=None,
                   api_base_url=None, request_timeout=_DEFAULT_TIMEOUT, session=None, user_agent=_DEFAULT_USER_AGENT):
        """
        Create a new app with given `client_name` and `scopes` (The basic scopes are "read", "write", "follow" and "push"
        - more granular scopes are available, please refer to Mastodon documentation for which) on the instance given
        by `api_base_url`.

        Specify `redirect_uris` if you want users to be redirected to a certain page after authenticating in an OAuth flow.
        You can specify multiple URLs by passing a list. Note that if you wish to use OAuth authentication with redirects,
        the redirect URI must be one of the URLs specified here.

        Specify `to_file` to persist your app's info to a file so you can use it in the constructor.
        Specify `website` to give a website for your app.

        Specify `session` with a requests.Session for it to be used instead of the default. This can be
        used to, amongst other things, adjust proxy or SSL certificate settings.

        Specify `user_agent` if you want to use a specific name as `User-Agent` header, otherwise "mastodonpy" will be used.

        Presently, app registration is open by default, but this is not guaranteed to be the case for all
        Mastodon instances in the future.


        Returns `client_id` and `client_secret`, both as strings.
        """
        if api_base_url is None:
            raise MastodonIllegalArgumentError("API base URL is required.")
        api_base_url = Mastodon.__protocolize(api_base_url)

        request_data = {
            'client_name': client_name,
            'scopes': " ".join(scopes)
        }
        headers = {
            'User-Agent': user_agent
        }

        if redirect_uris is not None:
            if isinstance(redirect_uris, (list, tuple)):
                redirect_uris = "\n".join(list(redirect_uris))
            request_data['redirect_uris'] = redirect_uris
        else:
            request_data['redirect_uris'] = 'urn:ietf:wg:oauth:2.0:oob'
        if website is not None:
            request_data['website'] = website
        try:
            if session:
                ret = session.post(f"{api_base_url}/api/v1/apps", data=request_data, headers=headers, timeout=request_timeout)
                response = ret.json()
            else:
                response = requests.post(f"{api_base_url}/api/v1/apps", data=request_data, headers=headers, timeout=request_timeout)
                response = response.json()
        except Exception as e:
            raise MastodonNetworkError(f"Could not complete request: {e}")

        if to_file is not None:
            with open(to_file, 'w') as secret_file:
                secret_file.write(response['client_id'] + "\n")
                secret_file.write(response['client_secret'] + "\n")
                secret_file.write(api_base_url + "\n")
                secret_file.write(client_name + "\n")

        return (response['client_id'], response['client_secret'])

    ###
    # Authentication, including constructor
    ###
    def __init__(self, client_id=None, client_secret=None, access_token=None, api_base_url=None, debug_requests=False,
                 ratelimit_method="wait", ratelimit_pacefactor=1.1, request_timeout=_DEFAULT_TIMEOUT, mastodon_version=None,
                 version_check_mode="created", session=None, feature_set="mainline", user_agent=_DEFAULT_USER_AGENT, lang=None):
        """
        Create a new API wrapper instance based on the given `client_secret` and `client_id` on the
        instance given by `api_base_url`. If you give a `client_id` and it is not a file, you must
        also give a secret. If you specify an `access_token` then you don't need to specify a `client_id`.
        It is allowed to specify neither - in this case, you will be restricted to only using endpoints
        that do not require authentication. If a file is given as `client_id`, client ID, secret and
        base url are read from that file.

        You can also specify an `access_token`, directly or as a file (as written by :ref:`log_in() <log_in()>`). If
        a file is given, Mastodon.py also tries to load the base URL from this file, if present. A
        client id and secret are not required in this case.

        Mastodon.py can try to respect rate limits in several ways, controlled by `ratelimit_method`.
        "throw" makes functions throw a `MastodonRatelimitError` when the rate
        limit is hit. "wait" mode will, once the limit is hit, wait and retry the request as soon
        as the rate limit resets, until it succeeds. "pace" works like throw, but tries to wait in
        between calls so that the limit is generally not hit (how hard it tries to avoid hitting the rate
        limit can be controlled by ratelimit_pacefactor). The default setting is "wait". Note that
        even in "wait" and "pace" mode, requests can still fail due to network or other problems! Also
        note that "pace" and "wait" are NOT thread safe.

        By default, a timeout of 300 seconds is used for all requests. If you wish to change this,
        pass the desired timeout (in seconds) as `request_timeout`.

        For fine-tuned control over the requests object use `session` with a requests.Session.

        The `mastodon_version` parameter can be used to specify the version of Mastodon that Mastodon.py will
        expect to be installed on the server. The function will throw an error if an unparseable
        Version is specified. If no version is specified, Mastodon.py will set `mastodon_version` to the
        detected version.

        The version check mode can be set to "created" (the default behaviour), "changed" or "none". If set to
        "created", Mastodon.py will throw an error if the version of Mastodon it is connected to is too old
        to have an endpoint. If it is set to "changed", it will throw an error if the endpoint's behaviour has
        changed after the version of Mastodon that is connected has been released. If it is set to "none",
        version checking is disabled.

        `feature_set` can be used to enable behaviour specific to non-mainline Mastodon API implementations.
        Details are documented in the functions that provide such functionality. Currently supported feature
        sets are `mainline`, `fedibird` and `pleroma`.

        For some Mastodon instances a `User-Agent` header is needed. This can be set by parameter `user_agent`. Starting from
        Mastodon.py 1.5.2 `create_app()` stores the application name into the client secret file. If `client_id` points to this file,
        the app name will be used as `User-Agent` header as default. It is possible to modify old secret files and append
        a client app name to use it as a `User-Agent` name.

        `lang` can be used to change the locale Mastodon will use to generate responses. Valid parameters are all ISO 639-1 (two letter)
        or for a language that has none, 639-3 (three letter) language codes. This affects some error messages (those related to validation) and 
        trends. You can change the language using :ref:`set_language()`.

        If no other `User-Agent` is specified, "mastodonpy" will be used.
        """
        self.api_base_url = api_base_url
        if self.api_base_url is not None:
            self.api_base_url = self.__protocolize(self.api_base_url)
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.debug_requests = debug_requests
        self.ratelimit_method = ratelimit_method
        self._token_expired = datetime.datetime.now()
        self._refresh_token = None
        
        self.__logged_in_id = None

        self.ratelimit_limit = 300
        self.ratelimit_reset = time.time()
        self.ratelimit_remaining = 300
        self.ratelimit_lastcall = time.time()
        self.ratelimit_pacefactor = ratelimit_pacefactor

        self.request_timeout = request_timeout

        if session:
            self.session = session
        else:
            self.session = requests.Session()

        self.feature_set = feature_set
        if not self.feature_set in ["mainline", "fedibird", "pleroma"]:
            raise MastodonIllegalArgumentError('Requested invalid feature set')

        # General defined user-agent
        self.user_agent = user_agent

        # Save language
        self.lang = lang

        # Token loading
        if self.client_id is not None:
            if os.path.isfile(self.client_id):
                with open(self.client_id, 'r') as secret_file:
                    self.client_id = secret_file.readline().rstrip()
                    self.client_secret = secret_file.readline().rstrip()

                    try_base_url = secret_file.readline().rstrip()
                    if try_base_url is not None and len(try_base_url) != 0:
                        try_base_url = Mastodon.__protocolize(try_base_url)
                        if not (self.api_base_url is None or try_base_url == self.api_base_url):
                            raise MastodonIllegalArgumentError('Mismatch in base URLs between files and/or specified')
                        self.api_base_url = try_base_url

                    # With new registrations we support the 4th line to store a client_name and use it as user-agent
                    client_name = secret_file.readline()
                    if client_name and self.user_agent is None:
                        self.user_agent = client_name.rstrip()
            else:
                if self.client_secret is None:
                    raise MastodonIllegalArgumentError('Specified client id directly, but did not supply secret')

        if self.access_token is not None and os.path.isfile(self.access_token):
            with open(self.access_token, 'r') as token_file:
                self.access_token = token_file.readline().rstrip()

                # For newer versions, we also store the URL
                try_base_url = token_file.readline().rstrip()
                if try_base_url is not None and len(try_base_url) != 0:
                    try_base_url = Mastodon.__protocolize(try_base_url)
                    if not (self.api_base_url is None or try_base_url == self.api_base_url):
                        raise MastodonIllegalArgumentError('Mismatch in base URLs between files and/or specified')
                    self.api_base_url = try_base_url

                # For EVEN newer vesions, we ALSO ALSO store the client id and secret so that you don't need to reauth to revoke
                if self.client_id is None:
                    try:
                        self.client_id = token_file.readline().rstrip()
                        self.client_secret = token_file.readline().rstrip()
                    except:
                        pass

        # Verify we have a base URL, protocolize
        if self.api_base_url is None:
            raise MastodonIllegalArgumentError("API base URL is required.")
        self.api_base_url = Mastodon.__protocolize(self.api_base_url)

        if not version_check_mode in ["created", "changed", "none"]:
            raise MastodonIllegalArgumentError("Invalid version check method.")
        self.version_check_mode = version_check_mode

        self.mastodon_major = 1
        self.mastodon_minor = 0
        self.mastodon_patch = 0
        self.version_check_worked = None

        # Versioning
        if mastodon_version is None and self.version_check_mode != 'none':
            self.retrieve_mastodon_version()
        elif self.version_check_mode != 'none':
            try:
                self.mastodon_major, self.mastodon_minor, self.mastodon_patch = parse_version_string(mastodon_version)
            except:
                raise MastodonVersionError("Bad version specified")

        # Ratelimiting parameter check
        if ratelimit_method not in ["throw", "wait", "pace"]:
            raise MastodonIllegalArgumentError("Invalid ratelimit method.")

    def auth_request_url(self, client_id=None, redirect_uris="urn:ietf:wg:oauth:2.0:oob", scopes=_DEFAULT_SCOPES, force_login=False, state=None, lang=None):
        """
        Returns the URL that a client needs to request an OAuth grant from the server.

        To log in with OAuth, send your user to this URL. The user will then log in and
        get a code which you can pass to :ref:`log_in() <log_in()>`.

        `scopes` are as in :ref:`log_in() <log_in()>`, redirect_uris is where the user should be redirected to
        after authentication. Note that `redirect_uris` must be one of the URLs given during
        app registration. When using urn:ietf:wg:oauth:2.0:oob, the code is simply displayed,
        otherwise it is added to the given URL as the "code" request parameter.

        Pass force_login if you want the user to always log in even when already logged
        into web Mastodon (i.e. when registering multiple different accounts in an app).

        `state` is the oauth `state` parameter to pass to the server. It is strongly suggested
        to use a random, nonguessable value (i.e. nothing meaningful and no incrementing ID)
        to preserve security guarantees. It can be left out for non-web login flows.

        Pass an ISO 639-1 (two letter) or, for languages that do not have one, 639-3 (three letter)
        language code as `lang` to control the display language for the oauth form.
        """
        if client_id is None:
            client_id = self.client_id
        else:
            if os.path.isfile(client_id):
                with open(client_id, 'r') as secret_file:
                    client_id = secret_file.readline().rstrip()

        params = dict()
        params['client_id'] = client_id
        params['response_type'] = "code"
        params['redirect_uri'] = redirect_uris
        params['scope'] = " ".join(scopes)
        params['force_login'] = force_login
        params['state'] = state
        params['lang'] = lang
        formatted_params = urlencode(params)
        return "".join([self.api_base_url, "/oauth/authorize?", formatted_params])

    def log_in(self, username=None, password=None, code=None, redirect_uri="urn:ietf:wg:oauth:2.0:oob", refresh_token=None, scopes=_DEFAULT_SCOPES, to_file=None):
        """
        Get the access token for a user.

        The username is the email address used to log in into Mastodon.

        Can persist access token to file `to_file`, to be used in the constructor.

        Handles password and OAuth-based authorization.

        Will throw a `MastodonIllegalArgumentError` if the OAuth flow data or the
        username / password credentials given are incorrect, and
        `MastodonAPIError` if all of the requested scopes were not granted.

        For OAuth 2, obtain a code via having your user go to the URL returned by
        :ref:`auth_request_url() <auth_request_url()>` and pass it as the code parameter. In this case,
        make sure to also pass the same redirect_uri parameter as you used when
        generating the auth request URL.

        Returns the access token as a string.
        """
        if username is not None and password is not None:
            params = self.__generate_params(locals(), ['scopes', 'to_file', 'code', 'refresh_token'])
            params['grant_type'] = 'password'
        elif code is not None:
            params = self.__generate_params(locals(), ['scopes', 'to_file', 'username', 'password', 'refresh_token'])
            params['grant_type'] = 'authorization_code'
        elif refresh_token is not None:
            params = self.__generate_params(locals(), ['scopes', 'to_file', 'username', 'password', 'code'])
            params['grant_type'] = 'refresh_token'
        else:
            raise MastodonIllegalArgumentError('Invalid arguments given. username and password or code are required.')

        params['client_id'] = self.client_id
        params['client_secret'] = self.client_secret
        params['scope'] = " ".join(scopes)

        try:
            response = self.__api_request('POST', '/oauth/token', params, do_ratelimiting=False)
            self.access_token = response['access_token']
            self.__set_refresh_token(response.get('refresh_token'))
            self.__set_token_expired(int(response.get('expires_in', 0)))
        except Exception as e:
            if username is not None or password is not None:
                raise MastodonIllegalArgumentError(f'Invalid user name, password, or redirect_uris: {e}')
            elif code is not None:
                raise MastodonIllegalArgumentError(f'Invalid access token or redirect_uris: {e}')
            else:
                raise MastodonIllegalArgumentError(f'Invalid request: {e}')

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
                token_file.write(self.client_id + "\n")
                token_file.write(self.client_secret + "\n")

        self.__logged_in_id = None

        # Retry version check if needed (might be required in limited federation mode)
        if not self.version_check_worked:
            self.retrieve_mastodon_version()

        return response['access_token']

    def revoke_access_token(self):
        """
        Revoke the oauth token the user is currently authenticated with, effectively removing
        the apps access and requiring the user to log in again.
        """
        if self.access_token is None:
            raise MastodonIllegalArgumentError("Not logged in, do not have a token to revoke.")
        if self.client_id is None or self.client_secret is None:
            raise MastodonIllegalArgumentError("Client authentication (id + secret) is required to revoke tokens.")
        params = collections.OrderedDict([])
        params['client_id'] = self.client_id
        params['client_secret'] = self.client_secret
        params['token'] = self.access_token
        self.__api_request('POST', '/oauth/revoke', params)

        # We are now logged out, clear token and logged in id
        self.access_token = None
        self.__logged_in_id = None

    ###
    # Reading data: Apps
    ###
    @api_version("2.0.0", "2.7.2", _DICT_VERSION_APPLICATION)
    def app_verify_credentials(self):
        """
        Fetch information about the current application.

        Returns an :ref:`application dict <application dict>`.
        """
        return self.__api_request('GET', '/api/v1/apps/verify_credentials')
