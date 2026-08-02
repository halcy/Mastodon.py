import pytest
from mastodon import Mastodon
from mastodon.Mastodon import MastodonIllegalArgumentError, MastodonNotFoundError

def test_constructor_from_filenames(tmpdir):
    client = tmpdir.join('client')
    client.write_text(u'foo\nbar\n', 'UTF-8')
    access = tmpdir.join('access')
    access.write_text(u'baz\n', 'UTF-8')
    api = Mastodon(
        str(client),
        access_token=str(access),
        api_base_url="mastodon.social"
    )
    assert api.client_id == 'foo'
    assert api.client_secret == 'bar'
    assert api.access_token == 'baz'

def test_constructor_illegal_ratelimit():
    with pytest.raises(MastodonIllegalArgumentError):
        api = Mastodon('foo', client_secret='bar', ratelimit_method='baz', api_base_url="whatever")

def test_constructor_no_url():
    with pytest.raises(MastodonIllegalArgumentError):
        api = Mastodon('foo', client_secret='bar')
        
    with pytest.raises(MastodonIllegalArgumentError):
        api = Mastodon(access_token='baz')

def test_constructor_illegal_versioncheckmode():
    with pytest.raises(MastodonIllegalArgumentError):
        api = Mastodon(
                'foo', client_secret='bar',
                version_check_mode='baz')


def test_constructor_missing_client_secret():
    with pytest.raises(MastodonIllegalArgumentError):
        api = Mastodon('foo')

@pytest.mark.vcr()
def test_verify_version(api):
    assert api.verify_minimum_version("2.3.3") is True
    assert api.verify_minimum_version("9999.9999.9999") is False
    assert api.verify_minimum_version("1.0.0") is True
    
def test_supported_version(api):
    assert Mastodon.get_supported_version()


def test_internal_instance_v1_cache(api, monkeypatch):
    calls = {"v1": 0}

    def fake_api_request(method, endpoint, **kwargs):
        if endpoint == '/api/v1/instance/':
            calls["v1"] += 1
            return {"version": "4.5.0", "urls": {"streaming_api": "wss://stream.example"}}
        raise AssertionError(f"Unexpected endpoint in test: {endpoint}")

    monkeypatch.setattr(api, "_Mastodon__api_request", fake_api_request)

    first = api._Mastodon__instance(cached=True)
    second = api._Mastodon__instance(cached=True)

    assert first["version"] == "4.5.0"
    assert second["version"] == "4.5.0"
    assert calls["v1"] == 1


def test_internal_instance_v2_cache(api, monkeypatch):
    calls = {"v2": 0}

    def fake_api_request(method, endpoint, **kwargs):
        if endpoint == '/api/v2/instance/':
            calls["v2"] += 1
            return {"api_versions": {"mastodon": "2"}}
        raise AssertionError(f"Unexpected endpoint in test: {endpoint}")

    monkeypatch.setattr(api, "_Mastodon__api_request", fake_api_request)

    first = api._Mastodon__instance_v2(cached=True)
    second = api._Mastodon__instance_v2(cached=True)

    assert first["api_versions"]["mastodon"] == "2"
    assert second["api_versions"]["mastodon"] == "2"
    assert calls["v2"] == 1


def test_clear_caches_invalidates_instance_caches(api, monkeypatch):
    calls = {"v1": 0}

    def fake_api_request(method, endpoint, **kwargs):
        if endpoint == '/api/v1/instance/':
            calls["v1"] += 1
            return {"version": "4.5.0", "urls": {"streaming_api": "wss://stream.example"}}
        raise AssertionError(f"Unexpected endpoint in test: {endpoint}")

    monkeypatch.setattr(api, "_Mastodon__api_request", fake_api_request)

    api._Mastodon__instance(cached=True)
    api._Mastodon__instance(cached=True)
    assert calls["v1"] == 1

    api.clear_caches()
    api._Mastodon__instance(cached=True)
    assert calls["v1"] == 2


def test_streaming_base_is_cached(api, monkeypatch):
    calls = {"v1": 0}

    def fake_instance(cached=False):
        calls["v1"] += 1
        return {"urls": {"streaming_api": "wss://stream.example"}}

    def fake_instance_v2(cached=False):
        raise AssertionError("v2 helper should not be needed when v1 contains streaming_api")

    monkeypatch.setattr(api, "_Mastodon__instance", fake_instance)
    monkeypatch.setattr(api, "_Mastodon__instance_v2", fake_instance_v2)

    first = api._Mastodon__get_streaming_base()
    second = api._Mastodon__get_streaming_base()

    assert first == "https://stream.example"
    assert second == "https://stream.example"
    assert calls["v1"] == 1


def test_timeline_is_available_from_v2_config(api, monkeypatch):
    def fake_instance_v2(cached=False):
        return {
            "configuration": {
                "timelines_access": {
                    "live_feeds": {"local": "disabled", "remote": "public"},
                    "hashtag_feeds": {"local": "disabled", "remote": "disabled"},
                }
            }
        }

    monkeypatch.setattr(api, "_Mastodon__instance_v2", fake_instance_v2)

    assert api.timeline_is_available("public", local=True, remote=False) is False
    assert api.timeline_is_available("public", local=False, remote=True) is True
    assert api.timeline_is_available("public") is True
    assert api.timeline_is_available("hashtag") is False


def test_timeline_is_available_fallback_on_missing_v2(api, monkeypatch):
    def fake_instance_v2(cached=False):
        raise MastodonNotFoundError("No v2 instance endpoint")

    monkeypatch.setattr(api, "_Mastodon__instance_v2", fake_instance_v2)

    assert api.timeline_is_available("public") is True
    assert api.timeline_is_available("hashtag", local=True) is True


def test_timeline_is_available_handles_weird_values(api, monkeypatch):
    def fake_instance_v2(cached=False):
        return {
            "configuration": {
                "timelines_access": {
                    "live_feeds": {"local": {"unexpected": "shape"}, "remote": None},
                }
            }
        }

    monkeypatch.setattr(api, "_Mastodon__instance_v2", fake_instance_v2)

    assert api.timeline_is_available("public", local=True) is True
    assert api.timeline_is_available("public", remote=True) is True


def test_timeline_is_available_invalid_timeline_raises(api):
    with pytest.raises(MastodonIllegalArgumentError):
        api.timeline_is_available("home", fail_hard=True)


@pytest.mark.skip(reason="TODO test against live server.")
def test_timeline_is_available_live_server_disabled(mastodon_base):
    assert isinstance(mastodon_base.timeline_is_available("public"), bool)
    assert isinstance(mastodon_base.timeline_is_available("local"), bool)
    assert isinstance(mastodon_base.timeline_is_available("remote"), bool)