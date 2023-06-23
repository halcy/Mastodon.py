import pytest
import vcr

from contextlib import contextmanager

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock
import requests_mock

UNLIKELY_HASHTAG = "fgiztsshwiaqqiztpmmjbtvmescsculuvmgjgopwoeidbcrixp"


@contextmanager
def many_statuses(api, n=10, suffix=''):
    statuses = list()
    for i in range(n):
        status = api.status_post(f"Toot number {i}!{suffix}")
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
        next_statuses = api.fetch_next(statuses._pagination_next)
        assert next_statuses
        previous_statuses = api.fetch_previous(next_statuses._pagination_prev)
        assert previous_statuses

@pytest.mark.vcr()
def test_fetch_remaining(api):
    with many_statuses(api, n=30, suffix=' #'+UNLIKELY_HASHTAG):
        hashtag = api.timeline_hashtag(UNLIKELY_HASHTAG, limit=10)
        hashtag_remaining = api.fetch_remaining(hashtag)
        assert hashtag_remaining
        assert len(hashtag_remaining) >= 30

def test_link_headers(api):
    rmock = requests_mock.Adapter()
    api.session.mount(api.api_base_url, rmock)

    _id='abc1234'

    rmock.register_uri(
        'GET',
        requests_mock.ANY,
        json=[{"foo": "bar"}],
        headers={
            "link": f"<{api.api_base_url}/api/v1/timelines/tag/{UNLIKELY_HASHTAG}?max_id={_id}>; rel=\"next\", "
                    f"<{api.api_base_url}/api/v1/timelines/tag/{UNLIKELY_HASHTAG}?since_id={_id}>; rel=\"prev\""
        }
    )

    resp = api.timeline_hashtag(UNLIKELY_HASHTAG)
    assert resp._pagination_next['max_id'] == _id
    assert resp._pagination_prev['since_id'] == _id
