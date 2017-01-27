# coding: utf-8

import requests
import os
import os.path
import mimetypes
import time
import random
import string
import pytz
import datetime
import dateutil
import dateutil.parser

class Mastodon:
    """
    Super basic but thorough and easy to use mastodon.social
    api wrapper in python.

    If anything is unclear, check the official API docs at
    https://github.com/Gargron/mastodon/wiki/API

    Presently, only username-password login is supported, somebody please
    patch in Real Proper OAuth if desired.
    """
    __DEFAULT_BASE_URL = 'https://mastodon.social'
    __DEFAULT_TIMEOUT = 300


    ###
    # Registering apps
    ###
    @staticmethod
    def create_app(client_name, scopes = ['read', 'write', 'follow'], redirect_uris = None, to_file = None, api_base_url = __DEFAULT_BASE_URL):
        """
        Create a new app with given client_name and scopes (read, write, follow)

        Specify redirect_uris if you want users to be redirected to a certain page after authenticating.
        Specify to_file to persist your apps info to a file so you can use them in the constructor.
        Specify api_base_url if you want to register an app on an instance different from the flagship one.

        Presently, app registration is open by default, but this is not guaranteed to be the case for all
        future mastodon instances or even the flagship instance in the future.

        Returns client_id and client_secret.
        """
        request_data = {
            'client_name': client_name,
            'scopes': " ".join(scopes)
        }

        try:
            if redirect_uris != None:
                request_data['redirect_uris'] = redirect_uris;
            else:
                request_data['redirect_uris'] = 'urn:ietf:wg:oauth:2.0:oob';

            response = requests.post(api_base_url + '/api/v1/apps', data = request_data, timeout = self.request_timeout).json()
        except:
            raise MastodonNetworkError("Could not complete request.")

        if to_file != None:
            with open(to_file, 'w') as secret_file:
                secret_file.write(response['client_id'] + '\n')
                secret_file.write(response['client_secret'] + '\n')

        return (response['client_id'], response['client_secret'])

    ###
    # Authentication, including constructor
    ###
    def __init__(self, client_id, client_secret = None, access_token = None, api_base_url = __DEFAULT_BASE_URL, debug_requests = False, ratelimit_method = "wait", ratelimit_pacefactor = 1.1, request_timeout = __DEFAULT_TIMEOUT):
        """
        Create a new API wrapper instance based on the given client_secret and client_id. If you
        give a client_id and it is not a file, you must also give a secret.

        You can also specify an access_token, directly or as a file (as written by log_in).

        Mastodon.py can try to respect rate limits in several ways, controlled by ratelimit_method.
        "throw" makes functions throw a MastodonRatelimitError when the rate
        limit is hit. "wait" mode will, once the limit is hit, wait and retry the request as soon
        as the rate limit resets, until it succeeds. "pace" works like throw, but tries to wait in
        between calls so that the limit is generally not hit (How hard it tries to not hit the rate
        limit can be controlled by ratelimit_pacefactor). The default setting is "wait". Note that
        even in "wait" and "pace" mode, requests can still fail due to network or other problems! Also
        note that "pace" and "wait" are NOT thread safe.

        Specify api_base_url if you wish to talk to an instance other than the flagship one.
        If a file is given as client_id, read client ID and secret from that file.

        By defautl, a timeout of 300 seconds is used for all requests. If you wish to change this,
        pass the desired timeout (in seconds) as request_timeout.
        """
        self.api_base_url = api_base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.debug_requests = debug_requests
        self.ratelimit_method = ratelimit_method

        self.ratelimit_limit = 150
        self.ratelimit_reset = time.time()
        self.ratelimit_remaining = 150
        self.ratelimit_lastcall = time.time()
        self.ratelimit_pacefactor = ratelimit_pacefactor

        self.request_timeout = request_timeout

        if not ratelimit_method in ["throw", "wait", "pace"]:
            raise MastodonIllegalArgumentError("Invalid ratelimit method.")

        if os.path.isfile(self.client_id):
            with open(self.client_id, 'r') as secret_file:
                self.client_id = secret_file.readline().rstrip()
                self.client_secret = secret_file.readline().rstrip()
        else:
            if self.client_secret == None:
                raise MastodonIllegalArgumentError('Specified client id directly, but did not supply secret')

        if self.access_token != None and os.path.isfile(self.access_token):
            with open(self.access_token, 'r') as token_file:
                self.access_token = token_file.readline().rstrip()

    def log_in(self, username, password, scopes = ['read', 'write', 'follow'], to_file = None):
        """
        Log in and sets access_token to what was returned. Note that your
        username is the e-mail you use to log in into mastodon.

        Can persist access token to file, to be used in the constructor.

        Will throw a MastodonIllegalArgumentError if username / password
        are wrong, scopes are not valid or granted scopes differ from requested.

        Returns the access_token.
        """
        params = self.__generate_params(locals())
        params['client_id'] = self.client_id
        params['client_secret'] = self.client_secret
        params['grant_type'] = 'password'
        params['scope'] = " ".join(scopes)

        try:
            response = self.__api_request('POST', '/oauth/token', params, do_ratelimiting = False)
            self.access_token = response['access_token']
        except:
            raise MastodonIllegalArgumentError('Invalid user name, password or scopes.')

        requested_scopes = " ".join(sorted(scopes))
        received_scopes = " ".join(sorted(response["scope"].split(" ")))

        if requested_scopes != received_scopes:
            raise MastodonAPIError('Granted scopes "' + received_scopes + '" differ from requested scopes "' + requested_scopes + '".')

        if to_file != None:
            with open(to_file, 'w') as token_file:
                token_file.write(response['access_token'] + '\n')

        return response['access_token']

    ###
    # Reading data: Timelines
    ##
    def timeline(self, timeline = "home", max_id = None, since_id = None, limit = None):
        """
        Fetch statuses, most recent ones first. Timeline can be home, mentions, public
        or tag/hashtag. See the following functions documentation for what those do.

        The default timeline is the "home" timeline.

        Returns a list of toot dicts.
        """
        params = self.__generate_params(locals(), ['timeline'])
        return self.__api_request('GET', '/api/v1/timelines/' + timeline, params)

    def timeline_home(self, max_id = None, since_id = None, limit = None):
        """
        Fetch the authenticated users home timeline (i.e. followed users and self).

        Returns a list of toot dicts.
        """
        return self.timeline('home', max_id = max_id, since_id = since_id, limit = limit)

    def timeline_mentions(self, max_id = None, since_id = None, limit = None):
        """
        Fetches the authenticated users mentions.

        Returns a list of toot dicts.
        """
        return self.timeline('mentions', max_id = max_id, since_id = since_id, limit = limit)

    def timeline_public(self, max_id = None, since_id = None, limit = None):
        """
        Fetches the public / visible-network timeline.

        Returns a list of toot dicts.
        """
        return self.timeline('public', max_id = max_id, since_id = since_id, limit = limit)

    def timeline_hashtag(self, hashtag, max_id = None, since_id = None, limit = None):
        """
        Fetch a timeline of toots with a given hashtag.

        Returns a list of toot dicts.
        """
        return self.timeline('tag/' + str(hashtag), max_id = max_id, since_id = since_id, limit = limit)

    ###
    # Reading data: Statuses
    ###
    def status(self, id):
        """
        Fetch information about a single toot.

        Returns a toot dict.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id))

    def status_context(self, id):
        """
        Fetch information about ancestors and descendants of a toot.

        Returns a context dict.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id) + '/context')

    def status_reblogged_by(self, id):
        """
        Fetch a list of users that have reblogged a status.

        Returns a list of user dicts.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id) + '/reblogged_by')

    def status_favourited_by(self, id):
        """
        Fetch a list of users that have favourited a status.

        Returns a list of user dicts.
        """
        return self.__api_request('GET', '/api/v1/statuses/' + str(id) + '/favourited_by')

    ###
    # Reading data: Notifications
    ###
    def notifications(self):
        """
        Fetch notifications (mentions, favourites, reblogs, follows) for the authenticated
        user.

        Returns a list of notification dicts.
        """
        return self.__api_request('GET', '/api/v1/notifications')

    ###
    # Reading data: Accounts
    ###
    def account(self, id):
        """
        Fetch account information by user id.

        Returns a user dict.
        """
        return self.__api_request('GET', '/api/v1/accounts/' + str(id))

    def account_verify_credentials(self):
        """
        Fetch authenticated user's account information.

        Returns a user dict.
        """
        return self.__api_request('GET', '/api/v1/accounts/verify_credentials')

    def account_statuses(self, id, max_id = None, since_id = None, limit = None):
        """
        Fetch statuses by user id. Same options as timeline are permitted.

        Returns a list of toot dicts.
        """
        params = self.__generate_params(locals(), ['id'])
        return self.__api_request('GET', '/api/v1/accounts/' + str(id) + '/statuses', params)

    def account_following(self, id):
        """
        Fetch users the given user is following.

        Returns a list of user dicts.
        """
        return self.__api_request('GET', '/api/v1/accounts/' + str(id) + '/following')

    def account_followers(self, id):
        """
        Fetch users the given user is followed by.

        Returns a list of user dicts.
        """
        return self.__api_request('GET', '/api/v1/accounts/' + str(id) + '/followers')

    def account_relationships(self, id):
        """
        Fetch relationships (following, followed_by, blocking) of the logged in user to
        a given account. id can be a list.

        Returns a list of relationship dicts.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/relationships', params)

    def account_search(self, q, limit = None):
        """
        Fetch matching accounts. Will lookup an account remotely if the search term is
        in the username@domain format and not yet in the database.

        Returns a list of user dicts.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/accounts/search', params)

    ###
    # Writing data: Statuses
    ###
    def status_post(self, status, in_reply_to_id = None, media_ids = None, sensitive = False, visibility = ''):
        """
        Post a status. Can optionally be in reply to another status and contain
        up to four pieces of media (Uploaded via media_post()). media_ids can
        also be the media dicts returned by media_post - they are unpacked
        automatically.

        The 'sensitive' boolean decides whether or not media attached to the post
        should be marked as sensitive, which hides it by default on the Mastodon
        web front-end.

        The visibility parameter is a string value and matches the visibility
        option on the /api/v1/status POST API endpoint. It accepts any of:
        'private' - post will be visible only to followers
        'unlisted' - post will be public but not appear on the public timeline
        'public' - post will be public

        If not passed in, visibility defaults to match the current account's
        privacy setting (private if the account is locked, public otherwise).

        Returns a toot dict with the new status.
        """
        params_initial = locals()

        # Validate visibility parameter
        valid_visibilities = ['private', 'public', 'unlisted', '']
        if params_initial['visibility'].lower() not in valid_visibilities:
            raise ValueError('Invalid visibility value! Acceptable values are %s' % valid_visibilities)

        if media_ids != None:
            try:
                media_ids_proper = []
                for media_id in media_ids:
                    if isinstance(media_id, dict):
                        media_ids_proper.append(media_id["id"])
                    else:
                        media_ids_proper.append(media_id)
            except:
                raise MastodonIllegalArgumentError("Invalid media dict.")

            params_initial["media_ids"] = media_ids_proper

        params = self.__generate_params(params_initial)
        return self.__api_request('POST', '/api/v1/statuses', params)

    def toot(self, status):
        """
        Synonym for status_post that only takes the status text as input.

        Returns a toot dict with the new status.
        """
        return self.status_post(status)

    def status_delete(self, id):
        """
        Delete a status

        Returns an empty dict for good measure.
        """
        return self.__api_request('DELETE', '/api/v1/statuses/' + str(id))

    def status_reblog(self, id):
        """Reblog a status.

        Returns a toot with with a new status that wraps around the reblogged one.
        """
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/reblog")

    def status_unreblog(self, id):
        """
        Un-reblog a status.

        Returns a toot dict with the status that used to be reblogged.
        """
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/unreblog")

    def status_favourite(self, id):
        """
        Favourite a status.

        Returns a toot dict with the favourited status.
        """
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/favourite")

    def status_unfavourite(self, id):
        """Favourite a status.

        Returns a toot dict with the un-favourited status.
        """
        return self.__api_request('POST', '/api/v1/statuses/' + str(id) + "/unfavourite")

    ###
    # Writing data: Accounts
    ###
    def account_follow(self, id):
        """
        Follow a user.

        Returns a relationship dict containing the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/follow")

    def account_unfollow(self, id):
        """
        Unfollow a user.

        Returns a relationship dict containing the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/unfollow")

    def account_block(self, id):
        """
        Block a user.

        Returns a relationship dict containing the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/block")

    def account_unblock(self, id):
        """
        Unblock a user.

        Returns a relationship dict containing the updated relationship to the user.
        """
        return self.__api_request('POST', '/api/v1/accounts/' + str(id) + "/unblock")

    ###
    # Writing data: Media
    ###
    def media_post(self, media_file, mime_type = None):
        """
        Post an image. media_file can either be image data or
        a file name. If image data is passed directly, the mime
        type has to be specified manually, otherwise, it is
        determined from the file name.

        Throws a MastodonIllegalArgumentError if the mime type of the
        passed data or file can not be determined properly.

        Returns a media dict. This contains the id that can be used in
        status_post to attach the media file to a toot.
        """
        if os.path.isfile(media_file) and mime_type == None:
            mime_type = mimetypes.guess_type(media_file)[0]
            media_file = open(media_file, 'rb')

        if mime_type == None:
            raise MastodonIllegalArgumentError('Could not determine mime type or data passed directly without mime type.')

        random_suffix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        file_name = "mastodonpyupload_" + str(time.time()) + "_" + str(random_suffix) + mimetypes.guess_extension(mime_type)

        media_file_description = (file_name, media_file, mime_type)
        return self.__api_request('POST', '/api/v1/media', files = {'file': media_file_description})

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
        if date_time.tzinfo == None:
            date_time_utc = date_time.replace(tzinfo = pytz.utc)
        else:
            date_time_utc = date_time.astimezone(pytz.utc)

        epoch_utc = datetime.datetime.utcfromtimestamp(0).replace(tzinfo = pytz.utc)

        return (date_time_utc - epoch_utc).total_seconds()

    def __api_request(self, method, endpoint, params = {}, files = {}, do_ratelimiting = True):
        """
        Internal API request helper.
        """
        response = None
        headers = None

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
        if self.access_token != None:
            headers = {'Authorization': 'Bearer ' + self.access_token}

        if self.debug_requests == True:
            print('Mastodon: Request to endpoint "' + endpoint + '" using method "' + method + '".')
            print('Parameters: ' + str(params))
            print('Headers: ' + str(headers))
            print('Files: ' + str(files))

        # Make request
        request_complete = False
        while not request_complete:
            request_complete = True

            response_object = None
            try:
                if method == 'GET':
                    response_object = requests.get(self.api_base_url + endpoint, data = params, headers = headers, files = files, timeout = self.request_timeout)

                if method == 'POST':
                    response_object = requests.post(self.api_base_url + endpoint, data = params, headers = headers, files = files, timeout = self.request_timeout)

                if method == 'DELETE':
                    response_object = requests.delete(self.api_base_url + endpoint, data = params, headers = headers, files = files, timeout = self.request_timeout)
            except:
                raise MastodonNetworkError("Could not complete request.")

            if response_object == None:
                raise MastodonIllegalArgumentError("Illegal request.")

            # Handle response
            if self.debug_requests == True:
                print('Mastodon: Response received with code ' + str(response_object.status_code) + '.')
                print('Respose headers: ' + str(response_object.headers))
                print('Response text content: ' + str(response_object.text))

            if response_object.status_code == 404:
                raise MastodonAPIError('Endpoint not found.')

            if response_object.status_code == 500:
                raise MastodonAPIError('General API problem.')

            try:
                response = response_object.json()
            except:
                raise MastodonAPIError("Could not parse response as JSON, respose code was " + str(response_object.status_code))

            # Handle rate limiting
            if 'X-RateLimit-Remaining' in response_object.headers and do_ratelimiting:
                self.ratelimit_remaining = int(response_object.headers['X-RateLimit-Remaining'])
                self.ratelimit_limit = int(response_object.headers['X-RateLimit-Limit'])

                try:
                    ratelimit_reset_datetime = dateutil.parser.parse(response_object.headers['X-RateLimit-Reset'])
                    self.ratelimit_reset = self.__datetime_to_epoch(ratelimit_reset_datetime)

                    # Adjust server time to local clock
                    server_time_datetime = dateutil.parser.parse(response_object.headers['Date'])
                    server_time = self.__datetime_to_epoch(server_time_datetime)
                    server_time_diff = time.time() - server_time
                    self.ratelimit_reset += server_time_diff
                    self.ratelimit_lastcall = time.time()
                except:
                    raise MastodonRatelimitError("Rate limit time calculations failed.")

                if "error" in response and response["error"] == "Throttled":
                    if self.ratelimit_method == "throw":
                        raise MastodonRatelimitError("Hit rate limit.")

                        if self.ratelimit_method == "wait" or self.ratelimit_method == "pace":
                            to_next = self.ratelimit_reset - time.time()
                            if to_next > 0:
                                # As a precaution, never sleep longer than 5 minutes
                                to_next = min(to_next, 5 * 60)
                                time.sleep(to_next)
                                request_complete = False

        return response

    def __generate_params(self, params, exclude = []):
        """
        Internal named-parameters-to-dict helper.

        Note for developers: If called with locals() as params,
        as is the usual practice in this code, the __generate_params call
        (or at least the locals() call) should generally be the first thing
        in your function.
        """
        params = dict(params)

        del params['self']
        param_keys = list(params.keys())
        for key in param_keys:
            if params[key] == None or key in exclude:
                del params[key]

        param_keys = list(params.keys())
        for key in param_keys:
            if isinstance(params[key], list):
                params[key + "[]"] = params[key]
                del params[key]

        return params

##
# Exceptions
##
class MastodonIllegalArgumentError(ValueError):
    pass

class MastodonFileNotFoundError(IOError):
    pass

class MastodonNetworkError(IOError):
    pass

class MastodonAPIError(Exception):
    pass

class MastodonRatelimitError(Exception):
    pass

