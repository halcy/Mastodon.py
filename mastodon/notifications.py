# notifications.py - notification endpoints
from mastodon.errors import MastodonIllegalArgumentError
from mastodon.utility import api_version

from mastodon.internals import Mastodon as Internals
from mastodon.return_types import Notification, IdType, PaginatableList, Account, UnreadNotificationsCount, NotificationPolicy, NotificationRequest, GroupedNotificationsResults, NonPaginatableList
from typing import Union, Optional, List

class Mastodon(Internals):
    ###
    # Reading data: Notifications
    ###
    @api_version("1.0.0", "3.5.0")
    def notifications(self, id: Optional[Union[Notification, IdType]] = None, account_id: Optional[Union[Account, IdType]] = None, max_id:  Optional[Union[Notification, IdType]] = None, 
                      min_id:  Optional[Union[Notification, IdType]] = None, since_id:  Optional[Union[Notification, IdType]] = None, limit: Optional[int] = None, 
                      exclude_types: Optional[List[str]] = None, types: Optional[List[str]] = None, mentions_only: Optional[bool] = None) -> Union[PaginatableList[Notification], Notification]:
        """
        Fetch notifications (mentions, favourites, reblogs, follows) for the logged-in
        user. Pass `account_id` to get only notifications originating from the given account.

        There are different types of notifications:
            - `follow` - A user followed the logged in user
            - `follow_request` - A user has requested to follow the logged in user (for locked accounts)
            - `favourite` - A user favourited a post by the logged in user
            - `reblog` - A user reblogged a post by the logged in user
            - `mention` - A user mentioned the logged in user
            - `poll` - A poll the logged in user created or voted in has ended
            - `update` - A status the logged in user has reblogged (and only those, as of 4.0.0) has been edited
            - `status` - A user that the logged in user has enabned notifications for has enabled `notify` (see :ref:`account_follow() <account_follow()>`)
            - `admin.sign_up` - For accounts with appropriate permissions: A new user has signed up
            - `admin.report` - For accounts with appropriate permissions: A new report has been received
            - `severed_relationships` - Some of the logged in users relationships have been severed due to a moderation action on this server
            - `moderation_warning` - The logged in user has been warned by a moderator
            
        Parameters `exclude_types` and `types` are array of these types, specifying them will in- or exclude the
        types of notifications given. It is legal to give both parameters at the same tine, the result will then
        be the intersection of the results of both filters. Specifying `mentions_only` is a deprecated way to set
        `exclude_types` to all but mentions.

        Can be passed an `id` to fetch a single notification.
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

        if account_id is not None:
            account_id = self.__unpack_id(account_id)

        if id is None:
            params = self.__generate_params(locals(), ['id'], dateconv=True)
            return self.__api_request('GET', '/api/v1/notifications', params)
        else:
            id = self.__unpack_id(id)
            return self.__api_request('GET', f"/api/v1/notifications/{id}", override_type=Notification)

    # Implement GET /api/v1/notifications/unread_count HTTP/1.1
    @api_version("4.3.0", "4.3.0")
    def notifications_unread_count(self) -> UnreadNotificationsCount:
        """
        Fetch the number of unread notifications for the logged-in user.
        """
        return self.__api_request('GET', '/api/v1/notifications/unread_count')

    ###
    # Writing data: Notifications
    ###
    @api_version("1.0.0", "1.0.0")
    def notifications_clear(self):
        """
        Clear out a user's notifications
        """
        self.__api_request('POST', '/api/v1/notifications/clear')

    @api_version("1.3.0", "2.9.2")
    def notifications_dismiss(self, id: Union[Notification, IdType]):
        """
        Deletes a single notification
        """
        id = self.__unpack_id(id)

        if self.verify_minimum_version("2.9.2", cached=True):
            self.__api_request('POST', f'/api/v1/notifications/{id}/dismiss')
        else:
            params = self.__generate_params(locals())
            self.__api_request('POST', '/api/v1/notifications/dismiss', params)

    
    ##
    # Notification policies
    ##

    @api_version("4.3.0", "4.3.0")
    def notifications_policy(self) -> NotificationPolicy:
        """
        Fetch the user's notification filtering policy. Requires scope `read:notifications`.
        """
        return self.__api_request('GET', '/api/v2/notifications/policy')

    @api_version("4.3.0", "4.3.0")
    def update_notifications_policy(self, for_not_following: Optional[str] = None, for_not_followers: Optional[str] = None,
                                    for_new_accounts: Optional[str] = None, for_private_mentions: Optional[str] = None,
                                    for_limited_accounts: Optional[str] = None) -> NotificationPolicy:
        """
        Update the user's notification filtering policy. Requires scope `write:notifications`.
        
        - `for_not_following`: "accept", "filter", or "drop" notifications from non-followed accounts.
        - `for_not_followers`: "accept", "filter", or "drop" notifications from non-followers.
        - `for_new_accounts`: "accept", "filter", or "drop" notifications from accounts created in the past 30 days.
        - `for_private_mentions`: "accept", "filter", or "drop" notifications from private mentions.
        - `for_limited_accounts`: "accept", "filter", or "drop" notifications from accounts limited by moderators.
        """
        params = self.__generate_params(locals())
        return self.__api_request('PATCH', '/api/v2/notifications/policy', params)

    ##
    # Notification requests
    ##
    @api_version("4.3.0", "4.3.0")
    def notification_requests(self, max_id: Optional[IdType] = None, since_id: Optional[IdType] = None,
                              min_id: Optional[IdType] = None, limit: Optional[int] = None) -> PaginatableList[NotificationRequest]:
        """
        Fetch notification requests filtered by the user's policy. Requires scope `read:notifications`.

        NB: Notification requests are what happens when the user has set their policy to filter notifications from some source.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v1/notifications/requests', params)

    @api_version("4.3.0", "4.3.0")
    def notification_request(self, id: Union[NotificationRequest, IdType]) -> NotificationRequest:
        """
        Fetch a single notification request by ID. Requires scope `read:notifications`.
        """
        id = self.__unpack_id(id)
        return self.__api_request('GET', f'/api/v1/notifications/requests/{id}')

    @api_version("4.3.0", "4.3.0")
    def accept_notification_request(self, id: Union[NotificationRequest, IdType]) -> None:
        """
        Accept a notification request. This moves filtered notifications from a user back into the main notifications feed
        and allows future notifications from them. Requires scope `write:notifications`.
        """
        id = self.__unpack_id(id)
        self.__api_request('POST', f'/api/v1/notifications/requests/{id}/accept')

    @api_version("4.3.0", "4.3.0")
    def dismiss_notification_request(self, id: Union[NotificationRequest, IdType]) -> None:
        """
        Dismiss a notification request, removing it from pending requests. Requires scope `write:notifications`.
        """
        id = self.__unpack_id(id)
        self.__api_request('POST', f'/api/v1/notifications/requests/{id}/dismiss')

    @api_version("4.3.0", "4.3.0")
    def accept_multiple_notification_requests(self, ids: List[Union[NotificationRequest, IdType]]) -> None:
        """
        Accept multiple notification requests at once. This moves filtered notifications from those users back into
        the main notifications feed and allows future notifications from them. Requires scope `write:notifications`.
        """
        params = self.__generate_params({"id[]": [self.__unpack_id(i) for i in ids]})
        self.__api_request('POST', '/api/v1/notifications/requests/accept', params)

    @api_version("4.3.0", "4.3.0")
    def dismiss_multiple_notification_requests(self, ids: List[Union[NotificationRequest, IdType]]) -> None:
        """
        Dismiss multiple notification requests, removing them from pending requests. Requires scope `write:notifications`.
        """
        params = self.__generate_params({"id[]": [self.__unpack_id(i) for i in ids]})
        self.__api_request('POST', '/api/v1/notifications/requests/dismiss', params)

    @api_version("4.3.0", "4.3.0")
    def notifications_merged(self) -> bool:
        """
        Check whether accepted notification requests have been merged into the main notification feed.
        Accepting a notification request schedules a background job that merges the filtered notifications.
        Clients can poll this endpoint to check if the merge has completed. Requires scope `read:notifications`.
        """
        result = self.__api_request('GET', '/api/v1/notifications/requests/merged', override_type = dict)
        return result["merged"]

    ##
    # Grouped notifications
    ##
    @api_version("4.3.0", "4.3.0")
    def grouped_notifications(self, max_id: Optional[IdType] = None, since_id: Optional[IdType] = None,
                              min_id: Optional[IdType] = None, limit: Optional[int] = None,
                              types: Optional[List[str]] = None, exclude_types: Optional[List[str]] = None,
                              account_id: Optional[Union[Account, IdType]] = None,
                              expand_accounts: Optional[str] = "partial_avatars", grouped_types: Optional[List[str]] = None,
                              include_filtered: Optional[bool] = None) -> GroupedNotificationsResults:
        """
        Fetch grouped notifications for the user. Requires scope `read:notifications`.

        For base parameters, see `notifications()`.

        `grouped_types` controls which notication types can be grouped together - all, if not specified.
        NB: "all" here means favourite, follow and reblog - other types are not groupable and are returned
        individually (with a unique group key) always.

        Pass `include_filtered=True` to include filtered notifications in the response.

        Pass `expand_accounts="full"` to include full account details in the response, or "partial_avatars" to
        include a smaller set of account details (in the `partial_accounts` field) for some (but not all - the most
        recent account triggering a notification is always returned in full) of the included accounts. 
        The default is partial_avatars.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v2/notifications', params, force_pagination=True)

    @api_version("4.3.0", "4.3.0")
    def grouped_notification(self, group_key: str) -> GroupedNotificationsResults:
        """
        Fetch details of a single grouped notification by its group key. Requires scope `read:notifications`.
        """
        return self.__api_request('GET', f'/api/v2/notifications/{group_key}')

    @api_version("4.3.0", "4.3.0")
    def dismiss_grouped_notification(self, group_key: str) -> None:
        """
        Dismiss a single grouped notification. Requires scope `write:notifications`.
        """
        self.__api_request('POST', f'/api/v2/notifications/{group_key}/dismiss')

    @api_version("4.3.0", "4.3.0")
    def grouped_notification_accounts(self, group_key: str) -> NonPaginatableList[Account]:
        """
        Fetch accounts associated with a grouped notification. Requires scope `write:notifications`.
        """
        return self.__api_request('GET', f'/api/v2/notifications/{group_key}/accounts')

    @api_version("4.3.0", "4.3.0")
    def unread_grouped_notifications_count(self, limit: Optional[int] = None,
                                           types: Optional[List[str]] = None, exclude_types: Optional[List[str]] = None,
                                           account_id: Optional[Union[Account, IdType]] = None,
                                           grouped_types: Optional[List[str]] = None) -> int:
        """
        Fetch the count of unread grouped notifications. Requires scope `read:notifications`.

        For parameters, see `notifications()` and `grouped_notifications()`.
        """
        params = self.__generate_params(locals())
        return self.__api_request('GET', '/api/v2/notifications/unread_count', params, override_type=dict)["count"]
