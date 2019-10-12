import pytest

@pytest.mark.vcr()
def test_markers(api, status):
    marker_a = api.markers_set("home", status)
    assert marker_a
    assert marker_a["home"]
    
    marker_b = api.markers_get("home")
    assert marker_b
    assert marker_b["home"]
    
    assert marker_a.home.version == marker_b.home.version
    assert marker_a.home.last_read_id == status.id
    assert marker_b.home.last_read_id == status.id

    
