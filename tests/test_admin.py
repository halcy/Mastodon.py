import pytest
import time
from datetime import datetime, timedelta
from mastodon import MastodonIllegalArgumentError
import hashlib

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
def test_admin_accounts_v1(api2):
    accounts = api2.admin_accounts_v1()
    
    assert accounts
    assert len(accounts) > 0
    
    account_self = api2.account_verify_credentials()
    account_admin = api2.admin_account(account_self)
    
    assert(account_admin)
    assert(account_admin.id == account_self.id)

@pytest.mark.vcr()
def test_admin_accounts_v2(api2):
    accounts = api2.admin_accounts_v2(permissions="staff", origin="local")
    
    assert accounts
    assert len(accounts) > 0
    
    account_self = api2.account_verify_credentials()
    account_admin = api2.admin_account(account_self)
    
    assert(account_admin)
    assert(account_admin.id == account_self.id)

    accounts = api2.admin_accounts_v2(permissions="staff", origin="remote")
    assert len(accounts) == 0
    
    with pytest.raises(MastodonIllegalArgumentError):
        accounts = api2.admin_accounts_v2(permissions="stave")

    with pytest.raises(MastodonIllegalArgumentError):
        accounts = api2.admin_accounts_v2(origin="global")

    with pytest.raises(MastodonIllegalArgumentError):
        accounts = api2.admin_accounts_v2(status="sick")

@pytest.mark.vcr(match_on=['path'])
def test_admin_moderation(api3, api2):
    account_initial = api3.account_verify_credentials()
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
        image = api3.media_post('tests/image.jpg')
        assert image
        status = api3.status_post("oh no!", media_ids=image, sensitive=False)
        assert status
        status = api2.status(status)
        assert status.sensitive
        api3.status_delete(status)

        account = api2.admin_account_unsensitive(account)
        image = api3.media_post('tests/image.jpg')
        assert image
        status = api3.status_post("oh no!", media_ids=image, sensitive=False)
        assert status
        status = api2.status(status)
        assert not status.sensitive
        api3.status_delete(status)

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
def test_admin_reports(api3, api2, status3):
    account = api3.account_verify_credentials()
    account2 = api2.account_verify_credentials()
    report = api2.report(account, status3, "api crimes")
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
    # The management functions are unfortunately not really testable easily.

@pytest.mark.skip(reason="reject / accept of account requests isn't really testable without modifying instance settings. anyone want to fumble those into the DB setup and write this test, please do.")
def test_admin_accountrequests(api2):
    pass

@pytest.mark.vcr()
def test_admin_domain_blocks(api2):
    block = api2.admin_create_domain_block(domain = "chitter.xyz", public_comment="sicko behaviour", severity="suspend")
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
    assert not any(x.id == block3.id for x in api2.admin_domain_blocks())

# Xfail test for domain block that starts with https://
@pytest.mark.xfail
@pytest.mark.vcr()
def test_admin_domain_blocks_protocol(api2):
    api2.admin_create_domain_block(domain = "https://chitter.xyz", public_comment="sicko behaviour", severity="silence")

@pytest.mark.vcr(match_on=['path'])
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

@pytest.mark.vcr()
def test_admin_canonical_email_block(api2):
    blocked_email = "test@example.com"
    try:
        response = api2.admin_create_canonical_email_block(email=blocked_email)
        assert response is not None
        assert hasattr(response, 'id')
        block_id = response.id
        
        test_response = api2.admin_test_canonical_email_block(blocked_email)
        assert any(b.id == block_id for b in test_response)
        
        variations = [
            "Test@example.com",
            "te.st@example.com",
            "test+other@EXAMPLE.com"
        ]
        for variation in variations:
            test_response = api2.admin_test_canonical_email_block(variation)
            assert any(b.id == block_id for b in test_response)
        
        all_blocks = api2.admin_canonical_email_blocks()
        assert any(b.id == block_id for b in all_blocks)
        
        api2.admin_delete_canonical_email_block(block_id)
        
        all_blocks_after_delete = api2.admin_canonical_email_blocks()
        assert not any(b.id == block_id for b in all_blocks_after_delete)
        
        email_hash = hashlib.sha256(blocked_email.encode("utf-8")).hexdigest()
        response = api2.admin_create_canonical_email_block(canonical_email_hash=email_hash)
        assert response is not None
        assert hasattr(response, 'id')
        block_id = response.id
        
        test_response = api2.admin_canonical_email_block(block_id)
        assert test_response.id == block_id
        for variation in variations:
            test_response = api2.admin_test_canonical_email_block(variation)
            assert any(b.id == block_id for b in test_response)
        
    finally:
        try:
            api2.admin_delete_canonical_email_block(block_id)
        except Exception:
            pass


@pytest.mark.vcr(match_on=['path'])
def test_admin_email_domain_blocks(api2):
    test_domain = "blockedexample.com"
    
    created_block = api2.admin_create_email_domain_block(test_domain)
    assert created_block is not None
    assert created_block.domain == test_domain
    
    retrieved_block = api2.admin_email_domain_block(created_block.id)
    assert retrieved_block.id == created_block.id
    assert retrieved_block.domain == test_domain
    
    all_blocks = api2.admin_email_domain_blocks()
    assert any(block.id == created_block.id for block in all_blocks)
    
    api2.admin_delete_email_domain_block(created_block.id)
    
    all_blocks_after_delete = api2.admin_email_domain_blocks()
    assert not any(block.id == created_block.id for block in all_blocks_after_delete)

@pytest.mark.vcr()
def test_admin_ip_blocks(api2):
    try:
        test_ip = "8.8.8.0/24"
        test_severity = "no_access"
        test_comment = "Google DNS is ULTRA BANNED"
        
        created_block = api2.admin_create_ip_block(test_ip, test_severity, comment=test_comment)
        assert created_block is not None
        assert created_block.ip == test_ip
        assert created_block.severity == test_severity
        assert created_block.comment == test_comment
        
        retrieved_block = api2.admin_ip_block(created_block.id)
        assert retrieved_block.id == created_block.id
        assert retrieved_block.ip == test_ip
        assert retrieved_block.severity == test_severity
        
        all_blocks = api2.admin_ip_blocks()
        assert any(block.id == created_block.id for block in all_blocks)
        
        updated_comment = "Updated test block"
        updated_block = api2.admin_update_ip_block(created_block.id, comment=updated_comment)
        assert updated_block.id == created_block.id
        assert updated_block.comment == updated_comment
        
        api2.admin_delete_ip_block(created_block.id)
        
        all_blocks_after_delete = api2.admin_ip_blocks()
        assert not any(block.id == created_block.id for block in all_blocks_after_delete)
    finally:
        all_blocks = api2.admin_ip_blocks()
        for block in all_blocks:
            api2.admin_delete_ip_block(block.id)
