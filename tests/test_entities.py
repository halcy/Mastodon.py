import pytest
import vcr      
from mastodon.return_types import *
from mastodon.types_base import real_issubclass, Entity
from datetime import datetime, timedelta, timezone
import sys
      
# "never record anything with admin in the URL" filter
def vcr_filter(request):
    # Better to be overly paranoid than the put sensitive data into a git repo
    if "admin" in request.path.lower():
        assert False, "Admin functions are not tested by default"
    return request

# Token scrubber
def token_scrubber(response):
    # Find any occurrences of the access token and replace it with DUMMY
    import json
    def zero_out_access_token(body):
        if isinstance(body, dict):
            for key in body:
                if key == "access_token":
                    body[key] = "DUMMY"
                else:
                    zero_out_access_token(body[key])
        elif isinstance(body, list):
            for item in body:
                zero_out_access_token(item)
    body = json.loads(response["body"]["string"])
    zero_out_access_token(body)
    response["body"]["string"] = bytes(json.dumps(body), "utf-8")
    return response

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_account(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.account(23972)
    assert real_issubclass(type(result), Account), str(type(result)) + ' is not a subclass of Account'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Account), str(type(result)) + ' is not a subclass of Account after to_json/from_json'
    result = mastodon.account_verify_credentials()
    assert real_issubclass(type(result), Account), str(type(result)) + ' is not a subclass of Account (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Account), str(type(result)) + ' is not a subclass of Account after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_accountfield(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.account(23972).fields[0]
    assert real_issubclass(type(result), AccountField), str(type(result)) + ' is not a subclass of AccountField'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AccountField), str(type(result)) + ' is not a subclass of AccountField after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_role(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.account_verify_credentials().role
    assert real_issubclass(type(result), Role), str(type(result)) + ' is not a subclass of Role'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Role), str(type(result)) + ' is not a subclass of Role after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_credentialaccountsource(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.account_verify_credentials()["source"]
    assert real_issubclass(type(result), CredentialAccountSource), str(type(result)) + ' is not a subclass of CredentialAccountSource'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), CredentialAccountSource), str(type(result)) + ' is not a subclass of CredentialAccountSource after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_status(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110446223051565765)
    assert real_issubclass(type(result), Status), str(type(result)) + ' is not a subclass of Status'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Status), str(type(result)) + ' is not a subclass of Status after to_json/from_json'
    result = mastodon.status(110446183735368325)
    assert real_issubclass(type(result), Status), str(type(result)) + ' is not a subclass of Status (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Status), str(type(result)) + ' is not a subclass of Status after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_quote(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(115044073088181107).quote
    assert real_issubclass(type(result), Quote), str(type(result)) + ' is not a subclass of Quote'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Quote), str(type(result)) + ' is not a subclass of Quote after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_shallowquote(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(115044073088181107).quote.quoted_status.quote
    assert real_issubclass(type(result), ShallowQuote), str(type(result)) + ' is not a subclass of ShallowQuote'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), ShallowQuote), str(type(result)) + ' is not a subclass of ShallowQuote after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_statusedit(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status_history(110446223051565765)[-1]
    assert real_issubclass(type(result), StatusEdit), str(type(result)) + ' is not a subclass of StatusEdit'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), StatusEdit), str(type(result)) + ' is not a subclass of StatusEdit after to_json/from_json'
    result = mastodon.status_history(110446183735368325)[-1]
    assert real_issubclass(type(result), StatusEdit), str(type(result)) + ' is not a subclass of StatusEdit (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), StatusEdit), str(type(result)) + ' is not a subclass of StatusEdit after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_filterresult(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447998920481458).filtered[0]
    assert real_issubclass(type(result), FilterResult), str(type(result)) + ' is not a subclass of FilterResult'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), FilterResult), str(type(result)) + ' is not a subclass of FilterResult after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_statusmention(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110446223051565765).mentions[0]
    assert real_issubclass(type(result), StatusMention), str(type(result)) + ' is not a subclass of StatusMention'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), StatusMention), str(type(result)) + ' is not a subclass of StatusMention after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_scheduledstatus(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status_post("posting in the far future", scheduled_at=datetime(2100,12,12))
    assert real_issubclass(type(result), ScheduledStatus), str(type(result)) + ' is not a subclass of ScheduledStatus'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), ScheduledStatus), str(type(result)) + ' is not a subclass of ScheduledStatus after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_scheduledstatusparams(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status_post("posting in the far future", scheduled_at=datetime(2100,12,12)).params
    assert real_issubclass(type(result), ScheduledStatusParams), str(type(result)) + ' is not a subclass of ScheduledStatusParams'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), ScheduledStatusParams), str(type(result)) + ' is not a subclass of ScheduledStatusParams after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_poll(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110446383900387196).poll
    assert real_issubclass(type(result), Poll), str(type(result)) + ' is not a subclass of Poll'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Poll), str(type(result)) + ' is not a subclass of Poll after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_polloption(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110446383900387196).poll.options[0]
    assert real_issubclass(type(result), PollOption), str(type(result)) + ' is not a subclass of PollOption'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), PollOption), str(type(result)) + ' is not a subclass of PollOption after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_conversation(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.conversations()[0]
    assert real_issubclass(type(result), Conversation), str(type(result)) + ' is not a subclass of Conversation'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Conversation), str(type(result)) + ' is not a subclass of Conversation after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_tag(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.trending_tags()[0]
    assert real_issubclass(type(result), Tag), str(type(result)) + ' is not a subclass of Tag'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Tag), str(type(result)) + ' is not a subclass of Tag after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_taghistory(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.trending_tags()[0].history[0]
    assert real_issubclass(type(result), TagHistory), str(type(result)) + ' is not a subclass of TagHistory'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), TagHistory), str(type(result)) + ' is not a subclass of TagHistory after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_customemoji(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110446223051565765).emojis[0]
    assert real_issubclass(type(result), CustomEmoji), str(type(result)) + ' is not a subclass of CustomEmoji'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), CustomEmoji), str(type(result)) + ' is not a subclass of CustomEmoji after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_application(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.app_verify_credentials()
    assert real_issubclass(type(result), Application), str(type(result)) + ' is not a subclass of Application'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Application), str(type(result)) + ' is not a subclass of Application after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_relationship(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.account_relationships(23972)[0]
    assert real_issubclass(type(result), Relationship), str(type(result)) + ' is not a subclass of Relationship'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Relationship), str(type(result)) + ' is not a subclass of Relationship after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_filter(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.filters()[0]
    assert real_issubclass(type(result), Filter), str(type(result)) + ' is not a subclass of Filter'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Filter), str(type(result)) + ' is not a subclass of Filter after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_filterv2(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.filters_v2()[0]
    assert real_issubclass(type(result), FilterV2), str(type(result)) + ' is not a subclass of FilterV2'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), FilterV2), str(type(result)) + ' is not a subclass of FilterV2 after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_notification(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.notifications()[0]
    assert real_issubclass(type(result), Notification), str(type(result)) + ' is not a subclass of Notification'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Notification), str(type(result)) + ' is not a subclass of Notification after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_context(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status_context(110446983926957470)
    assert real_issubclass(type(result), Context), str(type(result)) + ' is not a subclass of Context'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Context), str(type(result)) + ' is not a subclass of Context after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_userlist(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.lists()[0]
    assert real_issubclass(type(result), UserList), str(type(result)) + ' is not a subclass of UserList'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), UserList), str(type(result)) + ' is not a subclass of UserList after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_mediaattachment(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447012773105565).media_attachments[0]
    assert real_issubclass(type(result), MediaAttachment), str(type(result)) + ' is not a subclass of MediaAttachment'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachment), str(type(result)) + ' is not a subclass of MediaAttachment after to_json/from_json'
    result = mastodon.status(110447003454258227).media_attachments[0]
    assert real_issubclass(type(result), MediaAttachment), str(type(result)) + ' is not a subclass of MediaAttachment (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachment), str(type(result)) + ' is not a subclass of MediaAttachment after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_mediaattachmentmetadatacontainer(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447012773105565).media_attachments[0].meta
    assert real_issubclass(type(result), MediaAttachmentMetadataContainer), str(type(result)) + ' is not a subclass of MediaAttachmentMetadataContainer'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentMetadataContainer), str(type(result)) + ' is not a subclass of MediaAttachmentMetadataContainer after to_json/from_json'
    result = mastodon.status(110447003454258227).media_attachments[0].meta
    assert real_issubclass(type(result), MediaAttachmentMetadataContainer), str(type(result)) + ' is not a subclass of MediaAttachmentMetadataContainer (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentMetadataContainer), str(type(result)) + ' is not a subclass of MediaAttachmentMetadataContainer after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_mediaattachmentimagemetadata(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447003454258227).media_attachments[0].meta.original
    assert real_issubclass(type(result), MediaAttachmentImageMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentImageMetadata'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentImageMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentImageMetadata after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_mediaattachmentvideometadata(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447001287656894).media_attachments[0].meta.original
    assert real_issubclass(type(result), MediaAttachmentVideoMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentVideoMetadata'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentVideoMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentVideoMetadata after to_json/from_json'
    result = mastodon.status(113358687695262945).media_attachments[0].meta.original
    assert real_issubclass(type(result), MediaAttachmentVideoMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentVideoMetadata (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentVideoMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentVideoMetadata after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_mediaattachmentaudiometadata(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447012773105565).media_attachments[0].meta.original
    assert real_issubclass(type(result), MediaAttachmentAudioMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentAudioMetadata'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentAudioMetadata), str(type(result)) + ' is not a subclass of MediaAttachmentAudioMetadata after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_mediaattachmentfocuspoint(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447003454258227).media_attachments[0].meta.focus
    assert real_issubclass(type(result), MediaAttachmentFocusPoint), str(type(result)) + ' is not a subclass of MediaAttachmentFocusPoint'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentFocusPoint), str(type(result)) + ' is not a subclass of MediaAttachmentFocusPoint after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_mediaattachmentcolors(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status(110447012773105565).media_attachments[0].meta.colors
    assert real_issubclass(type(result), MediaAttachmentColors), str(type(result)) + ' is not a subclass of MediaAttachmentColors'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), MediaAttachmentColors), str(type(result)) + ' is not a subclass of MediaAttachmentColors after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_previewcard(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status_card(110447098625216345)
    assert real_issubclass(type(result), PreviewCard), str(type(result)) + ' is not a subclass of PreviewCard'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), PreviewCard), str(type(result)) + ' is not a subclass of PreviewCard after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_trendinglinkhistory(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.trending_links()[0].history[0]
    assert real_issubclass(type(result), TrendingLinkHistory), str(type(result)) + ' is not a subclass of TrendingLinkHistory'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), TrendingLinkHistory), str(type(result)) + ' is not a subclass of TrendingLinkHistory after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_previewcardauthor(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status_card(113481707975926080).authors[0]
    assert real_issubclass(type(result), PreviewCardAuthor), str(type(result)) + ' is not a subclass of PreviewCardAuthor'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), PreviewCardAuthor), str(type(result)) + ' is not a subclass of PreviewCardAuthor after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_searchv2(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.search("halcy")
    assert real_issubclass(type(result), SearchV2), str(type(result)) + ' is not a subclass of SearchV2'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), SearchV2), str(type(result)) + ' is not a subclass of SearchV2 after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instance(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v1()
    assert real_issubclass(type(result), Instance), str(type(result)) + ' is not a subclass of Instance'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Instance), str(type(result)) + ' is not a subclass of Instance after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceconfiguration(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v1().configuration
    assert real_issubclass(type(result), InstanceConfiguration), str(type(result)) + ' is not a subclass of InstanceConfiguration'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceConfiguration), str(type(result)) + ' is not a subclass of InstanceConfiguration after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceurls(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v1().urls
    assert real_issubclass(type(result), InstanceURLs), str(type(result)) + ' is not a subclass of InstanceURLs'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceURLs), str(type(result)) + ' is not a subclass of InstanceURLs after to_json/from_json'
    result = mastodon.instance_v1().urls
    assert real_issubclass(type(result), InstanceURLs), str(type(result)) + ' is not a subclass of InstanceURLs (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceURLs), str(type(result)) + ' is not a subclass of InstanceURLs after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancev2(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v2()
    assert real_issubclass(type(result), InstanceV2), str(type(result)) + ' is not a subclass of InstanceV2'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceV2), str(type(result)) + ' is not a subclass of InstanceV2 after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceicon(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v2().icon[0]
    assert real_issubclass(type(result), InstanceIcon), str(type(result)) + ' is not a subclass of InstanceIcon'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceIcon), str(type(result)) + ' is not a subclass of InstanceIcon after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceconfigurationv2(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v2().configuration
    assert real_issubclass(type(result), InstanceConfigurationV2), str(type(result)) + ' is not a subclass of InstanceConfigurationV2'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceConfigurationV2), str(type(result)) + ' is not a subclass of InstanceConfigurationV2 after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancevapidkey(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v2().configuration.vapid
    assert real_issubclass(type(result), InstanceVapidKey), str(type(result)) + ' is not a subclass of InstanceVapidKey'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceVapidKey), str(type(result)) + ' is not a subclass of InstanceVapidKey after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceurlsv2(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v2().configuration.urls
    assert real_issubclass(type(result), InstanceURLsV2), str(type(result)) + ' is not a subclass of InstanceURLsV2'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceURLsV2), str(type(result)) + ' is not a subclass of InstanceURLsV2 after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancethumbnail(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().thumbnail
    assert real_issubclass(type(result), InstanceThumbnail), str(type(result)) + ' is not a subclass of InstanceThumbnail'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceThumbnail), str(type(result)) + ' is not a subclass of InstanceThumbnail after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancethumbnailversions(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().thumbnail.versions
    assert real_issubclass(type(result), InstanceThumbnailVersions), str(type(result)) + ' is not a subclass of InstanceThumbnailVersions'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceThumbnailVersions), str(type(result)) + ' is not a subclass of InstanceThumbnailVersions after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancestatistics(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v1().stats
    assert real_issubclass(type(result), InstanceStatistics), str(type(result)) + ' is not a subclass of InstanceStatistics'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceStatistics), str(type(result)) + ' is not a subclass of InstanceStatistics after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceusage(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().usage
    assert real_issubclass(type(result), InstanceUsage), str(type(result)) + ' is not a subclass of InstanceUsage'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceUsage), str(type(result)) + ' is not a subclass of InstanceUsage after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceusageusers(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().usage.users
    assert real_issubclass(type(result), InstanceUsageUsers), str(type(result)) + ' is not a subclass of InstanceUsageUsers'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceUsageUsers), str(type(result)) + ' is not a subclass of InstanceUsageUsers after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_ruletranslation(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().rules[0].translations['de']
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), RuleTranslation), str(type(result)) + ' is not a subclass of RuleTranslation'
        result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), RuleTranslation), str(type(result)) + ' is not a subclass of RuleTranslation after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_rule(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().rules[0]
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Rule), str(type(result)) + ' is not a subclass of Rule'
        result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Rule), str(type(result)) + ' is not a subclass of Rule after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceregistrations(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v2().registrations
    assert real_issubclass(type(result), InstanceRegistrations), str(type(result)) + ' is not a subclass of InstanceRegistrations'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceRegistrations), str(type(result)) + ' is not a subclass of InstanceRegistrations after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancecontact(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().contact
    assert real_issubclass(type(result), InstanceContact), str(type(result)) + ' is not a subclass of InstanceContact'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceContact), str(type(result)) + ' is not a subclass of InstanceContact after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instanceaccountconfiguration(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().configuration.accounts
    assert real_issubclass(type(result), InstanceAccountConfiguration), str(type(result)) + ' is not a subclass of InstanceAccountConfiguration'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceAccountConfiguration), str(type(result)) + ' is not a subclass of InstanceAccountConfiguration after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancestatusconfiguration(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().configuration.statuses
    assert real_issubclass(type(result), InstanceStatusConfiguration), str(type(result)) + ' is not a subclass of InstanceStatusConfiguration'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceStatusConfiguration), str(type(result)) + ' is not a subclass of InstanceStatusConfiguration after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancetranslationconfiguration(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_v2().configuration.translation
    assert real_issubclass(type(result), InstanceTranslationConfiguration), str(type(result)) + ' is not a subclass of InstanceTranslationConfiguration'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceTranslationConfiguration), str(type(result)) + ' is not a subclass of InstanceTranslationConfiguration after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancemediaconfiguration(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().configuration.media_attachments
    assert real_issubclass(type(result), InstanceMediaConfiguration), str(type(result)) + ' is not a subclass of InstanceMediaConfiguration'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstanceMediaConfiguration), str(type(result)) + ' is not a subclass of InstanceMediaConfiguration after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_instancepollconfiguration(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance().configuration.polls
    assert real_issubclass(type(result), InstancePollConfiguration), str(type(result)) + ' is not a subclass of InstancePollConfiguration'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), InstancePollConfiguration), str(type(result)) + ' is not a subclass of InstancePollConfiguration after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_nodeinfo(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_nodeinfo()
    assert real_issubclass(type(result), Nodeinfo), str(type(result)) + ' is not a subclass of Nodeinfo'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Nodeinfo), str(type(result)) + ' is not a subclass of Nodeinfo after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_nodeinfosoftware(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_nodeinfo().software
    assert real_issubclass(type(result), NodeinfoSoftware), str(type(result)) + ' is not a subclass of NodeinfoSoftware'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NodeinfoSoftware), str(type(result)) + ' is not a subclass of NodeinfoSoftware after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_nodeinfoservices(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_nodeinfo().services
    assert real_issubclass(type(result), NodeinfoServices), str(type(result)) + ' is not a subclass of NodeinfoServices'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NodeinfoServices), str(type(result)) + ' is not a subclass of NodeinfoServices after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_nodeinfousage(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_nodeinfo().usage
    assert real_issubclass(type(result), NodeinfoUsage), str(type(result)) + ' is not a subclass of NodeinfoUsage'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NodeinfoUsage), str(type(result)) + ' is not a subclass of NodeinfoUsage after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_nodeinfousageusers(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_nodeinfo().usage.users
    assert real_issubclass(type(result), NodeinfoUsageUsers), str(type(result)) + ' is not a subclass of NodeinfoUsageUsers'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NodeinfoUsageUsers), str(type(result)) + ' is not a subclass of NodeinfoUsageUsers after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_nodeinfometadata(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_nodeinfo().metadata
    assert real_issubclass(type(result), NodeinfoMetadata), str(type(result)) + ' is not a subclass of NodeinfoMetadata'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NodeinfoMetadata), str(type(result)) + ' is not a subclass of NodeinfoMetadata after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_activity(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_activity()[0]
    assert real_issubclass(type(result), Activity), str(type(result)) + ' is not a subclass of Activity'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Activity), str(type(result)) + ' is not a subclass of Activity after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_adminreport(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_reports()[-1]
    assert real_issubclass(type(result), AdminReport), str(type(result)) + ' is not a subclass of AdminReport'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminReport), str(type(result)) + ' is not a subclass of AdminReport after to_json/from_json'
    result = mastodon.admin_reports(resolved=True)[-1]
    assert real_issubclass(type(result), AdminReport), str(type(result)) + ' is not a subclass of AdminReport (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminReport), str(type(result)) + ' is not a subclass of AdminReport after to_json/from_json (additional function)'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_webpushsubscription(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.push_subscription_set("http://halcy.de/",mastodon.push_subscription_generate_keys()[1],follow_events=True)
    assert real_issubclass(type(result), WebPushSubscription), str(type(result)) + ' is not a subclass of WebPushSubscription'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), WebPushSubscription), str(type(result)) + ' is not a subclass of WebPushSubscription after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_webpushsubscriptionalerts(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.push_subscription_set("http://halcy.de/",mastodon.push_subscription_generate_keys()[1],follow_events=True).alerts
    assert real_issubclass(type(result), WebPushSubscriptionAlerts), str(type(result)) + ' is not a subclass of WebPushSubscriptionAlerts'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), WebPushSubscriptionAlerts), str(type(result)) + ' is not a subclass of WebPushSubscriptionAlerts after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_preferences(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.preferences()
    assert real_issubclass(type(result), Preferences), str(type(result)) + ' is not a subclass of Preferences'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Preferences), str(type(result)) + ' is not a subclass of Preferences after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_featuredtag(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.featured_tags()[0]
    assert real_issubclass(type(result), FeaturedTag), str(type(result)) + ' is not a subclass of FeaturedTag'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), FeaturedTag), str(type(result)) + ' is not a subclass of FeaturedTag after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_marker(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.markers_get()["home"]
    assert real_issubclass(type(result), Marker), str(type(result)) + ' is not a subclass of Marker'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Marker), str(type(result)) + ' is not a subclass of Marker after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_announcement(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.announcements()[0]
    assert real_issubclass(type(result), Announcement), str(type(result)) + ' is not a subclass of Announcement'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Announcement), str(type(result)) + ' is not a subclass of Announcement after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_reaction(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.announcements()[0].reactions[0]
    assert real_issubclass(type(result), Reaction), str(type(result)) + ' is not a subclass of Reaction'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Reaction), str(type(result)) + ' is not a subclass of Reaction after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_familiarfollowers(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.account_familiar_followers(2)[0]
    assert real_issubclass(type(result), FamiliarFollowers), str(type(result)) + ' is not a subclass of FamiliarFollowers'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), FamiliarFollowers), str(type(result)) + ' is not a subclass of FamiliarFollowers after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_adminaccount(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_account(1)
    assert real_issubclass(type(result), AdminAccount), str(type(result)) + ' is not a subclass of AdminAccount'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminAccount), str(type(result)) + ' is not a subclass of AdminAccount after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_adminip(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_account(1).ips[0]
    assert real_issubclass(type(result), AdminIp), str(type(result)) + ' is not a subclass of AdminIp'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminIp), str(type(result)) + ' is not a subclass of AdminIp after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_adminmeasure(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_measures(datetime.now() - timedelta(hours=24*5), datetime.now(), interactions=True)[0]
    assert real_issubclass(type(result), AdminMeasure), str(type(result)) + ' is not a subclass of AdminMeasure'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminMeasure), str(type(result)) + ' is not a subclass of AdminMeasure after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_adminmeasuredata(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_measures(datetime.now() - timedelta(hours=24*5), datetime.now(), active_users=True)[0].data[0]
    assert real_issubclass(type(result), AdminMeasureData), str(type(result)) + ' is not a subclass of AdminMeasureData'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminMeasureData), str(type(result)) + ' is not a subclass of AdminMeasureData after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_admindimension(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_dimensions(datetime.now() - timedelta(hours=24*5), datetime.now(), languages=True)[0]
    assert real_issubclass(type(result), AdminDimension), str(type(result)) + ' is not a subclass of AdminDimension'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminDimension), str(type(result)) + ' is not a subclass of AdminDimension after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_admindimensiondata(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_dimensions(datetime.now() - timedelta(hours=24*5), datetime.now(), languages=True)[0].data[0]
    assert real_issubclass(type(result), AdminDimensionData), str(type(result)) + ' is not a subclass of AdminDimensionData'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminDimensionData), str(type(result)) + ' is not a subclass of AdminDimensionData after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_adminretention(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_retention(datetime.now() - timedelta(hours=24*5), datetime.now())[0]
    assert real_issubclass(type(result), AdminRetention), str(type(result)) + ' is not a subclass of AdminRetention'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminRetention), str(type(result)) + ' is not a subclass of AdminRetention after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_admincohort(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_retention(datetime.now() - timedelta(hours=24*5), datetime.now())[0].data[0]
    assert real_issubclass(type(result), AdminCohort), str(type(result)) + ' is not a subclass of AdminCohort'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminCohort), str(type(result)) + ' is not a subclass of AdminCohort after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_admindomainblock(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_domain_blocks()[0]
    assert real_issubclass(type(result), AdminDomainBlock), str(type(result)) + ' is not a subclass of AdminDomainBlock'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminDomainBlock), str(type(result)) + ' is not a subclass of AdminDomainBlock after to_json/from_json'

