import pytest
from mastodon.Mastodon import MastodonAPIError
from time import sleep

@pytest.mark.vcr()
def test_status(status, api):
    status2 = api.status(status['id'])
    assert status2

@pytest.mark.vcr()
def test_status_empty(api):
    with pytest.raises(MastodonAPIError):
        api.status_post('')

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

@pytest.mark.vcr()
def test_toot(api):
    status = api.toot('Toot!')
    try:
        assert status
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr()
@pytest.mark.parametrize('visibility', ('', 'direct', 'private', 'unlisted', 'public',
        pytest.param('foobar', marks=pytest.mark.xfail())))
@pytest.mark.parametrize('spoiler_text', (None, 'Content warning'))
def test_status_post(api, visibility, spoiler_text):
    status = api.status_post(
            'Toot!',
            visibility=visibility,
            spoiler_text=spoiler_text)
    try:
        assert status
        if visibility:
            assert status['visibility'] == visibility
        if spoiler_text:
            assert status['spoiler_text'] == spoiler_text
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr()
def test_status_reblog_unreblog(status, api):
    reblog = api.status_reblog(status['id'])
    assert reblog

    status = reblog['reblog']
    assert status['reblogged']

    status = api.status_unreblog(status['id'])
    assert not status['reblogged']


@pytest.mark.vcr()
def test_status_fav_unfav(status, api):
    status = api.status_favourite(status['id'])
    assert status['favourited']

    status = api.status_unfavourite(status['id'])
    assert not status['favourited']


@pytest.mark.vcr()
def test_status_mute_unmute(status, api):
    status = api.status_mute(status['id'])
    assert status['muted']

    status = api.status_unmute(status['id'])
    assert not status['muted']
