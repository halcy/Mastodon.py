# notifications.py - notification endpoints

from .versions import _DICT_VERSION_NOTIFICATION
from .errors import MastodonIllegalArgumentError
from .utility import api_version

from .internals import Mastodon as Internals


class Mastodon(Internals):
    ###
    # Reading data: Notifications
    ###
    @api_version("1.0.0", "3.5.0", _DICT_VERSION_NOTIFICATION)
    def notifications(self, id=None, account_id=None, max_id=None, min_id=None, since_id=None, limit=None, exclude_types=None, types=None, mentions_only=None):
        """
        Fetch notifications (mentions, favourites, reblogs, follows) for the logged-in
        user. Pass `account_id` to get only notifications originating from the given account.

        There are different types of notifications:
            * `follow` - A user followed the logged in user
            * `follow_request` - A user has requested to follow the logged in user (for locked accounts)
            * `favourite` - A user favourited a post by the logged in user
            * `reblog` - A user reblogged a post by the logged in user
            * `mention` - A user mentioned the logged in user
            * `poll` - A poll the logged in user created or voted in has ended
            * `update` - A status the logged in user has reblogged (and only those, as of 4.0.0) has been edited
            * `status` - A user that the logged in user has enabned notifications for has enabled `notify` (see :ref:`account_follow() <account_follow()>`)
            * `admin.sign_up` - For accounts with appropriate permissions (TODO: document which those are when adding the permission API): A new user has signed up
            * `admin.report` - For accounts with appropriate permissions (TODO: document which those are when adding the permission API): A new report has been received
        Parameters `exclude_types` and `types` are array of these types, specifying them will in- or exclude the
        types of notifications given. It is legal to give both parameters at the same tine, the result will then
        be the intersection of the results of both filters. Specifying `mentions_only` is a deprecated way to set
        `exclude_types` to all but mentions.

        Can be passed an `id` to fetch a single notification.

        Returns a list of :ref:`notification dicts <notification dicts>`.
        """
        if mentions_only is not None:
            if exclude_types is None and types is None:
                if mentions_only:
                    if self.verify_minimum_version("3.5.0", cached=True):
                        types = ["mention"]
                    else:
                        exclude_types = ["follow", "favourite", "reblog", "poll", "follow_request"]
            else:
                raise MastodonIllegalArgumentError('Cannot specify exclude_types/types when mentions_only is present')
            del mentions_only

        if max_id is not None:
            max_id = self.__unpack_id(max_id, dateconv=True)

        if min_id is not None:
            min_id = self.__unpack_id(min_id, dateconv=True)

        if since_id is not None:
            since_id = self.__unpack_id(since_id, dateconv=True)

        if account_id is not None:
            account_id = self.__unpack_id(account_id)

        if id is None:
            params = self.__generate_params(locals(), ['id'])
            return self.__api_request('GET', '/api/v1/notifications', params)
        else:
            id = self.__unpack_id(id)
            return self.__api_request('GET', f"/api/v1/notifications/{id}")

    ###
    # Writing data: Notifications
    ###
    @api_version("1.0.0", "1.0.0", "1.0.0")
    def notifications_clear(self):
        """
        Clear out a user's notifications
        """
        self.__api_request('POST', '/api/v1/notifications/clear')

    @api_version("1.3.0", "2.9.2", "2.9.2")
    def notifications_dismiss(self, id):
        """
        Deletes a single notification
        """
        id = self.__unpack_id(id)

        if self.verify_minimum_version("2.9.2", cached=True):
            self.__api_request('POST', f'/api/v1/notifications/{id}/dismiss')
        else:
            params = self.__generate_params(locals())
            self.__api_request('POST', '/api/v1/notifications/dismiss', params)
