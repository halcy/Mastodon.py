import pytest

@pytest.mark.vcr(match_on=['path'])
@pytest.mark.parametrize('sensitive', (False, True))
def test_media_post(api, sensitive):
    media = api.media_post(
            'tests/image.jpg',
            description="John Lennon doing a funny walk")

    assert media

    status = api.status_post(
            'LOL check this out',
            media_ids=[media],
            sensitive=sensitive
            )

    assert status

    try:
        assert status['sensitive'] == sensitive
        assert status['media_attachments']
        assert status['media_attachments'][0]['description']
    finally:
        api.status_delete(status['id'])

@pytest.mark.vcr(match_on=['path'])
def test_media_post_file(api):
    with open('tests/image.jpg', 'rb') as f:
        media = api.media_post(f, mime_type='image/jpeg')
        assert media
