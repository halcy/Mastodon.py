import pytest
import time
import vcr


# Explicitly give casette path due to a Very Weird Bug that happens on python 3.10 and 3.11 only
# and only on CI, somehow.
@pytest.mark.vcr(cassette_path='tests/cassettes/test_trending_tags.yaml')
def test_trending_tags(api):
    tags = api.trending_tags()
    assert isinstance(tags, list)
    tags = api.trends()
    assert isinstance(tags, list)

@pytest.mark.vcr()
def test_trending_statuses(api):
    statuses = api.trending_statuses()
    assert isinstance(statuses, list)

@pytest.mark.vcr()
def test_trending_links(api):
    links = api.trending_links()
    assert isinstance(links, list)
