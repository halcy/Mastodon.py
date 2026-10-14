import pytest

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
def test_collection_item_add_delete(api, api2, collection):
    account = api2.account_verify_credentials()
    result = api.collection_item_add(collection, account)

    assert isinstance(result, WrappedCollectionItem)
    assert result.collection_item.account_id == account.id

    assert isinstance(
        api.collection_item_delete(collection, result.collection_item),
        EmptyResponse,
    )
    assert all(
        item.id != result.collection_item.id
        for item in api.collection(collection).collection.items
    )


@pytest.mark.vcr()
def test_collection_item_revoke(api, api2):
    account = api2.account_verify_credentials()
    result = api.collection_create(
        name='Mastodon.py revocation test',
        discoverable=True,
        account_ids=[account],
    )

    try:
        item = result.collection.items[0]
        collections = api2.account_in_collections(account, limit=1, offset=0)
        assert isinstance(collections, Collections)
        assert any(entry.id == result.collection.id for entry in collections.collections)

        assert isinstance(
            api2.collection_item_revoke(result.collection, item),
            EmptyResponse,
        )
        collections = api2.account_in_collections(account)
        assert all(entry.id != result.collection.id for entry in collections.collections)
    finally:
        assert isinstance(api.collection_delete(result.collection), EmptyResponse)
