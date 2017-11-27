import pytest
from mastodon import Mastodon
from mastodon.Mastodon import MastodonIllegalArgumentError

def test_constructor_from_filenames(tmpdir):
    client = tmpdir.join('client')
    client.write_text('foo\nbar\n', 'UTF-8')
    access = tmpdir.join('access')
    access.write_text('baz\n', 'UTF-8')
    api = Mastodon(
            str(client),
            access_token = str(access))
    assert api.client_id == 'foo'
    assert api.client_secret == 'bar'
    assert api.access_token == 'baz'

def test_constructor_illegal_ratelimit():
    with pytest.raises(MastodonIllegalArgumentError):
        api = Mastodon(
                'foo', client_secret='bar',
                ratelimit_method='baz')

def test_constructor_missing_client_secret():
    with pytest.raises(MastodonIllegalArgumentError):
        api = Mastodon('foo')
