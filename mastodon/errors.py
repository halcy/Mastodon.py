# error.py - error classes

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
    """Raised when the Mastodon API returns a 404 Not Found error"""
    pass


class MastodonUnauthorizedError(MastodonAPIError):
    """Raised when the Mastodon API returns a 401 Unauthorized error

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

# Warnings
class MastodonWarning(Warning):
    """Base class for Mastodon.py warnings"""
    pass


class MastodonDeprecationWarning(MastodonWarning):
    """Raised when a deprecated feature is used"""
    pass