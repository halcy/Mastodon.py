import pytest
from mastodon.Mastodon import MastodonIllegalArgumentError
from mastodon import Mastodon
import vcr

@pytest.mark.vcr()
def test_zzz_revoke(api_anonymous):
    # No password login after 4.4.0, so this can't be tested anymore against newer servers
    with vcr.use_cassette('test_zzz_revoke.yaml', cassette_library_dir='tests/cassettes_pre_4_4_0', record_mode='none'):
        # Named zzz_revoke to ensure it runs last,
        # as it revokes the access token for the other tests
        token = api_anonymous.log_in(
            username='mastodonpy_test_2@localhost',
            password='5fc638e0e53eafd9c4145b6bb852667d',
            allow_http=True
        )
        api_anonymous.revoke_access_token(allow_http=True)

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