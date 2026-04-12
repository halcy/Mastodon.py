# async_refresh.py - async refresh endpoints and utilities

import time
import copy

from mastodon.utility import api_version
from mastodon.errors import MastodonIllegalArgumentError, MastodonAPIError
from mastodon.internals import Mastodon as Internals
from mastodon.return_types import AsyncRefresh
from mastodon.types_base import AttribAccessDict, IdType, try_cast_recurse
from typing import Optional, Union, Tuple

class Mastodon(Internals):
    ###
    # Reading data: Async refreshes
    ###
    def get_async_refresh_info(self, result) -> Optional[Tuple[AsyncRefresh, int]]:
        """
        Extract async refresh information from an API result, if present.

        Returns a tuple of (:class:`AsyncRefresh`, retry_seconds) where the entity
        contains the ``id``, ``status`` (always ``"running"``), and optionally
        ``result_count``, and retry_seconds is the server-suggested polling
        interval in seconds.

        Returns None if the result has no async refresh information.
        """
        raw = getattr(result, '_async_refresh', None)
        if raw is not None:
            entity = try_cast_recurse(AsyncRefresh, {
                'id': raw['id'],
                'status': 'running',
                'result_count': raw.get('result_count'),
            })
            return (entity, raw.get('retry', 3))
        return None

    @api_version("4.4.0", "4.4.0")
    def get_async_refresh_status(self, result_or_id: Union[IdType, AsyncRefresh, AttribAccessDict]) -> AsyncRefresh:
        """
        Get the status of an async refresh by its ID. The ID can be obtained from
        a previous API response that included the ``Mastodon-Async-Refresh`` header,
        accessible via :meth:`get_async_refresh_info`.

        You can pass in an async refresh ID, an :class:`AsyncRefresh` entity (e.g. from 
        a previous call to this function or from :meth:`get_async_refresh_info`), or 
        an API result that has async refresh information (i.e. a previous API 
        result that had the header set).

        Returns an :class:`AsyncRefresh` dict.
        """
        async_refresh_id = self.__get_async_refresh_id(result_or_id)
        response = self.__api_request('GET', f'/api/v1_alpha/async_refreshes/{async_refresh_id}', override_type=dict)
        if isinstance(response, dict) and 'async_refresh' in response:
            response = response['async_refresh']
        return try_cast_recurse(AsyncRefresh, response)

    @api_version("4.4.0", "4.4.0")
    def await_async_refresh(self, result, timeout: float = 0.0, max_attempts: int = -1) -> Optional[AttribAccessDict]:
        """
        Wait for an async refresh to finish, then re-fetch and return the 
        original resource.

        Polls the async refresh endpoint with backoff as indicated by the 
        server's ``retry`` hint. Once the refresh is ``finished``, re-issues 
        the original API request and returns the refreshed result entity.

        `result` should be a previous API result that has async refresh
        information (i.e. the server returned a ``Mastodon-Async-Refresh`` header
        with that response). If no such information is present, or the refresh
        info indicates the refresh is already finished, this function will
        return the original result as is immediately.

        `timeout` is the maximum total time in seconds to wait for the async refresh 
        to complete. Set to 0 for no timeout. Default is 0 (wait until done).

        `max_attempts` is the maximum number of polling attempts. Set to 0 or 
        negative for no limit. Default is -1 (wait until done).

        Returns the re-fetched original entity on success, or None if the 
        timeout or max attempts was exceeded before the refresh finished.

        Raises `MastodonIllegalArgumentError` if the passed object has async refresh 
        information but is missing the original request information needed to re-fetch.
        Raises `MastodonAPIError` if any of the API requests made during the process 
        fail with an error response.
        """
        async_refresh_info = getattr(result, '_async_refresh', None)
        if async_refresh_info is None:
            if not isinstance(result, (AttribAccessDict, list)):
                raise MastodonIllegalArgumentError("await_async_refresh expects an API result entity.")
            # no async refresh info -> just return right away
            return result
        else:
            # if we do have it, make sure it has the original request information we need to re-fetch later
            if '_method' not in async_refresh_info:
                raise MastodonIllegalArgumentError("The provided result's async refresh information is missing the original request information.")
        
        # already done -> just return right away
        if async_refresh_info.get('status') == 'finished':
            return result
            
        async_refresh_id = async_refresh_info['id']
        retry_seconds = async_refresh_info.get('retry', 3)

        start_time = time.monotonic()
        attempts = 0
        refresh_result = None

        while attempts < max_attempts or max_attempts <= 0:
            if timeout > 0 and (time.monotonic() - start_time) >= timeout:
                break
            
            if attempts > 0:
                wait = min(retry_seconds, timeout - (time.monotonic() - start_time)) if timeout > 0 else retry_seconds
                
                # Make sure wait is maximum 5 minutes to avoid hangs in case server is being silly
                wait = min(wait, 300)
                
                if wait > 0:
                    time.sleep(wait)

            refresh_result = self.get_async_refresh_status(async_refresh_id)
            attempts += 1

            if refresh_result.status == 'finished':
                # Re-fetch the original endpoint
                method = async_refresh_info['_method']
                endpoint = async_refresh_info['_endpoint']
                params = copy.deepcopy(async_refresh_info.get('_params', {}))
                response_type = async_refresh_info.get('_mastopy_type', None)
                return self.__api_request(method, endpoint, params, override_type=response_type)

            # Use retry hint from the polled response's header if available
            polled_raw = getattr(refresh_result, '_async_refresh', None)
            if polled_raw is not None:
                retry_seconds = polled_raw.get('retry', retry_seconds)

        return None

    def __get_async_refresh_id(self, result_or_id):
        """
        Internal helper: extract async refresh ID from an ID value or a result object.
        """
        if isinstance(result_or_id, (str, int)):
            return result_or_id
        if isinstance(result_or_id, AsyncRefresh):
            return result_or_id['id']
        raw = getattr(result_or_id, '_async_refresh', None)
        if raw is not None:
            return raw['id']
        raise MastodonIllegalArgumentError("Pass either an async refresh ID, an AsyncRefresh entity, or an API result with async refresh information.")
