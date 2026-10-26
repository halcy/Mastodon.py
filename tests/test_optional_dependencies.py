"""Tests to check for optional features missing. Only ran when MASTODON_TEST_NO_OPTIONAL_DEPS=1 is set."""

import importlib.util
import os

import pytest

from mastodon import WebSocketStreamHandle
from mastodon import compat
from mastodon.errors import MastodonIllegalArgumentError


pytestmark = pytest.mark.skipif(os.environ.get("MASTODON_TEST_NO_OPTIONAL_DEPS") != "1")

@pytest.mark.parametrize("module,flag", [
    ("cryptography", "IMPL_HAS_CRYPTO"),
    ("http_ece", "IMPL_HAS_ECE"),
    ("blurhash", "IMPL_HAS_BLURHASH"),
    ("grapheme", "IMPL_HAS_GRAPHEME"),
    ("websocket", "IMPL_HAS_WEBSOCKET"),
    ("magic", "IMPL_HAS_MAGIC"),
])
def test_missing_optional_dependency_detection(module, flag):
    assert importlib.util.find_spec(module) is None, "{} must not be installed".format(module)
    assert getattr(compat, module) is None
    assert getattr(compat, flag) is False


def test_missing_webpush_key_generation_dependency_error(api):
    with pytest.raises(NotImplementedError) as exc:
        api.push_subscription_generate_keys()
    assert str(exc.value) == (
        "To use the crypto tools, please install the webpush feature dependencies."
    )


def test_missing_webpush_decryption_dependency_error(api):
    with pytest.raises(NotImplementedError) as exc:
        api.push_subscription_decrypt_push(b"", {}, "", "")
    assert str(exc.value) == (
        "To use the crypto tools, please install the webpush feature dependencies."
    )


def test_missing_blurhash_dependency_error(api):
    with pytest.raises(NotImplementedError) as exc:
        api.decode_blurhash({"blurhash": "=~NdOWof1PbIPUXSvgbI$f"})
    assert str(exc.value) == (
        "To use the blurhash functions, please install the blurhash Python module."
    )


def test_missing_grapheme_dependency_error(api):
    with pytest.raises(NotImplementedError) as exc:
        api.get_status_length("hello")
    assert str(exc.value) == (
        "To use the get_status_length function, please install the grapheme Python module."
    )


def test_missing_websocket_dependency_error():
    with pytest.raises(NotImplementedError) as exc:
        WebSocketStreamHandle("ws://localhost", access_token=None, user_agent="tests")
    assert str(exc.value) == (
        "WebSocket streaming requires the websocket_streaming feature dependencies. "
        "Install Mastodon.py[websocket_streaming]."
    )


@pytest.mark.parametrize("filename,mime_type", [
    ("image.jpg", "image/jpeg"),
    ("image.png", "image/png"),
])
def test_missing_magic_falls_back_to_filename(api, filename, mime_type):
    assert compat.magic is None
    assert api._Mastodon__guess_type(filename) == mime_type


def test_missing_magic_unknown_mime_type_error(api, tmp_path):
    assert compat.magic is None
    path = tmp_path / "image.mastodon-unknown-type"
    path.write_bytes(b"image data")

    with pytest.raises(MastodonIllegalArgumentError) as exc:
        api.media_post(path)
    assert str(exc.value) == (
        "Could not determine mime type or data passed directly without mime type. "
        'Installing the "magic" extra dependency may help.'
    )
