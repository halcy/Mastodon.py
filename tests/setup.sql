DELETE FROM settings WHERE thing_id = 1234567890123456;
DELETE FROM settings WHERE thing_id = 1234567890123457;
DELETE FROM oauth_access_tokens WHERE id = 6543210987654321;
DELETE FROM oauth_access_tokens WHERE id = 1234567890123456;
DELETE FROM oauth_access_tokens WHERE id = 1234567890123457;
DELETE FROM oauth_applications WHERE id = 1234567890123456;
DELETE FROM users WHERE id = 1234567890123456;
DELETE FROM users WHERE id = 1234567890123457;
DELETE FROM accounts WHERE id = 1234567890123456;
DELETE FROM accounts WHERE id = 1234567890123457;

UPDATE accounts SET
    locked = 't'
WHERE username = 'mastodonpy_test';

UPDATE users SET 
    locale = 'ja'  -- japanese locale for unicode testing :p
WHERE email = 'mastodonpy_test@localhost:3000';

UPDATE accounts SET
    locked = 'f',
    discoverable = 't'
WHERE username = 'mastodonpy_test_2';

UPDATE users SET
    locale = 'ja',  -- japanese locale for unicode testing :p
    encrypted_password = '$2a$10$8eAdhF69RiZiV0puZ.8iOOgMqBACmwJu8Z9X4CiN91iwRXbeC2jvi'
WHERE email = 'mastodonpy_test_2@localhost:3000';

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
    'read write follow push admin:read admin:write',
    'User',
    (SELECT id FROM users WHERE email = 'mastodonpy_test@localhost:3000'),
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
    (SELECT id FROM users WHERE email = 'mastodonpy_test@localhost:3000'),
    now()
),
(
    1234567890123457,
    '__MASTODON_PY_TEST_ACCESS_TOKEN_3',
    'read write follow push',
    1234567890123456,
    (SELECT id FROM users WHERE email = 'mastodonpy_test_2@localhost:3000'),
    now()
),
(
    6543210987654321,
    '__MASTODON_PY_TEST_ACCESS_TOKEN_2',
    'read write follow push admin:read admin:write',
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
    (SELECT id FROM users WHERE email = 'mastodonpy_test@localhost:3000'),
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
    (SELECT id FROM users WHERE email = 'mastodonpy_test@localhost:3000'),
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
    (SELECT id FROM users WHERE email = 'mastodonpy_test@localhost:3000'),
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
    1234567890123459,
    'notification_emails',
    E'---\nfollow_request: false',
    'User',
    (SELECT id FROM users WHERE email = 'mastodonpy_test_2@localhost:3000'),
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
    1234567890123460, 
    'default_privacy', 
    E'--- public\n...\n', 
    'User',
    (SELECT id FROM users WHERE email = 'mastodonpy_test_2@localhost:3000'),
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
    1234567890123461,
    'default_sensitive',
    E'--- false\n...\n',
    'User',
    (SELECT id FROM users WHERE email = 'mastodonpy_test_2@localhost:3000'),
    now(),
    now()
);
