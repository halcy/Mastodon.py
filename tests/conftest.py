import pytest
import os
import vcr

# Set this to True to debug issues with tests
DEBUG_REQUESTS = False

def _api(access_token='__MASTODON_PY_TEST_ACCESS_TOKEN', version="4.4.0", version_check_mode="created"):
    import mastodon
    return mastodon.Mastodon(
            api_base_url='http://localhost:3000',
            client_id='__MASTODON_PY_TEST_CLIENT_ID',
            client_secret='__MASTODON_PY_TEST_CLIENT_SECRET',
            access_token=access_token,
            mastodon_version=version,
            version_check_mode=version_check_mode,
            user_agent='tests/v311',
            debug_requests=DEBUG_REQUESTS)


@pytest.fixture
def api():
    return _api()

@pytest.fixture
def api_low_version():
    return _api(version="1.2.0", version_check_mode="changed")

@pytest.fixture
def api2():
    return _api(access_token='__MASTODON_PY_TEST_ACCESS_TOKEN_2')

@pytest.fixture
def api3():
    return _api(access_token='__MASTODON_PY_TEST_ACCESS_TOKEN_3')

@pytest.fixture
def api_anonymous():
    return _api(access_token=None)

@pytest.fixture
def status(api):
    _status = api.status_post('Toot!')
    yield _status
    api.status_delete(_status['id'])

@pytest.fixture
def status2(api):
    _status = api.status_post('Toot, too!')
    yield _status
    api.status_delete(_status['id'])

@pytest.fixture
def status3(api3):
    _status = api3.status_post('Toot, finally!')
    yield _status
    api3.status_delete(_status['id'])

@pytest.fixture(scope="module")
def vcr_config():
    return dict(
        match_on = ['method', 'path', 'query', 'body'],
        decode_compressed_response = True
    )

@pytest.fixture(scope="module")
def vcr_cassette_dir(request) -> str:
    module = request.node.fspath  # current test file
    return os.path.join(module.dirname, "cassettes")

# Fixtures for testing against actual, real servers
# Please be extremely careful with these
@pytest.fixture
def mastodon_base():
    import mastodon
    secret_file = os.path.join(os.path.dirname(__file__), '..', 'srcgen', 'base_credentials.secret')
    if os.path.exists(secret_file):
        api =  mastodon.Mastodon(
            access_token=secret_file
        )
    else:
        api = mastodon.Mastodon(
            access_token='DUMMY',
            api_base_url='https://mastodon.social'
        )
    return api

# Same, but admin. Be even more careful with these.
@pytest.fixture
def mastodon_admin():
    import mastodon    
    secret_file = os.path.join(os.path.dirname(__file__), '..', 'srcgen', 'admin_credentials.secret')
    if os.path.exists(secret_file):
        api =  mastodon.Mastodon(
            access_token=secret_file
        )
    else:
        api = mastodon.Mastodon(
            access_token='DUMMY',
            api_base_url='https://icosahedron.website'
        )
    return api
