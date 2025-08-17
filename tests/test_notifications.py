import pytest
import vcr
import time
import sys

@pytest.fixture()
def mention(api2):
    status = api2.status_post('@mastodonpy_test hello!')
    yield status
    api2.status_delete(status)

@pytest.mark.vcr()
def test_notifications(api, mention):
    time.sleep(3)
    notifications = api.notifications()
    assert api.notifications(notifications[0])
    assert notifications[0].status.id == mention.id
    assert api.notifications_unread_count().count > 0

    notification_single_id = api.notifications(notifications[0])
    assert notification_single_id.id == notifications[0].id

@pytest.mark.vcr()
def test_notifications_mentions_only(api, mention):
    time.sleep(3)
    notifications = api.notifications(mentions_only=True)
    assert api.notifications(notifications[0])
    assert notifications[0].status.id == mention.id

@pytest.mark.vcr()
def test_notifications_exclude_types(api, mention):
    time.sleep(3)
    notifications = api.notifications(exclude_types=["mention"])
    if len(notifications) > 0:
        assert notifications[0].status is None

@pytest.mark.vcr()
def test_notifications_types(api, mention):
    time.sleep(3)
    notifications = api.notifications(types=["follow_request"])
    if len(notifications) > 0:
        assert notifications[0].status.id == mention.id
    notifications = api.notifications(types=["follow", "mention"])
    assert api.notifications(notifications[0])
    assert notifications[0].status.id == mention.id

@pytest.mark.vcr()
def test_notifications_exclude_and_types(api, mention):
    time.sleep(3)
    notifications = api.notifications(exclude_types=["mention"], types=["mention"])
    if len(notifications) > 0:
        assert notifications[0].status.id == mention.id
    notifications = api.notifications(exclude_types=["mention"], types=["follow_request"])
    if len(notifications) > 0:
        assert notifications[0].status.id == mention.id
    notifications = api.notifications(exclude_types=["follow_request"], types=["mention"])
    assert notifications[0].status.id == mention.id
    notifications = api.notifications(exclude_types=["follow_request"], types=["mention", "follow_request"])
    assert notifications[0].status.id == mention.id

@pytest.mark.vcr()
def test_notifications_dismiss(api, mention):
    time.sleep(3)
    notifications = api.notifications()
    api.notifications_dismiss(notifications[0])
    
# skip these entirely now, 2.9.2 was a long time ago and we can't regenerate them.
@pytest.mark.skip("Skipping pre-2.9.2 tests")
def test_notifications_dismiss_pre_2_9_2(api, api2):
    if sys.version_info > (3, 9): # 3.10 and up will not load the json data and regenerating it would require a 2.9.2 instance
        pytest.skip("Test skipped for 3.10 and up")
    else:
        api._Mastodon__version_check_worked = True
        api._Mastodon__version_check_tried = True
        api2._Mastodon__version_check_worked = True
        api2._Mastodon__version_check_tried = True
        with vcr.use_cassette('test_notifications_dismiss.yaml', cassette_library_dir='tests/cassettes_pre_2_9_2', record_mode='none'):
            status = None
            try:
                status = api2.status_post('@mastodonpy_test hello!')
                notifications = api.notifications()
                api.verify_minimum_version("2.9.2", cached=True)
                api.notifications_dismiss(notifications[0])
            finally:
                if status is not None:
                    api2.status_delete(status)            

@pytest.mark.vcr()
def test_notifications_clear(api):
    api.notifications_clear()


@pytest.mark.vcr(match_on=['path'])
def test_notifications_policy(api2):
    """Test fetching and updating the notifications policy."""
    # Fetch current policy
    policy = api2.notifications_policy()
    assert policy is not None
    
    # Update policy
    updated_policy = api2.update_notifications_policy(for_not_following="filter", for_not_followers="accept")
    assert updated_policy.for_not_following == "filter"
    assert updated_policy.for_not_followers == "accept"

    # Finally, change it to everything being accepted
    updated_policy = api2.update_notifications_policy(for_not_following="accept", for_not_followers="accept", for_new_accounts="accept", for_limited_accounts="accept", for_private_mentions="accept")

