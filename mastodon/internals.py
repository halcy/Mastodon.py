# internals.py - many internal helpers

from datetime import timezone, datetime, timedelta
from contextlib import closing
import mimetypes
import threading
import uuid
import dateutil.parser
import time
import copy
import requests
import re
import collections
import base64
import os
import inspect
import warnings

from mastodon.versions import parse_version_string
from mastodon.errors import MastodonNetworkError, MastodonIllegalArgumentError, MastodonRatelimitError, MastodonNotFoundError, \
                    MastodonUnauthorizedError, MastodonInternalServerError, MastodonBadGatewayError, MastodonServiceUnavailableError, \
                    MastodonGatewayTimeoutError, MastodonServerError, MastodonAPIError, MastodonMalformedEventError, MastodonDeprecationWarning
from mastodon.compat import urlparse, magic, PurePath, Path
from mastodon.defaults import _DEFAULT_STREAM_TIMEOUT, _DEFAULT_STREAM_RECONNECT_WAIT_SEC
from mastodon.return_types import AttribAccessDict, PaginatableList, try_cast_recurse
from mastodon.return_types import *

###
# Internal helpers, dragons probably
###
class Mastodon():
    def __datetime_to_epoch(self, date_time: datetime) -> float:
        """
        Converts a python datetime to unix epoch, accounting for
        time zones and such.

        Assumes UTC if timezone is not given.
        """
        if date_time.tzinfo is None:
            date_time = date_time.replace(tzinfo=timezone.utc)
        return date_time.timestamp()

    def __get_logged_in_id(self):
        """
        Fetch the logged in user's ID, with caching. ID is reset on calls to log_in.
        """
        if self.__logged_in_id is None:
            self.__logged_in_id = self.account_verify_credentials().id
        return self.__logged_in_id

    @staticmethod
    def __consistent_isoformat_utc(datetime_val: datetime) -> str:
        """
        Function that does what isoformat does but it actually does the same
        every time instead of randomly doing different things on some systems
        and also it represents that time as the equivalent UTC time.
        """
        isotime = datetime_val.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
        if isotime[-2] != ":":
            isotime = isotime[:-2] + ":" + isotime[-2:]
        return isotime

    def __try_cast_to_type(self, value, override_type = None):
        """
        Tries to cast a value to the type of the function two levels up in the call stack.
        Tries to cast to AttribAccessDict if it doesn't know what to cast to.

        This is used internally inside of __api_request.
        """
        try:
            if override_type is None:
                # Find type of function two frames up
                caller_frame = inspect.currentframe().f_back.f_back
                caller_function = caller_frame.f_code
                caller_func_name = caller_function.co_name
                func_obj = getattr(self, caller_func_name)

                # Very carefully try to find what we need to cast to
                return_type = AttribAccessDict
                if func_obj is not None:
                    return_type = func_obj.__annotations__.get('return', AttribAccessDict)
            else:
                return_type = override_type
        except:
            return_type = AttribAccessDict
        return_val = try_cast_recurse(return_type, value)
        return_type_repr = None
        try:
            return_type_repr = return_val._mastopy_type
        except:
            pass
        return return_val, return_type_repr

    def __api_request(self, method, endpoint, params={}, files={}, headers={}, access_token_override=None, base_url_override=None,
                        do_ratelimiting=True, use_json=False, parse=True, return_response_object=False, skip_error_check=False, lang_override=None, override_type=None,
                        force_pagination=False):
        """
        Internal API request helper.

        Does a large amount of different things that I should document one day, but not today.
        """
        response = None
        final_type = None
        remaining_wait = 0

        # Add language to params if not None
        lang = self.lang
        if lang_override is not None:
            lang = lang_override
        if lang is not None:
            params["lang"] = lang

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
        if self.access_token is not None:
            headers['Authorization'] = 'Bearer ' + self.access_token
        if access_token_override is not None:
            headers['Authorization'] = 'Bearer ' + access_token_override

        # Add user-agent
        if self.user_agent:
            headers['User-Agent'] = self.user_agent

        # Determine base URL
        base_url = self.api_base_url
        if base_url_override is not None:
            base_url = base_url_override

        if self.debug_requests:
            print(f'Mastodon: Request to endpoint "{base_url}{endpoint}" using method "{method}".')
            print(f'Parameters: {params}')
            print(f'Headers: {headers}')
            print(f'Files: {files}')

        # Make request
        request_complete = False
        while not request_complete:
            request_complete = True

            response_object = None
            try:
                kwargs = dict(headers=headers, files=files, timeout=self.request_timeout)
                if use_json:
                    kwargs['json'] = params
                elif method == 'GET':
                    kwargs['params'] = params
                else:
                    kwargs['data'] = params

                # nb: the no-op "auth" parameter is neccesary to ensure requests will never override
                # the Bearer auth header that we add with a HTTP Basic Auth header, which can otherwise
                # happen if the user has a .netrc file with a matching host (including a "default" entry).
                # Passing trust_env = False would also work, but would be worse, since it also disables
                # systemwide proxy settings, which are probably still good to respect, even if the .netrc
                # login behaviour is undesirable in every case.
                response_object = self.session.request(method, base_url + endpoint, **kwargs, auth=lambda x: x)
                if self.debug_requests:
                    print(f'Mastodon: Request URL: {response_object.request.url}')
                    print(f'Mastodon: Request body: {response_object.request.body}')
                    print(f'Mastodon: Response body: {response_object.text}')
            except Exception as e:
                raise MastodonNetworkError(f"Could not complete request: {e}")

            if response_object is None:
                raise MastodonIllegalArgumentError("Illegal request.")

            # Is there a "deprecation" header present?
            if 'deprecation' in response_object.headers:
                warnings.warn("Endpoint " + endpoint + " is marked as deprecated and may be removed in future Mastodon versions.", MastodonDeprecationWarning)

            # Parse rate limiting headers
            if 'X-RateLimit-Remaining' in response_object.headers and do_ratelimiting:
                self.ratelimit_remaining = int(
                    response_object.headers['X-RateLimit-Remaining'])
                self.ratelimit_limit = int(
                    response_object.headers['X-RateLimit-Limit'])

                # For gotosocial, we need an int representation, but for non-ints this would crash
                try:
                    ratelimit_intrep = str(int(response_object.headers['X-RateLimit-Reset']))
                except:
                    ratelimit_intrep = None

                try:
                    if ratelimit_intrep is not None and ratelimit_intrep == response_object.headers['X-RateLimit-Reset']:
                        self.ratelimit_reset = int(
                            response_object.headers['X-RateLimit-Reset'])
                    else:
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
                    raise MastodonRatelimitError(f"Rate limit time calculations failed: {e}")

            # Handle response
            if self.debug_requests:
                print(f'Mastodon: Response received with code {response_object.status_code}.')
                print(f'response headers: {response_object.headers}')
                print(f'Response text content: {response_object.text}')

            if not response_object.ok:
                try:
                    response, final_type = self.__try_cast_to_type(response_object.json(), override_type = override_type) # TODO actually cast to an error type
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

                if not skip_error_check:
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
                    elif response_object.status_code >= 500 and response_object.status_code <= 511:
                        ex_type = MastodonServerError
                    else:
                        ex_type = MastodonAPIError

                    raise ex_type('Mastodon API returned error', response_object.status_code, response_object.reason, error_msg)

            if return_response_object:
                return response_object

            if parse:
                try:
                    # The new parsing is very basic, type conversion happens later,
                    # within the new type system. This should be overall more robust.
                    response = response_object.json()
                except Exception as e:
                    raise MastodonAPIError(
                        f"Could not parse response as JSON, response code was {response_object.status_code}, "
                        f"bad json content was {response_object.content!r}.",
                        f"Exception was: {e}"
                    )
                response, final_type = self.__try_cast_to_type(response, override_type = override_type)
            else:
                response = response_object.content

            # Parse link headers
            if (isinstance(response, list) or force_pagination) and 'Link' in response_object.headers and response_object.headers['Link'] != "":
                if not isinstance(response, PaginatableList) and not force_pagination:
                    response = PaginatableList(response)
                if final_type is None:
                    final_type = str(type(response))
                tmp_urls = requests.utils.parse_header_links(response_object.headers['Link'].rstrip('>').replace('>,<', ',<'))
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
                            next_params['_mastopy_type'] = final_type
                            max_id = matchgroups.group(1)
                            if max_id.isdigit():
                                next_params['max_id'] = int(max_id)
                            else:
                                next_params['max_id'] = max_id
                            if "since_id" in next_params:
                                del next_params['since_id']
                            if "min_id" in next_params:
                                del next_params['min_id']
                            response._pagination_next = next_params

                    if url['rel'] == 'prev':
                        # Be paranoid and extract since_id or min_id specifically
                        prev_url = url['url']

                        # Old and busted (pre-2.6.0): since_id pagination
                        matchgroups = re.search(r"[?&]since_id=([^&]+)", prev_url)
                        if matchgroups:
                            prev_params = copy.deepcopy(params)
                            prev_params['_pagination_method'] = method
                            prev_params['_pagination_endpoint'] = endpoint
                            prev_params['_mastopy_type'] = final_type
                            since_id = matchgroups.group(1)
                            if since_id.isdigit():
                                prev_params['since_id'] = int(since_id)
                            else:
                                prev_params['since_id'] = since_id
                            if "max_id" in prev_params:
                                del prev_params['max_id']
                            response._pagination_prev = prev_params

                        # New and fantastico (post-2.6.0): min_id pagination
                        matchgroups = re.search(r"[?&]min_id=([^&]+)", prev_url)
                        if matchgroups:
                            prev_params = copy.deepcopy(params)
                            prev_params['_pagination_method'] = method
                            prev_params['_pagination_endpoint'] = endpoint
                            prev_params['_mastopy_type'] = final_type
                            min_id = matchgroups.group(1)
                            if min_id.isdigit():
                                prev_params['min_id'] = int(min_id)
                            else:
                                prev_params['min_id'] = min_id
                            if "max_id" in prev_params:
                                del prev_params['max_id']
                            response._pagination_prev = prev_params
        
        return response

    def __get_streaming_base(self) -> str:
        """
        Internal streaming API helper.

        Returns the correct URL for the streaming API.
        """
        if self.__streaming_base is not None:
            return self.__streaming_base
        
        # Try to support implementations that have no v1 endpoint (Sharkey does this)
        streaming_api_url = None
        try:
            instance = self.__instance()
            if  "streaming_api" in instance["urls"]:
                streaming_api_url = instance["urls"]["streaming_api"]
        except:
            try:
                streaming_api_url = self.__instance_v2().configuration.urls.streaming
            except:
                pass

        if not streaming_api_url is None and streaming_api_url != self.api_base_url:
            # This is probably a websockets URL, which is really for the browser, but requests can't handle it
            # So we do this below to turn it into an HTTPS or HTTP URL
            parse = urlparse(instance["urls"]["streaming_api"])
            if parse.scheme == 'wss':
                url = "https://" + parse.netloc
            elif parse.scheme == 'ws':
                url = "http://" + parse.netloc
            else:
                raise MastodonAPIError(
                    f"Could not parse streaming api location returned from server: {instance['urls']['streaming_api']}."
                )
        else:
            url = self.api_base_url
        assert not url is None
        return url

    def __stream(self, endpoint, listener, params={}, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
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
            if self.user_agent:
                headers['User-Agent'] = self.user_agent
            connection = self.session.get(url + endpoint, headers=headers, data=params, stream=True,
                                            timeout=(self.request_timeout, timeout))

            if connection.status_code != 200:
                raise MastodonNetworkError(f"Could not connect to streaming server: {connection.reason}")
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
                if self.connection is not None:
                    self.connection.close()

            def is_alive(self):
                return self._thread.is_alive()

            def is_receiving(self):
                if self.closed or not self.running or self.reconnecting or not self.is_alive():
                    return False
                else:
                    return True

            def _sleep_attentive(self):
                if self._thread != threading.current_thread():
                    raise RuntimeError(
                        "Illegal call from outside the stream_handle thread")
                time_remaining = self.reconnect_async_wait_sec
                while time_remaining > 0 and not self.closed:
                    time.sleep(0.5)
                    time_remaining -= 0.5

            def _threadproc(self):
                self._thread = threading.current_thread()

                # Run until closed or until error if not autoreconnecting
                while self.running:
                    if self.connection is not None:
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
                            if self.closed:
                                # Someone from outside stopped the streaming
                                self.running = False
                                break
                            try:
                                the_connection = self.connect_func()
                                if the_connection.status_code != 200:
                                    exception = MastodonNetworkError(f"Could not connect to server. "
                                                                        f"HTTP status: {the_connection.status_code}")
                                    listener.on_abort(exception)
                                    self._sleep_attentive()
                                if self.closed:
                                    # Here we have maybe a rare race condition. Exactly on connect, someone
                                    # stopped the streaming before. We close the previous established connection:
                                    the_connection.close()
                                else:
                                    self.connection = the_connection
                                    connect_success = True
                            except:
                                self._sleep_attentive()
                                connect_success = False
                        self.reconnecting = False
                    else:
                        self.running = False
                return 0

        if run_async:
            handle = __stream_handle(
                connection, connect_func, reconnect_async, reconnect_async_wait_sec)
            t = threading.Thread(args=(), target=handle._threadproc)
            t.daemon = True
            t.start()
            return handle
        else:
            # Blocking, never returns (can only leave via exception)
            connection = connect_func()
            with closing(connection) as r:
                listener.handle_stream(r)

    def __generate_params(self, params, exclude=[], dateconv=False, for_json=False):
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
            if isinstance(params[key], bool):
                params[key] = '1' if params[key] else '0'

        for key in param_keys:
            if params[key] is None or key in exclude:
                del params[key]

        if not for_json:
            param_keys = list(params.keys())
            for key in param_keys:
                if isinstance(params[key], list):
                    params[key + "[]"] = params[key]
                    del params[key]

        # Unpack min/max/since_id fields, since that is a very common operation
        # and we basically always want it
        for key in param_keys:
            if key in ['min_id', 'max_id', 'since_id']:
                params[key] = self.__unpack_id(params[key], dateconv = dateconv, listify = False)

        return params

    def __unpack_id(self, id, dateconv = False, listify = False, field = "id"):
        """
        Internal object-to-id converter

        Checks if id is a dict that contains id and
        returns the id inside, otherwise just returns
        the id straight.

        Also unpacks datetimes to snowflake IDs if requested.
        """
        if id is None:
            return None
        if not isinstance(id, list) and listify:
            id = [id]
        if isinstance(id, list):
            for i in range(len(id)):
                id[i] = self.__unpack_id(id[i], dateconv = dateconv, listify = False)
            return id
        if isinstance(id, dict) and field in id:
            id = id[field]
        if dateconv and isinstance(id, datetime):
            id = (int(id.timestamp()) << 16) * 1000
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
        return self._token_expired < datetime.now()

    def __set_token_expired(self, value):
        """Internal helper for oauth code"""
        self._token_expired = datetime.now() + timedelta(seconds=value)
        return

    def __get_refresh_token(self):
        """Internal helper for oauth code"""
        return self._refresh_token

    def __set_refresh_token(self, value):
        """Internal helper for oauth code"""
        self._refresh_token = value
        return

    def __guess_type(self, media_file):
        """Internal helper to guess media file type"""
        mime_type = None
        try:
            mime_type = magic.from_file(media_file, mime=True)
        except AttributeError:
            mime_type = mimetypes.guess_type(media_file)[0]
        return mime_type

    def __load_media_file(self, media_file, mime_type=None, file_name=None):
        """Internal helper to load a media file"""
        if isinstance(media_file, PurePath):
            media_file = str(media_file)
        if isinstance(media_file, str):
            try: # Explicitly resolve to canonical for robustness. This can and will fail if Path isn't available because python too old.
                media_file = str(Path(media_file).resolve())
            except:
                pass
        if isinstance(media_file, str) and os.path.isfile(media_file):
            mime_type = self.__guess_type(media_file)
            media_file = open(media_file, 'rb')
        if mime_type is None:
            raise MastodonIllegalArgumentError('Could not determine mime type or data passed directly without mime type.')
        if file_name is None:
            random_suffix = uuid.uuid4().hex
            file_name = f"mastodonpyupload_{time.time()}_{random_suffix}{mimetypes.guess_extension(mime_type)}"
        return (file_name, media_file, mime_type)

    @staticmethod
    def __protocolize(base_url):
        """Internal add-protocol-to-url helper"""
        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            base_url = "https://" + base_url

        # Some API endpoints can't handle extra /'s in path requests
        base_url = base_url.rstrip("/")
        return base_url

    @staticmethod
    def __oauth_url_check(oauth_url, allow_http=False):
        """Internal helper to check and normalize OAuth URLs"""
        if "?" in oauth_url:
            # Throw an error, we do not support OAuth URLs with query parameters, even if this is in theory a
            # valid thing to have for most endpoints.
            raise MastodonIllegalArgumentError("OAuth URLs with query parameters are not supported by Mastodon.py.")
        
        if "#" in oauth_url:
            # A fragment is just straight up not allowed by the spec.
            raise MastodonIllegalArgumentError("OAuth URLs with fragments are not permitted.")
        
        if "@" in oauth_url:
            # Username/password is RIGHT OUT.
            raise MastodonIllegalArgumentError("OAuth URLs with username/password are not permitted.")

        # OAuth URLs *must* include the scheme, and the scheme *must* be https.
        # We allow http if a flag is set because testing requires it.
        if not oauth_url.startswith("https://"):
            if allow_http:
                if not oauth_url.startswith("http://"):
                    raise MastodonIllegalArgumentError("OAuth URLs must use with http or https.")
            else:
                raise MastodonIllegalArgumentError("OAuth URLs must use with https.")

    @staticmethod
    def __deprotocolize(base_url):
        """Internal helper to strip http and https from a URL"""
        if base_url.startswith("http://"):
            base_url = base_url[7:]
        elif base_url.startswith("https://") or base_url.startswith("onion://"):
            base_url = base_url[8:]
        return base_url

    def __normalize_version_string(self, version_string):
        # Split off everything after the first space, to take care of Pleromalikes so that the parser doesn't get confused in case those have a + somewhere in their version
        version_string = version_string.split(" ")[0]
        try:
            # Attempt to split at + and check if the part after parses as a version string, to account for hometown
            ver_parts = parse_version_string(version_string.split("+")[1])
            # If the parsed version is less than 1.0, assume it's GoToSocial and return the *first* part
            if ver_parts[0] < 1:
                return version_string.split("+")[0]
            return version_string.split("+")[1]
        except:
            # If this fails, assume that if there is a +, what is before that is the masto version (or that there is no +)
            return version_string.split("+")[0]
