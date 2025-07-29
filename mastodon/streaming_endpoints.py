    # relationships.py - endpoints for user and domain blocks and mutes as well as follow requests

from mastodon.errors import MastodonIllegalArgumentError
from mastodon.defaults import _DEFAULT_STREAM_TIMEOUT, _DEFAULT_STREAM_RECONNECT_WAIT_SEC
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Streaming
    ###
    @api_version("1.1.0", "1.4.2")
    def stream_user(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams events that are relevant to the authorized user, i.e. home
        timeline and notifications.
        """
        return self.__stream('/api/v1/streaming/user', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2")
    def stream_public(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC, local=False, remote=False):
        """
        Streams public events.

        Set `local` to True to only get local statuses.
        Set `remote` to True to only get remote statuses.
        """
        base = '/api/v1/streaming/public'
        if local:
            base += '/local'
        if remote:
            if local:
                raise MastodonIllegalArgumentError("Cannot pass both local and remote - use either one or the other.")
            base += '/remote'
        return self.__stream(base, listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("1.1.0", "1.4.2")
    def stream_local(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams local public events.

        This function is deprecated. Please use stream_public() with parameter `local` set to True instead.
        """
        #return self.__stream('/api/v1/streaming/public/local', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)
        return self.stream_public(listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec, local=True)

    @api_version("1.1.0", "1.4.2")
    def stream_hashtag(self, tag, listener, local=False, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Stream for all public statuses for the hashtag 'tag' seen by the connected
        instance.

        Set `local` to True to only get local statuses.
        """
        if tag.startswith("#"):
            raise MastodonIllegalArgumentError("Tag parameter should omit leading #")
        base = '/api/v1/streaming/hashtag'
        if local:
            base += '/local'
        return self.__stream(f"{base}?tag={tag}", listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("2.1.0", "2.1.0")
    def stream_list(self, id, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Stream events for the current user, restricted to accounts on the given
        list.
        """
        id = self.__unpack_id(id)
        return self.__stream(f"/api/v1/streaming/list?list={id}", listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("2.6.0", "2.6.0")
    def stream_direct(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Streams direct message events for the logged-in user, as conversation events.
        """
        return self.__stream('/api/v1/streaming/direct', listener, run_async=run_async, timeout=timeout, reconnect_async=reconnect_async, reconnect_async_wait_sec=reconnect_async_wait_sec)

    @api_version("2.5.0", "2.5.0")
    def stream_healthy(self) -> bool:
        """
        Returns True if streaming API is okay, False or raises an error otherwise.
        """
        api_okay = self.__api_request('GET', '/api/v1/streaming/health', base_url_override=self.__get_streaming_base(), parse=False)
        if api_okay in [b'OK', b'success']:
            return True
        return False
