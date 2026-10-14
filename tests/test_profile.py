import pytest

from mastodon.return_types import Profile


@pytest.mark.vcr()
def test_profile(api):
    profile = api.profile()

    assert isinstance(profile, Profile)
    assert profile.id == api.account_verify_credentials().id


@pytest.mark.vcr()
def test_profile_update(api):
    original = api.profile()
    with open('tests/image.jpg', 'rb') as image_file:
        image = image_file.read()

    try:
        profile = api.profile_update(
            display_name='Raw John Lennon',
            note='I love doing a raw funny walk',
            avatar='tests/image.jpg',
            avatar_description='me doing a funny walk',
            header=image,
            header_mime_type='image/jpeg',
            header_description='me doing a funny walk in larger',
            locked=True,
            bot=True,
            discoverable=True,
            hide_collections=True,
            indexable=True,
            show_media=False,
            show_media_replies=False,
            show_featured=False,
            attribution_domains=['example.com'],
            fields=[('best beatle', 'john lennon')],
        )

        assert isinstance(profile, Profile)
        assert profile.display_name == 'Raw John Lennon'
        assert profile.note == 'I love doing a raw funny walk'
        assert profile.avatar_description == 'me doing a funny walk'
        assert profile.header_description == 'me doing a funny walk in larger'
        assert profile.locked is True
        assert profile.bot is True
        assert profile.discoverable is True
        assert profile.hide_collections is True
        assert profile.indexable is True
        assert profile.show_media is False
        assert profile.show_media_replies is False
        assert profile.show_featured is False
        assert profile.attribution_domains == ['example.com']
        assert profile.fields[0].name == 'best beatle'
        assert profile.fields[0].value == 'john lennon'

        profile_retrieved = api.profile()
        assert isinstance(profile_retrieved, Profile)
        assert profile_retrieved.display_name == 'Raw John Lennon'
        assert profile_retrieved.note == 'I love doing a raw funny walk'
        assert profile_retrieved.avatar_description == 'me doing a funny walk'
        assert profile_retrieved.header_description == 'me doing a funny walk in larger'
        assert profile_retrieved.locked is True
        assert profile_retrieved.bot is True
        assert profile_retrieved.discoverable is True
        assert profile_retrieved.hide_collections is True
        assert profile_retrieved.indexable is True
        assert profile_retrieved.show_media is False
        assert profile_retrieved.show_media_replies is False
        assert profile_retrieved.show_featured is False
        assert profile_retrieved.attribution_domains == ['example.com']
        assert profile_retrieved.fields[0].name == 'best beatle'
        assert profile_retrieved.fields[0].value == 'john lennon'
    finally:
        api.profile_update(
            display_name=original.display_name,
            note=original.note,
            locked=original.locked,
            bot=original.bot,
            discoverable=original.discoverable,
            hide_collections=original.hide_collections,
            indexable=original.indexable,
            show_media=original.show_media,
            show_media_replies=original.show_media_replies,
            show_featured=original.show_featured,
            attribution_domains=original.attribution_domains,
            fields=[(field.name, field.value) for field in original.fields],
        )
        api.account_delete_avatar()
        api.account_delete_header()
