# instance.py - instance-level endpoints, directory, emoji, announcements

from .versions import _DICT_VERSION_INSTANCE, _DICT_VERSION_ACTIVITY, _DICT_VERSION_ACCOUNT, _DICT_VERSION_EMOJI, _DICT_VERSION_ANNOUNCEMENT
from .errors import MastodonIllegalArgumentError, MastodonNotFoundError
from .utility import api_version
from .compat import urlparse

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Instances
    ###
    @api_version("1.1.0", "2.3.0", _DICT_VERSION_INSTANCE)
    def instance(self):
        """
        Retrieve basic information about the instance, including the URI and administrative contact email.

        Does not require authentication unless locked down by the administrator.

        Returns an :ref:`instance dict <instance dict>`.
        """
        return self.__instance()

    def __instance(self):
        """
        Internal, non-version-checking helper that does the same as instance()
        """
        instance = self.__api_request('GET', '/api/v1/instance/')
        return instance

    @api_version("2.1.2", "2.1.2", _DICT_VERSION_ACTIVITY)
    def instance_activity(self):
        """
        Retrieve activity stats about the instance. May be disabled by the instance administrator - throws
        a MastodonNotFoundError in that case.

        Activity is returned for 12 weeks going back from the current week.

        Returns a list of :ref:`activity dicts <activity dicts>`.
        """
        return self.__api_request('GET', '/api/v1/instance/activity')

    @api_version("2.1.2", "2.1.2", "2.1.2")
    def instance_peers(self):
        """
        Retrieve the instances that this instance knows about. May be disabled by the instance administrator - throws
        a MastodonNotFoundError in that case.

        Returns a list of URL strings.
        """
        return self.__api_request('GET', '/api/v1/instance/peers')

    @api_version("3.0.0", "3.0.0", "3.0.0")
    def instance_health(self):
        """
        Basic health check. Returns True if healthy, False if not.
        """
        status = self.__api_request('GET', '/health', parse=False).decode("utf-8")
        return status in ["OK", "success"]

    @api_version("3.0.0", "3.0.0", "3.0.0")
    def instance_nodeinfo(self, schema="http://nodeinfo.diaspora.software/ns/schema/2.0"):
        """
        Retrieves the instance's nodeinfo information.

        For information on what the nodeinfo can contain, see the nodeinfo
        specification: https://github.com/jhass/nodeinfo . By default,
        Mastodon.py will try to retrieve the version 2.0 schema nodeinfo.

        To override the schema, specify the desired schema with the `schema`
        parameter.
        """
        links = self.__api_request('GET', '/.well-known/nodeinfo')["links"]

        schema_url = None
        for available_schema in links:
            if available_schema.rel == schema:
                schema_url = available_schema.href

        if schema_url is None:
            raise MastodonIllegalArgumentError(
                "Requested nodeinfo schema is not available.")

        try:
            return self.__api_request('GET', schema_url, base_url_override="")
        except MastodonNotFoundError:
            parse = urlparse(schema_url)
            return self.__api_request('GET', parse.path + parse.params + parse.query + parse.fragment)

    @api_version("3.4.0", "3.4.0", _DICT_VERSION_INSTANCE)
    def instance_rules(self):
        """
        Retrieve instance rules.

        Returns a list of `id` + `text` dicts, same as the `rules` field in the :ref:`instance dicts <instance dicts>`.
        """
        return self.__api_request('GET', '/api/v1/instance/rules')

    ###
    # Reading data: Directory
    ###
    @api_version("3.0.0", "3.0.0", _DICT_VERSION_ACCOUNT)
    def directory(self, offset=None, limit=None, order=None, local=None):
        """
        Fetch the contents of the profile directory, if enabled on the server.

        `offset` how many accounts to skip before returning results. Default 0.

        `limit` how many accounts to load. Default 40.

        `order` "active" to sort by most recently posted statuses (default) or
                "new" to sort by most recently created profiles.

        `local` True to return only local accounts.

        Returns a list of :ref:`account dicts <account dicts>`.

        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/directory', params)

    ###
    # Reading data: Emoji
    ###
    @api_version("2.1.0", "2.1.0", _DICT_VERSION_EMOJI)
    def custom_emojis(self):
        """
        Fetch the list of custom emoji the instance has installed.

        Does not require authentication unless locked down by the administrator.

        Returns a list of :ref:`emoji dicts <emoji dicts>`.
        """
        return self.__api_request('GET', '/api/v1/custom_emojis')

    ##
    # Reading data: Announcements
    ##
    @api_version("3.1.0", "3.1.0", _DICT_VERSION_ANNOUNCEMENT)
    def announcements(self):
        """
        Fetch currently active announcements.

        Returns a list of :ref:`announcement dicts <announcement dicts>`.
        """
        return self.__api_request('GET', '/api/v1/announcements')

    ###
    # Writing data: Annoucements
    ###
    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_dismiss(self, id):
        """
        Set the given annoucement to read.
        """
        id = self.__unpack_id(id)

        self.__api_request('POST', f'/api/v1/announcements/{id}/dismiss')

    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_reaction_create(self, id, reaction):
        """
        Add a reaction to an announcement. `reaction` can either be a unicode emoji
        or the name of one of the instances custom emoji.

        Will throw an API error if the reaction name is not one of the allowed things
        or when trying to add a reaction that the user has already added (adding a
        reaction that a different user added is legal and increments the count).
        """
        id = self.__unpack_id(id)

        self.__api_request('PUT', f'/api/v1/announcements/{id}/reactions/{reaction}')

    @api_version("3.1.0", "3.1.0", "3.1.0")
    def announcement_reaction_delete(self, id, reaction):
        """
        Remove a reaction to an announcement.

        Will throw an API error if the reaction does not exist.
        """
        id = self.__unpack_id(id)

        self.__api_request('DELETE', f'/api/v1/announcements/{id}/reactions/{reaction}')
