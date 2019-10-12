import pytest
import vcr

@pytest.mark.vcr()
def test_search(api):    
    results = api.search_v2('mastodonpy_test')
    assert isinstance(results, dict)
    
    results = api.search('mastodonpy_test')
    assert isinstance(results, dict)

    results = api.search('mastodonpy_test', result_type="statuses")
    assert isinstance(results, dict)
    assert len(results["hashtags"]) == 0
    assert len(results["accounts"]) == 0

def test_search_pre_2_9_2(api):
    api.mastodon_major = 2
    api.mastodon_minor = 9
    api.mastodon_patch = 1
    with vcr.use_cassette('test_search.yaml', cassette_library_dir='tests/cassettes_pre_2_9_2', record_mode='none'):    
        results = api.search_v1('mastodonpy_test')
        assert isinstance(results, dict)
        
        results = api.search_v2('mastodonpy_test')
        assert isinstance(results, dict)
        
        results = api.search('mastodonpy_test')
        assert isinstance(results, dict)

        results = api.search('mastodonpy_test', result_type="statuses")
        assert isinstance(results, dict)
        assert len(results["hashtags"]) == 0
        assert len(results["accounts"]) == 0
