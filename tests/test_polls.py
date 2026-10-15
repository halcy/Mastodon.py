import pytest

@pytest.mark.vcr()
def test_polls(api, api2):
    poll_params = api2.make_poll(["four twenty", "sixty-nine"], 300, multiple=True)
    status_poll = api2.status_post("nice", poll=poll_params)
    poll = status_poll.poll
    assert poll.votes_count == 0
    assert poll.own_votes == []
    
    api.poll_vote(status_poll.poll, [1])
    poll2 = api.poll(poll)
    assert poll2.votes_count == 1
    assert poll2.own_votes == [1]
    
    api.poll_vote(status_poll.poll, [0])
    poll3 = api.poll(poll)
    assert poll3.votes_count == 2
    assert poll3.own_votes == [1, 0]
    
    api2.status_delete(status_poll)


@pytest.mark.vcr(match_on=['method', 'path', 'query'])
def test_poll_with_media(api2):
    media = api2.media_post("tests/image.jpg", synchronous=True)
    poll_params = api2.make_poll(["four twenty", "sixty-nine"], 300)
    status = api2.status_post("nice", media_ids=[media], poll=poll_params)

    try:
        assert status.poll
        assert status.media_attachments
        assert status.media_attachments[0].id == media.id
    finally:
        api2.status_delete(status, delete_media=True)
    
@pytest.mark.vcr()    
@pytest.mark.xfail(strict=True)
def test_poll_illegal_vote(api, api2):
    poll_params = api2.make_poll(["four twenty", "sixty-nine"], 300, multiple=False)
    status_poll = api2.status_post("nice", poll=poll_params)
    poll = status_poll.poll
    api.poll_vote(status_poll.poll, [1])
    api.poll_vote(status_poll.poll, [0])
