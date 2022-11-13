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
    api.notifications(notifications[0])

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
            api.notifications_dismiss(notifications[0])
        finally:
            if not status is None:
                api2.status_delete(status)            

@pytest.mark.vcr()
def test_notifications_clear(api):
    api.notifications_clear()

