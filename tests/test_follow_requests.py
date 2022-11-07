import pytest
import time

@pytest.mark.vcr()
def test_follow_requests(api):
    reqs = api.follow_requests()
    assert isinstance(reqs, list)


@pytest.mark.vcr()
def test_follow_request_authorize(api, api2):
    api2.account_follow(1234567890123456)
    time.sleep(2)
    request = api.follow_requests()[0]
    api.follow_request_authorize(request)
    api2.account_unfollow(1234567890123456)


@pytest.mark.vcr()
def test_follow_request_reject(api, api2):
    api2.account_follow(1234567890123456)
    time.sleep(2)
    request = api.follow_requests()[0]    
    api.follow_request_reject(request)


