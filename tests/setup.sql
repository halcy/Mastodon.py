DELETE FROM settings WHERE thing_id = 1234567890123456;
DELETE FROM oauth_access_tokens WHERE id = 6543210987654321;
DELETE FROM oauth_access_tokens WHERE id = 1234567890123456;
DELETE FROM oauth_applications WHERE id = 1234567890123456;
DELETE FROM users WHERE id = 1234567890123456;
DELETE FROM accounts WHERE id = 1234567890123456;

INSERT INTO accounts (
    id,
    username,
    locked,
    created_at,
    updated_at
) VALUES (
    1234567890123456,
    'mastodonpy_test',
    't',
    now(),
    now()
);

INSERT INTO users (
    id,
    email,
    account_id,
    created_at,
    updated_at,
    confirmed_at,
    locale
) VALUES (
    1234567890123456,
    'mastodonpy_test@localhost:3000',
    1234567890123456,
    now(),
    now(),
    now(),
    'ja'  -- japanese locale for unicode testing :p
);


INSERT INTO oauth_applications (
    id,
    name,
    uid,
    secret,
    redirect_uri,
    scopes,
    owner_type,
    owner_id,
    created_at,
    updated_at
) VALUES (
    1234567890123456,
    'Mastodon.py test suite',
    '__MASTODON_PY_TEST_CLIENT_ID',
    '__MASTODON_PY_TEST_CLIENT_SECRET',
    'urn:ietf:wg:oauth:2.0:oob',
    'read write follow push',
    'User',
    1234567890123456,
    now(),
    now()
);
INSERT INTO oauth_access_tokens (
    id,
    token,
    scopes,
    application_id,
    resource_owner_id,
    created_at
) VALUES (
    1234567890123456,
    '__MASTODON_PY_TEST_ACCESS_TOKEN',
    'read write follow push',
    1234567890123456,
    1234567890123456,
    now()
), (
    6543210987654321,
    '__MASTODON_PY_TEST_ACCESS_TOKEN_2',
    'read write follow push',
    1234567890123456,
    1,
    now()
);

INSERT INTO settings (
    id,
    var,
    value,
    thing_type,
    thing_id,
    created_at,
    updated_at
) VALUES (
    1234567890123456,
    'notification_emails',
    E'---\nfollow_request: false',
    'User',
    1234567890123456,
    now(),
    now()
);
INSERT INTO settings (
    id, 
    var, 
    value, 
    thing_type,
    thing_id,
    created_at,
    updated_at
) VALUES (
    1234567890123457, 
    'default_privacy', 
    E'--- public\n...\n', 
    'User',
    1234567890123456,
    now(),
    now()
);
INSERT INTO settings (
    id, 
    var, 
    value, 
    thing_type,
    thing_id,    
    created_at, 
    updated_at
) VALUES (
    1234567890123458,
    'default_sensitive',
    E'--- false\n...\n',
    'User',
    1234567890123456,
    now(),
    now()
);
