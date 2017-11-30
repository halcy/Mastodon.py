import pytest


@pytest.mark.vcr()
def test_domain_blocks(api):
    blocks = api.domain_blocks()
    assert isinstance(blocks, list)


@pytest.mark.vcr()
def test_domain_block_unblock(api):
    api.domain_block('example.com')
    api.domain_unblock('example.com')
