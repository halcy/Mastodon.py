from .versions import _DICT_VERSION_INSTANCE, _DICT_VERSION_ACTIVITY
from .error import MastodonIllegalArgumentError, MastodonNotFoundError
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
