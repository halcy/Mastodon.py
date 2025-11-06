# coding: utf-8

import json
import base64
import os
import os.path
import time
import datetime
import collections
from contextlib import closing
import requests
from requests.models import urlencode
import dateutil
import dateutil.parser
import re
import copy


from mastodon.compat import IMPL_HAS_CRYPTO, IMPL_HAS_ECE, IMPL_HAS_BLURHASH
from mastodon.compat import cryptography, default_backend, ec, serialization
from mastodon.compat import http_ece
from mastodon.compat import blurhash
from mastodon.compat import urlparse

from mastodon.utility import parse_version_string, max_version, api_version
from mastodon.utility import Mastodon as MastoUtility

from mastodon.return_types import *
from mastodon.errors import *

from mastodon.defaults import _DEFAULT_TIMEOUT, _DEFAULT_SCOPES, _DEFAULT_STREAM_TIMEOUT, _DEFAULT_STREAM_RECONNECT_WAIT_SEC
from mastodon.defaults import _SCOPE_SETS

from mastodon.internals import Mastodon as Internals
from mastodon.authentication import Mastodon as MastoAuthentication
from mastodon.accounts import Mastodon as MastoAccounts
from mastodon.instance import Mastodon as MastoInstance
from mastodon.timeline import Mastodon as MastoTimeline
from mastodon.statuses import Mastodon as MastoStatuses
from mastodon.media import Mastodon as MastoMedia
from mastodon.polls import Mastodon as MastoPolls
from mastodon.notifications import Mastodon as MastoNotifications
from mastodon.conversations import Mastodon as MastoConversations
from mastodon.hashtags import Mastodon as MastoHashtags
from mastodon.filters import Mastodon as MastoFilters
from mastodon.suggestions import Mastodon as MastoSuggestions
from mastodon.endorsements import Mastodon as MastoEndorsements
from mastodon.relationships import Mastodon as MastoRelationships
from mastodon.lists import Mastodon as MastoLists
from mastodon.trends import Mastodon as MastoTrends
from mastodon.search import Mastodon as MastoSearch
from mastodon.favourites import Mastodon as MastoFavourites
from mastodon.reports import Mastodon as MastoReports
from mastodon.preferences import Mastodon as MastoPreferences
from mastodon.push import Mastodon as MastoPush
from mastodon.admin import Mastodon as MastoAdmin
from mastodon.streaming_endpoints import Mastodon as MastoStreaming


###
# The actual Mastodon class
#
# Almost all code is now imported from smaller files to make editing a bit more pleasant
###
class Mastodon(MastoUtility, MastoAuthentication, MastoAccounts, MastoInstance, MastoTimeline, MastoStatuses, MastoPolls, MastoNotifications, MastoHashtags,
                MastoFilters, MastoSuggestions, MastoEndorsements, MastoRelationships, MastoLists, MastoTrends, MastoSearch, MastoFavourites, MastoReports,
                MastoPreferences, MastoPush, MastoAdmin, MastoConversations, MastoMedia, MastoStreaming):
    """
    Thorough and easy to use Mastodon
    API wrapper in Python.

    Main class, imports most things from modules
    """
    # Support level
    __SUPPORTED_MASTODON_VERSION = "4.4.3"
    __MASTODON_PY_VERSION = "2.1.4"
    
    @staticmethod
    def get_supported_version() -> str:
        """
        Retrieve the maximum version of Mastodon supported by this version of Mastodon.py
        """
        return Mastodon.__SUPPORTED_MASTODON_VERSION
