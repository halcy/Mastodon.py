import pytest
from datetime import datetime
from mastodon.return_types import IdType
import typing
import copy

def get_type_class(typ):
    try:
        return typ.__extra__
    except AttributeError:
        try:
            return typ.__origin__
        except AttributeError:
            pass
    return typ
        

def real_issubclass(obj1, type2orig):
    type1 = get_type_class(type(obj1))
    type2 = get_type_class(type2orig)
    valid_types = []
    if type2 is typing.Union:
        valid_types = type2orig.__args__
    elif type2 is typing.Generic:
        valid_types = [type2orig.__args__[0]]
    else:
        valid_types = [type2orig]
    return issubclass(type1, tuple(valid_types))

@pytest.mark.vcr()
def test_id_hook(status):
    assert real_issubclass(status['id'], IdType)


@pytest.mark.vcr()
def test_id_hook_in_reply_to(api, status):
    reply = api.status_post('Reply!', in_reply_to_id=status['id'])
    try:
        assert real_issubclass(reply['in_reply_to_id'], IdType)
        assert real_issubclass(reply['in_reply_to_account_id'], IdType)
    finally:
        api.status_delete(reply['id'])


@pytest.mark.vcr()
def test_id_hook_within_reblog(api, status):
    reblog = api.status_reblog(status['id'])
    try:
        assert real_issubclass(reblog['reblog']['id'], IdType)
    finally:
        api.status_delete(reblog['id'])


@pytest.mark.vcr()
def test_date_hook(status):
    assert real_issubclass(status['created_at'], datetime)

@pytest.mark.vcr()
def test_attribute_access(status):
    assert status.id is not None
    status2 = copy.deepcopy(status)
    status2.id = 420
    