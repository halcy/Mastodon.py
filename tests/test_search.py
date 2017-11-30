import pytest

@pytest.mark.vcr()
def test_search(api):
    results = api.search('mastodonpy_test')
    assert isinstance(results, dict)
