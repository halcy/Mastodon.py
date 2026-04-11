import pytest
import requests_mock

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from mastodon.types_base import AttribAccessDict, Entity, PaginatableList, NonPaginatableList, try_cast_recurse
from mastodon.return_types import AsyncRefresh, Context


def _mock_mastodon():
    m = MagicMock()
    m.version_check_mode = "none"
    return m


def test_parse_header_basic(api):
    rmock = requests_mock.Adapter()
    api.session.mount(api.api_base_url, rmock)
    rmock.register_uri('GET', requests_mock.ANY, json={"foo": "bar"},
                       headers={"Mastodon-Async-Refresh": 'id="abc123", retry=3'})
    result = api.timeline_hashtag("test")
    assert hasattr(result, '_async_refresh')
    assert result._async_refresh['id'] == 'abc123'
    assert result._async_refresh['retry'] == 3
    assert 'result_count' not in result._async_refresh

def test_parse_header_with_result_count(api):
    rmock = requests_mock.Adapter()
    api.session.mount(api.api_base_url, rmock)
    rmock.register_uri('GET', requests_mock.ANY, json={"foo": "bar"},
                       headers={"Mastodon-Async-Refresh": 'id="abc123", retry=5, result_count=2'})
    result = api.timeline_hashtag("test")
    assert result._async_refresh['id'] == 'abc123'
    assert result._async_refresh['retry'] == 5
    assert result._async_refresh['result_count'] == 2

def test_parse_header_long_id(api):
    long_id = 'ImNvbnRleHQ6MTEzNjQwNTczMzAzNzg1MTc4OnJlZnJlc2gi--c526259eb4a1f3ef0d4b91cf8c99bf501330a815'
    rmock = requests_mock.Adapter()
    api.session.mount(api.api_base_url, rmock)
    rmock.register_uri('GET', requests_mock.ANY, json={"foo": "bar"},
                       headers={"Mastodon-Async-Refresh": f'id="{long_id}", retry=3, result_count=0'})
    result = api.timeline_hashtag("test")
    assert result._async_refresh['id'] == long_id
    assert result._async_refresh['retry'] == 3
    assert result._async_refresh['result_count'] == 0

def test_parse_header_stores_request_info(api):
    rmock = requests_mock.Adapter()
    api.session.mount(api.api_base_url, rmock)
    rmock.register_uri('GET', requests_mock.ANY, json={"foo": "bar"},
                       headers={"Mastodon-Async-Refresh": 'id="test", retry=10'})
    result = api.timeline_hashtag("test")
    assert result._async_refresh['retry'] == 10
    assert result._async_refresh['_method'] == 'GET'
    assert '_endpoint' in result._async_refresh
    assert '_params' in result._async_refresh

def test_no_header_means_no_async_refresh(api):
    rmock = requests_mock.Adapter()
    api.session.mount(api.api_base_url, rmock)
    rmock.register_uri('GET', requests_mock.ANY, json={"foo": "bar"})
    result = api.timeline_hashtag("test")
    assert not hasattr(result, '_async_refresh')

def test_async_refresh_serialization_attrib_access_dict():
    d = try_cast_recurse(AsyncRefresh, {'id': 'test123', 'status': 'running', 'result_count': 5})
    d._async_refresh = {'id': 'test123', 'retry': 3, 'result_count': 5}
    json_str = d.to_json()
    assert 'test123' in json_str
    assert '_async_refresh' in json_str

def test_async_refresh_deserialization_attrib_access_dict():
    d = try_cast_recurse(AsyncRefresh, {'id': 'test123', 'status': 'running', 'result_count': 5})
    d._async_refresh = {'id': 'test123', 'retry': 3, 'result_count': 5}
    json_str = d.to_json()
    restored = Entity.from_json(json_str)
    assert hasattr(restored, '_async_refresh')
    assert restored._async_refresh['id'] == 'test123'
    assert restored._async_refresh['retry'] == 3
    assert restored._async_refresh['result_count'] == 5

def test_async_refresh_absent_from_serialization_when_not_set():
    d = try_cast_recurse(AsyncRefresh, {'id': 'test', 'status': 'running', 'result_count': None})
    json_str = d.to_json()
    assert '_async_refresh' not in json_str

def test_async_refresh_deserialization_without_async_refresh():
    d = try_cast_recurse(AsyncRefresh, {'id': 'test', 'status': 'running', 'result_count': None})
    json_str = d.to_json()
    restored = Entity.from_json(json_str)
    assert not hasattr(restored, '_async_refresh')

def test_get_async_refresh_info_present():
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    mastodon = _mock_mastodon()
    result = AttribAccessDict(data='test')
    result._async_refresh = {'id': 'abc', 'retry': 5, 'result_count': 2}
    info = MastoAsyncRefresh.get_async_refresh_info(mastodon, result)
    assert info is not None
    entity, retry = info
    assert isinstance(entity, AsyncRefresh)
    assert entity.id == 'abc'
    assert entity.status == 'running'
    assert entity.result_count == 2
    assert retry == 5

