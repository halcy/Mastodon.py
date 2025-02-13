import pytest
from mastodon.Mastodon import MastodonIllegalArgumentError
from mastodon import Mastodon

@pytest.mark.vcr()
def test_zzz_revoke(api_anonymous):
    # Named zzz_revoke to ensure it runs last,
    # as it revokes the access token for the other tests
    token = api_anonymous.log_in(
        username='mastodonpy_test_2@localhost',
        password='5fc638e0e53eafd9c4145b6bb852667d',
    )
    api_anonymous.revoke_access_token()

    try:
        api_anonymous.toot("illegal access detected")
        assert False
    except Exception as e:
        print(e)
        pass

    api_revoked_token = Mastodon(access_token = token, api_base_url='http://localhost:3000')
    try:
        api_revoked_token.toot("illegal access detected")
        assert False
    except Exception as e:
        print(e)
        pass