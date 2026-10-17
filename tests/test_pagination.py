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


@pytest.mark.vcr()
def test_offset_navigation(api):
    from mastodon.types_base import PaginatableList

    first = api.account_search('admin', limit=1)
    assert isinstance(first, PaginatableList)
    assert len(first) == 1
    assert isinstance(first._pagination_next, PaginationInfo)
    assert api.fetch_previous(first) is None

    restored = Entity.from_json(first.to_json())
    assert isinstance(restored._pagination_next, PaginationInfo)
    second = api.fetch_next(api.get_pagination_info(restored, 'next'))
    expected = api.account_search('admin', limit=1, offset=1)
    assert [account.id for account in second] == [account.id for account in expected]
    assert isinstance(second._pagination_prev, PaginationInfo)
    previous = api.fetch_previous(second)
    assert [account.id for account in previous] == [account.id for account in first]


@pytest.mark.vcr()
def test_offset_iteration(api):
    expected = api.account_search('admin')
    assert len(expected) == 2
    first = api.account_search('admin', limit=1)
    expected_ids = [account.id for account in expected]

    remaining = api.fetch_remaining(first)
    assert [account.id for account in remaining] == expected_ids
    assert [account.id for account in api.pagination_iterator(first)] == expected_ids
    assert [account.id for account in api.pagination_iterator(first._pagination_next)] == expected_ids[1:]

    second = api.fetch_next(first)
    empty = api.fetch_next(second)
    assert empty == []
    assert api.fetch_next(empty) is None
    previous = api.fetch_previous(Entity.from_json(empty.to_json()))
    assert [account.id for account in previous] == [account.id for account in second]


@pytest.mark.vcr()
@pytest.mark.parametrize('method', ['search', 'search_v2'])
def test_search_offset_navigation(api, method):
    from mastodon.return_types import SearchV2

    search = getattr(api, method)
    first = search('admin', result_type='accounts', limit=1)
    assert isinstance(first, SearchV2)
    assert '_pagination_next' not in first
    assert '_pagination_prev' not in first
    assert len(first.accounts) == 1
    assert first.statuses == []
    assert isinstance(first._pagination_next, PaginationInfo)
    assert api.fetch_previous(first) is None

    restored = Entity.from_json(first.to_json())
    second = api.fetch_next(restored)
    expected = search('admin', result_type='accounts', limit=1, offset=1)
    assert isinstance(second, SearchV2)
    assert [account.id for account in second.accounts] == [account.id for account in expected.accounts]
    assert len(second.accounts) == 1
    previous = api.fetch_previous(second)
    assert [account.id for account in previous.accounts] == [account.id for account in first.accounts]
    empty = api.fetch_next(second)
    assert empty.accounts == []
    assert api.fetch_next(empty) is None
    assert api.fetch_previous(empty).accounts[0].id == second.accounts[0].id

    untyped = search('admin', limit=1)
    assert api.fetch_next(untyped) is None
    assert api.fetch_previous(untyped) is None


@pytest.mark.vcr()
@pytest.mark.parametrize('method', ['account_collections', 'account_in_collections'])
def test_collections_offset_navigation(api, api3, method):
    from mastodon.return_types import Collections

    owner = api.account_verify_credentials()
    member = api3.account_verify_credentials()
    collections = []
    try:
        for i in range(2):
            result = api.collection_create(
                name='Pagination test ' + str(i), sensitive=False,
                discoverable=True, account_ids=[member])
            collections.append(result.collection)
        reader = api if method == 'account_collections' else api3
        account = owner if method == 'account_collections' else member
        fetch = getattr(reader, method)
        first = fetch(account, limit=1)
        assert isinstance(first, Collections)
        assert '_pagination_next' not in first
        assert '_pagination_prev' not in first
        assert len(first.collections) == 1
        assert isinstance(first._pagination_next, PaginationInfo)
        second = reader.fetch_next(Entity.from_json(first.to_json()))
        expected = fetch(account, limit=1, offset=1)
        assert isinstance(second, Collections)
        assert len(second.collections) == 1
        assert [item.id for item in second.collections] == [item.id for item in expected.collections]
        assert second.collections[0].id != first.collections[0].id
        previous = reader.fetch_previous(second)
        assert previous.collections[0].id == first.collections[0].id
        empty = fetch(account, offset=1000000, limit=1)
        assert empty.collections == []
        assert reader.fetch_next(empty) is None
    finally:
        for collection in collections:
            api.collection_delete(collection)


