import pytest
from mastodon.enums import MarkerTimeline

@pytest.mark.vcr()
def test_markers(api, status):
    marker_a = api.markers_set(MarkerTimeline.HOME, status)
    print("---------------- MARKER A", marker_a)
    assert marker_a
    assert marker_a["home"]
    
    marker_b = api.markers_get(MarkerTimeline.HOME)
    print("---------------- MARKER B", marker_b)
    assert marker_b
    assert marker_b["home"]
    assert next(iter(marker_b)) is MarkerTimeline.HOME
    
    assert marker_a.home.version == marker_b.home.version
    assert marker_a.home.last_read_id == status.id
    assert marker_b.home.last_read_id == status.id

    
