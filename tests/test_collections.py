import pytest
import time

from mastodon.return_types import CollectionWithAccounts, Collections, WrappedCollection, WrappedCollectionItem
from mastodon.types_base import EmptyResponse


@pytest.fixture
def collection(api):
    result = api.collection_create(
        name='my favourite accounts',
        description='beep boop',
        language='en',
        tag_name='#mastodonpy',
        sensitive=False,
        discoverable=True,
    )
    yield result.collection
    assert isinstance(api.collection_delete(result.collection), EmptyResponse)


@pytest.mark.vcr()
def test_collection_lifecycle(api, collection):
    assert isinstance(api.collection_update(
        collection,
        name='my LEAST favourite accounts',
        description='friendship ended with robots',
        language='en',
        tag_name='#mastodonpy',
        sensitive=True,
        discoverable=False,
    ), WrappedCollection)

    result = api.collection(collection)
    assert isinstance(result, CollectionWithAccounts)
    assert result.collection.name == 'my LEAST favourite accounts'
    assert result.collection.sensitive is True
    assert result.collection.discoverable is False

    collections = api.account_collections(
        api.account_verify_credentials(), limit=1, offset=0)
    assert isinstance(collections, Collections)
    assert any(item.id == collection.id for item in collections.collections)


@pytest.mark.vcr()
def test_collection_item_add_delete(api, api3, collection):
    account = api3.account_verify_credentials()
    result = api.collection_item_add(collection, account)

    assert isinstance(result, WrappedCollectionItem)
    assert result.collection_item.account_id == account.id

    assert isinstance(
        api.collection_item_delete(collection, result.collection_item),
        EmptyResponse,
    )
    assert all(
        item.id != result.collection_item.id
        for item in api.collection(collection).collection.collection_items
    )


@pytest.mark.vcr()
def test_collection_item_revoke(api, api3):
    account = api3.account_verify_credentials()
    result = api.collection_create(
        name='Mastodon.py revocation test',
        sensitive=False,
        discoverable=True,
        account_ids=[account],
    )

    try:
        item = result.collection.collection_items[0]
        collections = api3.account_in_collections(account, limit=1, offset=0)
        assert isinstance(collections, Collections)
        assert any(entry.id == result.collection.id for entry in collections.collections)

        assert isinstance(
            api3.collection_item_revoke(result.collection, item),
            EmptyResponse,
        )
        collections = api3.account_in_collections(account)
        assert all(
            collection_item.id != item.id
            for entry in collections.collections
            for collection_item in entry.collection_items
        )
    finally:
        assert isinstance(api.collection_delete(result.collection), EmptyResponse)


@pytest.mark.parametrize('flags', [{}, {'sensitive': True, 'discoverable': True}])
def test_collection_create_boolean_defaults(api, requests_mock, flags):
    from urllib.parse import parse_qs

    requests_mock.post('http://localhost:3000/api/v1/collections', json={
        'collection': {'id': '123', 'name': 'Example'},
    })
    api.collection_create('Example', **flags)
    params = parse_qs(requests_mock.last_request.text)
    expected = '1' if flags else '0'
    assert params['sensitive'] == [expected]
    assert params['discoverable'] == [expected]


def test_collection_update_omits_unspecified_booleans(api, requests_mock):
    from urllib.parse import parse_qs

    requests_mock.patch('http://localhost:3000/api/v1/collections/123', json={
        'collection': {'id': '123', 'name': 'Renamed'},
    })
    api.collection_update('123', name='Renamed')
    params = parse_qs(requests_mock.last_request.text)
    assert params['name'] == ['Renamed']
    assert 'sensitive' not in params
    assert 'discoverable' not in params


@pytest.mark.vcr()
def test_collection_notification_fallback(api, api3, collection):
    from mastodon.return_types import NotificationFallback

    account = api3.account_verify_credentials()
    api.collection_item_add(collection, account)
    notification = None
    try:
        for attempt in range(15):
            notifications = api3.notifications(
                types=['added_to_collection'], supported_types=['follow'], limit=40,
            )
            notification = next((
                candidate for candidate in notifications
                if candidate.collection is not None and candidate.collection.id == collection.id
            ), None)
            if notification is not None:
                break
            time.sleep(2)

        assert notification is not None, 'Collection notification was not delivered within 30 seconds'
        assert notification.type == 'added_to_collection'
        assert notification.account.id == collection.account_id
        assert isinstance(notification.fallback, NotificationFallback)
        assert isinstance(notification.fallback.title, str)
        assert notification.fallback.title

        single = api3.notifications(notification, supported_types=['follow'])
        assert isinstance(single.fallback, NotificationFallback)
        assert single.fallback == notification.fallback
        supported = api3.notifications(notification, supported_types=['added_to_collection'])
        assert supported.fallback is None
    finally:
        if notification is not None:
            api3.notifications_dismiss(notification)
