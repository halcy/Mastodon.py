import pytest
from contextlib import contextmanager

UNLIKELY_HASHTAG = "fgiztsshwiaqqiztpmmjbtvmescsculuvmgjgopwoeidbcrixp"


@contextmanager
def many_statuses(api, n=10, suffix=''):
    statuses = list()
    for i in range(n):
        status = api.status_post("Toot number {}!{}".format(i, suffix))
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


@pytest.mark.vcr()
def test_fetch_next_previous_from_pagination_info(api):
    account = api.account_verify_credentials()
    with many_statuses(api):
        statuses = api.account_statuses(account['id'], limit=5)
        next_statuses = api.fetch_next(statuses[-1]._pagination_next)
        assert next_statuses
        previous_statuses = api.fetch_previous(next_statuses[0]._pagination_prev)
        assert previous_statuses


@pytest.mark.vcr()
def test_fetch_remaining(api):
    with many_statuses(api, n=30, suffix=' #'+UNLIKELY_HASHTAG):
        hashtag = api.timeline_hashtag(UNLIKELY_HASHTAG, limit=10)
        hashtag_remaining = api.fetch_remaining(hashtag)
        assert hashtag_remaining
        assert len(hashtag_remaining) >= 30
