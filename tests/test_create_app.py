from mastodon import Mastodon
import pytest
import requests
import time

try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock

def test_create_app(mocker, to_file=None, redirect_uris=None, website=None):
    # there is no easy way to delete an anonymously created app so
    # instead we mock Requests
    resp = Mock()
    resp.json = Mock(return_value=dict(
            client_id='foo',
            client_secret='bar',
        ))
    mocker.patch('requests.post', return_value=resp)

    app = Mastodon.create_app("Mastodon.py test suite",
            api_base_url="example.com",
            to_file=to_file,
            redirect_uris=redirect_uris,
            website=website
            )

    assert app == ('foo', 'bar')
    assert requests.post.called

def test_create_app_to_file(mocker, tmpdir):
    filepath = tmpdir.join('credentials')
    test_create_app(mocker, to_file=str(filepath))
    assert filepath.read_text('UTF-8') == "foo\nbar\nhttps://example.com\nMastodon.py test suite\n"

def test_create_app_redirect_uris(mocker):
    test_create_app(mocker, redirect_uris='http://example.net')
    kwargs = requests.post.call_args[1]
    assert kwargs['data']['redirect_uris'] == 'http://example.net'

def test_create_app_website(mocker):
    test_create_app(mocker, website='http://example.net')
    kwargs = requests.post.call_args[1]
    assert kwargs['data']['website'] == 'http://example.net'

@pytest.mark.vcr()
def test_app_verify_credentials(api):
    app = api.app_verify_credentials()
    assert app
    assert app.name == 'Mastodon.py test suite'
    
@pytest.mark.vcr(match_on=['path'])
def test_app_account_create():    
    # This leaves behind stuff on the test server, which is unfortunate, but eh.
    suffix = str(time.time()).replace(".", "")[-5:]
    
    test_app = test_app = Mastodon.create_app(
        "mastodon.py generated test app", 
        api_base_url="http://localhost:3000/"
    )
    
    test_app_api = Mastodon(
        test_app[0], 
        test_app[1], 
        api_base_url="http://localhost:3000/"
    )
    test_token = test_app_api.create_account("coolguy" + suffix, "swordfish", "email@localhost" + suffix, agreement=True)
    assert test_token
    
