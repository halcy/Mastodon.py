import pytest

def _api(access_token='__MASTODON_PY_TEST_ACCESS_TOKEN'):
    import mastodon
    return mastodon.Mastodon(
            api_base_url='http://localhost:3000',
            client_id='__MASTODON_PY_TEST_CLIENT_ID',
            client_secret='__MASTODON_PY_TEST_CLIENT_SECRET',
            access_token=access_token,
            mastodon_version="2.0.0")


@pytest.fixture
def api():
    return _api()


@pytest.fixture
def api2():
    return _api(access_token='__MASTODON_PY_TEST_ACCESS_TOKEN_2')


@pytest.fixture
def api_anonymous():
    return _api(access_token=None)

@pytest.fixture()
def status(api):
    _status = api.status_post('Toot!')
    yield _status
    api.status_delete(_status['id'])


@pytest.fixture()
def vcr_config():
    return dict(
            match_on = ['method', 'path', 'query', 'body'],
            decode_compressed_response = True
            )
