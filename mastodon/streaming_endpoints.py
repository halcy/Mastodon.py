# streaming_endpoints.py - endpoints for getting streaming data using SSE or WebSockets

import warnings

from mastodon.errors import MastodonIllegalArgumentError, MastodonWarning
from mastodon.defaults import _DEFAULT_STREAM_TIMEOUT, _DEFAULT_STREAM_RECONNECT_WAIT_SEC
from mastodon.streaming_websocket import WebSocketStreamHandle
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals


class Mastodon(Internals):
    def __stream_or_subscribe(self, endpoint, stream, listener, stream_params=None, websocket_handle=None,
                              run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False,
                              reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        if websocket_handle is None:
            return self.__stream(
                endpoint, listener, run_async=run_async, timeout=timeout,
                reconnect_async=reconnect_async,
                reconnect_async_wait_sec=reconnect_async_wait_sec
            )
        if not isinstance(websocket_handle, WebSocketStreamHandle):
            raise MastodonIllegalArgumentError("websocket_handle must be a WebSocket stream handle.")
        return websocket_handle.subscribe(stream, listener=listener, **(stream_params or {}))

    ###
    # Streaming
    ###
    @api_version("1.1.0", "1.4.2")
    def stream_user(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False,
                    reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC, websocket_handle=None):
        """
        Streams events that are relevant to the authorized user, i.e. home
        timeline and notifications.
        """
        return self.__stream_or_subscribe(
            '/api/v1/streaming/user', 'user', listener, websocket_handle=websocket_handle,
            run_async=run_async, timeout=timeout, reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec
        )

    @api_version("1.4.2", "1.4.2")
    def stream_user_notifications(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT,
                                  reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC,
                                  websocket_handle=None):
        """Streams notifications for the authorized user."""
        return self.__stream_or_subscribe(
            '/api/v1/streaming/user/notification', 'user:notification', listener,
            websocket_handle=websocket_handle, run_async=run_async, timeout=timeout,
            reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec
        )

    @api_version("1.1.0", "1.4.2")
    def stream_public(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False,
                      reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC, local=False, remote=False,
                      only_media=False, websocket_handle=None):
        """
        Streams public events.

        Set `local` to True to only get local statuses.
        Set `remote` to True to only get remote statuses.
        Set `only_media` to True to only get statuses with media attachments.
        """
        if not self.timeline_is_available("public", local=local, remote=remote, with_auth=self.access_token is not None, fail_hard=False):
            warnings.warn(
                "Public stream appears to be unavailable on this instance for the current auth context.",
                MastodonWarning
            )

        base = '/api/v1/streaming/public'
        if local:
            base += '/local'
        if remote:
            if local:
                raise MastodonIllegalArgumentError("Cannot pass both local and remote - use either one or the other.")
            base += '/remote'
        stream = 'public'
        if local:
            stream += ':local'
        elif remote:
            stream += ':remote'
        if only_media:
            stream += ':media'
            base += '?only_media=true'
        return self.__stream_or_subscribe(
            base, stream, listener, websocket_handle=websocket_handle, run_async=run_async,
            timeout=timeout, reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec
        )

    @api_version("1.1.0", "1.4.2")
    def stream_local(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False,
                     reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC, only_media=False,
                     websocket_handle=None):
        """
        Streams local public events.

        This function is deprecated. Please use stream_public() with parameter `local` set to True instead.
        """
        return self.stream_public(
            listener, run_async=run_async, timeout=timeout,
            reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec,
            local=True, only_media=only_media, websocket_handle=websocket_handle
        )

    @api_version("1.1.0", "1.4.2")
    def stream_hashtag(self, tag, listener, local=False, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT,
                       reconnect_async=False, reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC,
                       websocket_handle=None):
        """
        Stream for all public statuses for the hashtag 'tag' seen by the connected
        instance.

        Set `local` to True to only get local statuses.
        """
        if tag.startswith("#"):
            raise MastodonIllegalArgumentError("Tag parameter should omit leading #")

        if not self.timeline_is_available("hashtag", local=local, with_auth=self.access_token is not None, fail_hard=False):
            warnings.warn(
                "Hashtag stream appears to be unavailable on this instance for the current auth context.",
                MastodonWarning
            )

        base = '/api/v1/streaming/hashtag'
        stream = 'hashtag'
        if local:
            base += '/local'
            stream += ':local'
        return self.__stream_or_subscribe(
            f"{base}?tag={tag}", stream, listener,
            stream_params={"tag": tag}, websocket_handle=websocket_handle,
            run_async=run_async, timeout=timeout, reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec
        )

    @api_version("2.1.0", "2.1.0")
    def stream_list(self, id, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False,
                    reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC, websocket_handle=None):
        """
        Stream events for the current user, restricted to accounts on the given
        list.
        """
        id = self.__unpack_id(id)
        return self.__stream_or_subscribe(
            f"/api/v1/streaming/list?list={id}", 'list', listener,
            stream_params={"list": id}, websocket_handle=websocket_handle,
            run_async=run_async, timeout=timeout, reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec
        )

    @api_version("2.6.0", "2.6.0")
    def stream_direct(self, listener, run_async=False, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False,
                      reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC, websocket_handle=None):
        """
        Streams direct message events for the logged-in user, as conversation events.
        """
        return self.__stream_or_subscribe(
            '/api/v1/streaming/direct', 'direct', listener,
            websocket_handle=websocket_handle, run_async=run_async, timeout=timeout,
            reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec
        )

    def stream_open_websocket(self, listener=None, timeout=_DEFAULT_STREAM_TIMEOUT, reconnect_async=False,
                         reconnect_async_wait_sec=_DEFAULT_STREAM_RECONNECT_WAIT_SEC):
        """
        Open an authenticated WebSocket streaming connection without subscribing
        to any streams. The returned handle supports multiplexed subscriptions.
        """
        return self.__open_websocket_stream(
            listener=listener, timeout=timeout,
            reconnect_async=reconnect_async,
            reconnect_async_wait_sec=reconnect_async_wait_sec
        )

    @api_version("2.5.0", "2.5.0")
    def stream_healthy(self) -> bool:
        """
        Returns True if streaming API is okay, False or raises an error otherwise.
        """
        api_okay = self.__api_request('GET', '/api/v1/streaming/health', base_url_override=self.__get_streaming_base(), parse=False)
        if api_okay in [b'OK', b'success']:
            return True
        return False
