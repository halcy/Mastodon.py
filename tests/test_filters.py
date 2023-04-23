import pytest
import time
import vcr

@pytest.mark.vcr()
def test_filter_create(api):
    with vcr.use_cassette('test_filter_create.yaml', cassette_library_dir='tests/cassettes_pre_4_0_0', record_mode='none'):
        keyword_filter = api.filter_create("anime", ['notifications'], irreversible = False, whole_word = True, expires_in = None)
        try:
            assert keyword_filter
            
            all_filters = api.filters()
            assert keyword_filter in all_filters
            assert keyword_filter.irreversible is False
            assert keyword_filter.whole_word is True
            
            keyword_filter_2 = api.filter(keyword_filter.id)
            assert(keyword_filter == keyword_filter_2)
        finally:
            api.filter_delete(keyword_filter)
    
    
        keyword_filter = api.filter_create("anime", ['notifications'], irreversible = False, whole_word = False, expires_in = None)
        try:
            assert keyword_filter
            assert keyword_filter.irreversible is False
            assert keyword_filter.whole_word is False
            
            all_filters = api.filters()
            assert(keyword_filter in all_filters)
            
            keyword_filter_2 = api.filter(keyword_filter.id)
            assert(keyword_filter == keyword_filter_2)
        finally:
            api.filter_delete(keyword_filter)
        time.sleep(2)
    
@pytest.mark.vcr()
def test_filter_update(api):
    with vcr.use_cassette('test_filter_update.yaml', cassette_library_dir='tests/cassettes_pre_4_0_0', record_mode='none'):
        keyword_filter = api.filter_create("anime", ['notifications'], irreversible = False, whole_word = True, expires_in = None)
        keyword_filter_2 = api.filter_update(keyword_filter, phrase = "japanimation")
        keyword_filter = api.filter(keyword_filter.id)
        assert(keyword_filter.phrase == "japanimation")

@pytest.mark.vcr()
def test_filter_serverside(api, api2):
    with vcr.use_cassette('test_filter_serverside.yaml', cassette_library_dir='tests/cassettes_pre_4_0_0', record_mode='none'):
        api.account_follow(api2.account_verify_credentials())
        keyword_filter_1 = api.filter_create("anime", ['home'], irreversible = True, whole_word = False, expires_in = None)
        keyword_filter_2 = api.filter_create("girugamesh", ['home'], irreversible = True, whole_word = True, expires_in = None)
        keyword_filter_3 = api.filter_create("japanimation", ['notifications'], irreversible = True, whole_word = True, expires_in = None)
        time.sleep(2)
        status_1 = api2.toot("I love animes")
        status_2 = api2.toot("Girugamesh!")
        status_3 = api2.toot("Girugameshnetworking!")
        status_4 = api2.toot("I love japanimation!")
        time.sleep(2)
        tl = api.timeline_home()
        try:
            st_ids = {st["id"] for st in tl}
            assert status_1["id"] not in st_ids
            assert status_2["id"] not in st_ids
            assert status_3["id"] in st_ids
            assert status_4["id"] in st_ids
        finally:
            api.filter_delete(keyword_filter_1)
            api.filter_delete(keyword_filter_2)
            api.filter_delete(keyword_filter_3)
            api2.status_delete(status_1)
            api2.status_delete(status_2)
            api2.status_delete(status_3)
            api2.status_delete(status_4)
        time.sleep(2)
        
@pytest.mark.vcr()
def test_filter_clientside(api, api2):
    with vcr.use_cassette('test_filter_clientside.yaml', cassette_library_dir='tests/cassettes_pre_4_0_0', record_mode='none'):
        # Make sure no filters are left over from some previous run
        # Unclean, but neccesary
        all_filters = api.filters()
        for mastodon_filter in all_filters:
            api.filter_delete(mastodon_filter)
        
        time.sleep(2)
        api.account_follow(api2.account_verify_credentials())
        keyword_filter_1 = api.filter_create("anime", ['home'], irreversible = False, whole_word = False, expires_in = None)
        keyword_filter_2 = api.filter_create("girugamesh", ['home'], irreversible = False, whole_word = True, expires_in = None)
        keyword_filter_3 = api.filter_create("japanimation", ['notifications'], irreversible = False, whole_word = True, expires_in = None)
        status_1 = api2.toot("I love animes")
        status_2 = api2.toot("Girugamesh!")
        status_3 = api2.toot("Girugameshnetworking!")
        status_4 = api2.toot("I love japanimation!")
        time.sleep(2)
        
        tl = api.timeline_home()
        try:
            st_ids = {st["id"] for st in tl}
            assert status_1['id'] in st_ids
            assert status_2['id'] in st_ids
            assert status_3['id'] in st_ids
            assert status_4['id'] in st_ids
            
            filtered = api.filters_apply(tl, [keyword_filter_1, keyword_filter_2, keyword_filter_3], 'home')
            st_ids = {st["id"] for st in filtered}
            assert status_1['id'] not in st_ids
            assert status_2['id'] not in st_ids
            assert status_3['id'] in st_ids
            assert status_4['id'] in st_ids
        finally:
            api.filter_delete(keyword_filter_1)
            api.filter_delete(keyword_filter_2)
            api.filter_delete(keyword_filter_3)
            api2.status_delete(status_1)
            api2.status_delete(status_2)
            api2.status_delete(status_3)
            api2.status_delete(status_4)
