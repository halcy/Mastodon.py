import pytest
import time

@pytest.mark.vcr()
def test_admin_accounts(api2):
    accounts = api2.admin_accounts()
    
    assert accounts
    assert len(accounts) > 0
    
    account_self = api2.account_verify_credentials()
    account_admin = api2.admin_account(account_self)
    
    assert(account_admin)
    assert(account_admin.id == account_self.id)

@pytest.mark.vcr(match_on=['path'])
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
        
        api2.admin_account_moderate(account, "sensitive")
        account = api2.admin_account(account_initial)
        image = api.media_post('tests/image.jpg')
        assert image
        status = api.status_post("oh no!", media_ids=image, sensitive=False)
        assert status
        status = api2.status(status)
        assert status.sensitive
        api.status_delete(status)

        account = api2.admin_account_unsensitive(account)
        image = api.media_post('tests/image.jpg')
        assert image
        status = api.status_post("oh no!", media_ids=image, sensitive=False)
        assert status
        status = api2.status(status)
        assert not status.sensitive
        api.status_delete(status)

        api2.admin_account_moderate(account, "suspend")
        account = api2.admin_account(account_initial)
        assert(account.suspended)
        
        account = api2.admin_account_unsuspend(account)
        assert(not account.suspended)
    finally:
        try:
            api2.admin_account_unsuspend(account)
        except:
            pass
        try:
            api2.admin_account_enable(account)
        except:
            pass
        try:
            api2.admin_account_unsilence(account)
        except:
            pass
        try:
            api.status_delete(status)
        except:
            pass

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

