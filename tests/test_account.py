import pytest
from mastodon.Mastodon import MastodonAPIError

@pytest.mark.vcr()
def test_account(api):
    account = api.account(1)
    assert account


@pytest.mark.vcr()
def test_account_following(api):
    following = api.account_following(1)
    assert isinstance(following, list)


@pytest.mark.vcr()
def test_account_followers(api):
    followers = api.account_followers(1)
    assert isinstance(followers, list)


@pytest.mark.vcr()
def test_account_relationships(api):
    relationships = api.account_relationships(1)
    assert isinstance(relationships, list)
    assert len(relationships) == 1


@pytest.mark.vcr()
def test_account_search(api):
    results = api.account_search('admin')
    assert isinstance(results, list)


@pytest.mark.vcr()
def test_account_follow_unfollow(api):
    relationship = api.account_follow(1)
    try:
        assert relationship
        assert relationship['following']
    finally:
        relationship = api.account_unfollow(1)
        assert relationship
        assert not relationship['following']


@pytest.mark.vcr()
def test_account_block_unblock(api):
    relationship = api.account_block(1)
    try:
        assert relationship
        assert relationship['blocking']
    finally:
        relationship = api.account_unblock(1)
        assert relationship
        assert not relationship['blocking']


@pytest.mark.vcr()
def test_account_mute_unmute(api):
    relationship = api.account_mute(1)
    try:
        assert relationship
        assert relationship['muting']
    finally:
        relationship = api.account_unmute(1)
        assert relationship
        assert not relationship['muting']


@pytest.mark.vcr()
def test_mutes(api):
    mutes = api.mutes()
    assert isinstance(mutes, list)


@pytest.mark.vcr()
def test_blocks(api):
    blocks = api.blocks()
    assert isinstance(blocks, list)


@pytest.mark.vcr()
def test_account_update_credentials(api):
    import base64
    with open('tests/image.jpg', 'rb') as f:
        image = f.read()
    b64_image = base64.b64encode(image)
    data_uri = b'data:image/jpeg;base64,' + b64_image

    account = api.account_update_credentials(
            display_name='John Lennon',
            note='I walk funny',
            avatar = data_uri,
            header = data_uri)
    assert account
