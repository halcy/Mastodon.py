import pytest
from mastodon.Mastodon import MastodonAPIError, MastodonNotFoundError

@pytest.mark.vcr()
def test_status(status, api):
    status2 = api.status(status['id'])
    assert status2

@pytest.mark.vcr()
def test_status_reply(status, api2):
    status2 = api2.status_reply(status, "same!")
    try:
        assert status2
        assert status2.mentions[0].id == status.account.id
    finally:
        api2.status_delete(status2['id'])
        
@pytest.mark.vcr()
def test_status_empty(api):
    with pytest.raises(MastodonAPIError):
        api.status_post('')

@pytest.mark.vcr()
def test_status_missing(api):
    with pytest.raises(MastodonNotFoundError):
        api.status(0)

# Messy and will only work if there is an internet connection that is decent, obviously.
@pytest.mark.vcr()
def test_status_card(api):
    import time
    status = api.status_post("http://example.org/")
    time.sleep(5) # Card generation may take time
    card = api.status_card(status['id'])
    try:
        assert card
    finally:
        api.status_delete(status['id'])

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
@pytest.mark.parametrize('visibility', (None, 'direct', 'private', 'unlisted', 'public',
        pytest.param('foobar', marks=pytest.mark.xfail(strict=True))))
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
def test_favourites(api):
    favs = api.favourites()
    assert isinstance(favs, list)


@pytest.mark.vcr()
def test_status_mute_unmute(status, api):
    status = api.status_mute(status['id'])
    assert status['muted']

    status = api.status_unmute(status['id'])
    assert not status['muted']
    
@pytest.mark.vcr()
def test_status_pin_unpin(status, api):
    status = api.status_pin(status['id'])
    assert status['pinned']

    status = api.status_unpin(status['id'])
    assert not status['pinned']
