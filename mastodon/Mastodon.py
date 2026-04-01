# coding: utf-8




from mastodon.utility import Mastodon as MastoUtility

from mastodon.return_types import *
from mastodon.errors import *


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
