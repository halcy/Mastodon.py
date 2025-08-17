import pytest
from mastodon.Mastodon import MastodonAPIError, MastodonNotFoundError
import datetime
try:
    import zoneinfo
    timezone = zoneinfo.ZoneInfo
except:
    import pytz
    timezone = pytz.timezone

import vcr
import time
import pickle
import os
import sys

@pytest.mark.vcr()
def test_status(status, api):
    status2 = api.status(status['id'])
    assert status2

@pytest.mark.vcr()
def test_status_reply(status3, api2):
    status2 = api2.status_reply(status3, "same!")
    try:
        assert status2
        assert status2.mentions[0].id == status3.account.id
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
# Also, deprecated, but still a good test (Mastodon.py tries to fake the old behaviour
# internally)
@pytest.mark.vcr()
def test_status_card(api):
    import time
    status = api.status_post("http://example.org/")
    time.sleep(20) # Card generation may take time
    card = api.status_card(status['id'])
    
    try:
        assert card
        assert card.url == "http://example.org/"
    finally:
        api.status_delete(status['id'])

# Old-version card api
# skip these entirely now, 2.9.2 was a long time ago and we can't regenerate them.
@pytest.mark.skip("Skipping pre-2.9.2 tests")
def test_status_card_pre_2_9_2(api):
    if sys.version_info > (3, 9): # 3.10 and up will not load the json data and regenerating it would require a 2.9.2 instance
        pytest.skip("Test skipped for 3.10 and up")
    else:
        api._Mastodon__version_check_worked = True
        api._Mastodon__version_check_tried = True
        with vcr.use_cassette('test_status_card.yaml', cassette_library_dir='tests/cassettes_pre_2_9_2', record_mode='none'):    
            import time
            status = api.status_post("http://example.org/")
            time.sleep(5) # Card generation may take time
            api.verify_minimum_version("2.9.2", cached=True)
            card = api.status_card(status['id'])
            try:
                assert card
                assert card.url == "http://example.org/"
            finally:
                api.status_delete(status['id'])

@pytest.mark.vcr()
def test_status_context(status, api):
    context = api.status_context(status['id'])
    assert context

@pytest.mark.vcr()
def test_status_reblogged_by(api, status3, api3):
    assert api3.status_reblog(status3['id'])
    time.sleep(3)
    reblogs = api3.status_reblogged_by(status3['id'])
    assert isinstance(reblogs, list)
    assert len(reblogs) == 1
    status = api.status_post("bwooh!", visibility='private')
    assert api.status_reblog(status)
    reblogs = api.status_reblogged_by(status['id'])
    assert isinstance(reblogs, list)
    assert len(reblogs) == 0

@pytest.mark.vcr()
def test_status_reblog_visibility(api, status3, api3):
    status = api.status_post("bwooh! secret", visibility='private')
    reblog_result = api.status_reblog(status['id'], visibility = 'unlisted')
    assert reblog_result.visibility == 'private'
    reblog_result = api3.status_reblog(status3, visibility = 'unlisted')
    assert reblog_result.visibility == 'unlisted'

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

@pytest.mark.vcr(match_on=['path'])
def test_scheduled_status(api):
    base_time = datetime.datetime(4000, 1, 1, 12, 13, 14, 0, timezone("Etc/GMT+2"))
    the_future = base_time + datetime.timedelta(minutes=20)
    scheduled_toot = api.status_post("please ensure adequate headroom", scheduled_at=the_future)
    assert scheduled_toot

    the_immediate_future = base_time + datetime.timedelta(minutes=10)
    scheduled_toot_2 = api.scheduled_status_update(scheduled_toot, the_immediate_future)
    assert scheduled_toot_2
    assert scheduled_toot_2.id == scheduled_toot.id
    assert scheduled_toot_2.scheduled_at < scheduled_toot.scheduled_at

    scheduled_toot_list = api.scheduled_statuses()
    assert any(x.id == scheduled_toot_2.id for x in scheduled_toot_list)

    scheduled_toot_3 = api.scheduled_status(scheduled_toot.id)
    assert scheduled_toot_2.id == scheduled_toot_3.id

    api.scheduled_status_delete(scheduled_toot_2)
    scheduled_toot_list_2 = api.scheduled_statuses()
    assert not any(x.id == scheduled_toot_2.id for x in scheduled_toot_list_2)
    
    if os.path.exists("tests/cassettes/test_scheduled_status_datetimeobjects.pkl"):
        the_very_immediate_future = datetime.datetime.fromtimestamp(pickle.load(open("tests/cassettes/test_scheduled_status_datetimeobjects.pkl", 'rb')))
    else:
        the_very_immediate_future = datetime.datetime.now(timezone("UTC")) + datetime.timedelta(seconds=5*60+1)
        pickle.dump(the_very_immediate_future.timestamp(), open("tests/cassettes/test_scheduled_status_datetimeobjects.pkl", 'wb'))
    scheduled_toot_4 = api.status_post("please ensure adequate headroom", scheduled_at=the_very_immediate_future)
    assert scheduled_toot_4

