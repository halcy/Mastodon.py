import pytest
from mastodon.Mastodon import MastodonAPIError

@pytest.mark.vcr()
def test_status(status, api):
    status2 = api.status(status['id'])
    assert status2 == status

@pytest.mark.vcr()
def test_status_missing(api):
    with pytest.raises(MastodonAPIError):
        api.status(0)

@pytest.mark.skip(reason="Doesn't look like mastodon will make a card for an url that doesn't have a TLD, and relying on some external website being reachable to make a card of is messy :/")
def test_status_card(api):
    status = api.status_post("http://localhost:3000")
    card = api.status_card(status['id'])
    assert card

@pytest.mark.vcr()
def test_status_context(status, api):
    context = api.status_context(status['id'])
    assert context

@pytest.mark.vcr()
def test_status_reblogged_by(status, api):
    api.status_reblog(status['id'])
    reblogs = api.status_reblogged_by(status['id'])
    assert reblogs

@pytest.mark.vcr()
def test_status_favourited_by(status, api):
    api.status_favourite(status['id'])
    favourites = api.status_favourited_by(status['id'])
    assert favourites
