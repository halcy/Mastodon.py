# admin.py - admin / moderation endpoints

from mastodon.errors import MastodonIllegalArgumentError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from typing import Optional, List, Union
from mastodon.return_types import IdType, PrimitiveIdType, Account, AdminAccount, AdminReport, PaginatableList, NonPaginatableList, Status, Tag,\
                PreviewCard, AdminDomainBlock, AdminMeasure, AdminDimension, AdminRetention, AdminCanonicalEmailBlock, AdminDomainAllow, AdminEmailDomainBlock, AdminIpBlock
from datetime import datetime

class Mastodon(Internals):
    ###
    # Moderation API
    ###
    @api_version("2.9.1", "4.0.0")
    def admin_accounts_v2(self, origin: Optional[str] = None, by_domain: Optional[str] = None, status: Optional[str] = None, username: Optional[str] = None, 
                          display_name: Optional[str] = None, email: Optional[str] = None, ip: Optional[str] = None, permissions: Optional[str] = None, 
                          invited_by: Union[Account, IdType] = None, role_ids: Optional[List[IdType]] = None, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None, 
                          since_id: Optional[IdType] = None, limit: Optional[int] = None) -> List[AdminAccount]:
        """
        Fetches a list of accounts that match given criteria. By default, local accounts are returned.

        * Set `origin` to "local" or "remote" to get only local or remote accounts.
        * Set `by_domain` to a domain to get only accounts from that domain.
        * Set `status` to one of "active", "pending", "disabled", "silenced" or "suspended" to get only accounts with that moderation status (default: active)
        * Set `username` to a string to get only accounts whose username contains this string.
        * Set `display_name` to a string to get only accounts whose display name contains this string.
        * Set `email` to an email to get only accounts with that email (this only works on local accounts).
        * Set `ip` to an ip (as a string, standard v4/v6 notation) to get only accounts whose last active ip is that ip (this only works on local accounts).
        * Set `permissions` to "staff" to only get accounts with staff permissions.
        * Set `invited_by` to an account id to get only accounts invited by this user.
        * Set `role_ids` to a list of role IDs to get only accounts with those roles.

        Pagination on this is a bit weird, so I would recommend not doing that and instead manually fetching.
        """
        if role_ids is not None:
            if not isinstance(role_ids, list):
                role_ids = [role_ids]
            role_ids = [self.__unpack_id(x) for x in role_ids]

        if invited_by is not None:
            invited_by = self.__unpack_id(invited_by)

        if permissions is not None and not permissions in ["staff"]:
            raise MastodonIllegalArgumentError("Permissions must be staff if passed")

        if origin is not None and not origin in ["local", "remote"]:
            raise MastodonIllegalArgumentError("Origin must be local or remote")

        if status is not None and not status in ["active", "pending", "disabled", "silenced", "suspended"]:
            raise MastodonIllegalArgumentError("Status must be local or active, pending, disabled, silenced or suspended")

        if not by_domain is None:
            by_domain = self.__deprotocolize(by_domain)

        params = self.__generate_params(locals(), dateconv=True)
        return self.__api_request('GET', '/api/v2/admin/accounts', params)

    @api_version("2.9.1", "2.9.1")
    def admin_accounts(self, remote: bool = False, by_domain: Optional[str] = None, status: str = 'active', username: Optional[str] = None, 
                       display_name: Optional[str] = None, email: Optional[str] = None, ip: Optional[str] = None, staff_only: bool = False, 
                       max_id: Optional[IdType] = None, min_id: Optional[IdType] = None, since_id: Optional[IdType] = None, 
                       limit: Optional[int] = None):
        """
        Currently a synonym for admin_accounts_v1, now deprecated. You are strongly encouraged to use admin_accounts_v2 instead, since this one is kind of bad.

        !!!!! This function may be switched to calling the v2 API in the future. This is your warning. If you want to keep using v1, use it explicitly. !!!!!

        Pagination on this is a bit weird, so I would recommend not doing that and instead manually fetching.
        """
        return self.admin_accounts_v1(
            remote=remote,
            by_domain=by_domain,
            status=status,
            username=username,
            display_name=display_name,
            email=email,
            ip=ip,
            staff_only=staff_only,
            max_id=max_id,
            min_id=min_id,
            since_id=since_id
        )

    @api_version("2.9.1", "2.9.1")
    def admin_accounts_v1(self, remote: bool = False, by_domain: Optional[str] = None, status: str = 'active', username: Optional[str] = None, 
                          display_name: Optional[str] = None, email: Optional[str] = None, ip: Optional[str] = None, staff_only: bool = False, 
                          max_id: Optional[IdType] = None, min_id: Optional[IdType] = None, since_id: Optional[IdType] = None, 
                          limit: Optional[int] = None) -> AdminAccount:
        """
        Fetches a list of accounts that match given criteria. By default, local accounts are returned.

        * Set `remote` to True to get remote accounts, otherwise local accounts are returned (default: local accounts)
        * Set `by_domain` to a domain to get only accounts from that domain.
        * Set `status` to one of "active", "pending", "disabled", "silenced" or "suspended" to get only accounts with that moderation status (default: active)
        * Set `username` to a string to get only accounts whose username contains this string.
        * Set `display_name` to a string to get only accounts whose display name contains this string.
        * Set `email` to an email to get only accounts with that email (this only works on local accounts).
        * Set `ip` to an ip (as a string, standard v4/v6 notation) to get only accounts whose last active ip is that ip (this only works on local accounts).
        * Set `staff_only` to True to only get staff accounts (this only works on local accounts).

        Note that setting the boolean parameters to False does not mean "give me users to which this does not apply" but
        instead means "I do not care if users have this attribute".

        Deprecated in Mastodon version 3.5.0.

        Pagination on this is a bit weird, so I would recommend not doing that and instead manually fetching.
        """
        params = self.__generate_params(locals(), ['remote', 'status', 'staff_only'], dateconv=True)

        if remote:
            params["remote"] = True

        mod_statuses = ["active", "pending", "disabled", "silenced", "suspended"]
        if not status in mod_statuses:
            raise ValueError("Invalid moderation status requested.")

        if staff_only:
            params["staff"] = True

        for mod_status in mod_statuses:
            if status == mod_status:
                params[status] = True

        if not by_domain is None:
            by_domain = self.__deprotocolize(by_domain)

        return self.__api_request('GET', '/api/v1/admin/accounts', params)

    @api_version("2.9.1", "2.9.1")
    def admin_account(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Fetches a single admin account for the user with the given id.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/accounts/{id}')

    @api_version("2.9.1", "2.9.1")
    def admin_account_enable(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Reenables login for a local account for which login has been disabled.

        The returned object reflects the updates to the account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/enable')

    @api_version("2.9.1", "2.9.1")
    def admin_account_approve(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Approves a pending account.

        The returned object reflects the updates to the account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/approve')

    @api_version("2.9.1", "2.9.1")
    def admin_account_reject(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Rejects and deletes a pending account.

        The returned object is that of the now-deleted account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/reject')

    @api_version("2.9.1", "2.9.1")
    def admin_account_unsilence(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Unsilences an account.

        The returned object reflects the updates to the account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/unsilence')

    @api_version("2.9.1", "2.9.1")
    def admin_account_unsuspend(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Unsuspends an account.

        The returned object reflects the updates to the account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/unsuspend')

    @api_version("3.3.0", "3.3.0")
    def admin_account_delete(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Delete a local user account.

        The returned object reflects the updates to the account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('DELETE', f'/api/v1/admin/accounts/{id}')

    @api_version("3.3.0", "3.3.0")
    def admin_account_unsensitive(self, id: Union[Account, AdminAccount, IdType]) -> AdminAccount:
        """
        Unmark an account as force-sensitive.

        The returned object reflects the updates to the account.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/unsensitive')

    @api_version("2.9.1", "2.9.1")
    def admin_account_moderate(self, id: Union[Account, AdminAccount, IdType], action: Optional[str] = None, report_id: Optional[Union[AdminReport, PrimitiveIdType]] = None, 
                               warning_preset_id: Optional[PrimitiveIdType] = None, text: Optional[str] = None, send_email_notification: Optional[bool] = True):
        """
        Perform a moderation action on an account.

        Valid actions are:
            * "disable" - for a local user, disable login.
            * "silence" - hide the users posts from all public timelines.
            * "suspend" - irreversibly delete all the user's posts, past and future.
            * "sensitive" - forcce an accounts media visibility to always be sensitive.

        If no action is specified, the user is only issued a warning.

        Specify the id of a report as `report_id` to close the report with this moderation action as the resolution.
        Specify `warning_preset_id` to use a warning preset as the notification text to the user, or `text` to specify text directly.
        If both are specified, they are concatenated (preset first). Note that there is currently no API to retrieve or create
        warning presets.

        Set `send_email_notification` to False to not send the user an email notification informing them of the moderation action.
        """
        if action is None:
            action = "none"

        if not send_email_notification:
            send_email_notification = None

        id = self.__unpack_id(id)
        if report_id is not None:
            report_id = self.__unpack_id(report_id)

        params = self.__generate_params(locals(), ['id', 'action'])

        params["type"] = action

        self.__api_request('POST', f'/api/v1/admin/accounts/{id}/action', params)

    @api_version("2.9.1", "2.9.1")
    def admin_reports(self, resolved: Optional[bool] = False, account_id: Optional[Union[Account, AdminAccount, IdType]] = None, 
                      target_account_id: Optional[Union[Account, AdminAccount, IdType]] = None, max_id: Optional[IdType] = None, 
                      min_id: Optional[IdType] = None, since_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[AdminReport]:
        """
        Fetches the list of reports.

        Set `resolved` to True to search for resolved reports. `account_id` and `target_account_id`
        can be used to get reports filed by or about a specific user.
        """
        if account_id is not None:
            account_id = self.__unpack_id(account_id)

        if target_account_id is not None:
            target_account_id = self.__unpack_id(target_account_id)

        if not resolved:
            resolved = None

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/reports', params)

    @api_version("2.9.1", "2.9.1")
    def admin_report(self, id: Union[AdminReport, IdType]) -> AdminReport:
        """
        Fetches the report with the given id.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/reports/{id}')

    @api_version("2.9.1", "2.9.1")
    def admin_report_assign(self, id: Union[AdminReport, IdType]) -> AdminReport:
        """
        Assigns the given report to the logged-in user.

        The returned object reflects the updates to the report.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/assign_to_self')

    @api_version("2.9.1", "2.9.1")
    def admin_report_unassign(self, id: Union[AdminReport, IdType]) -> AdminReport:
        """
        Unassigns the given report from the logged-in user.

        The returned object reflects the updates to the report.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/unassign')

    @api_version("2.9.1", "2.9.1")
    def admin_report_reopen(self, id: Union[AdminReport, IdType]) -> AdminReport:
        """
        Reopens a closed report.

        The returned object reflects the updates to the report.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/reopen')

    @api_version("2.9.1", "2.9.1")
    def admin_report_resolve(self, id: Union[AdminReport, IdType]) -> AdminReport:
        """
        Marks a report as resolved (without taking any action).

        The returned object reflects the updates to the report.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/resolve')

    @api_version("3.5.0", "3.5.0")
    def admin_trending_tags(self, limit: Optional[int] = None) -> NonPaginatableList[Tag]:
        """
        Admin version of :ref:`trending_tags() <trending_tags()>`. Includes unapproved tags.

        The returned list is sorted, descending, by the instance's trending algorithm.

        Returns a regular Tag without admin attributes between Mastodon.py v4.0.0 and v4.1.0 due to a bug.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/tags', params)

    @api_version("3.5.0", "3.5.0")
    def admin_trending_statuses(self) -> NonPaginatableList[Status]:
        """
        Admin version of :ref:`trending_statuses() <trending_statuses()>`. Includes unapproved tags.

        The returned list is sorted, descending, by the instance's trending algorithm.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/statuses', params)

    @api_version("3.5.0", "3.5.0")
    def admin_trending_links(self) -> NonPaginatableList[PreviewCard]:
        """
        Admin version of :ref:`trending_links() <trending_links()>`. Includes unapproved tags.

        The returned list is sorted, descending, by the instance's trending algorithm.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/links', params)

    @api_version("4.0.0", "4.0.0")
    def admin_domain_blocks(self, id: Optional[IdType] = None, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None, 
                            since_id: Optional[IdType] = None, limit: Optional[int] = None) -> Union[AdminDomainBlock, PaginatableList[AdminDomainBlock]]:
        """
        Fetches a list of blocked domains. Requires scope `admin:read:domain_blocks`.

        Provide an `id` to fetch a specific domain block based on its database id.

        Raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is not None:
            id = self.__unpack_id(id)
            return self.__api_request('GET', f'/api/v1/admin/domain_blocks/{id}')
        else:
            params = self.__generate_params(locals(), ['limit'])
            return self.__api_request('GET', '/api/v1/admin/domain_blocks/', params)

    @api_version("4.0.0", "4.0.0")
    def admin_create_domain_block(self, domain: str, severity: Optional[str] = None, reject_media: Optional[bool] = None, 
                                  reject_reports: Optional[bool] = None, private_comment: Optional[str] = None, 
                                  public_comment: Optional[str] = None, obfuscate: Optional[bool] = None) -> AdminDomainBlock:
        """
        Perform a moderation action on a domain. Requires scope `admin:write:domain_blocks`.

        Valid severities are:
            * "silence" - hide all posts from federated timelines and do not show notifications to local users from the remote instance's users unless they are following the remote user.
            * "suspend" - deny interactions with this instance going forward. This action is reversible.
            * "limit" - generally used with reject_media=true to force reject media from an instance without silencing or suspending..

        If no action is specified, the domain is only silenced.
        `domain` is the domain to block. Note that using the top level domain will also imapct all subdomains. ie, example.com will also impact subdomain.example.com.
        `reject_media` will not download remote media on to your local instance media storage.
        `reject_reports` ignores all reports from the remote instance.
        `private_comment` sets a private admin comment for the domain.
        `public_comment` sets a publicly available comment for this domain, which will be available to local users and may be available to everyone depending on your settings.
        `obfuscate` censors some part of the domain name. Useful if the domain name contains unwanted words like slurs.
        """
        if domain is None:
            raise MastodonIllegalArgumentError("Must provide a domain to block a domain")
        if domain.startswith("http://") or domain.startswith("https://"):
            raise MastodonIllegalArgumentError("Domain should not contain a protocol identifier.")
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/admin/domain_blocks/', params)

    @api_version("4.0.0", "4.0.0")
    def admin_update_domain_block(self, id, severity: Optional[str] = None, reject_media: Optional[bool] = None, reject_reports: Optional[bool] = None, 
                                  private_comment: Optional[str] = None, public_comment: Optional[str] = None, obfuscate: Optional[bool] = None) -> AdminDomainBlock:
        """
        Modify existing moderation action on a domain. Requires scope `admin:write:domain_blocks`.

        Valid severities are:
            * "silence" - hide all posts from federated timelines and do not show notifications to local users from the remote instance's users unless they are following the remote user.
            * "suspend" - deny interactions with this instance going forward. This action is reversible.
            * "limit" - generally used with reject_media=true to force reject media from an instance without silencing or suspending.

        If no action is specified, the domain is only silenced.
        `domain` is the domain to block. Note that using the top level domain will also imapct all subdomains. ie, example.com will also impact subdomain.example.com.
        `reject_media` will not download remote media on to your local instance media storage.
        `reject_reports` ignores all reports from the remote instance.
        `private_comment` sets a private admin comment for the domain.
        `public_comment` sets a publicly available comment for this domain, which will be available to local users and may be available to everyone depending on your settings.
        `obfuscate` censors some part of the domain name. Useful if the domain name contains unwanted words like slurs.

        Raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is None:
            raise MastodonIllegalArgumentError("Must provide an id to modify the existing moderation actions on a given domain.")
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])
        return self.__api_request('PUT', f'/api/v1/admin/domain_blocks/{id}', params)

    @api_version("4.0.0", "4.0.0")
    def admin_delete_domain_block(self, id = Union[AdminDomainBlock, IdType]):
        """
        Removes moderation action against a given domain. Requires scope `admin:write:domain_blocks`.

        Provide an `id` to remove a specific domain block based on its database id.

        Raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is not None:
            id = self.__unpack_id(id)
            self.__api_request('DELETE', f'/api/v1/admin/domain_blocks/{id}')
        else:
            raise MastodonIllegalArgumentError("You must provide an id of an existing domain block to remove it.")

    @api_version("3.5.0", "3.5.0")
    def admin_measures(self, start_at, end_at, active_users: bool = False, new_users: bool = False, interactions: bool = False, opened_reports: bool = False, resolved_reports: bool = False, 
                       tag_accounts: Optional[Union[Tag, IdType]] = None, tag_uses: Optional[Union[Tag, IdType]] = None, tag_servers: Optional[Union[Tag, IdType]] = None, 
                       instance_accounts: Optional[str] = None, instance_media_attachments: Optional[str] = None, instance_reports: Optional[str] = None,
                        instance_statuses: Optional[str] = None, instance_follows: Optional[str] = None, instance_followers: Optional[str] = None) -> NonPaginatableList[AdminMeasure]:
        """
        Retrieves numerical instance information for the time period (at day granularity) between `start_at` and `end_at`.

            * `active_users`: Pass true to retrieve the number of active users on your instance within the time period
            * `new_users`: Pass true to retrieve the number of users who joined your instance within the time period
            * `interactions`: Pass true to retrieve the number of interactions (favourites, boosts, replies) on local statuses within the time period
            * `opened_reports`: Pass true to retrieve the number of reports filed within the time period
            * `resolved_reports` = Pass true to retrieve the number of reports resolved within the time period
            * `tag_accounts`: Pass a tag ID to get the number of accounts which used that tag in at least one status within the time period
            * `tag_uses`: Pass a tag ID to get the number of statuses which used that tag within the time period
            * `tag_servers`: Pass a tag ID to to get the number of remote origin servers for statuses which used that tag within the time period
            * `instance_accounts`: Pass a domain to get the number of accounts originating from that remote domain within the time period
            * `instance_media_attachments`: Pass a domain to get the amount of space used by media attachments from that remote domain within the time period
            * `instance_reports`: Pass a domain to get the number of reports filed against accounts from that remote domain within the time period
            * `instance_statuses`: Pass a domain to get the number of statuses originating from that remote domain within the time period
            * `instance_follows`: Pass a domain to get the number of accounts from a remote domain followed by that local user within the time period
            * `instance_followers`: Pass a domain to get the number of local accounts followed by accounts from that remote domain within the time period

        This API call is relatively expensive - watch your servers load if you want to get a lot of statistical data. Especially the instance_statuses stats
        might take a long time to compute and, in fact, time out.

        There is currently no way to get tag IDs implemented in Mastodon.py, because the Mastodon public API does not implement one. This will be fixed in a future
        release.
        """
        params_init = locals()
        keys = []
        for key in ["active_users", "new_users", "interactions", "opened_reports", "resolved_reports"]:
            if params_init[key] == True:
                keys.append(key)

        params = {}
        for key in ["tag_accounts", "tag_uses", "tag_servers"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"id": self.__unpack_id(params_init[key])}
        for key in ["instance_accounts", "instance_media_attachments", "instance_reports", "instance_statuses", "instance_follows", "instance_followers"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"domain": Mastodon.__deprotocolize(params_init[key]).split("/")[0]}

        if len(keys) == 0:
            raise MastodonIllegalArgumentError("Must request at least one metric.")

        params["keys"] = keys
        params["start_at"] = self.__consistent_isoformat_utc(start_at)
        params["end_at"] = self.__consistent_isoformat_utc(end_at)

        return self.__api_request('POST', '/api/v1/admin/measures', params, use_json=True)

    @api_version("3.5.0", "3.5.0")
    def admin_dimensions(self, start_at: datetime, end_at: datetime, limit: Optional[int] = None, languages: bool = False, sources: bool = False, 
                         servers: bool = False, space_usage: bool = False, software_versions: bool = False, tag_servers: Optional[Union[Tag, IdType]] = None, 
                         tag_languages: Optional[Union[Tag, IdType]] = None, instance_accounts: Optional[str] = None, instance_languages: Optional[str] = None) -> NonPaginatableList[AdminDimension]:
        """
        Retrieves primarily categorical instance information for the time period (at day granularity) between `start_at` and `end_at`.

            * `languages`: Pass true to get the most-used languages on this server
            * `sources`: Pass true to get the most-used client apps on this server
            * `servers`: Pass true to get the remote servers with the most statuses
            * `space_usage`: Pass true to get the how much space is used by different components your software stack
            * `software_versions`: Pass true to get the version numbers for your software stack
            * `tag_servers`: Pass a tag ID to get the most-common servers for statuses including a trending tag
            * `tag_languages`: Pass a tag ID to get the most-used languages for statuses including a trending tag
            * `instance_accounts`: Pass a domain to get the most-followed accounts from a remote server
            * `instance_languages`: Pass a domain to get the most-used languages from a remote server

        Pass `limit` to set how many results you want on queries where that makes sense.

        This API call is relatively expensive - watch your servers load if you want to get a lot of statistical data.

        There is currently no way to get tag IDs implemented in Mastodon.py, because the Mastodon public API does not implement one. This will be fixed in a future
        release.
        """
        params_init = locals()
        keys = []
        for key in ["languages", "sources", "servers", "space_usage", "software_versions"]:
            if params_init[key] == True:
                keys.append(key)

        params = {}
        for key in ["tag_servers", "tag_languages"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"id": self.__unpack_id(params_init[key])}
        for key in ["instance_accounts", "instance_languages"]:
            if params_init[key] is not None:
                keys.append(key)
                params[key] = {"domain": Mastodon.__deprotocolize(params_init[key]).split("/")[0]}

        if len(keys) == 0:
            raise MastodonIllegalArgumentError("Must request at least one dimension.")

        params["keys"] = keys
        if limit is not None:
            params["limit"] = limit
        params["start_at"] = self.__consistent_isoformat_utc(start_at)
        params["end_at"] = self.__consistent_isoformat_utc(end_at)

        return self.__api_request('POST', '/api/v1/admin/dimensions', params, use_json=True)

    @api_version("3.5.0", "3.5.0")
    def admin_retention(self, start_at: datetime, end_at: datetime, frequency: str = "day") -> NonPaginatableList[AdminRetention]:
        """
        Gets user retention statistics (at `frequency` - "day" or "month" - granularity) between `start_at` and `end_at`.
        """
        if not frequency in ["day", "month"]:
            raise MastodonIllegalArgumentError("Frequency must be day or month")

        params = {
            "start_at": self.__consistent_isoformat_utc(start_at),
            "end_at": self.__consistent_isoformat_utc(end_at),
            "frequency": frequency
        }
        return self.__api_request('POST', '/api/v1/admin/retention', params)

    @api_version("4.0.0", "4.0.0")
    def admin_canonical_email_blocks(self, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None, 
                                     since_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[AdminCanonicalEmailBlock]:
        """
        Fetches a list of canonical email blocks. Requires scope `admin:read:canonical_email_blocks`.

        The returned list may be paginated using max_id, min_id, and since_id.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/canonical_email_blocks', params)

    @api_version("4.0.0", "4.0.0")
    def admin_canonical_email_block(self, id: IdType) -> AdminCanonicalEmailBlock:
        """
        Fetch a single canonical email block by ID. Requires scope `admin:read:canonical_email_blocks`.
        
        Raises `MastodonAPIError` if the email block does not exist.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/canonical_email_blocks/{id}')

    @api_version("4.0.0", "4.0.0")
    def admin_test_canonical_email_block(self, email: str) -> NonPaginatableList[AdminCanonicalEmailBlock]:
        """
        Canonicalize and hash an email address, returning all matching canonical email blocks. Requires scope `admin:read:canonical_email_blocks`.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/admin/canonical_email_blocks/test', params)

    @api_version("4.0.0", "4.0.0")
    def admin_create_canonical_email_block(self, email: Optional[str] = None, canonical_email_hash: Optional[str] = None) -> AdminCanonicalEmailBlock:
        """
        Block a canonical email. Requires scope `admin:write:canonical_email_blocks`.

        Either `email` (which will be canonicalized and hashed) or `canonical_email_hash` must be provided.

        Up do date details about the canonicalization and hashing process can be found here:
        
            https://github.com/mastodon/mastodon/blob/main/app/helpers/email_helper.rb

        As of Mastodon v4.4.0:
            * Everything lowercased
            * Dots are removed from the part before the @
            * Anything after a + is removed
            * The hash in use is SHA256
        """
        if email is None and canonical_email_hash is None:
            raise MastodonIllegalArgumentError("Either 'email' or 'canonical_email_hash' must be provided.")
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/admin/canonical_email_blocks', params)

    @api_version("4.0.0", "4.0.0")
    def admin_delete_canonical_email_block(self, id: IdType) -> AdminCanonicalEmailBlock:
        """
        Delete a canonical email block by ID. Requires scope `admin:write:canonical_email_blocks`.
        
        Raises `MastodonAPIError` if the email block does not exist.
        """
        id = self.__unpack_id(id)
        return self.__api_request('DELETE', f'/api/v1/admin/canonical_email_blocks/{id}')

    @api_version("4.0.0", "4.0.0")
    def admin_domain_allows(self, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None,
                            since_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[AdminDomainAllow]:
        """
        Fetches a list of allowed domains. Requires scope `admin:read:domain_allows`.
        
        The returned list may be paginated using max_id, min_id, and since_id.

        NB: Untested, since I don't have a Mastodon instance in allowlist mode to test this with.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/domain_allows', params)

    @api_version("4.0.0", "4.0.0")
    def admin_domain_allow(self, id: Union[AdminDomainAllow, IdType]) -> AdminDomainAllow:
        """
        Fetch a single allowed domain by ID. Requires scope `admin:read:domain_allows`.
        
        Raises `MastodonAPIError` if the domain allow does not exist.

        NB: Untested, since I don't have a Mastodon instance in allowlist mode to test this with.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/domain_allows/{id}')

    @api_version("4.0.0", "4.0.0")
    def admin_create_domain_allow(self, domain: str) -> AdminDomainAllow:
        """
        Allow a domain for federation. Requires scope `admin:write:domain_allows`.
        
        If the domain is already allowed, returns the existing record.

        NB: Untested, since I don't have a Mastodon instance in allowlist mode to test this with.
        """
        params = {"domain": domain}
        return self.__api_request('POST', '/api/v1/admin/domain_allows', params)

    @api_version("4.0.0", "4.0.0")
    def admin_delete_domain_allow(self, id: Union[AdminDomainAllow, IdType]):
        """
        Remove a domain from the allowlist. Requires scope `admin:write:domain_allows`.
        
        Raises `MastodonAPIError` if the domain allow does not exist.

        NB: Untested, since I don't have a Mastodon instance in allowlist mode to test this with.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/admin/domain_allows/{id}')

    @api_version("4.0.0", "4.0.0")
    def admin_email_domain_blocks(self, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None,
                                  since_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[AdminEmailDomainBlock]:
        """
        Fetches a list of blocked email domains. Requires scope `admin:read:email_domain_blocks`.
        
        The returned list may be paginated using max_id, min_id, and since_id.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/email_domain_blocks', params)

    @api_version("4.1.0", "4.1.0")
    def admin_email_domain_block(self, id: IdType) -> AdminEmailDomainBlock:
        """
        Fetch a single blocked email domain by ID. Requires scope `admin:read:email_domain_blocks`.
        
        Raises `MastodonAPIError` if the email domain block does not exist.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/email_domain_blocks/{id}')

    @api_version("4.0.0", "4.0.0")
    def admin_create_email_domain_block(self, domain: str) -> AdminEmailDomainBlock:
        """
        Block an email domain from signups. Requires scope `admin:write:email_domain_blocks`.
        
        If the domain contains invalid characters, a `MastodonAPIError` will be raised.
        """
        params = {"domain": domain}
        return self.__api_request('POST', '/api/v1/admin/email_domain_blocks', params)

    @api_version("4.0.0", "4.0.0")
    def admin_delete_email_domain_block(self, id: IdType):
        """
        Remove an email domain block. Requires scope `admin:write:email_domain_blocks`.
        
        Raises `MastodonAPIError` if the email domain block does not exist.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/admin/email_domain_blocks/{id}')

    @api_version("4.2.0", "4.2.0")
    def admin_approve_trending_link(self, id: Union[PreviewCard, IdType]) -> PreviewCard:
        """
        Approve a trending link. Requires scope `admin:write`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/trends/links/{id}/approve')

    @api_version("4.2.0", "4.2.0")
    def admin_reject_trending_link(self, id: Union[PreviewCard, IdType]) -> PreviewCard:
        """
        Reject a trending link. Requires scope `admin:write`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/trends/links/{id}/reject')

    @api_version("4.2.0", "4.2.0")
    def admin_approve_trending_status(self, id: Union[Status, IdType]) -> Status:
        """
        Approve a trending status. Requires scope `admin:write`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/trends/statuses/{id}/approve')

    @api_version("4.2.0", "4.2.0")
    def admin_reject_trending_status(self, id: Union[Status, IdType]) -> Status:
        """
        Reject a trending status. Requires scope `admin:write`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/trends/statuses/{id}/reject')

    @api_version("4.2.0", "4.2.0")
    def admin_approve_trending_tag(self, id: Union[Tag, IdType]) -> Tag:
        """
        Approve a trending tag. Requires scope `admin:write`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/trends/tags/{id}/approve')

    @api_version("4.2.0", "4.2.0")
    def admin_reject_trending_tag(self, id: Union[Tag, IdType]) -> Tag:
        """
        Reject a trending tag. Requires scope `admin:write`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/trends/tags/{id}/reject')

    @api_version("4.0.0", "4.0.0")
    def admin_ip_blocks(self, max_id: Optional[IdType] = None, min_id: Optional[IdType] = None,
                        since_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[AdminIpBlock]:
        """
        Fetches a list of blocked IP addresses and ranges. Requires scope `admin:read:ip_blocks`.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/ip_blocks', params)

    @api_version("4.0.0", "4.0.0")
    def admin_ip_block(self, id: Union[AdminIpBlock, IdType]) -> AdminIpBlock:
        """
        Fetch a single blocked IP address or range by ID. Requires scope `admin:read:ip_blocks`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/ip_blocks/{id}')

    @api_version("4.0.0", "4.0.0")
    def admin_create_ip_block(self, ip: str, severity: str, comment: Optional[str] = None,
                              expires_in: Optional[int] = None) -> AdminIpBlock:
        """
        Block an IP address or range from signups. Requires scope `admin:write:ip_blocks`.

        Provide the IP address as a CIDR range, e.g. "192.168.1.1/32" to block just that IP address, or
        "8.8.8.8/24" to block all addresses in the 8.8.8.* subnet.

        severity can be one of three values:
            * "sign_up_requires_approval" - signups from this IP will require manual approval
            * "sign_up_block" - signups from this IP will be blocked
            * "no_access" - all access from this IP will be blocked

        expires_in is the number of seconds until the block expires. If not provided, the block will be permanent.
        """
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/admin/ip_blocks', params)

    @api_version("4.0.0", "4.0.0")
    def admin_update_ip_block(self, id: Union[AdminIpBlock, IdType], ip: Optional[str] = None, severity: Optional[str] = None,
                              comment: Optional[str] = None, expires_in: Optional[int] = None) -> AdminIpBlock:
        """
        Update an existing IP block. Requires scope `admin:write:ip_blocks`.

        expires_in is the number of seconds until the block expires. If not provided, the block will be permanent.
        """
        id = self.__unpack_id(id)
        params = self.__generate_params(locals())
        return self.__api_request('PUT', f'/api/v1/admin/ip_blocks/{id}', params)

    @api_version("4.0.0", "4.0.0")
    def admin_delete_ip_block(self, id: Union[AdminIpBlock, IdType]):
        """
        Remove an IP block. Requires scope `admin:write:ip_blocks`.
        """
        id = self.__unpack_id(id)
        self.__api_request('DELETE', f'/api/v1/admin/ip_blocks/{id}')