def test_get_async_refresh_info_default_retry():
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    mastodon = _mock_mastodon()
    result = AttribAccessDict(data='test')
    result._async_refresh = {'id': 'abc'}
    info = MastoAsyncRefresh.get_async_refresh_info(mastodon, result)
    entity, retry = info
    assert retry == 3

def test_get_async_refresh_info_absent():
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    mastodon = _mock_mastodon()
    result = AttribAccessDict(data='test')
    info = MastoAsyncRefresh.get_async_refresh_info(mastodon, result)
    assert info is None

def test_get_async_refresh_info_none():
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    mastodon = _mock_mastodon()
    result = AttribAccessDict(data='test')
    result._async_refresh = None
    info = MastoAsyncRefresh.get_async_refresh_info(mastodon, result)
    assert info is None

def test_get_async_refresh_status_accepts_string():
    mastodon = _mock_mastodon()
    inner = {'id': 'my-refresh-id', 'status': 'running', 'result_count': None}
    mastodon._Mastodon__api_request = MagicMock(return_value={'async_refresh': inner})
    mastodon._Mastodon__get_async_refresh_id = MagicMock(return_value='my-refresh-id')
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.get_async_refresh_status(mastodon, 'my-refresh-id')
    
    mastodon._Mastodon__get_async_refresh_id.assert_called_once_with('my-refresh-id')
    mastodon._Mastodon__api_request.assert_called_once_with('GET', '/api/v1_alpha/async_refreshes/my-refresh-id', override_type=dict)

def test_get_async_refresh_status_accepts_int_id():
    mastodon = _mock_mastodon()
    inner = {'id': '12345', 'status': 'running', 'result_count': None}
    mastodon._Mastodon__api_request = MagicMock(return_value={'async_refresh': inner})
    mastodon._Mastodon__get_async_refresh_id = MagicMock(return_value='12345')
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.get_async_refresh_status(mastodon, 12345)
    
    mastodon._Mastodon__get_async_refresh_id.assert_called_once_with(12345)
    mastodon._Mastodon__api_request.assert_called_once_with('GET', '/api/v1_alpha/async_refreshes/12345', override_type=dict)

def test_get_async_refresh_status_accepts_result_with_attribute():
    mastodon = _mock_mastodon()
    inner = {'id': 'abc', 'status': 'finished', 'result_count': 0}
    mastodon._Mastodon__api_request = MagicMock(return_value={'async_refresh': inner})
    mastodon._Mastodon__get_async_refresh_id = MagicMock(return_value='abc')
    
    fake_result = AttribAccessDict(test='data')
    fake_result._async_refresh = {'id': 'abc', 'retry': 3}
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.get_async_refresh_status(mastodon, fake_result)
    
    mastodon._Mastodon__api_request.assert_called_once_with('GET', '/api/v1_alpha/async_refreshes/abc', override_type=dict)

def test_get_async_refresh_status_accepts_async_refresh_entity():
    mastodon = _mock_mastodon()
    inner = {'id': 'xyz', 'status': 'finished', 'result_count': 3}
    mastodon._Mastodon__api_request = MagicMock(return_value={'async_refresh': inner})
    mastodon._Mastodon__get_async_refresh_id = MagicMock(return_value='xyz')
    
    prev = AsyncRefresh(id='xyz', status='running', result_count=0)
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.get_async_refresh_status(mastodon, prev)
    
    mastodon._Mastodon__api_request.assert_called_once_with('GET', '/api/v1_alpha/async_refreshes/xyz', override_type=dict)
    assert isinstance(result, AsyncRefresh)
    assert result.status == 'finished'

def test_get_async_refresh_status_rejects_bad_input():
    mastodon = _mock_mastodon()
    from mastodon.errors import MastodonIllegalArgumentError
    mastodon._Mastodon__get_async_refresh_id = MagicMock(side_effect=MastodonIllegalArgumentError('test'))
    fake_result = AttribAccessDict(test='data')
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    with pytest.raises(MastodonIllegalArgumentError):
        MastoAsyncRefresh.get_async_refresh_status(mastodon, fake_result)

def test_get_async_refresh_status_unwraps_and_casts():
    mastodon = _mock_mastodon()
    inner = {'id': 'test', 'status': 'running', 'result_count': 2}
    mastodon._Mastodon__api_request = MagicMock(return_value={'async_refresh': inner})
    mastodon._Mastodon__get_async_refresh_id = MagicMock(return_value='test')
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.get_async_refresh_status(mastodon, 'test')
    assert isinstance(result, AsyncRefresh)
    assert result.id == 'test'
    assert result.status == 'running'
    assert result.result_count == 2

