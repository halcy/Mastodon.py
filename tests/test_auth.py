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
        username='mastodonpy_test_2@localhost:3000',
        password='5fc638e0e53eafd9c4145b6bb852667d'
    )
    assert token

@pytest.mark.vcr()
def test_revoke(api_anonymous):
    token = api_anonymous.log_in(
        username='mastodonpy_test_2@localhost:3000',
        password='5fc638e0e53eafd9c4145b6bb852667d'
    )
    api_anonymous.revoke_access_token()

    try:
        api_anonymous.toot("illegal access detected")
        assert False
    except Exception as e:
        print(e)
        pass

    api_revoked_token = Mastodon(access_token = token)
    try:
        api_anonymous.toot("illegal access detected")
        assert False
    except Exception as e:
        print(e)
        pass

@pytest.mark.vcr()
def test_log_in_password_incorrect(api_anonymous):
    with pytest.raises(MastodonIllegalArgumentError):
        api_anonymous.log_in(
            username='admin@localhost',
            password='hunter2')

@pytest.mark.vcr()
def test_log_in_password_to_file(api_anonymous, tmpdir):
    filepath = tmpdir.join('token')
    api_anonymous.log_in(
        username='mastodonpy_test_2@localhost:3000',
        password='5fc638e0e53eafd9c4145b6bb852667d',
        to_file=str(filepath))
    token = filepath.read_text('UTF-8').rstrip().split("\n")[0]
    assert token
    api = api_anonymous
    api.access_token = token
    assert api.account_verify_credentials()

@pytest.mark.vcr()
def test_url_errors(tmpdir):
    clientid_good = tmpdir.join("clientid")
    token_good = tmpdir.join("token")
    clientid_bad = tmpdir.join("clientid_bad")
    token_bad = tmpdir.join("token_bad")
    
    clientid_good.write_text("foo\nbar\nhttps://zombo.com\n", "UTF-8")
    token_good.write_text("foo\nhttps://zombo.com\n", "UTF-8")
    clientid_bad.write_text("foo\nbar\nhttps://evil.org\n", "UTF-8")
    token_bad.write_text("foo\nhttps://evil.org\n", "UTF-8")  
    
    api = Mastodon(client_id = clientid_good, access_token = token_good)
    assert api
    assert api.api_base_url == "https://zombo.com"
    assert Mastodon(client_id = clientid_good, access_token = token_good, api_base_url = "zombo.com")
    
    with pytest.raises(MastodonIllegalArgumentError):
        Mastodon(client_id = clientid_good, access_token = token_bad, api_base_url = "zombo.com")
        
    with pytest.raises(MastodonIllegalArgumentError):
        Mastodon(client_id = clientid_bad, access_token = token_good, api_base_url = "zombo.com")
        
    with pytest.raises(MastodonIllegalArgumentError):
        Mastodon(client_id = clientid_bad, access_token = token_bad, api_base_url = "zombo.com")        

@pytest.mark.skip(reason="Not sure how to test this without setting up selenium or a similar browser automation suite to click on the allow button")
def test_log_in_code(api_anonymous):
    pass

@pytest.mark.skip(reason="Not supported by Mastodon >:@ (yet?)")
def test_log_in_refresh(api_anonymous):
    pass
