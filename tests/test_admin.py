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

@pytest.mark.vcr()
def test_admin_reports(api, api2, status):
    account = api.account_verify_credentials()
    account2 = api2.account_verify_credentials()
    report = api2.report(account, status, "api crimes")
    assert(report)
    assert(not report.action_taken)
    
    report_list = api2.admin_reports()
    assert(report.id in [x.id for x in report_list])
    
    report = api2.admin_report_resolve(report)
    report_list = api2.admin_reports()
    assert(report.action_taken)
    assert(report.action_taken_by_account.id == account2.id)
    assert(not report.id in [x.id for x in report_list])
    
    report = api2.admin_report_reopen(report)
    report_list = api2.admin_reports()
    assert(not report.action_taken)
    assert(report.id in [x.id for x in report_list])
    
    report = api2.admin_report_assign(report)
    assert(report.assigned_account.id == account2.id)
    
    report = api2.admin_report_unassign(report)
    assert(report.assigned_account is None)
    
    report2 = api2.admin_report(report)
    assert(report2)
    assert(report2.id == report.id)     
    
@pytest.mark.skip(reason="reject / accept of account requests isn't really testable without modifying instance settings. anyone want to fumble those into the DB setup and write this test, please do.")
def test_admin_accountrequests(api2):
    pass

