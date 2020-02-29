# coding: utf-8

import os
import os.path
import mimetypes
import time
import random
import string
import datetime
import collections
from contextlib import closing
import pytz
import requests
from requests.models import urlencode
import dateutil
import dateutil.parser
import re
import copy
import threading
import sys
import six
from decorator import decorate
import hashlib

IMPL_HAS_CRYPTO = True
try:
    import cryptography
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization
except:
    IMPL_HAS_CRYPTO = False
    
IMPL_HAS_ECE = True    
try:
    import http_ece
except:
    IMPL_HAS_ECE = False

import base64
import json

IMPL_HAS_BLURHASH = True
try:
    import blurhash
except:
    IMPL_HAS_BLURHASH = False

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    import magic
except ImportError:
    magic = None

###
# Version check functions, including decorator and parser
###
def parse_version_string(version_string):
    """Parses a semver version string, stripping off "rc" stuff if present."""
    string_parts =  version_string.split(".")
    version_parts = [
        int(re.match("([0-9]*)", string_parts[0]).group(0)),
        int(re.match("([0-9]*)", string_parts[1]).group(0)),
        int(re.match("([0-9]*)", string_parts[2]).group(0))
    ]
    return version_parts

def bigger_version(version_string_a, version_string_b):
    """Returns the bigger version of two version strings."""
    major_a, minor_a, patch_a = parse_version_string(version_string_a)
    major_b, minor_b, patch_b = parse_version_string(version_string_b)

    if major_a > major_b:
        return version_string_a
    elif major_a == major_b and minor_a > minor_b:
        return version_string_a
    elif major_a == major_b and minor_a == minor_b and patch_a > patch_b:
        return version_string_a
    return version_string_b

def api_version(created_ver, last_changed_ver, return_value_ver):
    """Version check decorator. Currently only checks Bigger Than."""
    def api_min_version_decorator(function):      
        def wrapper(function, self, *args, **kwargs):
            if not self.version_check_mode == "none":
                if self.version_check_mode == "created":
                    version = created_ver
                else:
                    version = bigger_version(last_changed_ver, return_value_ver)
                major, minor, patch = parse_version_string(version)
                if major > self.mastodon_major:
                    raise MastodonVersionError("Version check failed (Need version " + version + ")")
                elif major == self.mastodon_major and minor > self.mastodon_minor:
                    print(self.mastodon_minor)
                    raise MastodonVersionError("Version check failed (Need version " + version + ")")
                elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
                    raise MastodonVersionError("Version check failed (Need version " + version + ", patch is " + str(self.mastodon_patch) + ")")
            return function(self, *args, **kwargs)
        function.__doc__ = function.__doc__ + "\n\n        *Added: Mastodon v" + created_ver + ", last changed: Mastodon v" + last_changed_ver + "*"
        return decorate(function, wrapper)
    return api_min_version_decorator

###
# Dict helper class.
# Defined at top level so it can be pickled.
###
class AttribAccessDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("Attribute not found: " + str(attr))
    
    def __setattr__(self, attr, val):
        if attr in self:
            raise AttributeError("Attribute-style access is read only")
        super(AttribAccessDict, self).__setattr__(attr, val)

###
# The actual Mastodon class
###