@pytest.mark.skip(reason="Admin functions are not tested by default")
@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_adminipblock(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.admin_ip_blocks()[0]
    assert real_issubclass(type(result), AdminIpBlock), str(type(result)) + ' is not a subclass of AdminIpBlock'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AdminIpBlock), str(type(result)) + ' is not a subclass of AdminIpBlock after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_domainblock(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.instance_domain_blocks()[0]
    assert real_issubclass(type(result), DomainBlock), str(type(result)) + ' is not a subclass of DomainBlock'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), DomainBlock), str(type(result)) + ' is not a subclass of DomainBlock after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_extendeddescription(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_extended_description()
    assert real_issubclass(type(result), ExtendedDescription), str(type(result)) + ' is not a subclass of ExtendedDescription'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), ExtendedDescription), str(type(result)) + ' is not a subclass of ExtendedDescription after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_filterkeyword(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.filters_v2()[0].keywords[0]
    assert real_issubclass(type(result), FilterKeyword), str(type(result)) + ' is not a subclass of FilterKeyword'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), FilterKeyword), str(type(result)) + ' is not a subclass of FilterKeyword after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_filterstatus(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.filter_statuses_v2(mastodon.filters_v2()[0])[0]
    assert real_issubclass(type(result), FilterStatus), str(type(result)) + ' is not a subclass of FilterStatus'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), FilterStatus), str(type(result)) + ' is not a subclass of FilterStatus after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_statussource(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.status_source(110446223051565765)
    assert real_issubclass(type(result), StatusSource), str(type(result)) + ' is not a subclass of StatusSource'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), StatusSource), str(type(result)) + ' is not a subclass of StatusSource after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_suggestion(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.suggestions_v2()[0]
    assert real_issubclass(type(result), Suggestion), str(type(result)) + ' is not a subclass of Suggestion'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), Suggestion), str(type(result)) + ' is not a subclass of Suggestion after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_accountcreationerror(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.create_account('halcy', 'secret', 'invalid email lol', True, return_detailed_error=True)[1]
    assert real_issubclass(type(result), AccountCreationError), str(type(result)) + ' is not a subclass of AccountCreationError'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AccountCreationError), str(type(result)) + ' is not a subclass of AccountCreationError after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_accountcreationerrordetails(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.create_account('halcy', 'secret', 'invalid email lol', False, return_detailed_error=True)[1].details
    assert real_issubclass(type(result), AccountCreationErrorDetails), str(type(result)) + ' is not a subclass of AccountCreationErrorDetails'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AccountCreationErrorDetails), str(type(result)) + ' is not a subclass of AccountCreationErrorDetails after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_accountcreationerrordetailsfield(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.create_account('halcy', 'secret', 'invalid email lol', True, return_detailed_error=True)[1].details.email[0]
    assert real_issubclass(type(result), AccountCreationErrorDetailsField), str(type(result)) + ' is not a subclass of AccountCreationErrorDetailsField'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), AccountCreationErrorDetailsField), str(type(result)) + ' is not a subclass of AccountCreationErrorDetailsField after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_notificationpolicy(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.notifications_policy()
    assert real_issubclass(type(result), NotificationPolicy), str(type(result)) + ' is not a subclass of NotificationPolicy'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NotificationPolicy), str(type(result)) + ' is not a subclass of NotificationPolicy after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_notificationpolicysummary(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.notifications_policy().summary
    assert real_issubclass(type(result), NotificationPolicySummary), str(type(result)) + ' is not a subclass of NotificationPolicySummary'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NotificationPolicySummary), str(type(result)) + ' is not a subclass of NotificationPolicySummary after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_groupednotificationsresults(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.grouped_notifications()
    assert real_issubclass(type(result), GroupedNotificationsResults), str(type(result)) + ' is not a subclass of GroupedNotificationsResults'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), GroupedNotificationsResults), str(type(result)) + ' is not a subclass of GroupedNotificationsResults after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_partialaccountwithavatar(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.grouped_notifications().partial_accounts[0]
    assert real_issubclass(type(result), PartialAccountWithAvatar), str(type(result)) + ' is not a subclass of PartialAccountWithAvatar'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), PartialAccountWithAvatar), str(type(result)) + ' is not a subclass of PartialAccountWithAvatar after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_notificationgroup(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.grouped_notifications().notification_groups[0]
    assert real_issubclass(type(result), NotificationGroup), str(type(result)) + ' is not a subclass of NotificationGroup'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), NotificationGroup), str(type(result)) + ' is not a subclass of NotificationGroup after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_unreadnotificationscount(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.notifications_unread_count()
    assert real_issubclass(type(result), UnreadNotificationsCount), str(type(result)) + ' is not a subclass of UnreadNotificationsCount'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), UnreadNotificationsCount), str(type(result)) + ' is not a subclass of UnreadNotificationsCount after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_supportedlocale(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.instance_languages()[0]
    assert real_issubclass(type(result), SupportedLocale), str(type(result)) + ' is not a subclass of SupportedLocale'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), SupportedLocale), str(type(result)) + ' is not a subclass of SupportedLocale after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_oauthserverinfo(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.oauth_authorization_server_info()
    assert real_issubclass(type(result), OAuthServerInfo), str(type(result)) + ' is not a subclass of OAuthServerInfo'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), OAuthServerInfo), str(type(result)) + ' is not a subclass of OAuthServerInfo after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_oauthuserinfo(mastodon_base, mastodon_admin):
    mastodon = mastodon_base
    result = mastodon.oauth_userinfo()
    assert real_issubclass(type(result), OAuthUserInfo), str(type(result)) + ' is not a subclass of OAuthUserInfo'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), OAuthUserInfo), str(type(result)) + ' is not a subclass of OAuthUserInfo after to_json/from_json'

@pytest.mark.vcr(
    filter_query_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_post_data_parameters=[('access_token', 'DUMMY'), ('client_id', 'DUMMY'), ('client_secret', 'DUMMY')],
    filter_headers=[('Authorization', 'DUMMY')],
    before_record_request=vcr_filter,
    before_record_response=token_scrubber,
    match_on=['method', 'uri'],
    cassette_library_dir='tests/cassettes_entity_tests'
)
def test_entity_termsofservice(mastodon_base, mastodon_admin):
    mastodon = mastodon_admin
    result = mastodon.instance_terms_of_service()
    assert real_issubclass(type(result), TermsOfService), str(type(result)) + ' is not a subclass of TermsOfService'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), TermsOfService), str(type(result)) + ' is not a subclass of TermsOfService after to_json/from_json'
    result = mastodon.instance_terms_of_service(datetime(2025, 8, 17))
    assert real_issubclass(type(result), TermsOfService), str(type(result)) + ' is not a subclass of TermsOfService (additional function)'
    result = Entity.from_json(result.to_json())
    if sys.version_info >= (3, 9):
        assert real_issubclass(type(result), TermsOfService), str(type(result)) + ' is not a subclass of TermsOfService after to_json/from_json (additional function)'

