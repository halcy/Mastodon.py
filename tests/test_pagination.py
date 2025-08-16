import pytest
import vcr

from contextlib import contextmanager

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock
import requests_mock

UNLIKELY_HASHTAG = "fgiztsshwiaqqiztpmmjbtvmescsculuvmgjgopwoeidbcrixp"

from mastodon.types_base import Entity, PaginationInfo

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
        assert type(next_statuses) == type(statuses)
        for status in next_statuses:
            assert status['id'] < statuses[0]['id']
            assert type(status) == type(statuses[0])
        previous_statuses = api.fetch_previous(next_statuses)
        assert previous_statuses
        assert type(previous_statuses) == type(statuses)
        for status in previous_statuses:
            assert status['id'] > next_statuses[-1]['id']
            assert type(status) == type(statuses[0])

@pytest.mark.vcr()
def test_fetch_next_previous_after_persist(api):
    account = api.account_verify_credentials()
    with many_statuses(api):
        statuses_orig = api.account_statuses(account['id'], limit=5)
        statuses_persist_json = statuses_orig.to_json()
        statuses = Entity.from_json(statuses_persist_json)
        assert type(statuses) == type(statuses_orig)
        assert type(statuses[0]) == type(statuses_orig[0])
        next_statuses = api.fetch_next(statuses)
        assert next_statuses
        assert type(next_statuses) == type(statuses)
        for status in next_statuses:
            assert status['id'] < statuses[0]['id']
            assert type(status) == type(statuses[0])
        persisted_next_json = next_statuses.to_json()
        next_statuses = Entity.from_json(persisted_next_json)
        assert type(next_statuses) == type(statuses)
        for status in next_statuses:
            assert status['id'] < statuses[0]['id']
            assert type(status) == type(statuses[0])
        previous_statuses = api.fetch_previous(next_statuses)
        assert previous_statuses
        assert type(previous_statuses) == type(statuses)
        for status in previous_statuses:
            assert status['id'] > next_statuses[-1]['id']
            assert type(status) == type(statuses[0])

@pytest.mark.vcr()
def test_fetch_next_previous_from_pagination_info(api):
    account = api.account_verify_credentials()
    with many_statuses(api):
        statuses = api.account_statuses(account['id'], limit=5)
        next_statuses = api.fetch_next(statuses._pagination_next)
        assert next_statuses
        assert type(next_statuses) == type(statuses)
        for status in next_statuses:
            assert status['id'] < statuses[0]['id']
            assert type(status) == type(statuses[0])
        previous_statuses = api.fetch_previous(next_statuses._pagination_prev)
        assert previous_statuses
        assert type(previous_statuses) == type(statuses)
        for status in previous_statuses:
            assert status['id'] > next_statuses[-1]['id']
            assert type(status) == type(statuses[0])


@pytest.mark.vcr()
def test_fetch_remaining(api3):
    with many_statuses(api3, n=30, suffix=' #'+UNLIKELY_HASHTAG):
        hashtag = api3.timeline_hashtag(UNLIKELY_HASHTAG, limit=10)
        hashtag_remaining = api3.fetch_remaining(hashtag)
        assert hashtag_remaining
        assert len(hashtag_remaining) >= 30
        for status in hashtag_remaining:
            assert UNLIKELY_HASHTAG in status['content']
            assert type(status) == type(hashtag[0])

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

@pytest.mark.vcr()
def test_get_pagination_info(api):
    account = api.account_verify_credentials()
    with many_statuses(api):
        statuses = api.account_statuses(account['id'], limit=5)
        pagination_info = api.get_pagination_info(statuses, "next")
        assert pagination_info
        assert pagination_info['max_id'] == statuses._pagination_next['max_id']
        assert isinstance(pagination_info, PaginationInfo)
        pagination_info = api.get_pagination_info(statuses, "previous")
        assert pagination_info
        assert pagination_info['min_id'] == statuses._pagination_prev['min_id']
        assert isinstance(pagination_info, PaginationInfo)
    empty_dict = {}
    assert api.get_pagination_info(empty_dict, "next") is None

@pytest.mark.vcr()
def test_pagination_iterator(api3):
    with many_statuses(api3, n=30, suffix=' #'+UNLIKELY_HASHTAG):
        hashtag = api3.timeline_hashtag(UNLIKELY_HASHTAG, limit=10)
        iterator = api3.pagination_iterator(hashtag, "next")
        assert iterator
        for status in iterator:
            print(status)
            assert UNLIKELY_HASHTAG in status['content']
            assert type(status) == type(hashtag[0])
        iterator = api3.pagination_iterator(hashtag._pagination_prev, "previous")
        assert iterator
        for status in iterator:
            print(status)
            assert UNLIKELY_HASHTAG in status['content']
            assert type(status) == type(hashtag[0])

        # Test with pagination info    
        pagination_info = hashtag._pagination_next
        iterator = api3.pagination_iterator(pagination_info, "next")
        assert iterator
        for status in iterator:
            assert UNLIKELY_HASHTAG in status['content']
            assert type(status) == type(hashtag[0])
        pagination_info = hashtag._pagination_prev
        iterator = api3.pagination_iterator(pagination_info, "previous")
        assert iterator
        for status in iterator:
            assert UNLIKELY_HASHTAG in status['content']
            assert type(status) == type(hashtag[0])
        