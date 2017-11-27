import pytest

@pytest.fixture
def mastodon():
    import mastodon as _mastodon
    return _mastodon.Mastodon(
            api_base_url='http://localhost:3000',
            client_id='__MASTODON_PY_TEST_ID',
            client_secret='__MASTODON_PY_TEST_SECRET',
            access_token='__MASTODON_PY_TEST_TOKEN')

@pytest.fixture
def mastodon_anonymous():
    import mastodon as _mastodon
    return _mastodon.Mastodon(
            api_base_url='http://localhost:3000',
            client_id='__MASTODON_PY_TEST_ID',
            client_secret='__MASTODON_PY_TEST_SECRET')

@pytest.fixture()
def status(mastodon):
    _status = mastodon.status_post('Toot!')
    yield _status
    mastodon.status_delete(_status['id'])


@pytest.fixture()
def vcr_config():
    return dict(
            match_on = ['method', 'path', 'query', 'body'],
            decode_compressed_response = True
            )