# The following two tests need to be manually (!) ran 10 minutes apart when recording.
# Sorry, I can't think of a better way to test scheduled statuses actually work as intended.
@pytest.mark.vcr(match_on=['path'])
def test_scheduled_status_long_part1(api):
    with vcr.use_cassette('test_scheduled_status_long_part1.yaml', cassette_library_dir='tests/cassettes_special', record_mode='once'):  
        if os.path.exists("tests/cassettes_special/test_scheduled_status_long_datetimeobjects.pkl"):
            the_medium_term_future = datetime.datetime.fromtimestamp(pickle.load(open("tests/cassettes_special/test_scheduled_status_long_datetimeobjects.pkl", 'rb')))
        else:
            the_medium_term_future = datetime.datetime.now() + datetime.timedelta(minutes=6)
            pickle.dump(the_medium_term_future.timestamp(), open("tests/cassettes_special/test_scheduled_status_long_datetimeobjects.pkl", 'wb'))
        scheduled_toot = api.status_post(f"please ensure maximum headroom at {the_medium_term_future}", scheduled_at=the_medium_term_future)
        scheduled_toot_list = api.scheduled_statuses()
        assert any(x.id == scheduled_toot.id for x in scheduled_toot_list)
        pickle.dump(scheduled_toot.params.text, open("tests/cassettes_special/test_scheduled_status_long_text.pkl", 'wb'))

@pytest.mark.vcr(match_on=['path'])    
def test_scheduled_status_long_part2(api):
        with vcr.use_cassette('test_scheduled_status_long_part2.yaml', cassette_library_dir='tests/cassettes_special', record_mode='once'):
            text = pickle.load(open("tests/cassettes_special/test_scheduled_status_long_text.pkl", 'rb'))
            statuses = api.timeline_home()
            print(text)
            found_status = False
            for status in statuses:
                if text in status.content:
                    found_status = True
            assert found_status

@pytest.mark.vcr()
def test_status_edit(api3, api2):
    status = api3.status_post("the best editor? why, of course it is VS Code")
    edit_list_1 = api2.status_history(status)
    status_edited = api3.status_update(status, "the best editor? why, of course it is the KDE Advanced Text Editor, Kate")
    status_result = api2.status(status)
    edit_list_2 = api2.status_history(status)

    assert len(edit_list_1) == 1
    assert len(edit_list_2) == 2
    assert "the best editor? why, of course it is the KDE Advanced Text Editor, Kate" in status_result.content

    source = api2.status_source(status)
    assert source.text == "the best editor? why, of course it is the KDE Advanced Text Editor, Kate"
    
@pytest.mark.vcr(match_on=['path'])
def test_status_update_with_media_edit(api2):
    media = api2.media_post(
        'tests/video.mp4',
        description="Original description",
        focus=(-0.5, 0.3),
        thumbnail='tests/amewatson.jpg'
    )
    
    assert media
    assert media.url is None
    
    time.sleep(5)
    media2 = api2.media(media)
    assert media2.id == media.id
    assert media2.url is not None

    status = api2.status_post(
        'Initial post with media',
        media_ids=media2
    )
    
    assert status
    assert status['media_attachments'][0]['description'] == "Original description"
    assert status['media_attachments'][0]['meta']['focus']['x'] == -0.5
    assert status['media_attachments'][0]['meta']['focus']['y'] == 0.3

    try:
        updated_media_attributes = api2.generate_media_edit_attributes(
            id=media2.id,
            description="Updated description",
            focus=(0.2, -0.1),
            thumbnail='tests/image.jpg'
        )
        
        updated_status = api2.status_update(
            status['id'],
            "I have altered the media attachment. Pray I do not alter it further.",
            media_attributes=[updated_media_attributes]
        )
        
        assert updated_status
        assert updated_status['media_attachments'][0]['description'] == "Updated description"
        assert updated_status['media_attachments'][0]['meta']['focus']['x'] == 0.2
        assert updated_status['media_attachments'][0]['meta']['focus']['y'] == -0.1
        assert updated_status['media_attachments'][0]['preview_url'] != status['media_attachments'][0]['preview_url']
    finally:
        api2.status_delete(status['id'])

@pytest.mark.vcr()
def test_status_translate(api, status):
    # our test server does not support translation, so this will raise a MastodonAPIError
    with pytest.raises(MastodonAPIError):
        translation = api.status_translate(status['id'], 'de')
        
@pytest.mark.vcr(match_on=['path'])   
def test_status_delete_media(api, status):
    # Prepare a status with media
    try:
        media = api.media_post('tests/image.jpg')
        status_with_media = api.status_post('Status with media', media_ids=media)

        # Delete it without media wipe
        deleted_status = api.status_delete(status_with_media['id'], delete_media=False)
        assert deleted_status['id'] == status_with_media['id']
        print(deleted_status.media_attachments[0].id)

        time.sleep(5)  # Wait for media deletion to be processed

        # Now repost and delete it with media wipe
        status_with_media = api.status_post('Status with media reposted', media_ids=[deleted_status.media_attachments[0].id])
        deleted_status = api.status_delete(status_with_media['id'], delete_media=True)
        assert deleted_status['id'] == status_with_media['id']

        time.sleep(5)  # Wait for media deletion to be processed

        # Check that the media is deleted by trying to repost again (should fail)
        with pytest.raises(MastodonAPIError):
            api.status_post('Trying to repost deleted media', media_ids=status_with_media['media_attachments'][0].id)
    finally:
        # Delete status if it exists
        try:
            api.status_delete(status_with_media['id'])
        except:
            pass

