try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
     from urlparse import urlparse, parse_qs

def test_auth_request_url(api):
    url = api.auth_request_url()
    parse = urlparse(url)
    assert parse.path == '/oauth/authorize'
    query = parse_qs(parse.query)
    assert query['client_id'][0] == api.client_id
    assert query['response_type'][0] == 'code'
    assert query['redirect_uri'][0] == 'urn:ietf:wg:oauth:2.0:oob'
    assert set(query['scope'][0].split()) == set(('read', 'write', 'follow'))


