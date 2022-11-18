import pytest

from mastodon.Mastodon import MastodonVersionError
import datetime
import os
import pickle

@pytest.mark.vcr()
def test_instance(api):
    instance = api.instance()

    assert isinstance(instance, dict)  # hehe, instance is instance

    expected_keys = set(('description', 'email', 'title', 'uri', 'version', 'urls'))
    assert set(instance.keys()) >= expected_keys

@pytest.mark.vcr()
def test_instance_activity(api):
    activity = api.instance_activity()
    
    assert len(activity) > 0
    assert "statuses" in activity[0]
    assert "logins" in activity[0]
    assert "week" in activity[0]

@pytest.mark.vcr()
def test_instance_peers(api):
    assert len(api.instance_peers()) == 0

@pytest.mark.vcr()
def test_low_version(api_low_version):
    with pytest.raises(MastodonVersionError):
        instance = api_low_version.instance()
    
@pytest.mark.vcr()
def test_emoji(api):
    assert len(api.custom_emojis()) == 0

@pytest.mark.vcr()
def test_health(api):
    assert api.instance_health() == True

@pytest.mark.vcr()
def test_server_time(api):
    # present date...
    present_time = api.get_approx_server_time()
    # hahahahaha

    if os.path.exists("tests/cassettes/test_server_time_datetimeobjects.pkl"):
        present_time_real = datetime.datetime.fromtimestamp(pickle.load(open("tests/cassettes/test_server_time_datetimeobjects.pkl", 'rb')))
    else:
        present_time_real = datetime.datetime.now()
        pickle.dump(present_time_real.timestamp(), open("tests/cassettes/test_server_time_datetimeobjects.pkl", 'wb'))
    
    assert isinstance(api.get_approx_server_time(), datetime.datetime)
    assert abs((api.get_approx_server_time() - present_time_real).total_seconds()) < 5

@pytest.mark.vcr()
def test_nodeinfo(api):
    nodeinfo = api.instance_nodeinfo()
    assert nodeinfo
    assert nodeinfo.version == '2.0'
    
@pytest.mark.vcr()
def test_trends(api):
    assert isinstance(api.trends(), list)
    
@pytest.mark.vcr()
def test_directory(api):
    directory = api.directory()
    assert directory
    assert isinstance(directory, list)
    assert len(directory) > 0

@pytest.mark.vcr()
def test_instance_rules(api):
    assert isinstance(api.instance_rules(), list)
