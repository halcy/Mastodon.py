# Ratelimit behaviour checks with mocked headers

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from mastodon import MastodonRatelimitError
import mastodon.internals


def _response(status=200, headers=None):
    return SimpleNamespace(
        ok=status < 400,
        status_code=status,
        headers=headers or {},
        text="",
        json=lambda: {},
    )


def _responses(api, responses):
    responses = iter(responses)

    def request(*args, **kwargs):
        response = next(responses)
        return response() if callable(response) else response

    api.session.request = MagicMock(side_effect=request)
    api.debug_requests = False
    return api.session.request


def _clock(monkeypatch):
    now = [1000.0]
    sleeps = []

    def sleep(seconds):
        sleeps.append(seconds)
        now[0] += seconds

    monkeypatch.setattr(
        mastodon.internals,
        "time",
        SimpleNamespace(time=lambda: now[0], sleep=sleep),
    )
    return now, sleeps


def _headers(remaining, reset=None):
    headers = {
        "X-RateLimit-Remaining": str(remaining),
        "X-RateLimit-Limit": "20",
    }
    if reset is not None:
        headers["X-RateLimit-Reset"] = str(reset)
    return headers


def test_ratelimit_wait(api, monkeypatch):
    now, sleeps = _clock(monkeypatch)
    request = _responses(api, [
        _response(),
        _response(headers=_headers("invalid", 1090)),
        _response(headers=_headers(10, 1100)),
        _response(headers=_headers(9)),
        _response(429, _headers(0, 1010)),
        _response(),
        _response(429, _headers(0)),
        _response(429, _headers(0)),
        _response(),
    ])

    api.toot("")
    assert api.ratelimit_lastcall is None
    api.toot("")
    assert api.ratelimit_reset == 1090
    assert api.ratelimit_lastcall is None
    api.toot("")
    api.toot("")
    assert api.ratelimit_reset == 1100

    api.toot("")
    assert sleeps == [10]
    api.toot("")
    assert sleeps == [10, 2, 4]
    assert api.ratelimit_reset is None
    assert request.call_count == 9


def test_ratelimit_throw(api, monkeypatch):
    now, sleeps = _clock(monkeypatch)
    api.ratelimit_method = "throw"
    request = _responses(api, [
        _response(),
        _response(headers=_headers("invalid", 1090)),
        _response(headers=_headers(10, 1100)),
        _response(headers=_headers(9)),
        _response(429, _headers(0, 1100)),
        _response(429, _headers(0)),
    ])

    api.toot("")
    api.toot("")
    assert api.ratelimit_reset == 1090
    assert api.ratelimit_lastcall is None
    api.toot("")
    api.toot("")
    assert api.ratelimit_reset == 1100

    with pytest.raises(MastodonRatelimitError):
        api.toot("")
    now[0] = 1100
    with pytest.raises(MastodonRatelimitError):
        api.toot("")
    assert api.ratelimit_reset is None
    assert sleeps == []
    assert request.call_count == 6


def test_ratelimit_pace(api, monkeypatch):
    now, sleeps = _clock(monkeypatch)
    api.ratelimit_method = "pace"

    def stale_429():
        now[0] = api.ratelimit_reset
        return _response(429, _headers(0))

    request = _responses(api, [
        _response(),
        _response(headers=_headers("invalid", 1090)),
        _response(headers=_headers(10, 1100)),
        _response(headers=_headers(9)),
        _response(429, _headers(0, 1200)),
        _response(headers=_headers(8, 1300)),
        stale_429,
    ])

    api.toot("")
    assert sleeps == []
    with pytest.raises(MastodonRatelimitError):
        api.toot("")
    assert api.ratelimit_lastcall is None
    api.toot("")
    api.toot("")
    assert api.ratelimit_reset == 1100

    api.toot("")
    assert api.ratelimit_reset == 1300
    with pytest.raises(MastodonRatelimitError):
        api.toot("")
    assert api.ratelimit_reset is None

    calls = request.call_count
    with pytest.raises(MastodonRatelimitError):
        api.toot("")
    assert request.call_count == calls
