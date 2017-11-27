WITH new_app AS (
    INSERT INTO oauth_applications (
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
            'Mastodon.py test suite',
            '__MASTODON_PY_TEST_ID',
            '__MASTODON_PY_TEST_SECRET',
            'urn:itef:wg:oauth:2.0:oob',
            'read write follow',
            'User',
            1,
            now(),
            now()
        )
    RETURNING id
)
INSERT INTO oauth_access_tokens (
    token,
    scopes,
    application_id,
    resource_owner_id,
    created_at
) SELECT
    '__MASTODON_PY_TEST_TOKEN',
    'read write follow',
    new_app.id,
    1,
    now()
FROM new_app;
