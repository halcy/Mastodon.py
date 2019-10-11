import pytest
import vcr

@pytest.fixture()
def mention(api2):
    status = api2.status_post('@mastodonpy_test hello!')
    yield status
    api2.status_delete(status)

@pytest.mark.vcr()
def test_notifications(api, mention):
    notifications = api.notifications()
    api.notifications(notifications[0])

@pytest.mark.vcr()
def test_notifications_dismiss(api, mention):
    notifications = api.notifications()
    api.notifications_dismiss(notifications[0]) # TODO possibly verify that this returns a notif dict

def test_notifications_dismiss_pre_2_9_2(api, mention):
    with vcr.use_cassette('test_notifications_dismiss.yaml', cassette_library_dir='tests/cassettes_pre_2_9_2', record_mode='none'):
        notifications = api.notifications()
        api.notifications_dismiss(notifications[0])

@pytest.mark.vcr()
def test_notifications_clear(api):
    api.notifications_clear()
