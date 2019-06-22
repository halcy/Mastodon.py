import pytest
from mastodon.Mastodon import MastodonAPIError

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

def test_nonstandard_errors(api):
    response = MagicMock()
    response.json = MagicMock(return_value=
            "I am a non-standard instance and this error is a plain string.")
    response.ok = False
    response.status_code = 501
    session = MagicMock()
    session.request = MagicMock(return_value=response)

    api.session = session
    with pytest.raises(MastodonAPIError):
        api.instance()

