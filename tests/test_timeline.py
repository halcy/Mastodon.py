import pytest

@pytest.mark.vcr()
def test_public_tl_anonymous(mastodon_anonymous, status):
    tl = mastodon_anonymous.timeline_public()
    assert status['id'] in map(lambda st: st['id'], tl)
    # although tempting, we can't do
    #     assert status in tl
    # because the statuses returned in the tl have additional
    # pagination-related attributes

@pytest.mark.vcr()
def test_public_tl(mastodon, status):
    tl = mastodon.timeline_public()
    print(tl[0])
    assert status['id'] in map(lambda st: st['id'], tl)

@pytest.mark.vcr()
def test_home_tl(mastodon, status):
    tl = mastodon.timeline_home()
    assert status['id'] in map(lambda st: st['id'], tl)

@pytest.mark.vcr()
def test_hashtag_tl(mastodon):
    status = mastodon.status_post('#hoot (hashtag toot)')
    tl = mastodon.timeline_hashtag('hoot')
    try:
        assert status['id'] in map(lambda st: st['id'], tl)
    finally:
        mastodon.status_delete(status['id'])
