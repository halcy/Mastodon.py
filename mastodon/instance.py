# instance.py - instance-level endpoints, directory, emoji, announcements
from mastodon.errors import MastodonDeprecationWarning, MastodonIllegalArgumentError, MastodonNotFoundError
from mastodon.utility import api_version
from mastodon.compat import urlparse

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Instance, InstanceV2, NonPaginatableList, Activity, Nodeinfo, AttribAccessDict, Rule, Announcement, CustomEmoji, Account, IdType, ExtendedDescription, DomainBlock, SupportedLocale, TermsOfService

from typing import Union, Optional, Dict, List

import datetime
import warnings

class Mastodon(Internals):
    ###
    # Reading data: Instances
    ###
    @api_version("1.1.0", "2.3.0")
    def instance_v1(self) -> Instance:
        """
        Retrieve basic information about the instance, including the URI and administrative contact email.

        Does not require authentication unless locked down by the administrator.

        This is the explicit v1 version of this function. The v2 version is available through instance_v2().
        It contains a bit more information than this one, but does not include whether invites are enabled.
        """
        instance = self.__api_request('GET', '/api/v1/instance/', override_type=Instance)
        return instance

    def __instance(self) -> Instance:
        """
        Internal, non-version-checking helper that does the same as instance_v1()

        Silences the deprecation warnning, we are careful about fallbacks anywhere this is used.
        If you are using this, this is your notice to do that.
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=MastodonDeprecationWarning)
            instance = self.__api_request('GET', '/api/v1/instance/', override_type=Instance)
        return instance

    @api_version("4.0.0", "4.0.0")
    def instance_v2(self) -> InstanceV2:
        """
        Retrieve basic information about the instance, including the URI and administrative contact email.

        Does not require authentication unless locked down by the administrator. This is the explicit v2 variant.
        """
        return self.__api_request('GET', '/api/v2/instance/')

    def __instance_v2(self) -> InstanceV2:
        """
        Internal, non-version-checking helper that does the same as instance_v2()
        """
        instance = self.__api_request('GET', '/api/v2/instance/', override_type=InstanceV2)
        return instance

    @api_version("1.1.0", "4.0.0")
    def instance(self) -> Union[InstanceV2, Instance]:
        """
        Retrieve basic information about the instance, including the URI and administrative contact email.

        Does not require authentication unless locked down by the administrator.

        Will return the latest available version of the instance information. If you want a specific one,
        call the _v1 or _v2 variants
        """
        if self.verify_minimum_version("4.0.0", cached=True):
            return self.instance_v2()
        else:
            return self.instance_v1()

    @api_version("2.1.2", "2.1.2")
    def instance_activity(self) -> NonPaginatableList[Activity]:
        """
        Retrieve activity stats about the instance. May be disabled by the instance administrator - throws
        a MastodonNotFoundError in that case.

        Activity is returned for 12 weeks going back from the current week.
        """
        return self.__api_request('GET', '/api/v1/instance/activity')

    @api_version("2.1.2", "2.1.2")
    def instance_peers(self) -> NonPaginatableList[str]:
        """
        Retrieve the instances that this instance knows about. May be disabled by the instance administrator - throws
        a MastodonNotFoundError in that case.

        Returns a list of URL strings.
        """
        return self.__api_request('GET', '/api/v1/instance/peers')

    @api_version("3.0.0", "3.0.0")
    def instance_health(self) -> bool:
        """
        Basic health check. Returns True if healthy, False if not.
        """
        status = self.__api_request('GET', '/health', parse=False).decode("utf-8")
        return status in ["OK", "success"]

    @api_version("3.0.0", "3.0.0")
    def instance_nodeinfo(self, schema: str = "http://nodeinfo.diaspora.software/ns/schema/2.0") -> Nodeinfo:
        """
        Retrieves the instance's nodeinfo information.

        For information on what the nodeinfo can contain, see the nodeinfo
        specification: https://github.com/jhass/nodeinfo . By default,
        Mastodon.py will try to retrieve the version 2.0 schema nodeinfo, for which
        we have a well defined return object. If you go outside of that, all bets
        are off.

        To override the schema, specify the desired schema with the `schema`
        parameter.
        """
        links = self.__api_request('GET', '/.well-known/nodeinfo', override_type = AttribAccessDict)["links"]

        schema_url = None
        for available_schema in links:
            if available_schema.rel == schema:
                schema_url = available_schema.href

        if schema_url is None:
            raise MastodonIllegalArgumentError("Requested nodeinfo schema is not available.")

        try:
            return self.__api_request('GET', schema_url, base_url_override="")
        except MastodonNotFoundError:
            parse = urlparse(schema_url)
            return self.__api_request('GET', parse.path + parse.params + parse.query + parse.fragment)

    @api_version("3.4.0", "3.4.0")
    def instance_rules(self) -> NonPaginatableList[Rule]:
        """
        Retrieve instance rules.
        """
        return self.__api_request('GET', '/api/v1/instance/rules')

    @api_version("4.4.0", "4.4.0")
    def instance_terms_of_service(self, date: Optional[datetime.date] = None) -> TermsOfService:
        """
        Retrieve the instance's terms of service.

        If `date` is specified, it will return the terms of service that were put in effect on that date.

        NB: This is not (currently?) a range lookup, you can only get the terms of service for a specific, exact date.
        """
        if date is not None and not isinstance(date, datetime.date):
            raise MastodonIllegalArgumentError("Date parameter should be a datetime.date object")
        if date is not None:
            date = date.strftime("%Y-%m-%d")
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/instance/terms_of_service', params)

    ###
    # Reading data: Directory
    ###
    @api_version("3.0.0", "3.0.0")
    def directory(self, offset: Optional[int] = None, limit: Optional[int] = None, 
                  order: Optional[str] = None, local: Optional[bool] = None) -> NonPaginatableList[Account]:
        """
        Fetch the contents of the profile directory, if enabled on the server.

        `offset` how many accounts to skip before returning results. Default 0.

        `limit` how many accounts to load. Default 40.

        `order` "active" to sort by most recently posted statuses (usually the default) or
                "new" to sort by most recently created profiles.

        `local` True to return only local accounts.

        Uses offset/limit pagination, not currently handled by the pagination utility functions,
        do it manually if you have to.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/directory', params)

    ###
    # Reading data: Emoji
    ###
    @api_version("2.1.0", "2.1.0")
    def custom_emojis(self) -> NonPaginatableList[CustomEmoji]:
        """
        Fetch the list of custom emoji the instance has installed.

        Does not require authentication unless locked down by the administrator.
        """
        return self.__api_request('GET', '/api/v1/custom_emojis')

    ##
    # Reading data: Announcements
    ##
    @api_version("3.1.0", "3.1.0")
    def announcements(self) -> NonPaginatableList[Announcement]:
        """
        Fetch currently active announcements.
        """
        return self.__api_request('GET', '/api/v1/announcements')

    ###
    # Writing data: Annoucements
    ###
    @api_version("3.1.0", "3.1.0")
    def announcement_dismiss(self, id: Union[Announcement, IdType]):
        """
        Set the given annoucement to read.
        """
        id = self.__unpack_id(id)
        self.__api_request('POST', f'/api/v1/announcements/{id}/dismiss')

    @api_version("3.1.0", "3.1.0")
    def announcement_reaction_create(self, id: Union[Announcement, IdType], reaction: str):
        """
        Add a reaction to an announcement. `reaction` can either be a unicode emoji
        or the name of one of the instances custom emoji.

        Will throw an API error if the reaction name is not one of the allowed things
        or when trying to add a reaction that the user has already added (adding a
        reaction that a different user added is legal and increments the count).
        """
        id = self.__unpack_id(id)
        self.__api_request('PUT', f'/api/v1/announcements/{id}/reactions/{reaction}')

    @api_version("3.1.0", "3.1.0")
    def announcement_reaction_delete(self, id: Union[Announcement, IdType], reaction: str):
        """
        Remove a reaction to an announcement.

        Will throw an API error if the reaction does not exist.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/announcements/{id}/reactions/{reaction}')

    @api_version("4.0.0", "4.0.0")
    def instance_extended_description(self) -> ExtendedDescription:
        """
        Retrieve the instance's extended description.
        """
        return self.__api_request('GET', '/api/v1/instance/extended_description')

    def instance_translation_languages(self) -> Dict[str, List[str]]:
        """
        Retrieve the instance's translation languages.

        Returns a dict with language pairs, where the key is the language code and the value is a list of language codes that the instance can translate that language to.
        """
        ret_value = self.__api_request('GET', '/api/v1/instance/translation_languages')
        result_real = AttribAccessDict()
        for key, value in ret_value.items():
            result_real[key] = NonPaginatableList(value)
        return result_real
        
    @api_version("4.0.0", "4.0.0")
    def instance_domain_blocks(self) -> NonPaginatableList[DomainBlock]:
        """
        Fetch a list of domains that have been blocked by the instance. Public endpoint, requires authentication if limited to users.

        Returns a MastodonAPIError if the admin has chosen to not make the list public, or to now show it at all.
        """
        return self.__api_request('GET', '/api/v1/instance/domain_blocks')

    @api_version("4.2.0", "4.2.0")
    def instance_languages(self) -> NonPaginatableList[SupportedLocale]:
        """
        Fetch a list of languages that the instance supports.
        """
        return self.__api_request('GET', '/api/v1/instance/languages')
    