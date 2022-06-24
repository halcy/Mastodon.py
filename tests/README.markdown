## Running

To run this test suite, install the testing dependencies:

    pip install -e .[test]

Then, run `pytest`.

If you wish to check test coverage:

    pytest --cov=mastodon

And if you want a complete HTML coverage report:

    pytest --cov=mastodon --cov-report html:coverage
    # then open coverage/index.html in your favourite web browser

Note that some tests are slightly unstable, as they require sidekiq to do things at the right time, and will thus sometimes break.

## Contributing

[VCR.py]: https://vcrpy.readthedocs.io/

This test suite uses [VCR.py][] to record requests to Mastodon and replay them in successive runs.

If you want to add or change tests, you will need a Mastodon development server running on `http://localhost:3000`, with the default `admin` user and default password.
To set this up, follow the development guide and set up the database using "rails db:setup".

It also needs a test OAuth app-registriation and an additional test user to be set up by applying the provided `setup.sql` to Mastodon's database:

    psql -d mastodon_development < tests/setup.sql

Tests that send requests to Mastodon should be marked as needing VCR with the `pytest.mark.vcr` decorator.

```python
import pytest

@pytest.mark.vcr()
def test_fun_new_feature(api):
    foo = api.fun_new_feature()
    assert foo = "bar"
```
