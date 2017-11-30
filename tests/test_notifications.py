import pytest

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
    api.notifications_dismiss(notifications[0])

@pytest.mark.vcr()
def test_notifications_clear(api):
    api.notifications_clear()
