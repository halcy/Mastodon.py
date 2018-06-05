import pytest
from mastodon.Mastodon import MastodonIllegalArgumentError
from mastodon import Mastodon
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs


def test_auth_request_url(api):
    url = api.auth_request_url()
    parse = urlparse(url)
    assert parse.path == '/oauth/authorize'
    query = parse_qs(parse.query)
    assert query['client_id'][0] == api.client_id
    assert query['response_type'][0] == 'code'
    assert query['redirect_uri'][0] == 'urn:ietf:wg:oauth:2.0:oob'
    assert set(query['scope'][0].split()) == set(('read', 'write', 'follow', 'push'))


def test_log_in_none(api_anonymous):
    with pytest.raises(MastodonIllegalArgumentError):
        api_anonymous.log_in()


@pytest.mark.vcr()
def test_log_in_password(api_anonymous):
    token = api_anonymous.log_in(
        username='admin@localhost:3000',
        password='mastodonadmin')
    assert token


@pytest.mark.vcr()
def test_log_in_password_incorrect(api_anonymous):
    with pytest.raises(MastodonIllegalArgumentError):
        api_anonymous.log_in(
            username='admin@localhost:3000',
            password='hunter2')


@pytest.mark.vcr()
def test_log_in_password_to_file(api_anonymous, tmpdir):
    filepath = tmpdir.join('token')
    api_anonymous.log_in(
        username='admin@localhost:3000',
        password='mastodonadmin',
        to_file=str(filepath))
    token = filepath.read_text('UTF-8').rstrip()
    assert token
    api = api_anonymous
    api.access_token = token
    assert api.account_verify_credentials()


@pytest.mark.skip(reason="Not sure how to test this without setting up selenium or a similar browser automation suite to click on the allow button")
def test_log_in_code(api_anonymous):
    pass


@pytest.mark.skip(reason="Not supported by Mastodon >:@ (yet?)")
def test_log_in_refresh(api_anonymous):
    pass
