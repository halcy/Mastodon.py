import pytest

@pytest.mark.vcr()
def test_search(api):
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
