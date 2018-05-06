import pytest

@pytest.mark.vcr()
def test_report(api, status):
    user = api.account_verify_credentials().id
    report = api.report(user, status, "makes the bad post")
    assert report in api.reports()
    