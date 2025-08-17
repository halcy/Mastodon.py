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
WHERE email = 'mastodonpy_test@localhost';

UPDATE accounts SET
    discoverable = 't',
    indexable = 't',
    trendable = 't',
    locked = 'f'
WHERE username = 'mastodonpy_test_2';

UPDATE users SET
    locale = 'ja',  -- japanese locale for unicode testing :p
    encrypted_password = '$2a$10$8eAdhF69RiZiV0puZ.8iOOgMqBACmwJu8Z9X4CiN91iwRXbeC2jvi'
WHERE email = 'mastodonpy_test_2@localhost';

UPDATE users SET
    locale = 'de',
    encrypted_password = '$2a$10$8eAdhF69RiZiV0puZ.8iOOgMqBACmwJu8Z9X4CiN91iwRXbeC2jvi'
WHERE email = 'zerocool@example.com';

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
    (SELECT id FROM users WHERE email = 'mastodonpy_test@localhost'),
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
    (SELECT id FROM users WHERE email = 'mastodonpy_test@localhost'),
    now()
),
(
    1234567890123457,
    '__MASTODON_PY_TEST_ACCESS_TOKEN_3',
    'read write follow push',
    1234567890123456,
    (SELECT id FROM users WHERE email = 'mastodonpy_test_2@localhost'),
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

-- set some global settings:
INSERT INTO settings (
    id,
    var,
    value,
    created_at,
    updated_at
) VALUES (
    123456,
    'open_registrations',
    E'--- true\n...\n',
    now(),
    now()
);

UPDATE users SET
    settings = '{"notification_emails.follow_request": false, "default_privacy": "public", "default_sensitive": false}'
WHERE email IN ('mastodonpy_test@localhost', 'mastodonpy_test_2@localhost');
