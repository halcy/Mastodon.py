# admin.py - admin / moderation endpoints

from .versions import _DICT_VERSION_ADMIN_ACCOUNT, _DICT_VERSION_REPORT, _DICT_VERSION_HASHTAG, _DICT_VERSION_STATUS, _DICT_VERSION_CARD, \
                        _DICT_VERSION_ADMIN_DOMAIN_BLOCK, _DICT_VERSION_ADMIN_MEASURE, _DICT_VERSION_ADMIN_DIMENSION, _DICT_VERSION_ADMIN_RETENTION
from .errors import MastodonIllegalArgumentError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Moderation API
    ###
    @api_version("2.9.1", "4.0.0", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_accounts_v2(self, origin=None, by_domain=None, status=None, username=None, display_name=None, email=None, ip=None,
                            permissions=None, invited_by=None, role_ids=None, max_id=None, min_id=None, since_id=None, limit=None):
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

        Returns a list of :ref:`admin account dicts <admin account dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

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

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v2/admin/accounts', params)

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_accounts(self, remote=False, by_domain=None, status='active', username=None, display_name=None, email=None, ip=None, staff_only=False, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Currently a synonym for admin_accounts_v1, now deprecated. You are strongly encouraged to use admin_accounts_v2 instead, since this one is kind of bad.

        !!!!! This function may be switched to calling the v2 API in the future. This is your warning. If you want to keep using v1, use it explicitly. !!!!!
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

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_accounts_v1(self, remote=False, by_domain=None, status='active', username=None, display_name=None, email=None, ip=None, staff_only=False, max_id=None, min_id=None, since_id=None, limit=None):
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

        Returns a list of :ref:`admin account dicts <admin account dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        params = self.__generate_params(locals(), ['remote', 'status', 'staff_only'])

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

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account(self, id):
        """
        Fetches a single :ref:`admin account dict <admin account dict>` for the user with the given id.

        Returns that dict.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/accounts/{id}')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_enable(self, id):
        """
        Reenables login for a local account for which login has been disabled.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/enable')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_approve(self, id):
        """
        Approves a pending account.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/approve')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_reject(self, id):
        """
        Rejects and deletes a pending account.

        Returns the updated :ref:`admin account dict <admin account dict>` for the account that is now gone.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/reject')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsilence(self, id):
        """
        Unsilences an account.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/unsilence')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsuspend(self, id):
        """
        Unsuspends an account.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/unsuspend')

    @api_version("3.3.0", "3.3.0", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_delete(self, id):
        """
        Delete a local user account.

        The deleted accounts :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('DELETE', f'/api/v1/admin/accounts/{id}')

    @api_version("3.3.0", "3.3.0", _DICT_VERSION_ADMIN_ACCOUNT)
    def admin_account_unsensitive(self, id):
        """
        Unmark an account as force-sensitive.

        Returns the updated :ref:`admin account dict <admin account dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/accounts/{id}/unsensitive')

    @api_version("2.9.1", "2.9.1", "2.9.1")
    def admin_account_moderate(self, id, action=None, report_id=None, warning_preset_id=None, text=None, send_email_notification=True):
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

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_reports(self, resolved=False, account_id=None, target_account_id=None, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches the list of reports.

        Set `resolved` to True to search for resolved reports. `account_id` and `target_account_id`
        can be used to get reports filed by or about a specific user.

        Returns a list of :ref:`report dicts <report dicts>`.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        if account_id is not None:
            account_id = self.__unpack_id(account_id)

        if target_account_id is not None:
            target_account_id = self.__unpack_id(target_account_id)

        if not resolved:
            resolved = None

        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/reports', params)

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report(self, id):
        """
        Fetches the report with the given id.

        Returns a :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/admin/reports/{id}')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_assign(self, id):
        """
        Assigns the given report to the logged-in user.

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/assign_to_self')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_unassign(self, id):
        """
        Unassigns the given report from the logged-in user.

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/unassign')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_reopen(self, id):
        """
        Reopens a closed report.

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/reopen')

    @api_version("2.9.1", "2.9.1", _DICT_VERSION_REPORT)
    def admin_report_resolve(self, id):
        """
        Marks a report as resolved (without taking any action).

        Returns the updated :ref:`report dict <report dict>`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('POST', f'/api/v1/admin/reports/{id}/resolve')

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_HASHTAG)
    def admin_trending_tags(self, limit=None):
        """
        Admin version of :ref:`trending_tags() <trending_tags()>`. Includes unapproved tags.

        Returns a list of :ref:`hashtag dicts <hashtag dicts>`, sorted by the instance's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/tags', params)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_STATUS)
    def admin_trending_statuses(self):
        """
        Admin version of :ref:`trending_statuses() <trending_statuses()>`. Includes unapproved tags.

        Returns a list of :ref:`status dicts <status dicts>`, sorted by the instance's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/statuses', params)

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_CARD)
    def admin_trending_links(self):
        """
        Admin version of :ref:`trending_links() <trending_links()>`. Includes unapproved tags.

        Returns a list of :ref:`card dicts <card dicts>`, sorted by the instance's trending algorithm,
        descending.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/admin/trends/links', params)

    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_domain_blocks(self, id=None, max_id=None, min_id=None, since_id=None, limit=None):
        """
        Fetches a list of blocked domains. Requires scope `admin:read:domain_blocks`.

        Provide an `id` to fetch a specific domain block based on its database id.

        Returns a list of :ref:`admin domain block dicts <admin domain block dicts>`, raises a `MastodonAPIError` if the specified block does not exist.
        """
        if max_id is not None:
            max_id = self.__unpack_id(max_id)

        if min_id is not None:
            min_id = self.__unpack_id(min_id)

        if since_id is not None:
            since_id = self.__unpack_id(since_id)

        if id is not None:
            id = self.__unpack_id(id)
            return self.__api_request('GET', f'/api/v1/admin/domain_blocks/{id}')
        else:
            params = self.__generate_params(locals(), ['limit'])
            return self.__api_request('GET', '/api/v1/admin/domain_blocks/', params)

    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_create_domain_block(self, domain:str, severity:str=None, reject_media:bool=None, reject_reports:bool=None, private_comment:str=None, public_comment:str=None, obfuscate:bool=None):
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

        Returns the new domain block as an :ref:`admin domain block dict <admin domain block dict>`.
        """
        if domain is None:
            raise AttributeError("Must provide a domain to block a domain")
        params = self.__generate_params(locals())
        return self.__api_request('POST', '/api/v1/admin/domain_blocks/', params)

    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_update_domain_block(self, id, severity:str=None, reject_media:bool=None, reject_reports:bool=None, private_comment:str=None, public_comment:str=None, obfuscate:bool=None):
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

        Returns the modified domain block as an :ref:`admin domain block dict <admin domain block dict>`, raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is None:
            raise AttributeError("Must provide an id to modify the existing moderation actions on a given domain.")
        id = self.__unpack_id(id)
        params = self.__generate_params(locals(), ["id"])
        return self.__api_request('PUT', f'/api/v1/admin/domain_blocks/{id}', params)

    @api_version("4.0.0", "4.0.0", _DICT_VERSION_ADMIN_DOMAIN_BLOCK)
    def admin_delete_domain_block(self, id=None):
        """
        Removes moderation action against a given domain. Requires scope `admin:write:domain_blocks`.

        Provide an `id` to remove a specific domain block based on its database id.

        Raises a `MastodonAPIError` if the specified block does not exist.
        """
        if id is not None:
            id = self.__unpack_id(id)
            self.__api_request('DELETE', f'/api/v1/admin/domain_blocks/{id}')
        else:
            raise AttributeError("You must provide an id of an existing domain block to remove it.")

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_ADMIN_MEASURE)
    def admin_measures(self, start_at, end_at, active_users=False, new_users=False, interactions=False, opened_reports = False, resolved_reports=False,
                        tag_accounts=None, tag_uses=None, tag_servers=None, instance_accounts=None, instance_media_attachments=None, instance_reports=None,
                        instance_statuses=None, instance_follows=None, instance_followers=None):
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

        Returns a list of :ref:`admin measure dicts <admin measure dicts>`.
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

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_ADMIN_DIMENSION)
    def admin_dimensions(self, start_at, end_at, limit=None, languages=False, sources=False, servers=False, space_usage=False, software_versions=False,
                            tag_servers=None, tag_languages=None, instance_accounts=None, instance_languages=None):
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

        Returns a list of :ref:`admin dimension dicts <admin dimension dicts>`.
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

    @api_version("3.5.0", "3.5.0", _DICT_VERSION_ADMIN_RETENTION)
    def admin_retention(self, start_at, end_at, frequency="day"):
        """
        Gets user retention statistics (at `frequency` - "day" or "month" - granularity) between `start_at` and `end_at`.

        Returns a list of :ref:`admin retention dicts <admin retention dicts>`
        """
        if not frequency in ["day", "month"]:
            raise MastodonIllegalArgumentError("Frequency must be day or month")

        params = {
            "start_at": self.__consistent_isoformat_utc(start_at),
            "end_at": self.__consistent_isoformat_utc(end_at),
            "frequency": frequency
        }
        return self.__api_request('POST', '/api/v1/admin/retention', params)
