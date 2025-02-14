import pytest
import time
from mastodon.Mastodon import MastodonAPIError, MastodonIllegalArgumentError, MastodonUnauthorizedError, MastodonNotFoundError
import datetime
import pickle
import os

@pytest.mark.vcr()
def test_public_tl_anonymous(api_anonymous, status3):
    time.sleep(3)
    tl = api_anonymous.timeline_public()
    assert any(st["id"] == status3["id"] for st in tl)

@pytest.mark.vcr()
def test_public_tl(api3, status3):
    public = api3.timeline_public()
    local = api3.timeline_local()
    assert any(st["id"] == status3["id"] for st in public)
    assert any(st["id"] == status3["id"] for st in local)

@pytest.mark.vcr()
def test_unauthed_home_tl_throws(api_anonymous, status):
    with pytest.raises(MastodonUnauthorizedError):
        api_anonymous.timeline_home()

@pytest.mark.vcr()
def test_home_tl(api, status):
    time.sleep(3)
    tl = api.timeline_home()
    assert any(st["id"] == status["id"] for st in tl)

@pytest.mark.vcr()
def test_hashtag_tl(api3):
    status = api3.status_post('#hoot (hashtag toot)')
    tl = api3.timeline_hashtag('hoot')
    try:
        assert any(st["id"] == status["id"] for st in tl)
    finally:
        api3.status_delete(status['id'])

def test_hashtag_tl_leading_hash(api):
    with pytest.raises(MastodonIllegalArgumentError):
        api.timeline_hashtag('#hoot')

@pytest.mark.vcr()
def test_home_tl_anonymous_throws(api_anonymous):
    with pytest.raises(MastodonAPIError):
        api_anonymous.timeline_home()

@pytest.mark.vcr()
def test_conversations(api3, api2):
    account = api2.account_verify_credentials()
    status = api3.status_post("@admin ilu bby ;3", visibility="direct")
    time.sleep(2)
    conversations = api3.conversations()
    api3.conversations_read(conversations[0])
    time.sleep(2)
    conversations2 = api3.conversations()
    api3.status_delete(status)
    assert conversations
    assert any(x.last_status.id == status.id for x in conversations)
    assert any(x.accounts[0].id == account.id for x in conversations)
    assert conversations2[0].unread is False

@pytest.mark.vcr()
def test_min_max_id(api, status):
    time.sleep(3)
    tl = api.timeline_home(min_id = int(status.id) - 1000, max_id = int(status.id) + 1000)
    assert any(st["id"] == status["id"] for st in tl)

    tl = api.timeline_home(min_id = int(status.id) - 2000, max_id = int(status.id) - 1000)
    assert not any(st["id"] == status["id"] for st in tl)

    tl = api.timeline_home(min_id = int(status.id) + 1000, max_id = int(status.id)+ 2000)
    assert not any(st["id"] == status["id"] for st in tl)

    tl = api.timeline_home(since_id = int(status.id) - 1000)
    assert any(st["id"] == status["id"] for st in tl)

@pytest.mark.vcr()
def test_min_max_id_datetimes(api, status):
    if os.path.exists("tests/cassettes/test_min_max_id_datetimes_datetimeobjects.pkl"):
        data_dict = pickle.load(open("tests/cassettes/test_min_max_id_datetimes_datetimeobjects.pkl", 'rb'))
        the_past = datetime.datetime.fromtimestamp(data_dict["the_past"])
        the_future = datetime.datetime.fromtimestamp(data_dict["the_future"])
        the_far_future = datetime.datetime.fromtimestamp(data_dict["the_far_future"])
    else:
        epoch_time = datetime.datetime.now().timestamp()
        now = datetime.datetime.fromtimestamp(epoch_time)
        the_past = now - datetime.timedelta(seconds=20)
        the_future = now + datetime.timedelta(seconds=20)
        the_far_future = now + datetime.timedelta(seconds=40)
        pickle.dump({
            "the_past": the_past.timestamp(),
            "the_future": the_future.timestamp(),
            "the_far_future": the_far_future.timestamp(),
        }, open("tests/cassettes/test_min_max_id_datetimes_datetimeobjects.pkl", 'wb'))

    time.sleep(3)
    tl = api.timeline_home(min_id = the_past, max_id = the_future)
    assert any(st["id"] == status["id"] for st in tl)

    tl = api.timeline_home(min_id = the_future, max_id = the_far_future)
    assert not any(st["id"] == status["id"] for st in tl)

@pytest.mark.vcr()
def test_timeline_link_fails(api):
    with pytest.raises(MastodonNotFoundError):
        api.timeline_link("http://example.com/")
        