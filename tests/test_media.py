import pytest
import vcr
import time

@pytest.mark.vcr(match_on=['path'])
def test_media_post_v1(api):
    with vcr.use_cassette('test_media_post.yaml', cassette_library_dir='tests/cassettes_pre_4_0_0', record_mode='none'):
        media = api.media_post(
                'tests/image.jpg',
                description="John Lennon doing a funny walk",
                focus=(-0.5, 0.3))
        
        assert media

        status = api.status_post(
                'LOL check this out',
                media_ids=media,
                sensitive=False
                )

        assert status

        try:
            assert status['sensitive'] == False
            assert status['media_attachments']
            assert status['media_attachments'][0]['description'] == "John Lennon doing a funny walk"
            assert status['media_attachments'][0]['meta']['focus']['x'] == -0.5
            assert status['media_attachments'][0]['meta']['focus']['y'] == 0.3
        finally:
            api.status_delete(status['id'])

@pytest.mark.vcr(match_on=['path'])
@pytest.mark.parametrize('sensitive', (False, True))
def test_media_post(api, sensitive):
    media = api.media_post(
        'tests/video.mp4',
        description="me when a cat",
        focus=(-0.5, 0.3),
        thumbnail='tests/amewatson.jpg'
    )
    
    assert media
    assert media.url is None

    time.sleep(10)
    media2 = api.media(media)
    assert media2.id == media.id
    assert not media2.url is None

    status = api.status_post(
        'LOL check this out',
        media_ids=media2,
        sensitive=sensitive
    )

    assert status

    try:
        assert status['sensitive'] == sensitive
        assert status['media_attachments']
        assert status['media_attachments'][0]['description'] == "me when a cat"
        assert status['media_attachments'][0]['meta']['focus']['x'] == -0.5
        assert status['media_attachments'][0]['meta']['focus']['y'] == 0.3
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr(match_on=['path'])
def test_media_post_multiple(api):
    media = api.media_post(
            'tests/image.jpg',
            description="John Lennon doing a funny walk",
            focus=(-0.5, 0.3),
            synchronous=True)
    media2 = api.media_post(
            'tests/amewatson.jpg',
            description="hololives #1 detective, watson ameliachan",
            focus=(0.5, 0.5),
            synchronous=True)

    assert media
    assert media.url is not None
    assert media2
    assert media2.url is not None

    status = api.status_post(
            'LOL check this out',
            media_ids=[media, media2.id],
            )

    assert status

    try:
        assert status['media_attachments']
        assert status['media_attachments'][0]['description'] == "John Lennon doing a funny walk"
        assert status['media_attachments'][0]['meta']['focus']['x'] == -0.5
        assert status['media_attachments'][0]['meta']['focus']['y'] == 0.3
        assert status['media_attachments'][1]['description'] == "hololives #1 detective, watson ameliachan"
        assert status['media_attachments'][1]['meta']['focus']['x'] == 0.5
        assert status['media_attachments'][1]['meta']['focus']['y'] == 0.5
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr(match_on=['path'])
def test_media_update(api):
    media = api.media_post(
        'tests/video.mp4',
        description="me when a cat",
        focus=(-0.5, 0.3)
    )
    
    assert media

    media_up = api.media_update(
        media,
        description="John Lennon doing a cool walk",
        focus=(0.69, 0.69),
        thumbnail='tests/amewatson.jpg'
    )

    assert media_up
    assert media_up['description'] == "John Lennon doing a cool walk"
    assert media_up['meta']['focus']['x'] == 0.69
    assert media_up['meta']['focus']['y'] == 0.69

@pytest.mark.vcr(match_on=['path'])
def test_media_post_file(api):
    with open('tests/image.jpg', 'rb') as f:
        media = api.media_post(f, mime_type='image/jpeg')
        assert media
