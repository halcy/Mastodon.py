#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import datetime
from contextlib import closing

import pytz
import dateutil
import requests

from mastodon.exceptions import *


"""Internal helpers, dragons probably"""

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
    next_url = None

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
    if self.access_token is not None:
        headers = {'Authorization': 'Bearer ' + self.access_token}

    if self.debug_requests is True:
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
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise MastodonNetworkError("Could not complete request: %s" % e)

        if response_object == None:
            raise MastodonIllegalArgumentError("Illegal request.")

        # Handle response
        if self.debug_requests == True:
            print('Mastodon: Response received with code ' + str(response_object.status_code) + '.')
            print('response headers: ' + str(response_object.headers))
            #print('Response text content: ' + str(response_object.text))

        if response_object.status_code == 404:
            raise MastodonAPIError('Endpoint not found.')

        if response_object.status_code == 500:
            raise MastodonAPIError('General API problem.')

        try:
            response = response_object.json()
        except:
            import traceback
            traceback.print_exc()
            raise MastodonAPIError("Could not parse response as JSON, response code was %s, bad json content was '%s'" % (response_object.status_code, response_object.content))

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
            except Exception as e:
                import traceback
                traceback.print_exc()
                raise MastodonRatelimitError("Rate limit time calculations failed: %s" % e)

            if "error" in response and response["error"] == "Throttled":
                if self.ratelimit_method == "throw":
                    raise MastodonRatelimitError("Hit rate limit.")

                if self.ratelimit_method == "wait" or self.ratelimit_method == "pace":
                    to_next = self.ratelimit_reset - time.time()
                    if to_next > 0:
                        # As a precaution, never sleep longer than 5 minutes
                        request_complete = False
                        to_next = min(to_next, 5 * 60)
                        time.sleep(to_next)

    return response

def __stream(self, endpoint, listener, params = {}):
    """
    Internal streaming API helper.
    """

    headers = {}
    if self.access_token != None:
        headers = {'Authorization': 'Bearer ' + self.access_token}

    url = self.api_base_url + endpoint
    with closing(requests.get(url, headers = headers, data = params, stream = True)) as r:
        listener.handle_stream(r.iter_lines())


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