@pytest.mark.vcr()
def test_notification_requests_accept(api, api2):
    """Test fetching, accepting, and dismissing notification requests."""
    
    # Ensure that our two users do not follow each other
    api2.account_unfollow(api.account_verify_credentials().id)
    api.account_unfollow(api2.account_verify_credentials().id)
    time.sleep(5)

    # Set the notification policy such that requests should be generated
    posted = []
    api2.update_notifications_policy(for_not_following="filter", for_not_followers="filter", for_new_accounts="filter", for_limited_accounts="filter", for_private_mentions="filter")
    time.sleep(5)

    # validate that our policy is set correctly
    policy = api2.notifications_policy()
    assert policy.for_not_following == "filter"
    assert policy.for_not_followers == "filter"
    assert policy.for_new_accounts == "filter"
    assert policy.for_limited_accounts == "filter"
    assert policy.for_private_mentions == "filter"

    while not api2.notifications_merged():
        time.sleep(1)
        print("Waiting for notifications to merge...")
    time.sleep(1)
    
    try:
        reply_name = api2.account_verify_credentials().username
        for i in range(5):
            posted.append(api.status_post(f"@{reply_name} please follow me - {i+600}!", visibility="direct"))

        time.sleep(3)

        # Fetch notification requests
        requests = api2.notification_requests()
        print(posted)
        print(api2.notifications())
        print(requests)
        assert requests is not None
        assert len(requests) > 0

        request_id = requests[0].id
        
        # Fetch a single request
        single_request = api2.notification_request(request_id)
        assert single_request.id == request_id
        
        # Accept the request
        api2.accept_notification_request(request_id)
        time.sleep(5)

        # Check if notifications have been merged
        merged_status = api2.notifications_merged()
        assert isinstance(merged_status, bool)
        assert merged_status == True
    finally:
        for status in posted:
            api.status_delete(status)
        api2.update_notifications_policy(for_not_following="accept", for_not_followers="accept", for_new_accounts="accept", for_limited_accounts="accept", for_private_mentions="accept")

@pytest.mark.vcr()
def test_grouped_notifications(api, api2, api3):
    try:
        status = api.status_post("Testing grouped notifications!", visibility="public")
        api2.status_favourite(status["id"])
        api3.status_favourite(status["id"])
        
        time.sleep(2)

        grouped_notifs = api.grouped_notifications(limit=10, expand_accounts="partial_avatars")
        assert grouped_notifs
        assert hasattr(grouped_notifs, "_pagination_next")
        assert hasattr(grouped_notifs, "_pagination_prev")

        group_keys = [group.group_key for group in grouped_notifs.notification_groups]
        assert any("favourite" in key or "reblog" in key for key in group_keys), "Expected a grouped notification"

        group_key = group_keys[0]  # Take first group
        single_grouped_notif = api.grouped_notification(group_key)
        assert single_grouped_notif
        assert single_grouped_notif.notification_groups[0].group_key == group_key

        accounts = api.grouped_notification_accounts(group_key)
        assert isinstance(accounts, list)
        assert len(accounts) > 0

        partial_accounts = [acc for acc in accounts if hasattr(acc, 'avatar_static')]
        assert len(partial_accounts) > 0, "Expected at least one partial account"

        api.dismiss_grouped_notification(group_key)

        updated_grouped_notifs = api.grouped_notifications(limit=10)
        updated_group_keys = [group.group_key for group in updated_grouped_notifs.notification_groups]
        assert group_key not in updated_group_keys, "Dismissed notification still appears"
    finally:
        api.status_delete(status["id"])

@pytest.mark.vcr()
def test_grouped_notification_pagination(api, api2):
    try:
        # Post 10 statuses that mention api
        posted = []
        api_name = api.account_verify_credentials().username
        for i in range(10):
            posted.append(api2.status_post(f"@{api_name} hey how you doing - {i}!", visibility="public"))
        time.sleep(5)

        grouped_notifs = api.grouped_notifications(limit=5, expand_accounts="full")
        assert len(grouped_notifs.notification_groups) == 5
        assert grouped_notifs._pagination_next
        assert grouped_notifs._pagination_prev

        # Fetch next page
        next_notifs = api.fetch_next(grouped_notifs)
        assert len(next_notifs.notification_groups) == 5
        assert next_notifs._pagination_next
        assert next_notifs._pagination_prev

        # Fetch previous page
        prev_notifs = api.fetch_previous(next_notifs)
        assert len(prev_notifs.notification_groups) == 5
        assert prev_notifs._pagination_next
        assert prev_notifs._pagination_prev
    finally:
        for status in posted:
            api2.status_delete(status["id"])