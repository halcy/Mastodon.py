import pytest
from datetime import datetime


@pytest.mark.vcr()
def test_id_hook(status):
    assert isinstance(status['id'], int)


@pytest.mark.vcr()
def test_id_hook_in_reply_to(api, status):
    reply = api.status_post('Reply!', in_reply_to_id=status['id'])
    try:
        assert isinstance(reply['in_reply_to_id'], int)
        assert isinstance(reply['in_reply_to_account_id'], int)
    finally:
        api.status_delete(reply['id'])


@pytest.mark.vcr()
def test_id_hook_within_reblog(api, status):
    reblog = api.status_reblog(status['id'])
    try:
        assert isinstance(reblog['reblog']['id'], int)
    finally:
        api.status_delete(reblog['id'])


@pytest.mark.vcr()
def test_date_hook(status):
    assert isinstance(status['created_at'], datetime)

@pytest.mark.vcr()
def test_attribute_access(status):
    assert status.id != None
    with pytest.raises(AttributeError):
        status.id = 420
    