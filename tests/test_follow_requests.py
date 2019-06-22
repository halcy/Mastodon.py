import pytest
import time

@pytest.mark.vcr()
def test_follow_requests(api3):
    reqs = api3.follow_requests()
    assert isinstance(reqs, list)


@pytest.mark.vcr()
def test_follow_request_authorize(api3, api2):
    api2.account_follow(1234567890123457)
    time.sleep(2)
    request = api3.follow_requests()[0]
    api3.follow_request_authorize(request)
    api2.account_unfollow(1234567890123457)


@pytest.mark.vcr()
def test_follow_request_reject(api3, api2):
    api2.account_follow(1234567890123457)
    time.sleep(2)
    request = api3.follow_requests()[0]    
    api3.follow_request_reject(request)


