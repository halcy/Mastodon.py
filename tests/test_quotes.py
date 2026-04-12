import pytest

@pytest.mark.vcr()
def test_status_post_with_quote(api, status):
    quoted = api.status_post('yoooooooo', quoted_status_id=status)
    try:
        assert quoted
        assert quoted.quote is not None or quoted.quoted_status is not None
    finally:
        api.status_delete(quoted)

@pytest.mark.vcr()
def test_status_post_with_quote_approval_policy(api):
    api.account_update_credentials(default_quote_policy='nobody')
    status = api.status_post('tehehe', quote_approval_policy='followers')
    try:
        assert status
        assert status.quote_approval.current_user == 'automatic'
    finally:
        api.status_delete(status)

@pytest.mark.vcr()
def test_status_quotes(api, status):
    quotes = api.status_quotes(status)
    assert isinstance(quotes, list)

@pytest.mark.vcr()
def test_status_update_quote_approval_policy(api):
    api.account_update_credentials(default_quote_policy='followers')
    status = api.status_post('do not @ me', quote_approval_policy='followers')
    updated = api.status_update_quote_approval_policy(status, quote_approval_policy='nobody')
    assert updated
    assert updated.quote_approval.current_user == 'automatic'

@pytest.mark.vcr()
def test_status_quote_approval_visibility(api, api2):
    # Ensure api2 does not follow api
    api2.account_unfollow(api.account_verify_credentials().id)
    
    # Post a status with public quote policy
    original = api.status_post('https://www.youtube.com/watch?v=FAEKjYroiME', visibility='public', quote_approval_policy='public')
    try:
        # api2 should see automatic approval
        status_from_api2 = api2.status(original)
        assert status_from_api2.quote_approval is not None
        assert status_from_api2.quote_approval.current_user == 'automatic'

        # Change policy to followers-only
        api.status_update_quote_approval_policy(original, quote_approval_policy='followers')

        # api2 (non-follower) should now see denied
        status_from_api2 = api2.status(original)
        assert status_from_api2.quote_approval is not None
        assert status_from_api2.quote_approval.current_user == 'denied'

        # Change policy to nobody
        api.status_update_quote_approval_policy(original, quote_approval_policy='nobody')

        # api2 should still see denied
        status_from_api2 = api2.status(original)
        assert status_from_api2.quote_approval is not None
        assert status_from_api2.quote_approval.current_user == 'denied'
    finally:
        api.status_delete(original)

@pytest.mark.vcr()
def test_status_quote_revoke(api, api2):
    original = api.status_post('https://www.youtube.com/watch?v=FAEKjYroiME', visibility='public', quote_approval_policy='public')
    try:
        quoted = api2.status_post('check this mother fucker out', quoted_status_id=original)
        try:
            revoked = api.status_quote_revoke(original, quoted)
            assert revoked
        finally:
            api2.status_delete(quoted)
    finally:
        api.status_delete(original)

@pytest.mark.vcr()
def test_status_reply_with_quote(api, status):
    reply_target = api.status_post('reply to me')
    try:
        quoted = api.status_reply(reply_target, 'yoooo check this out', quoted_status_id=status)
        try:
            assert quoted
            assert quoted.in_reply_to_id == reply_target.id
            assert quoted.quote is not None or quoted.quoted_status is not None
        finally:
            api.status_delete(quoted)
    finally:
        api.status_delete(reply_target)
