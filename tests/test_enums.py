import json
import pickle

import pytest

from mastodon.enums import (
    DefaultPostVisibility, FilterAction, FilterContext, Language,
    PostVisibility, ReblogVisibility, StatusVisibility, StreamEventType, Visibility,
)
from mastodon.errors import MastodonAPIError
from mastodon.return_types import FilterV2, Rule, Status
from mastodon.types_base import Entity
from mastodon.streaming import StreamListener


def test_enum_response_roundtrip_and_string_fallback():
    status = Status(
        visibility="public",
        language="en",
        account={"source": {"privacy": "private", "language": "de"}},
        reblog={"visibility": "FutureVisibility", "language": "xyz"},
        filtered=[{
            "filter": {
                "context": ["home", "future_context"],
                "filter_action": "future_action",
            },
        }],
    )

    assert status.visibility is StatusVisibility.PUBLIC
    assert status.language is Language.EN
    assert status.account.source.privacy is DefaultPostVisibility.PRIVATE
    assert status.account.source.language is Language.DE
    assert type(status.reblog.visibility) is str
    assert status.reblog.visibility == "FutureVisibility"
    assert status.reblog.language == "xyz"
    assert status.filtered[0].filter.context == [FilterContext.HOME, "future_context"]
    assert status.filtered[0].filter.context[0] is FilterContext.HOME
    assert type(status.filtered[0].filter.filter_action) is str

    restored = Entity.from_json(status.to_json())
    assert restored == status
    assert restored.visibility is StatusVisibility.PUBLIC
    assert restored.account.source.privacy is DefaultPostVisibility.PRIVATE
    assert restored.filtered[0].filter.context[0] is FilterContext.HOME
    assert type(restored.reblog.visibility) is str
    assert restored.reblog.visibility == "FutureVisibility"
    assert restored.reblog.language == "xyz"
    assert json.loads(restored.to_json())["_mastopy_data"]["visibility"] == "public"

    restored.visibility = "AnotherFutureVisibility"
    assert restored.visibility == "AnotherFutureVisibility"
    restored["visibility"] = PostVisibility.PRIVATE
    assert restored.visibility is StatusVisibility.PRIVATE
    assert pickle.loads(pickle.dumps(restored)).visibility is StatusVisibility.PRIVATE
    assert Status(visibility=None, language=None).visibility is None
    assert FilterV2(context=["future_context"], filter_action="future_action").filter_action == "future_action"

    rule = Rule(translations={"en": {"text": "Be kind"}, "xyz": {"text": "Future language"}})
    restored_rule = Entity.from_json(rule.to_json())
    assert list(restored_rule.translations) == [Language.EN, "xyz"]
    assert next(iter(restored_rule.translations)) is Language.EN
    assert restored_rule.translations[Language.EN].text == "Be kind"
    assert restored_rule.translations["xyz"].text == "Future language"


def test_enum_comparison_domains_and_wire_values():
    assert isinstance(PostVisibility.PUBLIC, Visibility)
    assert isinstance(StatusVisibility.PUBLIC, Visibility)
    assert PostVisibility.PUBLIC == StatusVisibility.PUBLIC == ReblogVisibility.PUBLIC == "public"
    assert hash(PostVisibility.PUBLIC) == hash(StatusVisibility.PUBLIC) == hash("public")
    assert {"public": 1}[PostVisibility.PUBLIC] == 1
    assert str(PostVisibility.PUBLIC) == "public"
    assert f"{PostVisibility.PUBLIC}" == "public"
    assert json.dumps({"visibility": PostVisibility.PUBLIC}) == '{"visibility": "public"}'
    assert FilterAction.WARN == "warn"
    assert len(Language) == 184


def test_enum_stream_response_casting():
    events = []

    class Listener(StreamListener):
        def on_any_event(self, name, data, for_stream=None):
            events.append((name, data))

    listener = Listener()
    payload = json.dumps({"visibility": "public", "language": "en"})
    listener.handle_websocket_message({"event": "status.update", "payload": payload})
    listener._dispatch({"event": "status_update", "data": payload})
    listener.handle_websocket_message({
        "event": "mastodonpy.future_event",
        "payload": json.dumps({"visibility": "FutureVisibility"}),
    })

    for name, status in events[:2]:
        assert isinstance(name, StreamEventType)
        assert isinstance(status, Status)
        assert status.visibility is StatusVisibility.PUBLIC
        assert status.language is Language.EN
    assert events[0][0] is StreamEventType("status.update")
    assert events[1][0] is StreamEventType("status_update")
    assert type(events[2][0]) is str
    assert events[2][0] == "mastodonpy.future_event"
    assert events[2][1].visibility == "FutureVisibility"
