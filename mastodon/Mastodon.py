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


from .compat import IMPL_HAS_CRYPTO, IMPL_HAS_ECE, IMPL_HAS_BLURHASH
from .compat import cryptography, default_backend, ec, serialization
from .compat import http_ece
from .compat import blurhash
from .compat import urlparse

from .utility import parse_version_string, max_version, api_version
from .utility import AttribAccessDict, AttribAccessDict
from .utility import Mastodon as Utility

from .errors import *
from .versions import _DICT_VERSION_APPLICATION, _DICT_VERSION_MENTION, _DICT_VERSION_MEDIA, _DICT_VERSION_ACCOUNT, _DICT_VERSION_POLL, \
                        _DICT_VERSION_STATUS, _DICT_VERSION_INSTANCE, _DICT_VERSION_HASHTAG, _DICT_VERSION_EMOJI, _DICT_VERSION_RELATIONSHIP, \
                        _DICT_VERSION_NOTIFICATION, _DICT_VERSION_CONTEXT, _DICT_VERSION_LIST, _DICT_VERSION_CARD, _DICT_VERSION_SEARCHRESULT, \
                        _DICT_VERSION_ACTIVITY, _DICT_VERSION_REPORT, _DICT_VERSION_PUSH, _DICT_VERSION_PUSH_NOTIF, _DICT_VERSION_FILTER, \
                        _DICT_VERSION_CONVERSATION, _DICT_VERSION_SCHEDULED_STATUS, _DICT_VERSION_PREFERENCES, _DICT_VERSION_ADMIN_ACCOUNT, \
                        _DICT_VERSION_FEATURED_TAG, _DICT_VERSION_MARKER, _DICT_VERSION_REACTION, _DICT_VERSION_ANNOUNCEMENT, _DICT_VERSION_STATUS_EDIT, \
                        _DICT_VERSION_FAMILIAR_FOLLOWERS, _DICT_VERSION_ADMIN_DOMAIN_BLOCK, _DICT_VERSION_ADMIN_MEASURE, _DICT_VERSION_ADMIN_DIMENSION, \
                        _DICT_VERSION_ADMIN_RETENTION

from .defaults import _DEFAULT_TIMEOUT, _DEFAULT_SCOPES, _DEFAULT_STREAM_TIMEOUT, _DEFAULT_STREAM_RECONNECT_WAIT_SEC
from .defaults import _SCOPE_SETS

from .internals import Mastodon as Internals
from .authentication import Mastodon as Authentication
from .accounts import Mastodon as Accounts
from .instance import Mastodon as Instance
from .timeline import Mastodon as Timeline
from .statuses import Mastodon as Statuses
from .media import Mastodon as Media
from .polls import Mastodon as Polls
from .notifications import Mastodon as Notifications
from .conversations import Mastodon as Conversations
from .hashtags import Mastodon as Hashtags
from .filters import Mastodon as Filters
from .suggestions import Mastodon as Suggestions
from .endorsements import Mastodon as Endorsements
from .relationships import Mastodon as Relationships
from .lists import Mastodon as Lists
from .trends import Mastodon as Trends
from .search import Mastodon as Search
from .favourites import Mastodon as Favourites
from .reports import Mastodon as Reports
from .preferences import Mastodon as Preferences
from .push import Mastodon as Push
from .admin import Mastodon as Admin
from .streaming_endpoints import Mastodon as Streaming


###
# The actual Mastodon class
#
# Almost all code is now imported from smaller files to make editing a bit more pleasant
###
class Mastodon(Utility, Authentication, Accounts, Instance, Timeline, Statuses, Polls, Notifications, Hashtags,
                Filters, Suggestions, Endorsements, Relationships, Lists, Trends, Search, Favourites, Reports,
                Preferences, Push, Admin, Conversations, Media, Streaming):
    """
    Thorough and easy to use Mastodon
    API wrapper in Python.

    Main class, imports most things from modules
    """
    # Support level
    __SUPPORTED_MASTODON_VERSION = "3.5.5"

    @staticmethod
    def get_supported_version():
        """
        Retrieve the maximum version of Mastodon supported by this version of Mastodon.py
        """
        return Mastodon.__SUPPORTED_MASTODON_VERSION
