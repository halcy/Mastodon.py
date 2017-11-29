from mastodon import Mastodon
import pytest
import requests
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
    assert filepath.read_text('UTF-8') == "foo\nbar\n"

def test_create_app_redirect_uris(mocker):
    test_create_app(mocker, redirect_uris='http://example.net')
    kwargs = requests.post.call_args[1]
    assert kwargs['data']['redirect_uris'] == 'http://example.net'

def test_create_app_website(mocker):
    test_create_app(mocker, website='http://example.net')
    kwargs = requests.post.call_args[1]
    assert kwargs['data']['website'] == 'http://example.net'
