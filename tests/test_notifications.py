import pytest
import vcr
import time

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
        assert notifications[0].status.id == mention.id

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
    
def test_notifications_dismiss_pre_2_9_2(api, api2):
    with vcr.use_cassette('test_notifications_dismiss.yaml', cassette_library_dir='tests/cassettes_pre_2_9_2', record_mode='none'):
        status = None
        try:
            status = api2.status_post('@mastodonpy_test hello!')
            notifications = api.notifications()
            api.verify_minimum_version("2.9.2", cached=False)
            api.notifications_dismiss(notifications[0])
        finally:
            if status is not None:
                api2.status_delete(status)            

@pytest.mark.vcr()
def test_notifications_clear(api):
    api.notifications_clear()

