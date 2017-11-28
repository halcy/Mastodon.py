import pytest
from contextlib import contextmanager


@contextmanager
def many_statuses(api, n=10):
    statuses = list()
    for i in range(n):
        status = api.status_post("Toot number {}!".format(i))
        statuses.append(status)
    yield statuses
    for status in statuses:
        api.status_delete(status['id'])


@pytest.mark.vcr()
def test_fetch_next_previous(api):
    account = api.account_verify_credentials()
    with many_statuses(api):
        statuses = api.account_statuses(account['id'], limit=5)
        next_statuses = api.fetch_next(statuses)
        assert next_statuses
        previous_statuses = api.fetch_previous(next_statuses)
        assert previous_statuses
