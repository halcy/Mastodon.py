import pytest
import time
from datetime import datetime, timedelta
from mastodon import MastodonIllegalArgumentError

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

@pytest.mark.vcr()
def test_admin_trends(api2):
    assert isinstance(api2.admin_trending_tags(), list)
    assert isinstance(api2.admin_trending_statuses(), list)
    assert isinstance(api2.admin_trending_links(), list)
    assert isinstance(api2.admin_trending_tags(limit=5), list)

@pytest.mark.skip(reason="reject / accept of account requests isn't really testable without modifying instance settings. anyone want to fumble those into the DB setup and write this test, please do.")
def test_admin_accountrequests(api2):
    pass

@pytest.mark.vcr()
def test_admin_domain_blocks(api2):
    block = api2.admin_create_domain_block(domain = "https://chitter.xyz/", public_comment="sicko behaviour", severity="suspend")
    assert isinstance(api2.admin_domain_blocks(), list)
    block2 = api2.admin_domain_blocks(block)
    assert block.severity == "suspend"
    assert block.public_comment == "sicko behaviour"
    assert block.severity == block2.severity
    block3 = api2.admin_update_domain_block(block, severity="silence", private_comment="jk ilu <3")
    assert block3.severity == "silence"
    assert block3.public_comment == "sicko behaviour"
    assert block3.private_comment == "jk ilu <3"
    api2.admin_delete_domain_block(block2)
    assert not block3.id in map(lambda x: x.id, api2.admin_domain_blocks())

@pytest.mark.vcr()
def test_admin_stats(api2):
    assert api2.admin_measures(
        datetime(2020, 10, 10) - timedelta(hours=24*5), 
        datetime(2020, 10, 10), 
        active_users=True,
        new_users=True,
        opened_reports=True,
        resolved_reports=True,
        instance_accounts="chitter.xyz",
        instance_media_attachments="chitter.xyz",
        instance_reports="http://chitter.xyz/",
        instance_statuses="chitter.xyz",
        instance_follows="http://chitter.xyz",
        instance_followers="chitter.xyz",
        #tag_accounts=0,
        #tag_uses=0,
        #tag_servers=0,
    )

    assert api2.admin_dimensions(
        datetime(2020, 10, 10) - timedelta(hours=24*5), 
        datetime(2020, 10, 10),
        limit=3,
        languages=True,
        sources=True,
        servers=True,
        space_usage=True,
        #tag_servers=0,
        #tag_languages=0,
        instance_accounts="chitter.xyz",
        instance_languages="https://chitter.xyz"
    )

    api2.admin_retention(
        datetime(2020, 10, 10) - timedelta(days=10), 
        datetime(2020, 10, 10)
    )

    with pytest.raises(MastodonIllegalArgumentError):
        api2.admin_retention(
            datetime(2020, 10, 10) - timedelta(days=10), 
            datetime(2020, 10, 10),
            frequency="dayz"
        )