class Mastodon:
    """
    Thorough and easy to use Mastodon
    api wrapper in python.

    If anything is unclear, check the official API docs at
    https://github.com/tootsuite/documentation/blob/master/Using-the-API/API.md
    """
    __DEFAULT_BASE_URL = 'https://mastodon.social'
    __DEFAULT_TIMEOUT = 300
    __DEFAULT_STREAM_TIMEOUT = 300
    __DEFAULT_STREAM_RECONNECT_WAIT_SEC = 5
    __DEFAULT_SCOPES = ['read', 'write', 'follow', 'push']
    __SCOPE_SETS = {
        'read': [
            'read:accounts', 
            'read:blocks', 
            'read:favourites', 
            'read:filters', 
            'read:follows', 
            'read:lists', 
            'read:mutes', 
            'read:notifications', 
            'read:search', 
            'read:statuses',
            'read:bookmarks'
        ],
        'write': [
            'write:accounts', 
            'write:blocks', 
            'write:favourites', 
            'write:filters', 
            'write:follows', 
            'write:lists', 
            'write:media', 
            'write:mutes', 
            'write:notifications', 
            'write:reports', 
            'write:statuses',
            'write:bookmarks'
        ],
        'follow': [
            'read:blocks',
            'read:follows',
            'read:mutes',
            'write:blocks',  
            'write:follows',
            'write:mutes', 
        ],
        'admin:read': [
            'admin:read:accounts', 
            'admin:read:reports',
        ],
        'admin:write': [
            'admin:write:accounts', 
            'admin:write:reports',
        ],
    }
    __VALID_SCOPES = ['read', 'write', 'follow', 'push', 'admin:read', 'admin:write'] + \
        __SCOPE_SETS['read'] + __SCOPE_SETS['write'] + __SCOPE_SETS['admin:read'] + __SCOPE_SETS['admin:write']
        
    __SUPPORTED_MASTODON_VERSION = "3.1.1"
    
    # Dict versions
    __DICT_VERSION_APPLICATION = "2.7.2"
    __DICT_VERSION_MENTION = "1.0.0"
    __DICT_VERSION_MEDIA = "2.8.2"
    __DICT_VERSION_ACCOUNT = "3.1.0"
    __DICT_VERSION_POLL = "2.8.0"
    __DICT_VERSION_STATUS = bigger_version(bigger_version(bigger_version(bigger_version(bigger_version("3.1.0", 
            __DICT_VERSION_MEDIA), __DICT_VERSION_ACCOUNT), __DICT_VERSION_APPLICATION), __DICT_VERSION_MENTION), __DICT_VERSION_POLL)
    __DICT_VERSION_INSTANCE = bigger_version("2.9.2", __DICT_VERSION_ACCOUNT)
    __DICT_VERSION_HASHTAG = "2.3.4"
    __DICT_VERSION_EMOJI = "3.0.0"
    __DICT_VERSION_RELATIONSHIP = "2.5.0"
    __DICT_VERSION_NOTIFICATION = bigger_version(bigger_version("1.0.0",  __DICT_VERSION_ACCOUNT), __DICT_VERSION_STATUS)
    __DICT_VERSION_CONTEXT = bigger_version("1.0.0",  __DICT_VERSION_STATUS)
    __DICT_VERSION_LIST = "2.1.0"
    __DICT_VERSION_CARD = "2.0.0"
    __DICT_VERSION_SEARCHRESULT = bigger_version(bigger_version(bigger_version("1.0.0", 
            __DICT_VERSION_ACCOUNT), __DICT_VERSION_STATUS), __DICT_VERSION_HASHTAG)
    __DICT_VERSION_ACTIVITY = "2.1.2" 
    __DICT_VERSION_REPORT = "2.9.1"
    __DICT_VERSION_PUSH = "2.4.0"
    __DICT_VERSION_PUSH_NOTIF = "2.4.0"
    __DICT_VERSION_FILTER = "2.4.3"
    __DICT_VERSION_CONVERSATION = bigger_version(bigger_version("2.6.0", __DICT_VERSION_ACCOUNT), __DICT_VERSION_STATUS)
    __DICT_VERSION_SCHEDULED_STATUS = bigger_version("2.7.0", __DICT_VERSION_STATUS)
    __DICT_VERSION_PREFERENCES = "2.8.0"
    __DICT_VERSION_ADMIN_ACCOUNT = bigger_version("2.9.1", __DICT_VERSION_ACCOUNT)
    __DICT_VERSION_FEATURED_TAG = "3.0.0"
    __DICT_VERSION_MARKER = "3.0.0"
    __DICT_VERSION_REACTION = "3.1.0"
    __DICT_VERSION_ANNOUNCEMENT = bigger_version("3.1.0", __DICT_VERSION_REACTION)
    
    ###
    # Registering apps
    ###
    @staticmethod
    def create_app(client_name, scopes=__DEFAULT_SCOPES, redirect_uris=None, website=None, to_file=None,
                   api_base_url=__DEFAULT_BASE_URL, request_timeout=__DEFAULT_TIMEOUT, session=None):
        """
        Create a new app with given `client_name` and `scopes` (The basic scropse are "read", "write", "follow" and "push" 
        - more granular scopes are available, please refere to Mastodon documentation for which).

        Specify `redirect_uris` if you want users to be redirected to a certain page after authenticating in an oauth flow.
        You can specify multiple URLs by passing a list. Note that if you wish to use OAuth authentication with redirects,
        the redirect URI must be one of the URLs specified here.
        
        Specify `to_file` to persist your apps info to a file so you can use them in the constructor.
        Specify `api_base_url` if you want to register an app on an instance different from the flagship one.        
        Specify `website` to give a website for your app.

        Specify `session` with a requests.Session for it to be used instead of the deafult. This can be
        used to, amongst other things, adjust proxy or ssl certificate settings.
        
        Presently, app registration is open by default, but this is not guaranteed to be the case for all
        future mastodon instances or even the flagship instance in the future.
        

        Returns `client_id` and `client_secret`, both as strings.
        """
        api_base_url = Mastodon.__protocolize(api_base_url)

        request_data = {
            'client_name': client_name,
            'scopes': " ".join(scopes)
        }

        try:
            if redirect_uris is not None:
                if isinstance(redirect_uris, (list, tuple)):
                    redirect_uris = "\n".join(list(redirect_uris))
                request_data['redirect_uris'] = redirect_uris
            else:
                request_data['redirect_uris'] = 'urn:ietf:wg:oauth:2.0:oob'
            if website is not None:
                request_data['website'] = website
            if session:
                ret = session.post(api_base_url + '/api/v1/apps', data=request_data, timeout=request_timeout)
                response = ret.json()
            else:
                response = requests.post(api_base_url + '/api/v1/apps', data=request_data, timeout=request_timeout)
                response = response.json()
        except Exception as e:
            raise MastodonNetworkError("Could not complete request: %s" % e)

        if to_file is not None:
            with open(to_file, 'w') as secret_file:
                secret_file.write(response['client_id'] + "\n")
                secret_file.write(response['client_secret'] + "\n")
                secret_file.write(api_base_url + "\n")
                
        return (response['client_id'], response['client_secret'])

    ###
    # Authentication, including constructor
    ###
    def __init__(self, client_id=None, client_secret=None, access_token=None,
                 api_base_url=None, debug_requests=False,
                 ratelimit_method="wait", ratelimit_pacefactor=1.1,
                 request_timeout=__DEFAULT_TIMEOUT, mastodon_version=None,
                 version_check_mode = "created", session=None, feature_set="mainline"):
        """
        Create a new API wrapper instance based on the given `client_secret` and `client_id`. If you
        give a `client_id` and it is not a file, you must also give a secret. If you specify an
        `access_token` then you don't need to specify a `client_id`. It is allowed to specify
        neither - in this case, you will be restricted to only using endpoints that do not
        require authentication.  If a file is given as `client_id`, client ID, secret and 
        base url are read from that file.

        You can also specify an `access_token`, directly or as a file (as written by `log_in()`_). If
        a file is given, Mastodon.py also tries to load the base URL from this file, if present. A
        client id and secret are not required in this case.

        Mastodon.py can try to respect rate limits in several ways, controlled by `ratelimit_method`.
        "throw" makes functions throw a `MastodonRatelimitError` when the rate
        limit is hit. "wait" mode will, once the limit is hit, wait and retry the request as soon
        as the rate limit resets, until it succeeds. "pace" works like throw, but tries to wait in
        between calls so that the limit is generally not hit (How hard it tries to not hit the rate
        limit can be controlled by ratelimit_pacefactor). The default setting is "wait". Note that
        even in "wait" and "pace" mode, requests can still fail due to network or other problems! Also
        note that "pace" and "wait" are NOT thread safe.

        Specify `api_base_url` if you wish to talk to an instance other than the flagship one. When
        reading from client id or access token files as written by Mastodon.py 1.5.0 or larger,
        this can be omitted.

        By default, a timeout of 300 seconds is used for all requests. If you wish to change this,
        pass the desired timeout (in seconds) as `request_timeout`.

        For fine-tuned control over the requests object use `session` with a requests.Session.
                
        The `mastodon_version` parameter can be used to specify the version of Mastodon that Mastodon.py will
        expect to be installed on the server. The function will throw an error if an unparseable 
        Version is specified. If no version is specified, Mastodon.py will set `mastodon_version` to the 
        detected version.
        
        The version check mode can be set to "created" (the default behaviour), "changed" or "none". If set to 
        "created", Mastodon.py will throw an error if the version of Mastodon it is connected to is too old
        to have an endpoint. If it is set to "changed", it will throw an error if the endpoints behaviour has
        changed after the version of Mastodon that is connected has been released. If it is set to "none",
        version checking is disabled.
        
        `feature_set` can be used to enable behaviour specific to non-mainline Mastodon API implementations.
        Details are documented in the functions that provide such functionality. Currently supported feature
        sets are `mainline`, `fedibird` and `pleroma`.
        """
        self.api_base_url = None
        if not api_base_url is None:
            self.api_base_url = Mastodon.__protocolize(api_base_url)
        
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
        
        # Token loading
        if self.client_id is not None:
            if os.path.isfile(self.client_id):
                with open(self.client_id, 'r') as secret_file:
                    self.client_id = secret_file.readline().rstrip()
                    self.client_secret = secret_file.readline().rstrip()
                    
                    try_base_url = secret_file.readline().rstrip()
                    if (not try_base_url is None) and len(try_base_url) != 0:
                        try_base_url = Mastodon.__protocolize(try_base_url)
                        if not (self.api_base_url is None or try_base_url == self.api_base_url):
                            raise MastodonIllegalArgumentError('Mismatch in base URLs between files and/or specified')
                        self.api_base_url = try_base_url
            else:
                if self.client_secret is None:
                    raise MastodonIllegalArgumentError('Specified client id directly, but did not supply secret')

        if self.access_token is not None and os.path.isfile(self.access_token):
            with open(self.access_token, 'r') as token_file:
                self.access_token = token_file.readline().rstrip()
                
                try_base_url = token_file.readline().rstrip()
                if (not try_base_url is None) and len(try_base_url) != 0:
                    try_base_url = Mastodon.__protocolize(try_base_url)
                    if not (self.api_base_url is None or try_base_url == self.api_base_url):
                         raise MastodonIllegalArgumentError('Mismatch in base URLs between files and/or specified')
                    self.api_base_url = try_base_url
        
        # Versioning
        if mastodon_version == None:
            self.retrieve_mastodon_version()
        else:
            try:
                self.mastodon_major, self.mastodon_minor, self.mastodon_patch = parse_version_string(mastodon_version)
            except:
                raise MastodonVersionError("Bad version specified")
        
        if not version_check_mode in ["created", "changed", "none"]:
            raise MastodonIllegalArgumentError("Invalid version check method.")
        self.version_check_mode = version_check_mode
        
        # Ratelimiting parameter check
        if ratelimit_method not in ["throw", "wait", "pace"]:
            raise MastodonIllegalArgumentError("Invalid ratelimit method.")
        
        
    def retrieve_mastodon_version(self):
        """
        Determine installed mastodon version and set major, minor and patch (not including RC info) accordingly.
        
        Returns the version string, possibly including rc info.
        """
        try:
            version_str = self.__instance()["version"]
        except:
            # instance() was added in 1.1.0, so our best guess is 1.0.0.
            version_str = "1.0.0"
            
        self.mastodon_major, self.mastodon_minor, self.mastodon_patch = parse_version_string(version_str)
        return version_str
        
    def verify_minimum_version(self, version_str, cached=False):
        """
        Update version info from server and verify that at least the specified version is present.
        
        If you specify "cached", the version info update part is skipped.
        
        Returns True if version requirement is satisfied, False if not.
        """
        if not cached:
            self.retrieve_mastodon_version()
        major, minor, patch = parse_version_string(version_str)
        if major > self.mastodon_major:
            return False
        elif major == self.mastodon_major and minor > self.mastodon_minor:
            return False
        elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
            return False
        return True

    @staticmethod
    def get_supported_version():
        """
        Retrieve the maximum version of Mastodon supported by this version of Mastodon.py
        """
        return Mastodon.__SUPPORTED_MASTODON_VERSION
    
    def auth_request_url(self, client_id=None, redirect_uris="urn:ietf:wg:oauth:2.0:oob",
                         scopes=__DEFAULT_SCOPES, force_login=False):
        """
        Returns the url that a client needs to request an oauth grant from the server.
        
        To log in with oauth, send your user to this URL. The user will then log in and
        get a code which you can pass to log_in.
        
        scopes are as in `log_in()`_, redirect_uris is where the user should be redirected to
        after authentication. Note that redirect_uris must be one of the URLs given during
        app registration. When using urn:ietf:wg:oauth:2.0:oob, the code is simply displayed,
        otherwise it is added to the given URL as the "code" request parameter.
        
        Pass force_login if you want the user to always log in even when already logged
        into web mastodon (i.e. when registering multiple different accounts in an app).
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
        formatted_params = urlencode(params)
        return "".join([self.api_base_url, "/oauth/authorize?", formatted_params])

    def log_in(self, username=None, password=None,
               code=None, redirect_uri="urn:ietf:wg:oauth:2.0:oob", refresh_token=None,
               scopes=__DEFAULT_SCOPES, to_file=None):
        """
        Get the access token for a user.
        
        The username is the e-mail used to log in into mastodon.

        Can persist access token to file `to_file`, to be used in the constructor.

        Handles password and OAuth-based authorization.
        
        Will throw a `MastodonIllegalArgumentError` if the OAuth or the
        username / password credentials given are incorrect, and
        `MastodonAPIError` if all of the requested scopes were not granted.

        For OAuth2, obtain a code via having your user go to the url returned by 
        `auth_request_url()`_ and pass it as the code parameter. In this case,
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
                raise MastodonIllegalArgumentError('Invalid user name, password, or redirect_uris: %s' % e)
            elif code is not None:
                raise MastodonIllegalArgumentError('Invalid access token or redirect_uris: %s' % e)
            else:
                raise MastodonIllegalArgumentError('Invalid request: %s' % e)

        received_scopes = response["scope"].split(" ")
        for scope_set in self.__SCOPE_SETS.keys():
            if scope_set in received_scopes:
                received_scopes += self.__SCOPE_SETS[scope_set]
        
        if not set(scopes) <= set(received_scopes):
            raise MastodonAPIError(
                'Granted scopes "' + " ".join(received_scopes) + '" do not contain all of the requested scopes "' + " ".join(scopes) + '".')

        if to_file is not None:
            with open(to_file, 'w') as token_file:
                token_file.write(response['access_token'] + "\n")
                token_file.write(self.api_base_url + "\n")
                
        self.__logged_in_id = None
        
        return response['access_token']
    
    @api_version("2.7.0", "2.7.0", "2.7.0")
    def create_account(self, username, password, email, agreement=False, reason=None, locale="en", scopes=__DEFAULT_SCOPES, to_file=None):
        """
        Creates a new user account with the given username, password and email. "agreement"
        must be set to true (after showing the user the instances user agreement and having
        them agree to it), "locale" specifies the language for the confirmation e-mail as an
        ISO 639-1 (two-letter) language code. `reason` can be used to specify why a user
        would like to join if approved-registrations mode is on.
        
        Does not require an access token, but does require a client grant.
        
        By default, this method is rate-limited by IP to 5 requests per 30 minutes.
        
        Returns an access token (just like log_in), which it can also persist to to_file,
        and sets it internally so that the user is now logged in. Note that this token 
        can only be used after the user has confirmed their e-mail.
        """
        params = self.__generate_params(locals(), ['to_file', 'scopes'])
        params['client_id'] = self.client_id
        params['client_secret'] = self.client_secret
        
        if agreement == False:
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
            response = self.__api_request('POST', '/api/v1/accounts', params, do_ratelimiting=False, 
                                          access_token_override = temp_access_token)
            self.access_token = response['access_token']
            self.__set_refresh_token(response.get('refresh_token'))
            self.__set_token_expired(int(response.get('expires_in', 0)))
        except Exception as e:
            raise MastodonIllegalArgumentError('Invalid request: %s' % e)
        
        # Step 3: Check scopes, persist, et cetera
        received_scopes = response["scope"].split(" ")
        for scope_set in self.__SCOPE_SETS.keys():
            if scope_set in received_scopes:
                received_scopes += self.__SCOPE_SETS[scope_set]
        
        if not set(scopes) <= set(received_scopes):
            raise MastodonAPIError(
                'Granted scopes "' + " ".join(received_scopes) + '" do not contain all of the requested scopes "' + " ".join(scopes) + '".')
        
        if to_file is not None:
            with open(to_file, 'w') as token_file:
                token_file.write(response['access_token'] + "\n")
                token_file.write(self.api_base_url + "\n")
                
        self.__logged_in_id = None
        
        return response['access_token']
        
    ###
    # Reading data: Instances
    ###
    @api_version("1.1.0", "2.3.0", __DICT_VERSION_INSTANCE)
    def instance(self):
        """
        Retrieve basic information about the instance, including the URI and administrative contact email.

        Does not require authentication unless locked down by the administrator.

        Returns an `instance dict`_.
        """
        return self.__instance()

    def __instance(self):
        """
        Internal, non-version-checking helper that does the same as instance()
        """
        instance = self.__api_request('GET', '/api/v1/instance/')
        return instance

    @api_version("2.1.2", "2.1.2", __DICT_VERSION_ACTIVITY)
    def instance_activity(self):
        """
        Retrieve activity stats about the instance. May be disabled by the instance administrator - throws
        a MastodonNotFoundError in that case.
        
        Activity is returned for 12 weeks going back from the current week.
        
        Returns a list of `activity dicts`_.
        """
        return self.__api_request('GET', '/api/v1/instance/activity')

    @api_version("2.1.2", "2.1.2", "2.1.2")
    def instance_peers(self):
        """
        Retrieve the instances that this instance knows about. May be disabled by the instance administrator - throws
        a MastodonNotFoundError in that case.
        
        Returns a list of URL strings.
        """
        return self.__api_request('GET', '/api/v1/instance/peers')

    @api_version("3.0.0", "3.0.0", "3.0.0")
    def instance_health(self):
        """
        Basic health check. Returns True if healthy, False if not.
        """
        return self.__api_request('GET', '/health', parse=False).decode("utf-8") == "success"
    
    @api_version("3.0.0", "3.0.0", "3.0.0")
    def instance_nodeinfo(self, schema = "http://nodeinfo.diaspora.software/ns/schema/2.0"):
        """
        Retrieves the instances nodeinfo information.
        
        For information on what the nodeinfo can contain, see the nodeinfo
        specification: https://github.com/jhass/nodeinfo . By default,
        Mastodon.py will try to retrieve the version 2.0 schema nodeinfo.
        
        To override the schema, specify the desired schema with the `schema`
        parameter.
        """
        links = self.__api_request('GET', '/.well-known/nodeinfo')["links"]
        
        schema_url = None
        for available_schema in links:
            if available_schema.rel == schema:
                schema_url = available_schema.href
                
        if schema_url is None:
            raise MastodonIllegalArgumentError("Requested nodeinfo schema is not available.")
        
        try:
            return self.__api_request('GET', schema_url, base_url_override="")
        except MastodonNotFoundError:
            parse = urlparse(schema_url)
            return self.__api_request('GET', parse.path + parse.params + parse.query + parse.fragment)
    
    ###
    # Reading data: Timelines
    ##
    @api_version("1.0.0", "2.6.0", __DICT_VERSION_STATUS)
    def timeline(self, timeline="home", max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch statuses, most recent ones first. `timeline` can be 'home', 'local', 'public',
        'tag/hashtag' or 'list/id'. See the following functions documentation for what those do.
        Local hashtag timelines are supported via the `timeline_hashtag()`_ function.
        
        The default timeline is the "home" timeline.

        Media only queries are supported via the `timeline_public()`_ and `timeline_hashtag()`_ functions.
        
        May or may not require authentication depending on server settings and what is specifically requested.

        Returns a list of `toot dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
            
        if since_id != None:
            since_id = self.__unpack_id(since_id)
        
        params_initial = locals()

        if timeline == "local":
            timeline = "public"
            params_initial['local'] = True

        params = self.__generate_params(params_initial, ['timeline'])
        url = '/api/v1/timelines/{0}'.format(timeline)
        return self.__api_request('GET', url, params)
    
    @api_version("1.0.0", "2.6.0", __DICT_VERSION_STATUS)
    def timeline_home(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in users home timeline (i.e. followed users and self).

        Returns a list of `toot dicts`_.
        """
        return self.timeline('home', max_id=max_id, min_id=min_id, 
                             since_id=since_id, limit=limit)

    @api_version("1.0.0", "2.6.0", __DICT_VERSION_STATUS)
    def timeline_local(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches the local / instance-wide timeline, not including replies.

        Returns a list of `toot dicts`_.
        """
        return self.timeline('local', max_id=max_id, min_id=min_id,
                             since_id=since_id, limit=limit)

    @api_version("1.0.0", "2.6.0", __DICT_VERSION_STATUS)
    def timeline_public(self, max_id=None, min_id=None, since_id=None, limit=None, only_media=False):
        """
        Fetches the public / visible-network timeline, not including replies.

        Set `only_media` to True to retrieve only statuses with media attachments.

        Returns a list of `toot dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
            
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
        
        params_initial = locals()        
        
        if only_media == False:
            del params_initial['only_media']
            
        url = '/api/v1/timelines/public'        
        params = self.__generate_params(params_initial)
        
        return self.__api_request('GET', url, params)

    @api_version("1.0.0", "2.6.0", __DICT_VERSION_STATUS)    
    def timeline_hashtag(self, hashtag, local=False, max_id=None, min_id=None, since_id=None, limit=None, only_media=False):
        """
        Fetch a timeline of toots with a given hashtag. The hashtag parameter
        should not contain the leading #.

        Set `local` to True to retrieve only instance-local tagged posts.
        Set `only_media` to True to retrieve only statuses with media attachments.
        
        Returns a list of `toot dicts`_.
        """
        if hashtag.startswith("#"):
            raise MastodonIllegalArgumentError("Hashtag parameter should omit leading #")
            
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)        
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params_initial = locals()        
        
        if local == False:
            del params_initial['local']
        
        if only_media == False:
            del params_initial['only_media']
            
        url = '/api/v1/timelines/tag/{0}'.format(hashtag)        
        params = self.__generate_params(params_initial, ['hashtag'])
        
        return self.__api_request('GET', url, params)

    @api_version("2.1.0", "2.6.0", __DICT_VERSION_STATUS)
    def timeline_list(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches a timeline containing all the toots by users in a given list.

        Returns a list of `toot dicts`_.
        """
        id = self.__unpack_id(id)
        return self.timeline('list/{0}'.format(id), max_id=max_id,
                             min_id=min_id, since_id=since_id, limit=limit)

    @api_version("2.6.0", "2.6.0", __DICT_VERSION_CONVERSATION)
    def conversations(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches a users conversations.
        
        Returns a list of `conversation dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
            
        if since_id != None:
            since_id = self.__unpack_id(since_id)            
        
        params = self.__generate_params(locals())
        return self.__api_request('GET', "/api/v1/conversations/", params)
        
    ###
    # Reading data: Statuses
    ###
    @api_version("1.0.0", "2.0.0", __DICT_VERSION_STATUS)
    def status(self, id):
        """
        Fetch information about a single toot.

        Does not require authentication for publicly visible statuses.

        Returns a `toot dict`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("1.0.0", "3.0.0", __DICT_VERSION_CARD)
    def status_card(self, id):
        """
        Fetch a card associated with a status. A card describes an object (such as an
        external video or link) embedded into a status.

        Does not require authentication for publicly visible statuses.

        This function is deprecated as of 3.0.0 and the endpoint does not
        exist anymore - you should just use the "card" field of the status dicts
        instead. Mastodon.py will try to mimick the old behaviour, but this
        is somewhat inefficient and not guaranteed to be the case forever.

        Returns a `card dict`_.
        """
        if self.verify_minimum_version("3.0.0"):
            return self.status(id).card
        else:
            id = self.__unpack_id(id)
            url = '/api/v1/statuses/{0}/card'.format(str(id))
            return self.__api_request('GET', url)

    @api_version("1.0.0", "1.0.0", __DICT_VERSION_CONTEXT)
    def status_context(self, id):
        """
        Fetch information about ancestors and descendants of a toot.

        Does not require authentication for publicly visible statuses.

        Returns a `context dict`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/context'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("1.0.0", "2.1.0", __DICT_VERSION_ACCOUNT)
    def status_reblogged_by(self, id):
        """
        Fetch a list of users that have reblogged a status.

        Does not require authentication for publicly visible statuses.

        Returns a list of `user dicts`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/reblogged_by'.format(str(id))
        return self.__api_request('GET', url)

    @api_version("1.0.0", "2.1.0", __DICT_VERSION_ACCOUNT)
    def status_favourited_by(self, id):
        """
        Fetch a list of users that have favourited a status.

        Does not require authentication for publicly visible statuses.

        Returns a list of `user dicts`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/favourited_by'.format(str(id))
        return self.__api_request('GET', url)

    ###
    # Reading data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0", __DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_statuses(self):
        """
        Fetch a list of scheduled statuses

        Returns a list of `scheduled toot dicts`_.
        """
        return self.__api_request('GET', '/api/v1/scheduled_statuses')
    
    @api_version("2.7.0", "2.7.0", __DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_status(self, id):
        """
        Fetch information about the scheduled status with the given id.

        Returns a `scheduled toot dict`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/scheduled_statuses/{0}'.format(str(id))
        return self.__api_request('GET', url)
    
    ###
    # Reading data: Polls
    ###
    @api_version("2.8.0", "2.8.0", __DICT_VERSION_POLL)
    def poll(self, id):
        """
        Fetch information about the poll with the given id

        Returns a `poll dict`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/polls/{0}'.format(str(id))
        return self.__api_request('GET', url)
    
    ###
    # Reading data: Notifications
    ###
    @api_version("1.0.0", "2.9.0", __DICT_VERSION_NOTIFICATION)
    def notifications(self, id=None, account_id=None, max_id=None, min_id=None, since_id=None, limit=None, mentions_only=None):
        """
        Fetch notifications (mentions, favourites, reblogs, follows) for the logged-in
        user. Pass `account_id` to get only notifications originating from the given account.
        
        Can be passed an `id` to fetch a single notification.

        Returns a list of `notification dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
        
        if account_id != None:
            account_id = self.__unpack_id(account_id)
        
        if id is None:
            params = self.__generate_params(locals(), ['id'])
            return self.__api_request('GET', '/api/v1/notifications', params)
        else:
            id = self.__unpack_id(id)
            url = '/api/v1/notifications/{0}'.format(str(id))
            return self.__api_request('GET', url)

    ###
    # Reading data: Accounts
    ###
    @api_version("1.0.0", "1.0.0", __DICT_VERSION_ACCOUNT)
    def account(self, id):
        """
        Fetch account information by user `id`.
        
        Does not require authentication for publicly visible accounts.
        
        Returns a `user dict`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}'.format(str(id))
        return self.__api_request('GET', url)
    
    @api_version("1.0.0", "2.1.0", __DICT_VERSION_ACCOUNT)
    def account_verify_credentials(self):
        """
        Fetch logged-in user's account information.

        Returns a `user dict`_ (Starting from 2.1.0, with an additional "source" field).
        """
        return self.__api_request('GET', '/api/v1/accounts/verify_credentials')

    @api_version("1.0.0", "2.1.0", __DICT_VERSION_ACCOUNT)
    def me(self):
        """
        Get this users account. Symonym for `account_verify_credentials()`, does exactly
        the same thing, just exists becase `account_verify_credentials()` has a confusing
        name.
        """
        return self.account_verify_credentials()
    
    @api_version("1.0.0", "2.7.0", __DICT_VERSION_STATUS)
    def account_statuses(self, id, only_media=False, pinned=False, exclude_replies=False, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch statuses by user `id`. Same options as `timeline()`_ are permitted.
        Returned toots are from the perspective of the logged-in user, i.e.
        all statuses visible to the logged-in user (including DMs) are
        included.

        If `only_media` is set, return only statuses with media attachments.
        If `pinned` is set, return only statuses that have been pinned. Note that 
        as of Mastodon 2.1.0, this only works properly for instance-local users.
        If `exclude_replies` is set, filter out all statuses that are replies.

        Does not require authentication for Mastodon versions after 2.7.0 (returns
        publicly visible statuses in that case), for publicly visible accounts.

        Returns a list of `toot dicts`_.
        """
        id = self.__unpack_id(id)
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
        
        params = self.__generate_params(locals(), ['id'])
        if pinned == False:
            del params["pinned"]
        if only_media == False:
            del params["only_media"]
        if exclude_replies == False:
            del params["exclude_replies"]
        
        url = '/api/v1/accounts/{0}/statuses'.format(str(id))
        return self.__api_request('GET', url, params)

    @api_version("1.0.0", "2.6.0", __DICT_VERSION_ACCOUNT)
    def account_following(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch users the given user is following.

        Returns a list of `user dicts`_.
        """
        id = self.__unpack_id(id)
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/following'.format(str(id))
        return self.__api_request('GET', url, params)

    @api_version("1.0.0", "2.6.0", __DICT_VERSION_ACCOUNT)
    def account_followers(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch users the given user is followed by.

        Returns a list of `user dicts`_.
        """
        id = self.__unpack_id(id)
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/followers'.format(str(id))
        return self.__api_request('GET', url, params)
    
    @api_version("1.0.0", "1.4.0", __DICT_VERSION_RELATIONSHIP)
    def account_relationships(self, id):
        """
        Fetch relationship (following, followed_by, blocking, follow requested) of 
        the logged in user to a given account. `id` can be a list.

        Returns a list of `relationship dicts`_.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/relationships',
                                  params)

    @api_version("1.0.0", "2.3.0", __DICT_VERSION_ACCOUNT)
    def account_search(self, q, limit=None, following=False):
        """
        Fetch matching accounts. Will lookup an account remotely if the search term is
        in the username@domain format and not yet in the database. Set `following` to
        True to limit the search to users the logged-in user follows.

        Returns a list of `user dicts`_.
        """
        params = self.__generate_params(locals())
        
        if params["following"] == False:
            del params["following"]
            
        return self.__api_request('GET', '/api/v1/accounts/search', params)

    @api_version("2.1.0", "2.1.0", __DICT_VERSION_LIST)
    def account_lists(self, id):
        """
        Get all of the logged-in users lists which the specified user is
        a member of.
        
        Returns a list of `list dicts`_.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/lists'.format(str(id))
        return self.__api_request('GET', url, params)
    
    ###
    # Reading data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", __DICT_VERSION_FEATURED_TAG)
    def featured_tags(self):
        """
        Return the hashtags the logged-in user has set to be featured on 
        their profile as a list of `featured tag dicts`_.
        
        Returns a list of `featured tag dicts`_.
        """
        return self.__api_request('GET', '/api/v1/featured_tags')
    
    @api_version("3.0.0", "3.0.0", __DICT_VERSION_HASHTAG)
    def featured_tag_suggestions(self):
        """
        Returns the logged-in users 10 most commonly hashtags.
        
        Returns a list of `hashtag dicts`_.
        """
        return self.__api_request('GET', '/api/v1/featured_tags/suggestions')
    
    ###
    # Reading data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3", __DICT_VERSION_FILTER)
    def filters(self):
        """
        Fetch all of the logged-in users filters.
        
        Returns a list of `filter dicts`_. Not paginated.
        """
        return self.__api_request('GET', '/api/v1/filters')
        
    @api_version("2.4.3", "2.4.3", __DICT_VERSION_FILTER)
    def filter(self, id):
        """
        Fetches information about the filter with the specified `id`.
        
        Returns a `filter dict`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/filters/{0}'.format(str(id))
        return self.__api_request('GET', url)
    
    @api_version("2.4.3", "2.4.3", __DICT_VERSION_FILTER)
    def filters_apply(self, objects, filters, context):
        """
        Helper function: Applies a list of filters to a list of either statuses 
        or notifications and returns only those matched by none. This function will
        apply all filters that match the context provided in `context`, i.e.
        if you want to apply only notification-relevant filters, specify
        'notifications'. Valid contexts are 'home', 'notifications', 'public' and 'thread'.
        """
        
        # Build filter regex
        filter_strings = []
        for keyword_filter in filters: 
            if not context in keyword_filter["context"]:
                continue
            
            filter_string = re.escape(keyword_filter["phrase"])
            if keyword_filter["whole_word"] == True:
                filter_string = "\\b" + filter_string + "\\b"
            filter_strings.append(filter_string)
        filter_re = re.compile("|".join(filter_strings), flags = re.IGNORECASE)
        
        # Apply
        filter_results = []
        for filter_object in objects:
            filter_status = filter_object
            if "status" in filter_object:
                filter_status = filter_object["status"]
            filter_text = filter_status["content"]
            filter_text = re.sub(r"<.*?>", " ", filter_text)
            filter_text = re.sub(r"\s+", " ", filter_text).strip()
            if not filter_re.search(filter_text):
                filter_results.append(filter_object)
        return filter_results
    
    ###
    # Reading data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", __DICT_VERSION_ACCOUNT)
    def suggestions(self):
        """
        Fetch follow suggestions for the logged-in user.

        Returns a list of `user dicts`_.
        
        """
        return self.__api_request('GET', '/api/v1/suggestions')
    
    ###
    # Reading data: Follow suggestions
    ###
    @api_version("3.0.0", "3.0.0", __DICT_VERSION_ACCOUNT)
    def directory(self):
        """
        Fetch the contents of the profile directory, if enabled on the server.

        Returns a list of `user dicts`_.
        
        """
        return self.__api_request('GET', '/api/v1/directory')
    
    ###
    # Reading data: Endorsements
    ###
    @api_version("2.5.0", "2.5.0", __DICT_VERSION_ACCOUNT)
    def endorsements(self):
        """
        Fetch list of users endorsemed by the logged-in user.

        Returns a list of `user dicts`_.
        
        """
        return self.__api_request('GET', '/api/v1/endorsements')
    
    
    ###
    # Reading data: Searching
    ###
    def __ensure_search_params_acceptable(self, account_id, offset, min_id, max_id):
        """
        Internal Helper: Throw a MastodonVersionError if version is < 2.8.0 but parameters
        for search that are available only starting with 2.8.0 are specified.
        """
        if not account_id is None or not offset is None or not min_id is None or not max_id is None:
            if self.verify_minimum_version("2.8.0", cached=True) == False:
                raise MastodonVersionError("Advanced search parameters require Mastodon 2.8.0+")
            
    @api_version("1.1.0", "2.8.0", __DICT_VERSION_SEARCHRESULT)
    def search(self, q, resolve=True, result_type=None, account_id=None, offset=None, min_id=None, max_id=None, exclude_unreviewed=True):
        """
        Fetch matching hashtags, accounts and statuses. Will perform webfinger
        lookups if resolve is True. Full-text search is only enabled if
        the instance supports it, and is restricted to statuses the logged-in
        user wrote or was mentioned in.
        
        `result_type` can be one of "accounts", "hashtags" or "statuses", to only
        search for that type of object.
        
        Specify `account_id` to only get results from the account with that id.
        
        `offset`, `min_id` and `max_id` can be used to paginate.

        `exclude_unreviewed` can be used to restrict search results for hashtags to only
        those that have been reviewed by moderators. It is on by default.
    
        Will use search_v1 (no tag dicts in return values) on Mastodon versions before 
        2.4.1), search_v2 otherwise. Parameters other than resolve are only available
        on Mastodon 2.8.0 or above - this function will throw a MastodonVersionError
        if you try to use them on versions before that. Note that the cached version
        number will be used for this to avoid uneccesary requests. 

        Returns a `search result dict`_, with tags as `hashtag dicts`_.
        """
        if self.verify_minimum_version("2.4.1", cached=True) == True:
            return self.search_v2(q, resolve=resolve, result_type=result_type, account_id=account_id,
                                offset=offset, min_id=min_id, max_id=max_id)
        else:
            self.__ensure_search_params_acceptable(account_id, offset, min_id, max_id)
            return self.search_v1(q, resolve=resolve)
        
    @api_version("1.1.0", "2.1.0", "2.1.0")
    def search_v1(self, q, resolve=False):
        """
        Identical to `search_v2()`, except in that it does not return
        tags as `hashtag dicts`_.

        Returns a `search result dict`_.
        """
        params = self.__generate_params(locals())
        if resolve == False:
            del params['resolve']
        return self.__api_request('GET', '/api/v1/search', params)

    @api_version("2.4.1", "2.8.0", __DICT_VERSION_SEARCHRESULT)
    def search_v2(self, q, resolve=True, result_type=None, account_id=None, offset=None, min_id=None, max_id=None, exclude_unreviewed=True):
        """
        Identical to `search_v1()`, except in that it returns tags as
        `hashtag dicts`_, has more parameters, and resolves by default.
        
        For more details documentation, please see `search()`

        Returns a `search result dict`_.
        """
        self.__ensure_search_params_acceptable(account_id, offset, min_id, max_id)
        params = self.__generate_params(locals())
        
        if resolve == False:
            del params["resolve"]
        
        if exclude_unreviewed == False or not self.verify_minimum_version("3.0.0", cached=True):
            del params["exclude_unreviewed"]
        
        if "result_type" in params:
            params["type"] = params["result_type"]
            del params["result_type"]
        
        return self.__api_request('GET', '/api/v2/search', params)

    ###
    # Reading data: Trends
    ###
    @api_version("2.4.3", "3.0.0", __DICT_VERSION_HASHTAG)
    def trends(self, limit = None):
        """
        Fetch trending-hashtag information, if the instance provides such information.
        
        Specify `limit` to limit how many results are returned (the maximum number
        of results is 10, the endpoint is not paginated).
        
        Does not require authentication unless locked down by the administrator.
        
        Important versioning note: This endpoint does not exist for Mastodon versions
        between 2.8.0 (inclusive) and 3.0.0 (exclusive).
        
        Returns a list of `hashtag dicts`_, sorted by the instances trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/trends', params)

    ###
    # Reading data: Lists
    ###
    @api_version("2.1.0", "2.1.0", __DICT_VERSION_LIST)
    def lists(self):
        """
        Fetch a list of all the Lists by the logged-in user.
        
        Returns a list of `list dicts`_.
        """
        return self.__api_request('GET', '/api/v1/lists')

    @api_version("2.1.0", "2.1.0", __DICT_VERSION_LIST)
    def list(self, id):
        """
        Fetch info about a specific list.
        
        Returns a `list dict`_.
        """
        id = self.__unpack_id(id)        
        return self.__api_request('GET', '/api/v1/lists/{0}'.format(id))

    @api_version("2.1.0", "2.6.0", __DICT_VERSION_ACCOUNT)
    def list_accounts(self, id, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Get the accounts that are on the given list.
        
        Returns a list of `user dicts`_.
        """
        id = self.__unpack_id(id)
        
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
        
        params = self.__generate_params(locals(), ['id']) 
        return self.__api_request('GET', '/api/v1/lists/{0}/accounts'.format(id))

    ###
    # Reading data: Mutes and Blocks
    ###
    @api_version("1.1.0", "2.6.0", __DICT_VERSION_ACCOUNT)    
    def mutes(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch a list of users muted by the logged-in user.

        Returns a list of `user dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)        
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/mutes', params)

    @api_version("1.0.0", "2.6.0", __DICT_VERSION_ACCOUNT)
    def blocks(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch a list of users blocked by the logged-in user.

        Returns a list of `user dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/blocks', params)

    ###
    # Reading data: Reports
    ###
    @api_version("1.1.0", "1.1.0", __DICT_VERSION_REPORT)
    def reports(self):
        """
        Fetch a list of reports made by the logged-in user.

        Returns a list of `report dicts`_.
        
        Warning: This method has now finally been removed, and will not 
        work on mastodon versions 2.5.0 and above.
        """
        return self.__api_request('GET', '/api/v1/reports')

    ###
    # Reading data: Favourites
    ###
    @api_version("1.0.0", "2.6.0", __DICT_VERSION_STATUS)
    def favourites(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in user's favourited statuses.

        Returns a list of `toot dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)        
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/favourites', params)

    ###
    # Reading data: Follow requests
    ###
    @api_version("1.0.0", "2.6.0", __DICT_VERSION_ACCOUNT)
    def follow_requests(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in user's incoming follow requests.

        Returns a list of `user dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)        
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/follow_requests', params)

    ###
    # Reading data: Domain blocks
    ###
    @api_version("1.4.0", "2.6.0", "1.4.0")
    def domain_blocks(self, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetch the logged-in user's blocked domains.

        Returns a list of blocked domain URLs (as strings, without protocol specifier).
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)        
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
            
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/domain_blocks', params)

    ###
    # Reading data: Emoji
    ###
    @api_version("2.1.0", "2.1.0", __DICT_VERSION_EMOJI)
    def custom_emojis(self):
        """
        Fetch the list of custom emoji the instance has installed.

        Does not require authentication unless locked down by the administrator.

        Returns a list of `emoji dicts`_.
        
        """
        return self.__api_request('GET', '/api/v1/custom_emojis')

    ###
    # Reading data: Apps
    ###
    @api_version("2.0.0", "2.7.2", __DICT_VERSION_APPLICATION)
    def app_verify_credentials(self):
        """
        Fetch information about the current application.

        Returns an `application dict`_.
        
        """
        return self.__api_request('GET', '/api/v1/apps/verify_credentials')

    ###
    # Reading data: Webpush subscriptions
    ###
    @api_version("2.4.0", "2.4.0", __DICT_VERSION_PUSH)
    def push_subscription(self):
        """
        Fetch the current push subscription the logged-in user has for this app.

        Returns a `push subscription dict`_.
        
        """
        return self.__api_request('GET', '/api/v1/push/subscription')

    ###
    # Reading data: Preferences
    ###
    @api_version("2.8.0", "2.8.0", __DICT_VERSION_PREFERENCES)
    def preferences(self):
        """
        Fetch the users preferences, which can be used to set some default options.
        As of 2.8.0, apps can only fetch, not update preferences.

        Returns a `preference dict`_.
        
        """
        return self.__api_request('GET', '/api/v1/preferences')

    ##
    # Reading data: Announcements
    ##
    
    #/api/v1/announcements
    @api_version("3.1.0", "3.1.0", __DICT_VERSION_ANNOUNCEMENT)
    def announcements(self):
        """
        Fetch currently active annoucements.
        
        Returns a list of `annoucement dicts`_.
        """
        return self.__api_request('GET', '/api/v1/announcements')
    
    ##
    # Reading data: Read markers
    ##
    @api_version("3.0.0", "3.0.0", __DICT_VERSION_MARKER)
    def markers_get(self, timeline=["home"]):
        """
        Get the last-read-location markers for the specified timelines. Valid timelines
        are the same as in `timeline()`_
        
        Note that despite the singular name, `timeline` can be a list.
        
        Returns a dict of `read marker dicts`_, keyed by timeline name.
        """
        if not isinstance(timeline, (list, tuple)):
            timeline = [timeline]
        params = self.__generate_params(locals())
        
        return self.__api_request('GET', '/api/v1/markers', params)

    ###
    # Reading data: Bookmarks
    ###
    @api_version("3.1.0", "3.1.0", __DICT_VERSION_STATUS)
    def bookmarks(self):
        """
        Get a list of statuses bookmarked by the logged-in user.
        
        Returns a list of `toot dicts`_.
        """
        return self.__api_request('GET', '/api/v1/bookmarks')
    
    ###
    # Writing data: Statuses
    ###
    @api_version("1.0.0", "2.8.0", __DICT_VERSION_STATUS)
    def status_post(self, status, in_reply_to_id=None, media_ids=None,
                    sensitive=False, visibility=None, spoiler_text=None,
                    language=None, idempotency_key=None, content_type=None,
                    scheduled_at=None, poll=None, quote_id=None):
        """
        Post a status. Can optionally be in reply to another status and contain
        media.
        
        `media_ids` should be a list. (If it's not, the function will turn it
        into one.) It can contain up to four pieces of media (uploaded via 
        `media_post()`_). `media_ids` can also be the `media dicts`_ returned 
        by `media_post()`_ - they are unpacked automatically.

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
        accepts all valid ISO 639-2 language codes.

        You can set `idempotency_key` to a value to uniquely identify an attempt
        at posting a status. Even if you call this function more than once,
        if you call it with the same `idempotency_key`, only one status will
        be created.

        Pass a datetime as `scheduled_at` to schedule the toot for a specific time
        (the time must be at least 5 minutes into the future). If this is passed,
        status_post returns a `scheduled toot dict`_ instead.

        Pass `poll` to attach a poll to the status. An appropriate object can be
        constructed using `make_poll()`_ . Note that as of Mastodon version
        2.8.2, you can only have either media or a poll attached, not both at 
        the same time.

        **Specific to `pleroma` feature set:**: Specify `content_type` to set 
        the content type of your post on Pleroma. It accepts 'text/plain' (default), 
        'text/markdown', 'text/html' and 'text/bbcode. This parameter is not 
        supported on Mastodon servers, but will be safely ignored if set.

        **Specific to `fedibird` feature set:**: The `quote_id` parameter is 
        a non-standard extension that specifies the id of a quoted status.

        Returns a `toot dict`_ with the new status.
        """
        if quote_id != None:
            if self.feature_set != "fedibird":
                raise MastodonIllegalArgumentError('quote_id is only available with feature set fedibird')
            quote_id = self.__unpack_id(quote_id)
           
        if content_type != None:
            if self.feature_set != "pleroma":
                raise MastodonIllegalArgumentError('quote_id is only available with feature set pleroma')
            # It would be better to read this from nodeinfo and cache, but this is easier
            if not content_type in ["text/plain", "text/html", "text/markdown", "text/bbcode"]:
                raise MastodonIllegalArgumentError('Invalid content type specified')
            
        if in_reply_to_id != None:
            in_reply_to_id = self.__unpack_id(in_reply_to_id)
        
        if scheduled_at != None:
            scheduled_at = self.__consistent_isoformat_utc(scheduled_at)
        
        params_initial = locals()
        
        # Validate poll/media exclusivity
        if not poll is None:
            if (not media_ids is None) and len(media_ids) != 0:
                raise ValueError('Status can have media or poll attached - not both.')
        
        # Validate visibility parameter
        valid_visibilities = ['private', 'public', 'unlisted', 'direct']
        if params_initial['visibility'] == None:
            del params_initial['visibility']
        else:
            params_initial['visibility'] = params_initial['visibility'].lower()
            if params_initial['visibility'] not in valid_visibilities:
                raise ValueError('Invalid visibility value! Acceptable '
                                'values are %s' % valid_visibilities)

        if params_initial['language'] == None:
            del params_initial['language']

        if params_initial['sensitive'] is False:
            del [params_initial['sensitive']]

        headers = {}
        if idempotency_key != None:
            headers['Idempotency-Key'] = idempotency_key
            
        if media_ids is not None:
            try:
                media_ids_proper = []
                if not isinstance(media_ids, (list, tuple)):
                    media_ids = [media_ids]
                for media_id in media_ids:
                    if isinstance(media_id, dict):
                        media_ids_proper.append(media_id["id"])
                    else:
                        media_ids_proper.append(media_id)
            except Exception as e:
                raise MastodonIllegalArgumentError("Invalid media "
                                                   "dict: %s" % e)

            params_initial["media_ids"] = media_ids_proper

        if params_initial['content_type'] == None:
            del params_initial['content_type']

        use_json = False
        if not poll is None:
            use_json = True

        params = self.__generate_params(params_initial, ['idempotency_key'])
        return self.__api_request('POST', '/api/v1/statuses', params, headers = headers, use_json = use_json)

    @api_version("1.0.0", "2.8.0", __DICT_VERSION_STATUS)
    def toot(self, status):
        """
        Synonym for `status_post()`_ that only takes the status text as input.

        Usage in production code is not recommended.

        Returns a `toot dict`_ with the new status.
        """
        return self.status_post(status)

    @api_version("1.0.0", "2.8.0", __DICT_VERSION_STATUS)
    def status_reply(self, to_status, status, in_reply_to_id=None, media_ids=None,
                    sensitive=False, visibility=None, spoiler_text=None,
                    language=None, idempotency_key=None, content_type=None,
                    scheduled_at=None, poll=None, untag=False):
        """
        Helper function - acts like status_post, but prepends the name of all
        the users that are being replied to to the status text and retains
        CW and visibility if not explicitly overridden.
        
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
        mentioned_accounts[to_status.account.id] = to_status.account.acct
        
        if not untag:
            for account in to_status.mentions:
                if account.id != user_id and not account.id in mentioned_accounts.keys():
                    mentioned_accounts[account.id] = account.acct
                
        # Join into one piece of text. The space is added inside because of self-replies.
        status = "".join(map(lambda x: "@" + x + " ", mentioned_accounts.values())) + status
            
        # Retain visibility / cw
        if visibility == None and 'visibility' in to_status:
            visibility = to_status.visibility
        if spoiler_text == None and 'spoiler_text' in to_status:
            spoiler_text = to_status.spoiler_text
        
        keyword_args["status"] = status
        keyword_args["visibility"] = visibility
        keyword_args["spoiler_text"] = spoiler_text
        keyword_args["in_reply_to_id"] = to_status.id
        return self.status_post(**keyword_args)
    
    @api_version("2.8.0", "2.8.0", __DICT_VERSION_POLL)
    def make_poll(self, options, expires_in, multiple=False, hide_totals=False):
        """
        Generate a poll object that can be passed as the `poll` option when posting a status.
        
        options is an array of strings with the poll options (Maximum, by default: 4),
        expires_in is the time in seconds for which the poll should be open.
        Set multiple to True to allow people to choose more than one answer. Set
        hide_totals to True to hide the results of the poll until it has expired.
        """            
        poll_params = locals()
        del poll_params["self"]
        return poll_params
    
    @api_version("1.0.0", "1.0.0", "1.0.0")
    def status_delete(self, id):
        """
        Delete a status
        
        Returns the now-deleted status, with an added "source" attribute that contains
        the text that was used to compose this status (this can be used to power
        "delete and redraft" functionality)
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}'.format(str(id))
        return self.__api_request('DELETE', url)

    @api_version("1.0.0", "2.0.0", __DICT_VERSION_STATUS)
    def status_reblog(self, id, visibility=None):
        """
        Reblog / boost a status.
        
        The visibility parameter functions the same as in `status_post()`_ and
        allows you to reduce the visibility of a reblogged status.

        Returns a `toot dict`_ with a new status that wraps around the reblogged one.
        """
        params = self.__generate_params(locals(), ['id'])
        valid_visibilities = ['private', 'public', 'unlisted', 'direct']
        if 'visibility' in params:
            params['visibility'] = params['visibility'].lower()
            if params['visibility'] not in valid_visibilities:
                raise ValueError('Invalid visibility value! Acceptable '
                                'values are %s' % valid_visibilities)
        
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/reblog'.format(str(id))
        return self.__api_request('POST', url, params)

    @api_version("1.0.0", "2.0.0", __DICT_VERSION_STATUS)
    def status_unreblog(self, id):
        """
        Un-reblog a status.

        Returns a `toot dict`_ with the status that used to be reblogged.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unreblog'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "2.0.0", __DICT_VERSION_STATUS)
    def status_favourite(self, id):
        """
        Favourite a status.

        Returns a `toot dict`_ with the favourited status.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/favourite'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "2.0.0", __DICT_VERSION_STATUS)
    def status_unfavourite(self, id):
        """
        Un-favourite a status.

        Returns a `toot dict`_ with the un-favourited status.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unfavourite'.format(str(id))
        return self.__api_request('POST', url)
    
    @api_version("1.4.0", "2.0.0", __DICT_VERSION_STATUS)
    def status_mute(self, id):
        """
        Mute notifications for a status.

        Returns a `toot dict`_ with the now muted status
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/mute'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.4.0", "2.0.0", __DICT_VERSION_STATUS)
    def status_unmute(self, id):
        """
        Unmute notifications for a status.

        Returns a `toot dict`_ with the status that used to be muted.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unmute'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("2.1.0", "2.1.0", __DICT_VERSION_STATUS)
    def status_pin(self, id):
        """
        Pin a status for the logged-in user.

        Returns a `toot dict`_ with the now pinned status
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/pin'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("2.1.0", "2.1.0", __DICT_VERSION_STATUS)
    def status_unpin(self, id):
        """
        Unpin a pinned status for the logged-in user.

        Returns a `toot dict`_ with the status that used to be pinned.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unpin'.format(str(id))
        return self.__api_request('POST', url)
    
    
    @api_version("3.1.0", "3.1.0", __DICT_VERSION_STATUS)
    def status_bookmark(self, id):
        """
        Bookmark a status as the logged-in user.

        Returns a `toot dict`_ with the now bookmarked status
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/bookmark'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("3.1.0", "3.1.0", __DICT_VERSION_STATUS)
    def status_unbookmark(self, id):
        """
        Unbookmark a bookmarked status for the logged-in user.

        Returns a `toot dict`_ with the status that used to be bookmarked.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/statuses/{0}/unbookmark'.format(str(id))
        return self.__api_request('POST', url)

    ###
    # Writing data: Scheduled statuses
    ###
    @api_version("2.7.0", "2.7.0", __DICT_VERSION_SCHEDULED_STATUS)
    def scheduled_status_update(self, id, scheduled_at):
        """
        Update the scheduled time of a scheduled status.
        
        New time must be at least 5 minutes into the future.
        
        Returns a `scheduled toot dict`_
        """
        scheduled_at = self.__consistent_isoformat_utc(scheduled_at)
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/scheduled_statuses/{0}'.format(str(id))
        return self.__api_request('PUT', url, params)
    
    @api_version("2.7.0", "2.7.0", "2.7.0")
    def scheduled_status_delete(self, id):
        """
        Deletes a scheduled status.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/scheduled_statuses/{0}'.format(str(id))
        self.__api_request('DELETE', url)
    
    ###
    # Writing data: Polls
    ###
    @api_version("2.8.0", "2.8.0", __DICT_VERSION_POLL)
    def poll_vote(self, id, choices):
        """
        Vote in the given poll.
        
        `choices` is the index of the choice you wish to register a vote for 
        (i.e. its index in the corresponding polls `options` field. In case 
        of a poll that allows selection of more than one option, a list of
        indices can be passed.
        
        You can only submit choices for any given poll once in case of
        single-option polls, or only once per option in case of multi-option
        polls.
        
        Returns the updated `poll dict`_
        """
        id = self.__unpack_id(id)
        if not isinstance(choices, list):
            choices = [choices]
        params = self.__generate_params(locals(), ['id'])
        
        url = '/api/v1/polls/{0}/votes'.format(id)
        self.__api_request('POST', url, params)
        
    
    ###
    # Writing data: Notifications
    ###
    @api_version("1.0.0", "1.0.0", "1.0.0")
    def notifications_clear(self):
        """
        Clear out a users notifications
        """
        self.__api_request('POST', '/api/v1/notifications/clear')


    @api_version("1.3.0", "2.9.2", "2.9.2")
    def notifications_dismiss(self, id):
        """
        Deletes a single notification
        """
        id = self.__unpack_id(id)
        
        if self.verify_minimum_version("2.9.2"):
            url = '/api/v1/notifications/{0}/dismiss'.format(str(id))
            self.__api_request('POST', url)
        else:
            params = self.__generate_params(locals())
            self.__api_request('POST', '/api/v1/notifications/dismiss', params)

    ###
    # Writing data: Conversations
    ###
    @api_version("2.6.0", "2.6.0", __DICT_VERSION_CONVERSATION)
    def conversations_read(self, id):
        """
        Marks a single conversation as read.
        
        Returns the updated `conversation dict`_.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/conversations/{0}/read'.format(str(id))
        return self.__api_request('POST', url)

    ###
    # Writing data: Accounts
    ###
    @api_version("1.0.0", "2.4.3", __DICT_VERSION_RELATIONSHIP)
    def account_follow(self, id, reblogs=True):
        """
        Follow a user.

        Set `reblogs` to False to hide boosts by the followed user.

        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals())
        
        if params["reblogs"] == None:
            del params["reblogs"]
            
        url = '/api/v1/accounts/{0}/follow'.format(str(id))
        return self.__api_request('POST', url, params)

    @api_version("1.0.0", "2.1.0", __DICT_VERSION_ACCOUNT)
    def follows(self, uri):
        """
        Follow a remote user by uri (username@domain).

        Returns a `user dict`_.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/follows', params)

    @api_version("1.0.0", "1.4.0", __DICT_VERSION_RELATIONSHIP)
    def account_unfollow(self, id):
        """
        Unfollow a user.

        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/unfollow'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "1.4.0", __DICT_VERSION_RELATIONSHIP)
    def account_block(self, id):
        """
        Block a user.

        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/block'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "1.4.0", __DICT_VERSION_RELATIONSHIP)
    def account_unblock(self, id):
        """
        Unblock a user.

        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/unblock'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.1.0", "2.4.3", __DICT_VERSION_RELATIONSHIP)
    def account_mute(self, id, notifications=True):
        """
        Mute a user.

        Set `notifications` to False to receive notifications even though the user is
        muted from timelines.

        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/accounts/{0}/mute'.format(str(id))
        return self.__api_request('POST', url, params)

    @api_version("1.1.0", "1.4.0", __DICT_VERSION_RELATIONSHIP)
    def account_unmute(self, id):
        """
        Unmute a user.

        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/unmute'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.1.1", "3.1.0", __DICT_VERSION_ACCOUNT)
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
        appear as semi-structured information in the users profile.
        
        Returns the updated `user dict` of the logged-in user.
        """
        params_initial = collections.OrderedDict(locals())
        
        # Load avatar, if specified
        if not avatar is None:
            if avatar_mime_type is None and (isinstance(avatar, str) and os.path.isfile(avatar)):
                avatar_mime_type = guess_type(avatar)
                avatar = open(avatar, 'rb')

            if avatar_mime_type is None:
                raise MastodonIllegalArgumentError('Could not determine mime type or data passed directly without mime type.')
        
        # Load header, if specified
        if not header is None:
            if header_mime_type is None and (isinstance(header, str) and os.path.isfile(header)):
                header_mime_type = guess_type(header)
                header = open(header, 'rb')

            if header_mime_type is None:
                raise MastodonIllegalArgumentError('Could not determine mime type or data passed directly without mime type.')
        
        # Convert fields
        if fields != None:
            if len(fields) > 4:
                raise MastodonIllegalArgumentError('A maximum of four fields are allowed.')
            
            fields_attributes = []
            for idx, (field_name, field_value) in enumerate(fields):
                params_initial['fields_attributes[' + str(idx) + '][name]'] = field_name
                params_initial['fields_attributes[' + str(idx) + '][value]'] = field_value
            
        # Clean up params
        for param in ["avatar", "avatar_mime_type", "header", "header_mime_type", "fields"]:
            if param in params_initial:
                del params_initial[param]
        
        # Create file info
        files = {}
        if not avatar is None:
            avatar_file_name = "mastodonpyupload_" + mimetypes.guess_extension(avatar_mime_type)
            files["avatar"] = (avatar_file_name, avatar, avatar_mime_type)
        if not header is None:
            header_file_name = "mastodonpyupload_" + mimetypes.guess_extension(header_mime_type)
            files["header"] = (header_file_name, header, header_mime_type)
        
        params = self.__generate_params(params_initial)
        return self.__api_request('PATCH', '/api/v1/accounts/update_credentials', params, files=files)


    @api_version("2.5.0", "2.5.0", __DICT_VERSION_RELATIONSHIP)
    def account_pin(self, id):
        """
        Pin / endorse a user.
        
        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/pin'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("2.5.0", "2.5.0", __DICT_VERSION_RELATIONSHIP)
    def account_unpin(self, id):
        """
        Unpin / un-endorse a user.

        Returns a `relationship dict`_ containing the updated relationship to the user.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/accounts/{0}/unpin'.format(str(id))
        return self.__api_request('POST', url)

    ###
    # Writing data: Featured hashtags
    ###
    @api_version("3.0.0", "3.0.0", __DICT_VERSION_FEATURED_TAG)
    def featured_tag_create(self, name):
        """
        Creates a new featured hashtag displayed on the logged-in users profile.
        
        Returns a `featured tag dict`_ with the newly featured tag.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/featured_tags', params)
    
    @api_version("3.0.0", "3.0.0", __DICT_VERSION_FEATURED_TAG)
    def featured_tag_delete(self, id):
        """
        Deletes one of the logged-in users featured hashtags.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/featured_tags/{0}'.format(str(id))
        self.__api_request('DELETE', url)

    ###
    # Writing data: Keyword filters
    ###
    @api_version("2.4.3", "2.4.3", __DICT_VERSION_FILTER)
    def filter_create(self, phrase, context, irreversible = False, whole_word = True, expires_in = None):
        """
        Creates a new keyword filter. `phrase` is the phrase that should be
        filtered out, `context` specifies from where to filter the keywords.
        Valid contexts are 'home', 'notifications', 'public' and 'thread'.
        
        Set `irreversible` to True if you want the filter to just delete statuses
        server side. This works only for the 'home' and 'notifications' contexts.
        
        Set `whole_word` to False if you want to allow filter matches to
        start or end within a word, not only at word boundaries.
        
        Set `expires_in` to specify for how many seconds the filter should be
        kept around.
        
        Returns the `filter dict`_ of the newly created filter. 
        """
        params = self.__generate_params(locals())
        
        for context_val in context:
            if not context_val in ['home', 'notifications', 'public', 'thread']:
                raise MastodonIllegalArgumentError('Invalid filter context.')
        
        return self.__api_request('POST', '/api/v1/filters', params)
        
    @api_version("2.4.3", "2.4.3", __DICT_VERSION_FILTER)
    def filter_update(self, id, phrase = None, context = None, irreversible = None, whole_word = None, expires_in = None):
        """
        Updates the filter with the given `id`. Parameters are the same
        as in `filter_create()`.
        
        Returns the `filter dict`_ of the updated filter. 
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        url = '/api/v1/filters/{0}'.format(str(id))
        return self.__api_request('PUT', url, params)
    
    @api_version("2.4.3", "2.4.3", "2.4.3")
    def filter_delete(self, id):
        """
        Deletes the filter with the given `id`.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/filters/{0}'.format(str(id))
        self.__api_request('DELETE', url)
        
    ###
    # Writing data: Follow suggestions
    ###
    @api_version("2.4.3", "2.4.3", __DICT_VERSION_ACCOUNT)
    def suggestion_delete(self, account_id):
        """
        Remove the user with the given `account_id` from the follow suggestions.
        """
        account_id = self.__unpack_id(account_id)
        url = '/api/v1/suggestions/{0}'.format(str(account_id))
        self.__api_request('DELETE', url)

    ###
    # Writing data: Lists
    ###
    @api_version("2.1.0", "2.1.0", __DICT_VERSION_LIST)
    def list_create(self, title):
        """
        Create a new list with the given `title`.
        
        Returns the `list dict`_ of the created list.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/lists', params)
    
    @api_version("2.1.0", "2.1.0", __DICT_VERSION_LIST)
    def list_update(self, id, title):
        """
        Update info about a list, where "info" is really the lists `title`.
        
        Returns the `list dict`_ of the modified list.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('PUT', '/api/v1/lists/{0}'.format(id), params)
    
    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_delete(self, id):
        """
        Delete a list.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', '/api/v1/lists/{0}'.format(id))
    
    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_accounts_add(self, id, account_ids):
        """
        Add the account(s) given in `account_ids` to the list.
        """
        id = self.__unpack_id(id)
        
        if not isinstance(account_ids, list):
            account_ids = [account_ids]
        account_ids = list(map(lambda x: self.__unpack_id(x), account_ids))
        
        params = self.__generate_params(locals(), ['id'])        
        self.__api_request('POST', '/api/v1/lists/{0}/accounts'.format(id), params)
        
    @api_version("2.1.0", "2.1.0", "2.1.0")
    def list_accounts_delete(self, id, account_ids):
        """
        Remove the account(s) given in `account_ids` from the list.
        """
        id = self.__unpack_id(id)
        
        if not isinstance(account_ids, list):
            account_ids = [account_ids]
        account_ids = list(map(lambda x: self.__unpack_id(x), account_ids))
        
        params = self.__generate_params(locals(), ['id'])        
        self.__api_request('DELETE', '/api/v1/lists/{0}/accounts'.format(id), params)
        
    ###
    # Writing data: Reports
    ###
    @api_version("1.1.0", "2.5.0", __DICT_VERSION_REPORT)
    def report(self, account_id, status_ids = None, comment = None, forward = False):
        """
        Report statuses to the instances administrators.

        Accepts a list of toot IDs associated with the report, and a comment.
        
        Set forward to True to forward a report of a remote user to that users
        instance as well as sending it to the instance local administrators.

        Returns a `report dict`_.
        """
        account_id = self.__unpack_id(account_id)
        
        if not status_ids is None:
            if not isinstance(status_ids, list):
                status_ids = [status_ids]
        status_ids = list(map(lambda x: self.__unpack_id(x), status_ids))
        
        params_initial = locals()        
        if forward == False:
            del params_initial['forward']
        
        params = self.__generate_params(params_initial)
        return self.__api_request('POST', '/api/v1/reports/', params)

    ###
    # Writing data: Follow requests
    ###
    @api_version("1.0.0", "3.0.0", __DICT_VERSION_RELATIONSHIP)
    def follow_request_authorize(self, id):
        """
        Accept an incoming follow request.
        
        Returns the updated `relationship dict`_ for the requesting account.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/follow_requests/{0}/authorize'.format(str(id))
        return self.__api_request('POST', url)

    @api_version("1.0.0", "3.0.0", __DICT_VERSION_RELATIONSHIP)
    def follow_request_reject(self, id):
        """
        Reject an incoming follow request.
        
        Returns the updated `relationship dict`_ for the requesting account.
        """
        id = self.__unpack_id(id)
        url = '/api/v1/follow_requests/{0}/reject'.format(str(id))
        return self.__api_request('POST', url)

    ###
    # Writing data: Media
    ###
    @api_version("1.0.0", "2.9.1", __DICT_VERSION_MEDIA)
    def media_post(self, media_file, mime_type=None, description=None, focus=None):
        """
        Post an image, video or audio file. `media_file` can either be image data or
        a file name. If image data is passed directly, the mime
        type has to be specified manually, otherwise, it is
        determined from the file name. `focus` should be a tuple
        of floats between -1 and 1, giving the x and y coordinates
        of the images focus point for cropping (with the origin being the images
        center).

        Throws a `MastodonIllegalArgumentError` if the mime type of the
        passed data or file can not be determined properly.

        Returns a `media dict`_. This contains the id that can be used in
        status_post to attach the media file to a toot.
        """
        if mime_type is None and (isinstance(media_file, str) and os.path.isfile(media_file)):
            mime_type = guess_type(media_file)
            media_file = open(media_file, 'rb')
        elif isinstance(media_file, str) and os.path.isfile(media_file):
            media_file = open(media_file, 'rb')

        if mime_type is None:
            raise MastodonIllegalArgumentError('Could not determine mime type'
                                               ' or data passed directly '
                                               'without mime type.')

        random_suffix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        file_name = "mastodonpyupload_" + str(time.time()) + "_" + str(random_suffix) + mimetypes.guess_extension(
            mime_type)

        if focus != None:
            focus = str(focus[0]) + "," + str(focus[1])
            
        media_file_description = (file_name, media_file, mime_type)
        return self.__api_request('POST', '/api/v1/media',
                                  files={'file': media_file_description},
                                  params={'description': description, 'focus': focus})
    
    @api_version("2.3.0", "2.3.0", __DICT_VERSION_MEDIA)
    def media_update(self, id, description=None, focus=None):
        """
        Update the metadata of the media file with the given `id`. `description` and 
        `focus` are as in `media_post()`_ .
        
        Returns the updated `media dict`_.
        """
        id = self.__unpack_id(id)

        if focus != None:
            focus = str(focus[0]) + "," + str(focus[1])
            
        params = self.__generate_params(locals(), ['id'])  
        return self.__api_request('PUT', '/api/v1/media/{0}'.format(str(id)), params)
    
    ###
    # Writing data: Domain blocks
    ###
    @api_version("1.4.0", "1.4.0", "1.4.0")
    def domain_block(self, domain=None):
        """
        Add a block for all statuses originating from the specified domain for the logged-in user.
        """
        params = self.__generate_params(locals())
        self.__api_request('POST', '/api/v1/domain_blocks', params)

    @api_version("1.4.0", "1.4.0", "1.4.0")
    def domain_unblock(self, domain=None):
        """
        Remove a domain block for the logged-in user.
        """
        params = self.__generate_params(locals())
        self.__api_request('DELETE', '/api/v1/domain_blocks', params)

    ##
    # Writing data: Read markers
    ##
    @api_version("3.0.0", "3.0.0", __DICT_VERSION_MARKER)
    def markers_set(self, timelines, last_read_ids):
        """
        Set the "last read" marker(s) for the given timeline(s) to the given id(s)
        
        Note that if you give an invalid timeline name, this will silently do nothing.
        
        Returns a dict with the updated `read marker dicts`_, keyed by timeline name.
        """
        if not isinstance(timelines, (list, tuple)):
            timelines = [timelines]
            
        if not isinstance(last_read_ids, (list, tuple)):
            last_read_ids = [last_read_ids]
            
        if len(last_read_ids) != len(timelines):
            raise MastodonIllegalArgumentError("Number of specified timelines and ids must be the same")
        
        params = collections.OrderedDict()
        for timeline, last_read_id in zip(timelines, last_read_ids):
            params[timeline] = collections.OrderedDict()
            params[timeline]["last_read_id"] = self.__unpack_id(last_read_id)
        
        return self.__api_request('POST', '/api/v1/markers', params, use_json=True)

    ###
    # Writing data: Push subscriptions
    ###
    @api_version("2.4.0", "2.4.0", __DICT_VERSION_PUSH)
    def push_subscription_set(self, endpoint, encrypt_params, follow_events=None, 
                              favourite_events=None, reblog_events=None, 
                              mention_events=None, poll_events=None,
                              follow_request_events=None):
        """
        Sets up or modifies the push subscription the logged-in user has for this app.
        
        `endpoint` is the endpoint URL mastodon should call for pushes. Note that mastodon
        requires https for this URL. `encrypt_params` is a dict with key parameters that allow
        the server to encrypt data for you: A public key `pubkey` and a shared secret `auth`.
        You can generate this as well as the corresponding private key using the 
        `push_subscription_generate_keys()`_ function.
        
        The rest of the parameters controls what kind of events you wish to subscribe to.
        
        Returns a `push subscription dict`_.
        """
        endpoint = Mastodon.__protocolize(endpoint)
        
        push_pubkey_b64 = base64.b64encode(encrypt_params['pubkey'])
        push_auth_b64 = base64.b64encode(encrypt_params['auth'])
        
        params = {
            'subscription[endpoint]': endpoint,
            'subscription[keys][p256dh]': push_pubkey_b64,
            'subscription[keys][auth]': push_auth_b64
        }
        
        if follow_events != None:
            params['data[alerts][follow]'] = follow_events
        
        if favourite_events != None:
            params['data[alerts][favourite]'] = favourite_events
            
        if reblog_events != None:
            params['data[alerts][reblog]'] = reblog_events
            
        if mention_events != None:
            params['data[alerts][mention]'] = mention_events
            
        if poll_events != None:
            params['data[alerts][poll]'] = poll_events
            
        if follow_request_events != None:
            params['data[alerts][follow_request]'] = follow_request_events
        
        # Canonicalize booleans
        params = self.__generate_params(params)
        
        return self.__api_request('POST', '/api/v1/push/subscription', params)
    
    @api_version("2.4.0", "2.4.0", __DICT_VERSION_PUSH)
    def push_subscription_update(self, follow_events=None, 
                              favourite_events=None, reblog_events=None, 
                              mention_events=None, poll_events=None,
                              follow_request_events=None):
        """
        Modifies what kind of events the app wishes to subscribe to.
        
        Returns the updated `push subscription dict`_.
        """
        params = {}
        
        if follow_events != None:
            params['data[alerts][follow]'] = follow_events
        
        if favourite_events != None:
            params['data[alerts][favourite]'] = favourite_events
            
        if reblog_events != None:
            params['data[alerts][reblog]'] = reblog_events
            
        if mention_events != None:
            params['data[alerts][mention]'] = mention_events
            
        if poll_events != None:
            params['data[alerts][poll]'] = poll_events
            
        if follow_request_events != None:
            params['data[alerts][follow_request]'] = follow_request_events
            
        # Canonicalize booleans
        params = self.__generate_params(params)            
            
        return self.__api_request('PUT', '/api/v1/push/subscription', params)
    
    @api_version("2.4.0", "2.4.0", "2.4.0")
    def push_subscription_delete(self):
        """
        Remove the current push subscription the logged-in user has for this app.
        """
        self.__api_request('DELETE', '/api/v1/push/subscription')
    
    ###
    # Writing data: Annoucements
    ###
    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_dismiss(self, id):
        """
        Set the given annoucement to read.
        """
        id = self.__unpack_id(id)
        
        url = '/api/v1/announcements/{0}/dismiss'.format(str(id))
        self.__api_request('POST', url)
        
    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_reaction_create(self, id, reaction):
        """
        Add a reaction to an announcement. `reaction` can either be a unicode emoji
        or the name of one of the instances custom emoji.
        
        Will throw an API error if the reaction name is not one of the allowed things
        or when trying to add a reaction that the user has already added (adding a
        reaction that a different user added is legal and increments the count).
        """
        id = self.__unpack_id(id)
        
        url = '/api/v1/announcements/{0}/reactions/{1}'.format(str(id), reaction)
        self.__api_request('PUT', url)
     
    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_reaction_delete(self, id, reaction):
        """
        Remove a reaction to an announcement.
        
        Will throw an API error if the reaction does not exist.
        """        
        id = self.__unpack_id(id)
        
        url = '/api/v1/announcements/{0}/reactions/{1}'.format(str(id), reaction)
        self.__api_request('DELETE', url)
        
    ###
    # Moderation API
    ###
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_ADMIN_ACCOUNT)
    def admin_accounts(self, remote=False, by_domain=None, status='active', username=None, display_name=None, email=None, ip=None, staff_only=False, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches a list of accounts that match given criteria. By default, local accounts are returned.
        
        * Set `remote` to True to get remote accounts, otherwise local accounts are returned (default: local accounts)
        * Set `by_domain` to a domain to get only accounts from that domain.
        * Set `status` to one of "active", "pending", "disabled", "silenced" or "suspended" to get only accounts with that moderation status (default: active)
        * Set `username` to a string to get only accounts whose username contains this string.
        * Set `display_name` to a string to get only accounts whose display name contains this string.
        * Set `email` to an email to get only accounts with that email (this only works on local accounts).
        * Set `ip` to an ip (as a string, standard v4/v6 notation) to get only accounts whose last active ip is that ip (this only works on local accounts).
        * Set `staff_only` to True to only get staff accounts (this only works on local accounts).
        
        Note that setting the boolean parameters to False does not mean "give me users to which this does not apply" but
        instead means "I do not care if users have this attribute".
        
        Returns a list of `admin account dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
        
        params = self.__generate_params(locals(), ['remote', 'status', 'staff_only'])
        
        if remote == True:
            params["remote"] = True
        
        mod_statuses = ["active", "pending", "disabled", "silenced", "suspended"]
        if not status in mod_statuses:
            raise ValueError("Invalid moderation status requested.")
        
        if staff_only == True:
            params["staff"] = True
        
        for mod_status in mod_statuses:
            if status == mod_status:
                params[status] = True
        
        return self.__api_request('GET', '/api/v1/admin/accounts', params)
        
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account(self, id):
        """
        Fetches a single `admin account dict`_ for the user with the given id.
        
        Returns that dict.
        """
        id = self.__unpack_id(id)        
        return self.__api_request('GET', '/api/v1/admin/accounts/{0}'.format(id))
    
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_enable(self, id):
        """
        Reenables login for a local account for which login has been disabled.
        
        Returns the updated `admin account dict`_.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/enable'.format(id))
        
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_approve(self, id):
        """
        Approves a pending account.
        
        Returns the updated `admin account dict`_.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/approve'.format(id))

    @api_version("2.9.1", "2.9.1", __DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_reject(self, id):
        """
        Rejects and deletes a pending account.
        
        Returns the updated `admin account dict`_ for the account that is now gone.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/reject'.format(id))
      
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsilence(self, id):
        """
        Unsilences an account.
        
        Returns the updated `admin account dict`_.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/unsilence'.format(id))
        
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsuspend(self, id):
        """
        Unsuspends an account.
        
        Returns the updated `admin account dict`_.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', '/api/v1/admin/accounts/{0}/unsuspend'.format(id))
    
    @api_version("2.9.1", "2.9.1", "2.9.1")
    def admin_account_moderate(self, id, action=None, report_id=None, warning_preset_id=None, text=None, send_email_notification=True):
        """
        Perform a moderation action on an account.
        
        Valid actions are:
            * "disable" - for a local user, disable login.
            * "silence" - hide the users posts from all public timelines.
            * "suspend" - irreversibly delete all the users posts, past and future.
        If no action is specified, the user is only issued a warning.
        
        Specify the id of a report as `report_id` to close the report with this moderation action as the resolution.
        Specify `warning_preset_id` to use a warning preset as the notification text to the user, or `text` to specify text directly.
        If both are specified, they are concatenated (preset first). Note that there is currently no API to retrieve or create
        warning presets.
        
        Set `send_email_notification` to False to not send the user an e-mail notification informing them of the moderation action.
        """
        if action is None:
            action = "none"
        
        if send_email_notification == False:
            send_email_notification = None
            
        id = self.__unpack_id(id)
        if not report_id is None:
            report_id = self.__unpack_id(report_id)
            
        params = self.__generate_params(locals(), ['id', 'action'])
        
        params["type"] = action
        
        self.__api_request('POST', '/api/v1/admin/accounts/{0}/action'.format(id), params)
        
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_REPORT)
    def admin_reports(self, resolved=False, account_id=None, target_account_id=None, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches the list of reports. 
        
        Set `resolved` to True to search for resolved reports. `account_id` and `target_account_id`
        can be used to get reports filed by or about a specific user.
        
        Returns a list of `report dicts`_.
        """
        if max_id != None:
            max_id = self.__unpack_id(max_id)
        
        if min_id != None:
            min_id = self.__unpack_id(min_id)
        
        if since_id != None:
            since_id = self.__unpack_id(since_id)
        
        if not account_id is None:
            account_id = self.__unpack_id(account_id)
            
        if not target_account_id is None:
            target_account_id = self.__unpack_id(target_account_id)
            
        if resolved == False:
            resolved = None
            
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/reports', params)
        
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_REPORT)    
    def admin_report(self, id):
        """
        Fetches the report with the given id.
        
        Returns a `report dict`_.
        """
        id = self.__unpack_id(id)        
        return self.__api_request('GET', '/api/v1/admin/reports/{0}'.format(id))
    
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_REPORT)
    def admin_report_assign(self, id):
        """
        Assigns the given report to the logged-in user.
        
        Returns the updated `report dict`_.
        """
        id = self.__unpack_id(id)        
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/assign_to_self'.format(id))
    
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_REPORT)
    def admin_report_unassign(self, id):
        """
        Unassigns the given report from the logged-in user.
        
        Returns the updated `report dict`_.
        """
        id = self.__unpack_id(id)        
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/unassign'.format(id))
    
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_REPORT)
    def admin_report_reopen(self, id):
        """
        Reopens a closed report.
        
        Returns the updated `report dict`_.
        """
        id = self.__unpack_id(id)        
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/reopen'.format(id))
        
    @api_version("2.9.1", "2.9.1", __DICT_VERSION_REPORT)
    def admin_report_resolve(self, id):
        """
        Marks a report as resolved (without taking any action).
        
        Returns the updated `report dict`_.
        """
        id = self.__unpack_id(id)        
        return self.__api_request('POST', '/api/v1/admin/reports/{0}/resolve'.format(id))
        
    ###
    # Push subscription crypto utilities
    ###     
    def push_subscription_generate_keys(self):
        """
        Generates a private key, public key and shared secret for use in webpush subscriptions.
        
        Returns two dicts: One with the private key and shared secret and another with the 
        public key and shared secret.
        """
        if not IMPL_HAS_CRYPTO:
            raise NotImplementedError('To use the crypto tools, please install the webpush feature dependencies.')
        
        push_key_pair = ec.generate_private_key(ec.SECP256R1(), default_backend())
        push_key_priv = push_key_pair.private_numbers().private_value
        
        crypto_ver = cryptography.__version__
        if len(crypto_ver) < 5:
            crypto_ver += ".0"
        if bigger_version(crypto_ver, "2.5.0") == crypto_ver:
            push_key_pub = push_key_pair.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
        else:
            push_key_pub = push_key_pair.public_key().public_numbers().encode_point() 
        push_shared_secret = os.urandom(16)
        
        priv_dict = {
            'privkey': push_key_priv,
            'auth': push_shared_secret
        }
        
        pub_dict = {
            'pubkey': push_key_pub,
            'auth': push_shared_secret
        }
        
        return priv_dict, pub_dict
    
    def push_subscription_decrypt_push(self, data, decrypt_params, encryption_header, crypto_key_header):
        """
        Decrypts `data` received in a webpush request. Requires the private key dict 
        from `push_subscription_generate_keys()`_ (`decrypt_params`) as well as the 
        Encryption and server Crypto-Key headers from the received webpush
        
        Returns the decoded webpush as a `push notification dict`_.
        """
        if (not IMPL_HAS_ECE) or (not IMPL_HAS_CRYPTO):
            raise NotImplementedError('To use the crypto tools, please install the webpush feature dependencies.')
        
        salt = self.__decode_webpush_b64(encryption_header.split("salt=")[1].strip())
        dhparams = self.__decode_webpush_b64(crypto_key_header.split("dh=")[1].split(";")[0].strip())
        p256ecdsa = self.__decode_webpush_b64(crypto_key_header.split("p256ecdsa=")[1].strip())
        dec_key = ec.derive_private_key(decrypt_params['privkey'], ec.SECP256R1(), default_backend())
        decrypted = http_ece.decrypt(
            data,
            salt = salt,
            key = p256ecdsa,
            private_key = dec_key, 
            dh = dhparams, 
            auth_secret=decrypt_params['auth'],
            keylabel = "P-256",
            version = "aesgcm"
        )
        
        return json.loads(decrypted.decode('utf-8'), object_hook = Mastodon.__json_hooks)
   
    ###
    # Blurhash utilities
    ###    
    def decode_blurhash(self, media_dict, out_size = (16, 16), size_per_component = True, return_linear = True):
        """
        Basic media-dict blurhash decoding.
        
        out_size is the desired result size in pixels, either absolute or per blurhash
        component (this is the default).
        
        By default, this function will return the image as linear RGB, ready for further
        scaling operations. If you want to display the image directly, set return_linear 
        to False.
        
        Returns the decoded blurhash image as a three-dimensional list: [height][width][3],
        with the last dimension being RGB colours.
        
        For further info and tips for advanced usage, refer to the documentation for the
        blurhash module: https://github.com/halcy/blurhash-python
        """
        if not IMPL_HAS_BLURHASH:
            raise NotImplementedError('To use the blurhash functions, please install the blurhash python module.')

        # Figure out what size to decode to
        decode_components_x, decode_components_y = blurhash.components(media_dict["blurhash"])
        if size_per_component == False:
            decode_size_x = out_size[0]
            decode_size_y = out_size[1]
        else:
            decode_size_x = decode_components_x * out_size[0]
            decode_size_y = decode_components_y * out_size[1]

        # Decode
        decoded_image = blurhash.decode(media_dict["blurhash"], decode_size_x, decode_size_y, linear = return_linear)

        # And that's pretty much it.
        return decoded_image
        
    ###
    # Pagination
    ###
    def fetch_next(self, previous_page):
        """
        Fetches the next page of results of a paginated request. Pass in the
        previous page in its entirety, or the pagination information dict
        returned as a part of that pages last status ('_pagination_next').

        Returns the next page or None if no further data is available.
        """
        if isinstance(previous_page, list) and len(previous_page) != 0:
            if hasattr(previous_page[-1], '_pagination_next'):
                params = copy.deepcopy(previous_page[-1]._pagination_next)
            else:
                return None
        else:
            params = copy.deepcopy(previous_page)

        method = params['_pagination_method']
        del params['_pagination_method']

        endpoint = params['_pagination_endpoint']
        del params['_pagination_endpoint']

        return self.__api_request(method, endpoint, params)

    def fetch_previous(self, next_page):
        """
        Fetches the previous page of results of a paginated request. Pass in the
        previous page in its entirety, or the pagination information dict
        returned as a part of that pages first status ('_pagination_prev').

        Returns the previous page or None if no further data is available.
        """
        if isinstance(next_page, list) and len(next_page) != 0:
            if hasattr(next_page[0], '_pagination_prev'):
                params = copy.deepcopy(next_page[0]._pagination_prev)
            else:
                return None
        else:
            params = copy.deepcopy(next_page)

        method = params['_pagination_method']
        del params['_pagination_method']

        endpoint = params['_pagination_endpoint']
        del params['_pagination_endpoint']

        return self.__api_request(method, endpoint, params)

    def fetch_remaining(self, first_page):
        """
        Fetches all the remaining pages of a paginated request starting from a
        first page and returns the entire set of results (including the first page
        that was passed in) as a big list.

        Be careful, as this might generate a lot of requests, depending on what you are
        fetching, and might cause you to run into rate limits very quickly.
        """
        first_page = copy.deepcopy(first_page)

        all_pages = []
        current_page = first_page
        while current_page is not None and len(current_page) > 0:
            all_pages.extend(current_page)
            current_page = self.fetch_next(current_page)

        return all_pages

    ###
    # Streaming
    ###
    @api_version("1.1.0", "1.4.2", __DICT_VERSION_STATUS)    
    def stream_user(self, listener, run_async=False, timeout=__DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=__DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams events that are relevant to the authorized user, i.e. home
        timeline and notifications.
        """
        return self.__stream('/api/v1/streaming/user', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2", __DICT_VERSION_STATUS)
    def stream_public(self, listener, run_async=False, timeout=__DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=__DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams public events.
        """
        return self.__stream('/api/v1/streaming/public', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2", __DICT_VERSION_STATUS)
    def stream_local(self, listener, run_async=False, timeout=__DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=__DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams local public events.
        """
        return self.__stream('/api/v1/streaming/public/local', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2", __DICT_VERSION_STATUS)
    def stream_hashtag(self, tag, listener, local=False, run_async=False, timeout=__DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=__DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Stream for all public statuses for the hashtag 'tag' seen by the connected
        instance.
        
        Set local to True to only get local statuses.
        """
        if tag.startswith("#"):
            raise MastodonIllegalArgumentError("Tag parameter should omit leading #")
        base = '/api/v1/streaming/hashtag'
        if local:
            base += '/local'
        return self.__stream("{}?tag={}".format(base, tag), listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("2.1.0", "2.1.0", __DICT_VERSION_STATUS)
    def stream_list(self, id, listener, run_async=False, timeout=__DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=__DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Stream events for the current user, restricted to accounts on the given
        list. 
        """
        id =  self.__unpack_id(id)
        return self.__stream("/api/v1/streaming/list?list={}".format(id), listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)
    
    @api_version("2.6.0", "2.6.0", __DICT_VERSION_STATUS)
    def stream_direct(self, listener, run_async=False, timeout=__DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=__DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams direct message events for the logged-in user, as conversation events.
        """
        return self.__stream('/api/v1/streaming/direct', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)
    
    @api_version("2.5.0", "2.5.0", "2.5.0")
    def stream_healthy(self):
        """
        Returns without True if streaming API is okay, False or raises an error otherwise.
        """
        api_okay = self.__api_request('GET', '/api/v1/streaming/health', base_url_override = self.__get_streaming_base(), parse=False)
        if api_okay == b'OK':
            return True
        return False
    
    ###
    # Internal helpers, dragons probably
    ###
    def __datetime_to_epoch(self, date_time):
        """
        Converts a python datetime to unix epoch, accounting for
        time zones and such.

        Assumes UTC if timezone is not given.
        """
        date_time_utc = None
        if date_time.tzinfo is None:
            date_time_utc = date_time.replace(tzinfo=pytz.utc)
        else:
            date_time_utc = date_time.astimezone(pytz.utc)

        epoch_utc = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)

        return (date_time_utc - epoch_utc).total_seconds()

    def __get_logged_in_id(self):
        """
        Fetch the logged in users ID, with caching. ID is reset on calls to log_in.
        """
        if self.__logged_in_id == None:
            self.__logged_in_id = self.account_verify_credentials().id
        return self.__logged_in_id
            

    @staticmethod
    def __json_allow_dict_attrs(json_object):
        """
        Makes it possible to use attribute notation to access a dicts
        elements, while still allowing the dict to act as a dict.
        """
        if isinstance(json_object, dict):
            return AttribAccessDict(json_object)
        return json_object

    @staticmethod
    def __json_date_parse(json_object):
        """
        Parse dates in certain known json fields, if possible.
        """
        known_date_fields = ["created_at", "week", "day", "expires_at", "scheduled_at", "updated_at", "last_status_at", "starts_at", "ends_at", "published_at"]
        for k, v in json_object.items():
            if k in known_date_fields:
                if v != None:
                    try:
                        if isinstance(v, int):
                            json_object[k] = datetime.datetime.fromtimestamp(v, pytz.utc)
                        else:
                            json_object[k] = dateutil.parser.parse(v)
                    except:
                        raise MastodonAPIError('Encountered invalid date.')
        return json_object

    @staticmethod
    def __json_truefalse_parse(json_object):
        """
        Parse 'True' / 'False' strings in certain known fields
        """
        for key in ('follow', 'favourite', 'reblog', 'mention'):
            if (key in json_object and isinstance(json_object[key], six.text_type)):
                if json_object[key].lower() == 'true':
                    json_object[key] = True
                if json_object[key].lower() == 'False':
                    json_object[key] = False
        return json_object
    
    @staticmethod
    def __json_strnum_to_bignum(json_object):
        """
        Converts json string numerals to native python bignums.
        """
        for key in ('id', 'week', 'in_reply_to_id', 'in_reply_to_account_id', 'logins', 'registrations', 'statuses', 'day', 'last_read_id'):
            if (key in json_object and isinstance(json_object[key], six.text_type)):
                try:
                    json_object[key] = int(json_object[key])
                except ValueError:
                    pass

        return json_object
    
    @staticmethod
    def __json_hooks(json_object):
        """
        All the json hooks. Used in request parsing.
        """
        json_object = Mastodon.__json_strnum_to_bignum(json_object)        
        json_object = Mastodon.__json_date_parse(json_object)
        json_object = Mastodon.__json_truefalse_parse(json_object)
        json_object = Mastodon.__json_allow_dict_attrs(json_object)
        return json_object

    @staticmethod
    def __consistent_isoformat_utc(datetime_val):
        """
        Function that does what isoformat does but it actually does the same
        every time instead of randomly doing different things on some systems
        and also it represents that time as the equivalent UTC time.
        """
        isotime = datetime_val.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        if isotime[-2] != ":":
            isotime = isotime[:-2] + ":" + isotime[-2:]
        return isotime

    def __api_request(self, method, endpoint, params={}, files={}, headers={}, access_token_override=None, base_url_override=None, do_ratelimiting=True, use_json=False, parse=True):
        """
        Internal API request helper.
        """
        response = None
        remaining_wait = 0
        
        # "pace" mode ratelimiting: Assume constant rate of requests, sleep a little less long than it
        # would take to not hit the rate limit at that request rate.
        if do_ratelimiting and self.ratelimit_method == "pace":
            if self.ratelimit_remaining == 0:
                to_next = self.ratelimit_reset - time.time()
                if to_next > 0:
                    # As a precaution, never sleep longer than 5 minutes
                    to_next = min(to_next, 5 * 60)
                    time.sleep(to_next)
            else:
                time_waited = time.time() - self.ratelimit_lastcall
                time_wait = float(self.ratelimit_reset - time.time()) / float(self.ratelimit_remaining)
                remaining_wait = time_wait - time_waited

            if remaining_wait > 0:
                to_next = remaining_wait / self.ratelimit_pacefactor
                to_next = min(to_next, 5 * 60)
                time.sleep(to_next)

        # Generate request headers
        headers = copy.deepcopy(headers)
        if not self.access_token is None:
            headers['Authorization'] = 'Bearer ' + self.access_token
        if not access_token_override is None:
            headers['Authorization'] = 'Bearer ' + access_token_override

        # Determine base URL
        base_url = self.api_base_url
        if not base_url_override is None:
            base_url = base_url_override

        if self.debug_requests:
            print('Mastodon: Request to endpoint "' + base_url + endpoint + '" using method "' + method + '".')
            print('Parameters: ' + str(params))
            print('Headers: ' + str(headers))
            print('Files: ' + str(files))

        # Make request
        request_complete = False
        while not request_complete:
            request_complete = True

            response_object = None
            try:
                kwargs = dict(headers=headers, files=files,
                              timeout=self.request_timeout)
                if use_json == False:
                    if method == 'GET':
                        kwargs['params'] = params
                    else:
                        kwargs['data'] = params
                else:
                    kwargs['json'] = params
                
                # Block list with exactly three entries, matching on hashes of the instance API domain
                # For more information, have a look at the docs
                if hashlib.sha256(",".join(base_url.split("//")[-1].split("/")[0].split(".")[-2:]).encode("utf-8")).hexdigest() in \
                    [
                        "f3b50af8594eaa91dc440357a92691ff65dbfc9555226e9545b8e083dc10d2e1", 
                        "b96d2de9784efb5af0af56965b8616afe5469c06e7188ad0ccaee5c7cb8a56b6",
                        "2dc0cbc89fad4873f665b78cc2f8b6b80fae4af9ac43c0d693edfda27275f517"
                    ]:
                    raise Exception("Access denied.")
                    
                response_object = self.session.request(method, base_url + endpoint, **kwargs)
            except Exception as e:
                raise MastodonNetworkError("Could not complete request: %s" % e)

            if response_object is None:
                raise MastodonIllegalArgumentError("Illegal request.")

            # Parse rate limiting headers
            if 'X-RateLimit-Remaining' in response_object.headers and do_ratelimiting:
                self.ratelimit_remaining = int(response_object.headers['X-RateLimit-Remaining'])
                self.ratelimit_limit = int(response_object.headers['X-RateLimit-Limit'])

                try:
                    ratelimit_reset_datetime = dateutil.parser.parse(response_object.headers['X-RateLimit-Reset'])
                    self.ratelimit_reset = self.__datetime_to_epoch(ratelimit_reset_datetime)

                    # Adjust server time to local clock
                    if 'Date' in response_object.headers:
                        server_time_datetime = dateutil.parser.parse(response_object.headers['Date'])
                        server_time = self.__datetime_to_epoch(server_time_datetime)
                        server_time_diff = time.time() - server_time
                        self.ratelimit_reset += server_time_diff
                        self.ratelimit_lastcall = time.time()
                except Exception as e:
                    raise MastodonRatelimitError("Rate limit time calculations failed: %s" % e)

            # Handle response
            if self.debug_requests:
                print('Mastodon: Response received with code ' + str(response_object.status_code) + '.')
                print('response headers: ' + str(response_object.headers))
                print('Response text content: ' + str(response_object.text))

            if not response_object.ok:
                try:
                    response = response_object.json(object_hook=self.__json_hooks)
                    if isinstance(response, dict) and 'error' in response:
                        error_msg = response['error']
                    elif isinstance(response, str):
                        error_msg = response
                    else:
                        error_msg = None
                except ValueError:
                    error_msg = None

                # Handle rate limiting
                if response_object.status_code == 429:
                    if self.ratelimit_method == 'throw' or not do_ratelimiting:
                        raise MastodonRatelimitError('Hit rate limit.')
                    elif self.ratelimit_method in ('wait', 'pace'):
                        to_next = self.ratelimit_reset - time.time()
                        if to_next > 0:
                            # As a precaution, never sleep longer than 5 minutes
                            to_next = min(to_next, 5 * 60)
                            time.sleep(to_next)
                            request_complete = False
                            continue

                if response_object.status_code == 404:
                    ex_type = MastodonNotFoundError
                    if not error_msg:
                        error_msg = 'Endpoint not found.'
                        # this is for compatibility with older versions
                        # which raised MastodonAPIError('Endpoint not found.')
                        # on any 404
                elif response_object.status_code == 401:
                    ex_type = MastodonUnauthorizedError
                elif response_object.status_code == 500:
                    ex_type = MastodonInternalServerError
                elif response_object.status_code == 502:
                    ex_type = MastodonBadGatewayError
                elif response_object.status_code == 503:
                    ex_type = MastodonServiceUnavailableError
                elif response_object.status_code == 504:
                    ex_type = MastodonGatewayTimeoutError
                elif response_object.status_code >= 500 and \
                     response_object.status_code <= 511:
                    ex_type = MastodonServerError
                else:
                    ex_type = MastodonAPIError

                raise ex_type(
                        'Mastodon API returned error',
                        response_object.status_code,
                        response_object.reason,
                        error_msg)

            if parse == True:
                try:
                    response = response_object.json(object_hook=self.__json_hooks)
                except:
                    raise MastodonAPIError(
                        "Could not parse response as JSON, response code was %s, "
                        "bad json content was '%s'" % (response_object.status_code,
                                                    response_object.content))
            else:
                response = response_object.content
                
            # Parse link headers
            if isinstance(response, list) and \
                    'Link' in response_object.headers and \
                    response_object.headers['Link'] != "":
                tmp_urls = requests.utils.parse_header_links(
                    response_object.headers['Link'].rstrip('>').replace('>,<', ',<'))
                for url in tmp_urls:
                    if 'rel' not in url:
                        continue

                    if url['rel'] == 'next':
                        # Be paranoid and extract max_id specifically
                        next_url = url['url']
                        matchgroups = re.search(r"[?&]max_id=([^&]+)", next_url)

                        if matchgroups:
                            next_params = copy.deepcopy(params)
                            next_params['_pagination_method'] = method
                            next_params['_pagination_endpoint'] = endpoint
                            max_id = matchgroups.group(1)
                            if max_id.isdigit():
                                next_params['max_id'] = int(max_id)
                            else:
                                next_params['max_id'] = max_id
                            if "since_id" in next_params:
                                del next_params['since_id']
                            if "min_id" in next_params:
                                del next_params['min_id']
                            response[-1]._pagination_next = next_params

                    if url['rel'] == 'prev':
                        # Be paranoid and extract since_id or min_id specifically
                        prev_url = url['url']
                        
                        # Old and busted (pre-2.6.0): since_id pagination
                        matchgroups = re.search(r"[?&]since_id=([^&]+)", prev_url)
                        if matchgroups:
                            prev_params = copy.deepcopy(params)
                            prev_params['_pagination_method'] = method
                            prev_params['_pagination_endpoint'] = endpoint
                            since_id = matchgroups.group(1)
                            if since_id.isdigit():
                                prev_params['since_id'] = int(since_id)
                            else:
                                prev_params['since_id'] = since_id
                            if "max_id" in prev_params:
                                del prev_params['max_id']
                            response[0]._pagination_prev = prev_params
                            
                        # New and fantastico (post-2.6.0): min_id pagination
                        matchgroups = re.search(r"[?&]min_id=([^&]+)", prev_url)
                        if matchgroups:
                            prev_params = copy.deepcopy(params)
                            prev_params['_pagination_method'] = method
                            prev_params['_pagination_endpoint'] = endpoint
                            min_id = matchgroups.group(1)
                            if min_id.isdigit():
                                prev_params['min_id'] = int(min_id)
                            else:
                                prev_params['min_id'] = min_id
                            if "max_id" in prev_params:
                                del prev_params['max_id']
                            response[0]._pagination_prev = prev_params

        return response

    def __get_streaming_base(self):
        """
        Internal streaming API helper.
        
        Returns the correct URL for the streaming API.
        """
        instance = self.instance()
        if "streaming_api" in instance["urls"] and instance["urls"]["streaming_api"] != self.api_base_url:
            # This is probably a websockets URL, which is really for the browser, but requests can't handle it
            # So we do this below to turn it into an HTTPS or HTTP URL
            parse = urlparse(instance["urls"]["streaming_api"])
            if parse.scheme == 'wss':
                url = "https://" + parse.netloc
            elif parse.scheme == 'ws':
                url = "http://" + parse.netloc
            else:
                raise MastodonAPIError(
                        "Could not parse streaming api location returned from server: {}.".format(
                            instance["urls"]["streaming_api"]))
        else:
            url = self.api_base_url
        return url

    def __stream(self, endpoint, listener, params={}, run_async=False, timeout=__DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=__DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Internal streaming API helper.

        Returns a handle to the open connection that the user can close if they
        wish to terminate it.
        """

        # Check if we have to redirect
        url = self.__get_streaming_base()

        # The streaming server can't handle two slashes in a path, so remove trailing slashes
        if url[-1] == '/':
            url = url[:-1]
        
        # Connect function (called and then potentially passed to async handler)
        def connect_func():
            headers = {"Authorization": "Bearer " + self.access_token} if self.access_token else {}
            connection = self.session.get(url + endpoint, headers = headers, data = params, stream = True,
                                  timeout=(self.request_timeout, timeout))

            if connection.status_code != 200:
                raise MastodonNetworkError("Could not connect to streaming server: %s" % connection.reason)
            return connection
        connection = None
        
        # Async stream handler
        class __stream_handle():
            def __init__(self, connection, connect_func, reconnect_async, reconnect_async_wait_sec):
                self.closed = False
                self.running = True
                self.connection = connection
                self.connect_func = connect_func
                self.reconnect_async = reconnect_async
                self.reconnect_async_wait_sec = reconnect_async_wait_sec
                self.reconnecting = False
                
            def close(self):
                self.closed = True
                self.connection.close()

            def is_alive(self):
                return self._thread.is_alive()

            def is_receiving(self):
                if self.closed or not self.running or self.reconnecting or not self.is_alive():
                    return False
                else:
                    return True

            def _threadproc(self):
                self._thread = threading.current_thread()
                
                # Run until closed or until error if not autoreconnecting
                while self.running:
                    if not self.connection is None:
                        with closing(self.connection) as r:
                            try:
                                listener.handle_stream(r)
                            except (AttributeError, MastodonMalformedEventError, MastodonNetworkError) as e:
                                if not (self.closed or self.reconnect_async):
                                    raise e
                                else:
                                    if self.closed:
                                        self.running = False

                    # Reconnect loop. Try immediately once, then with delays on error.
                    if (self.reconnect_async and not self.closed) or self.connection is None:
                        self.reconnecting = True
                        connect_success = False
                        while not connect_success:
                            connect_success = True
                            try:
                                self.connection = self.connect_func()
                                if self.connection.status_code != 200:
                                    time.sleep(self.reconnect_async_wait_sec)
                                    connect_success = False
                                    exception = MastodonNetworkError("Could not connect to server.")
                                    listener.on_abort(exception)
                            except:
                                time.sleep(self.reconnect_async_wait_sec)
                                connect_success = False
                        self.reconnecting = False
                    else:
                        self.running = False
                return 0

        if run_async:
            handle = __stream_handle(connection, connect_func, reconnect_async, reconnect_async_wait_sec)
            t = threading.Thread(args=(), target=handle._threadproc)
            t.daemon = True
            t.start()
            return handle
        else:
            # Blocking, never returns (can only leave via exception)
            connection = connect_func()            
            with closing(connection) as r:
                listener.handle_stream(r)

    def __generate_params(self, params, exclude=[]):
        """
        Internal named-parameters-to-dict helper.

        Note for developers: If called with locals() as params,
        as is the usual practice in this code, the __generate_params call
        (or at least the locals() call) should generally be the first thing
        in your function.
        """
        params = collections.OrderedDict(params)

        if 'self' in params:
            del params['self']
        
        param_keys = list(params.keys())
        for key in param_keys:
            if isinstance(params[key], bool) and params[key] == False:
                params[key] = '0'
            if isinstance(params[key], bool) and params[key] == True:
                params[key] = '1'
                
        for key in param_keys:
            if params[key] is None or key in exclude:
                del params[key]

        param_keys = list(params.keys())
        for key in param_keys:
            if isinstance(params[key], list):
                params[key + "[]"] = params[key]
                del params[key]
            
        return params
    
    def __unpack_id(self, id):
        """
        Internal object-to-id converter
        
        Checks if id is a dict that contains id and
        returns the id inside, otherwise just returns
        the id straight.
        """
        if isinstance(id, dict) and "id" in id:
            return id["id"]
        else:
            return id
    
    def __decode_webpush_b64(self, data):
        """
        Re-pads and decodes urlsafe base64.
        """
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += '=' * (4 - missing_padding)
        return base64.urlsafe_b64decode(data)
    
    def __get_token_expired(self):
        """Internal helper for oauth code"""
        return self._token_expired < datetime.datetime.now()

    def __set_token_expired(self, value):
        """Internal helper for oauth code"""
        self._token_expired = datetime.datetime.now() + datetime.timedelta(seconds=value)
        return

    def __get_refresh_token(self):
        """Internal helper for oauth code"""
        return self._refresh_token

    def __set_refresh_token(self, value):
        """Internal helper for oauth code"""
        self._refresh_token = value
        return
    
    @staticmethod
    def __protocolize(base_url):
        """Internal add-protocol-to-url helper"""
        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            base_url = "https://" + base_url

        # Some API endpoints can't handle extra /'s in path requests
        base_url = base_url.rstrip("/")
        return base_url


##
# Exceptions
##
class MastodonError(Exception):
    """Base class for Mastodon.py exceptions"""

class MastodonVersionError(MastodonError):
    """Raised when a function is called that the version of Mastodon for which
       Mastodon.py was instantiated does not support"""

class MastodonIllegalArgumentError(ValueError, MastodonError):
    """Raised when an incorrect parameter is passed to a function"""
    pass


class MastodonIOError(IOError, MastodonError):
    """Base class for Mastodon.py I/O errors"""


class MastodonFileNotFoundError(MastodonIOError):
    """Raised when a file requested to be loaded can not be opened"""
    pass


class MastodonNetworkError(MastodonIOError):
    """Raised when network communication with the server fails"""
    pass

class MastodonReadTimeout(MastodonNetworkError):
    """Raised when a stream times out"""
    pass


class MastodonAPIError(MastodonError):
    """Raised when the mastodon API generates a response that cannot be handled"""
    pass

class MastodonServerError(MastodonAPIError):
    """Raised if the Server is malconfigured and returns a 5xx error code"""
    pass

class MastodonInternalServerError(MastodonServerError):
    """Raised if the Server returns a 500 error"""
    pass

class MastodonBadGatewayError(MastodonServerError):
    """Raised if the Server returns a 502 error"""
    pass

class MastodonServiceUnavailableError(MastodonServerError):
    """Raised if the Server returns a 503 error"""
    pass

class MastodonGatewayTimeoutError(MastodonServerError):
    """Raised if the Server returns a 504 error"""
    pass

class MastodonNotFoundError(MastodonAPIError):
    """Raised when the mastodon API returns a 404 Not Found error"""
    pass

class MastodonUnauthorizedError(MastodonAPIError):
    """Raised when the mastodon API returns a 401 Unauthorized error

       This happens when an OAuth token is invalid or has been revoked,
       or when trying to access an endpoint that can't be used without
       authentication without providing credentials."""
    pass


class MastodonRatelimitError(MastodonError):
    """Raised when rate limiting is set to manual mode and the rate limit is exceeded"""
    pass

class MastodonMalformedEventError(MastodonError):
    """Raised when the server-sent event stream is malformed"""
    pass

def guess_type(media_file):
    mime_type = None
    try:
        mime_type = magic.from_file(media_file, mime=True)
    except AttributeError:
        mime_type = mimetypes.guess_type(media_file)[0]
    return mime_type
