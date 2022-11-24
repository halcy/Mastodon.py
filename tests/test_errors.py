import pytest
import vcr
from mastodon.Mastodon import MastodonAPIError
import json

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

def test_nonstandard_errors(api):
    response = MagicMock()
    response.json = MagicMock(return_value="I am a non-standard instance and this error is a plain string.")
    response.ok = False
    response.status_code = 501
    session = MagicMock()
    session.request = MagicMock(return_value=response)

    api.session = session
    with pytest.raises(MastodonAPIError):
        api.instance()

@pytest.mark.vcr()
def test_lang_for_errors(api):
    try:
        api.status_post("look at me i am funny shark gawr gura: " + "a" * 50000)
    except Exception as e:
        e1 = str(e)
    api.set_language("de")
    try:
        api.status_post("look at me i am funny shark gawr gura: " + "a" * 50000)
    except Exception as e:
        e2 = str(e)
    assert e1 != e2

def test_broken_date(api):
    dict1 = json.loads('{"uri":"icosahedron.website", "created_at": "", "edited_at": "2012-09-27"}', object_hook=api._Mastodon__json_hooks)
    dict2 = json.loads('{"uri":"icosahedron.website", "created_at": "2012-09-27", "subfield": {"edited_at": "null"}}', object_hook=api._Mastodon__json_hooks)
    assert "edited_at" in dict1
    assert not "created_at" in dict1
    assert "created_at" in dict2
    assert not "edited_at" in dict2.subfield
