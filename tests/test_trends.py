import pytest
import time
import vcr


@pytest.mark.vcr()
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
