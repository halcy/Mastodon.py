import pytest

@pytest.mark.vcr()
def test_follow_requests(api):
    reqs = api.follow_requests()
    assert isinstance(reqs, list)


# warning: these two send emails, which open in letter opener by default
# so if you are re-recording a cassette for either of these mastodon will
# probably open a browser window for you, which you can safely close
@pytest.mark.vcr()
def test_follow_request_authorize(api, api2):
    api2.account_follow(1234567890123456)
    api.follow_request_authorize(1)
    api2.account_unfollow(1234567890123456)


@pytest.mark.vcr()
def test_follow_request_reject(api, api2):
    api2.account_follow(1234567890123456)
    api.follow_request_reject(1)


