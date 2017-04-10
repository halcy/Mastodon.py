#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Exceptions"""

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
