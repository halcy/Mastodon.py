import pytest

@pytest.mark.vcr(match_on=['path'])
@pytest.mark.parametrize('sensitive', (False, True))
def test_media_post(api, sensitive):
    media = api.media_post(
            'tests/image.jpg',
            description="John Lennon doing a funny walk",
            focus=(-0.5, 0.3))
    
    assert media

    status = api.status_post(
            'LOL check this out',
            media_ids=media,
            sensitive=sensitive
            )

    assert status

    try:
        assert status['sensitive'] == sensitive
        assert status['media_attachments']
        assert status['media_attachments'][0]['description'] == "John Lennon doing a funny walk"
        assert status['media_attachments'][0]['meta']['focus']['x'] == -0.5
        assert status['media_attachments'][0]['meta']['focus']['y'] == 0.3
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr(match_on=['path'])
def test_media_update(api):
    media = api.media_post(
            'tests/image.jpg',
            description="John Lennon doing a funny walk",
            focus=(-0.5, 0.3))
    
    assert media

    media_up = api.media_update(
            media,
            description="John Lennon doing a cool walk",
            focus=(0.69, 0.69))

    assert media_up
    assert media_up['description'] == "John Lennon doing a cool walk"
    assert media_up['meta']['focus']['x'] == 0.69
    assert media_up['meta']['focus']['y'] == 0.69

@pytest.mark.vcr(match_on=['path'])
def test_media_post_file(api):
    with open('tests/image.jpg', 'rb') as f:
        media = api.media_post(f, mime_type='image/jpeg')
        assert media
