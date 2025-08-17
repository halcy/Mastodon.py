# defaults.py - default values for various parameters

_DEFAULT_TIMEOUT = 300
_DEFAULT_STREAM_TIMEOUT = 300
_DEFAULT_STREAM_RECONNECT_WAIT_SEC = 5
_DEFAULT_USER_AGENT = "mastodonpy"
_DEFAULT_SCOPES = ['read', 'write', 'follow', 'push']
_SCOPE_SETS = {
    'read': [
        'read:accounts',
        'read:blocks',
        'read:favourites',
        'read:filters',
        'read:follows',
        'read:lists',
        'read:mutes',
        'read:notifications',
        'read:search',
        'read:statuses',
        'read:bookmarks'
    ],
    'write': [
        'write:accounts',
        'write:blocks',
        'write:favourites',
        'write:filters',
        'write:follows',
        'write:lists',
        'write:media',
        'write:mutes',
        'write:notifications',
        'write:reports',
        'write:statuses',
        'write:bookmarks'
    ],
    'follow': [
        'read:blocks',
        'read:follows',
        'read:mutes',
        'write:blocks',
        'write:follows',
        'write:mutes',
    ],
    'admin:read': [
        'admin:read:accounts',
        'admin:read:reports',
        'admin:read:domain_allows',
        'admin:read:domain_blocks',
        'admin:read:ip_blocks',
        'admin:read:email_domain_blocks',
        'admin:read:canonical_email_blocks',
    ],
    'admin:write': [
        'admin:write:accounts',
        'admin:write:reports',
        'admin:write:domain_allows',
        'admin:write:domain_blocks',
        'admin:write:ip_blocks',
        'admin:write:email_domain_blocks',
        'admin:write:canonical_email_blocks',
    ],
    'profile': []
}
_VALID_SCOPES = ['read', 'write', 'follow', 'push', 'admin:read', 'admin:write', 'profile'] + \
    _SCOPE_SETS['read'] + _SCOPE_SETS['write'] + \
    _SCOPE_SETS['admin:read'] + _SCOPE_SETS['admin:write']