@pytest.mark.vcr()
@pytest.mark.parametrize('wrapped', [False, True])
def test_pagination_page_iterator(api, wrapped):
    from mastodon.errors import MastodonIllegalArgumentError

    if wrapped:
        first = api.search_v2('admin', result_type='accounts', limit=1)
        entries = lambda page: page.accounts
    else:
        first = api.account_search('admin', limit=1)
        entries = lambda page: page

    pages = list(api.pagination_page_iterator(first))
    assert len(pages) == 3
    assert pages[0] is first
    assert [len(entries(page)) for page in pages] == [1, 1, 0]
    assert entries(pages[0])[0].id != entries(pages[1])[0].id
    assert all(type(page) is type(first) for page in pages)

    backwards = list(api.pagination_page_iterator(pages[1], direction='previous'))
    assert [entries(page)[0].id for page in backwards] == [entries(pages[1])[0].id, entries(first)[0].id]
    resumed = list(api.pagination_page_iterator(api.get_pagination_info(first, 'next'), return_pagination_info=True))
    assert [len(entries(page)) for page, info in resumed] == [1, 0]
    assert isinstance(resumed[0][1], PaginationInfo)
    assert resumed[1][1] is None
    previous_info = api.get_pagination_info(pages[1], 'previous')
    resumed_backwards = list(api.pagination_page_iterator(previous_info, direction='previous', return_pagination_info=True))
    assert len(resumed_backwards) == 1
    assert entries(resumed_backwards[0][0])[0].id == entries(first)[0].id
    assert resumed_backwards[0][1] is None
    with pytest.raises(MastodonIllegalArgumentError):
        list(api.pagination_page_iterator(first, direction='invalid'))


@pytest.mark.vcr()
def test_collections_page_iterator(api, api3):
    from mastodon.return_types import Collections

    member = api3.account_verify_credentials()
    created = []
    try:
        for i in range(2):
            created.append(api.collection_create(
                name='Page iterator test ' + str(i), sensitive=False,
                discoverable=True, account_ids=[member]).collection)
        first = api.account_collections(api.account_verify_credentials(), limit=1)
        pages = list(api.pagination_page_iterator(first))
        assert all(isinstance(page, Collections) for page in pages)
        ids = [item.id for page in pages for item in page.collections]
        assert all(collection.id in ids for collection in created)
        assert len(ids) == len(set(ids))
        assert api.get_pagination_info(pages[-1], 'next') is None
    finally:
        for collection in created:
            api.collection_delete(collection)


@pytest.mark.vcr()
def test_grouped_notifications_page_iterator(api, api2):
    import time
    from itertools import islice
    from mastodon.return_types import GroupedNotificationsResults

    posted = []
    try:
        username = api.account_verify_credentials().username
        for i in range(2):
            posted.append(api2.status_post('@' + username + ' page iterator test ' + str(i), visibility='public'))
        time.sleep(5)
        first = api.grouped_notifications(limit=1, types=['mention'], expand_accounts='full')
        pages = list(islice(api.pagination_page_iterator(first), 2))
        assert len(pages) == 2
        assert all(isinstance(page, GroupedNotificationsResults) for page in pages)
        assert all(len(page.notification_groups) == 1 for page in pages)
        assert pages[0].notification_groups[0].group_key != pages[1].notification_groups[0].group_key
        for page in pages:
            status_ids = [status.id for status in page.statuses]
            assert page.notification_groups[0].status_id in status_ids
            assert page.accounts
    finally:
        for status in posted:
            api2.status_delete(status)
