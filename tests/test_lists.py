import pytest
import time

@pytest.fixture()
def mastodon_list(api):
    mastodon_list = api.list_create('ham burglars')
    yield mastodon_list
    api.list_delete(mastodon_list)

@pytest.mark.vcr()
def test_list_create(api, mastodon_list):
    assert mastodon_list in api.lists()

@pytest.mark.vcr()
def test_list_update(api, mastodon_list):
    mastodon_list_modified = api.list_update(mastodon_list, 'fry kids')
    assert not mastodon_list in api.lists()
    assert mastodon_list_modified in api.lists()
    assert api.list(mastodon_list) == mastodon_list_modified
    
@pytest.mark.vcr()
def test_list_add_remove_account(api, api2, mastodon_list):
    user = api2.account_verify_credentials()
    
    api.account_follow(user)
    api.list_accounts_add(mastodon_list, user)
    assert user.id in map(lambda x: x.id, api.list_accounts(mastodon_list))
    
    api.account_unfollow(user)
    assert len(api.list_accounts(mastodon_list)) == 0
    
    api.account_follow(user)
    api.list_accounts_add(mastodon_list, user)
    assert user.id in map(lambda x: x.id, api.list_accounts(mastodon_list))
    
    api.list_accounts_delete(mastodon_list, user)
    assert len(api.list_accounts(mastodon_list)) == 0
    
    api.account_unfollow(user)
    
@pytest.mark.vcr()
def test_list_by_account(api, api2, mastodon_list):
    user = api2.account_verify_credentials()
    
    api.account_follow(user)
    api.list_accounts_add(mastodon_list, user)
    assert mastodon_list in api.account_lists(user)
    api.account_unfollow(user)
    
@pytest.mark.vcr()
def test_list_timeline(api, api2, mastodon_list):
    user = api2.account_verify_credentials()
    
    api.account_follow(user)
    api.list_accounts_add(mastodon_list, user)
    
    status = api2.status_post("I have never stolen a ham in my life.", visibility="public")
    time.sleep(2)
    list_tl = list(map(lambda x: x.id, api.timeline_list(mastodon_list)))
    assert status.id in list_tl
    
    api2.status_delete(status)
    api.account_unfollow(user)
    