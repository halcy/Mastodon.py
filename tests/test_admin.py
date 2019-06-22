import pytest

@pytest.mark.vcr()
def test_admin_accounts(api2):
    accounts = api2.admin_accounts()
    
    assert accounts
    assert len(accounts) > 0
    
    account_self = api2.account_verify_credentials()
    account_admin = api2.admin_account(account_self)
    
    assert(account_admin)
    assert(account_admin.id == account_self.id)

@pytest.mark.vcr()
def test_admin_moderation(api, api2):
    account_initial = api.account_verify_credentials()
    account = account_initial
    
    try:        
        api2.admin_account_moderate(account, "disable")
        account = api2.admin_account(account_initial)
        assert(account.disabled)
        
        account = api2.admin_account_enable(account)
        assert(not account.disabled)
        
        api2.admin_account_moderate(account, "silence")
        account = api2.admin_account(account_initial)
        assert(account.silenced)
        
        account = api2.admin_account_unsilence(account)
        assert(not account.silenced)
        
        api2.admin_account_moderate(account, "suspend")
        account = api2.admin_account(account_initial)
        assert(account.suspended)
        
        account = api2.admin_account_unsuspend(account)
        assert(not account.suspended)
    finally:
        api2.admin_account_unsuspend(account)
        api2.admin_account_enable(account)
        api2.admin_account_unsilence(account)
        
