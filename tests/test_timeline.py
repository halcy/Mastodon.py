import pytest
import time
from mastodon.Mastodon import MastodonAPIError,\
                              MastodonIllegalArgumentError,\
                              MastodonUnauthorizedError

@pytest.mark.vcr()
def test_public_tl_anonymous(api_anonymous, status3):
    time.sleep(3)
    tl = api_anonymous.timeline_public()
    assert status3['id'] in list(map(lambda st: st['id'], tl))

@pytest.mark.vcr()
def test_public_tl(api, status):
    public = api.timeline_public()
    local = api.timeline_local()
    assert status['id'] in map(lambda st: st['id'], public)
    assert status['id'] in map(lambda st: st['id'], local)

@pytest.mark.vcr()
def test_unauthed_home_tl_throws(api_anonymous, status):
    with pytest.raises(MastodonUnauthorizedError):
        api_anonymous.timeline_home()

@pytest.mark.vcr()
def test_home_tl(api, status):
    time.sleep(3)
    tl = api.timeline_home()
    assert status['id'] in map(lambda st: st['id'], tl)

@pytest.mark.vcr()
def test_hashtag_tl(api):
    status = api.status_post('#hoot (hashtag toot)')
    tl = api.timeline_hashtag('hoot')
    try:
        assert status['id'] in map(lambda st: st['id'], tl)
    finally:
        api.status_delete(status['id'])

def test_hashtag_tl_leading_hash(api):
    with pytest.raises(MastodonIllegalArgumentError):
        api.timeline_hashtag('#hoot')

@pytest.mark.vcr()
def test_home_tl_anonymous_throws(api_anonymous):
    with pytest.raises(MastodonAPIError):
        api_anonymous.timeline_home()

@pytest.mark.vcr()
def test_conversations(api, api2):
    account = api.account_verify_credentials()
    status = api.status_post("@admin ilu bby ;3", visibility="direct")
    time.sleep(2)
    conversations = api2.conversations()
    api2.conversations_read(conversations[0])
    time.sleep(2)
    conversations2 = api2.conversations()
    api.status_delete(status)
    assert conversations
    assert status.id in map(lambda x: x.last_status.id, conversations)
    assert account.id in map(lambda x: x.accounts[0].id, conversations)
    assert conversations[0].unread == True
    assert conversations2[0].unread == False
