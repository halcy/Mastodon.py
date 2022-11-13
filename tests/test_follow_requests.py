import pytest
import time

@pytest.mark.vcr()
def test_follow_requests(api):
    reqs = api.follow_requests()
    assert isinstance(reqs, list)


@pytest.mark.vcr()
def test_follow_request_authorize(api, api2):
    api_id = api.account_verify_credentials()
    api2.account_follow(api_id)
    time.sleep(2)
    request = api.follow_requests()[0]
    api.follow_request_authorize(request)
    api2.account_unfollow(api_id)


@pytest.mark.vcr()
def test_follow_request_reject(api, api2):
    api2.account_follow(api.account_verify_credentials())
    time.sleep(2)
    request = api.follow_requests()[0]    
    api.follow_request_reject(request)