def test_await_async_refresh_refetches_original_endpoint():
    finished = AsyncRefresh(id='test', status='finished', result_count=3)
    refetched_context = Context(ancestors=[], descendants=[])
    
    mastodon = _mock_mastodon()
    mastodon.get_async_refresh_status = MagicMock(return_value=finished)
    mastodon._Mastodon__api_request = MagicMock(return_value=refetched_context)
    
    fake_result = AttribAccessDict()
    fake_result._async_refresh = {
        'id': 'test', 'retry': 1,
        '_method': 'GET', '_endpoint': '/api/v1/statuses/123/context',
        '_params': {}, '_mastopy_type': 'Context',
    }
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.await_async_refresh(mastodon, fake_result, timeout=10, max_attempts=5)
    
    assert mastodon.get_async_refresh_status.call_count == 1
    mastodon._Mastodon__api_request.assert_called_once_with('GET', '/api/v1/statuses/123/context', {}, override_type='Context')
    assert result is refetched_context

def test_await_async_refresh_polls_then_refetches():
    running1 = AsyncRefresh(id='test', status='running', result_count=0)
    running1._async_refresh = {'id': 'test', 'retry': 7}
    running2 = AsyncRefresh(id='test', status='running', result_count=1)
    finished = AsyncRefresh(id='test', status='finished', result_count=3)
    refetched = AttribAccessDict(ancestors=['a'], descendants=['b'])
    
    mastodon = _mock_mastodon()
    mastodon.get_async_refresh_status = MagicMock(side_effect=[running1, running2, finished])
    mastodon._Mastodon__api_request = MagicMock(return_value=refetched)
    
    fake_result = AttribAccessDict(data='test')
    fake_result._async_refresh = {'id': 'test', 'retry': 0, '_method': 'GET', '_endpoint': '/api/v1/statuses/123/context', '_params': {}, '_mastopy_type': 'Context'}
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.await_async_refresh(mastodon, fake_result, timeout=60, max_attempts=10)
    
    assert mastodon.get_async_refresh_status.call_count == 3
    mastodon._Mastodon__api_request.assert_called_once()
    assert result is refetched

def test_await_async_refresh_returns_none_on_max_attempts():
    running = AsyncRefresh(id='test', status='running', result_count=0)
    
    mastodon = _mock_mastodon()
    mastodon.get_async_refresh_status = MagicMock(return_value=running)
    
    fake_result = PaginatableList([])
    fake_result._async_refresh = {'id': 'test', 'retry': 0, '_method': 'GET', '_endpoint': '/api/v1/timelines/home', '_params': {'limit': 20}, '_mastopy_type': None}
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.await_async_refresh(mastodon, fake_result, timeout=0, max_attempts=3)
    
    assert mastodon.get_async_refresh_status.call_count == 3
    assert result is None

def test_await_async_refresh_passes_correct_override_type():
    finished = AsyncRefresh(id='test', status='finished', result_count=5)
    refetched = Context(ancestors=['a'], descendants=['b'])
    
    mastodon = _mock_mastodon()
    mastodon.get_async_refresh_status = MagicMock(return_value=finished)
    mastodon._Mastodon__api_request = MagicMock(return_value=refetched)
    
    fake_result = AttribAccessDict()
    fake_result._async_refresh = {
        'id': 'test', 'retry': 1,
        '_method': 'GET', '_endpoint': '/api/v1/statuses/999/context',
        '_params': {'some': 'param'}, '_mastopy_type': Context,
    }
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.await_async_refresh(mastodon, fake_result, timeout=10, max_attempts=5)
    
    mastodon._Mastodon__api_request.assert_called_once_with('GET', '/api/v1/statuses/999/context', {'some': 'param'}, override_type=Context)
    assert isinstance(result, Context)

def test_await_async_refresh_returns_result_when_no_async_refresh():
    mastodon = _mock_mastodon()
    fake_result = AttribAccessDict(test='data')
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.await_async_refresh(mastodon, fake_result)
    assert result is fake_result

def test_await_async_refresh_rejects_non_entity():
    mastodon = _mock_mastodon()
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    from mastodon.errors import MastodonIllegalArgumentError
    with pytest.raises(MastodonIllegalArgumentError):
        MastoAsyncRefresh.await_async_refresh(mastodon, 'my-id')
    with pytest.raises(MastodonIllegalArgumentError):
        MastoAsyncRefresh.await_async_refresh(mastodon, 12345)

def test_await_async_refresh_raises_when_missing_method():
    mastodon = _mock_mastodon()
    fake_result = AttribAccessDict(test='data')
    fake_result._async_refresh = {'id': 'test', 'retry': 3}
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    from mastodon.errors import MastodonIllegalArgumentError
    with pytest.raises(MastodonIllegalArgumentError):
        MastoAsyncRefresh.await_async_refresh(mastodon, fake_result)

def test_await_async_refresh_returns_immediately_when_already_finished():
    mastodon = _mock_mastodon()
    fake_result = AttribAccessDict(data='test')
    fake_result._async_refresh = {
        'id': 'test', 'retry': 3, 'status': 'finished',
        '_method': 'GET', '_endpoint': '/api/v1/statuses/123/context',
        '_params': {}, '_mastopy_type': 'Context',
    }
    
    from mastodon.async_refresh import Mastodon as MastoAsyncRefresh
    result = MastoAsyncRefresh.await_async_refresh(mastodon, fake_result)
    assert result is fake_result
