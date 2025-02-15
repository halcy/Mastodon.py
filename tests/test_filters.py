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

@pytest.mark.vcr()
def test_v2_filters_keywords(api2):
    new_filter = api2.create_filter_v2(
        title="Test Filter",
        context=["home", "public"],
        filter_action="warn",
        keywords_attributes=[
            {"keyword": "spam", "whole_word": True},
            {"keyword": "eggs", "whole_word": False}
        ]
    )
    assert new_filter is not None
    assert new_filter["title"] == "Test Filter"
    assert len(new_filter["keywords"]) == 2

    filter_id = new_filter["id"]

    try:
        fetched_filter = api2.filter_v2(filter_id)
        assert fetched_filter["title"] == "Test Filter"

        updated_filter = api2.update_filter_v2(
            filter_id,
            title="Updated Title",
            filter_action="hide"
        )
        assert updated_filter["title"] == "Updated Title"
        assert updated_filter["filter_action"] == "hide"

        filter_keywords = api2.filter_keywords_v2(filter_id)
        assert len(filter_keywords) == 2
        keyword_ids = [kw["id"] for kw in filter_keywords]

        new_kw = api2.add_filter_keyword_v2(filter_id, keyword="foo", whole_word=True)
        assert new_kw["keyword"] == "foo"
        updated_keywords = api2.filter_keywords_v2(filter_id)
        assert len(updated_keywords) == 3

        api2.delete_filter_keyword_v2(keyword_ids[0])
        after_delete_keywords = api2.filter_keywords_v2(filter_id)
        assert len(after_delete_keywords) == 2

    finally:
        api2.delete_filter_v2(filter_id)

@pytest.mark.vcr()
def test_v2_filters_statuses(api2, api):
    new_filter = api2.create_filter_v2(
        title="Status Filter Test",
        context=["home"],
        filter_action="warn",
    )
    assert new_filter is not None
    filter_id = new_filter["id"]

    status = api.status_post("This is a test status for filter!", visibility="public")
    status_id = status["id"]

    try:
        filter_status = api2.add_filter_status_v2(filter_id, status_id)
        assert filter_status is not None
        assert filter_status["status_id"] == status_id

        statuses_list = api2.filter_statuses_v2(filter_id)
        assert len(statuses_list) == 1
        assert statuses_list[0]["status_id"] == status_id

        filter_status_id = statuses_list[0]["id"]

        single_status = api2.filter_status_v2(filter_status_id)
        assert single_status["id"] == filter_status_id
        assert single_status["status_id"] == status_id

    finally:
        statuses_list = api2.filter_statuses_v2(filter_id)
        for st in statuses_list:
            api2.delete_filter_status_v2(st["id"])

        api2.delete_filter_v2(filter_id)

        # Clean up the status
        if status_id:
            api.status_delete(status_id)
