
import pytest

from  mastodon import Mastodon

TEST_CASES = [
    # Simple
    ("", 0),
    ("hello", 5),
    (" leading and trailing spaces   ", 31),
    (" tabs\tand\nnewlines\r\n", 19),

    # URLs - schemes, TLDs, IPv4/IPv6, ports, creds
    ("check http://example.com and https://example.org/page?x=1#frag", 1000 - 943),
    ("ftp://files.example.net/resource", 1000 - 968),
    ("http://user:pass@example.com:8080/path", 1000 - 962),
    ("http://127.0.0.1:3000/health", 1000 - 972),
    ("https://[2001:db8::1]/status", 1000 - 972),
    ("https://[2001:db8:85a3::8a2e:370:7334]:443/path?ok=1", 1000 - 948),
    ("mailto:someone@example.com", 1000 - 974),
    ("git+ssh://git@example.co.uk:22/repo.git", 1000 - 961),
    ("https://very.long.tld.example.museum/collection/item", 1000 - 977),

    # Usernames - local and remote
    ("@alice", 6),
    ("@bob@example.com", 4),
    ("hi @charlie and @dora@example.social!", 1000 -978),

    # Mixed
    ("hey @me@example.com look at https://example.com/a-b_c~d?e=f#g and @you  ", 50),

    # Grapheme cluster vs code point differences
    ("a: 🇪🇪", 4),
    ("b: 👨‍👩‍👧‍👦", 4),
    ("c: 👩🏽‍💻", 4),
    ("d: ✊🏿", 4),
    ("é", 1),
    ("f\u0301", 1),

    # Stress-tests
    ("https://sub.sub2.Путин.рф/увидимся/в?Гааге=военный#преступник", 1000 - 952),
    ("clusters: 😀😃😄😁😆😅😂🤣😊🙂😉🙃😇🥰😍🤩😘😗😙😚", 30),

    # Varied compositions
    ("See: http://example.com https://[2001:db8::2]:8443/a ftp://user:pw@files.example.org:21/x http://192.168.0.1/", 1000 - 886),
    ("@one https://example.social/@two 👩🏽‍💻 🇪🇪 @three@example.com ✊🏿", 1000 - 959),

    # Edge punctuation around URLs/usernames
    ("(see https://example.com.)", 30),
    ("[link: http://user:pass@host.example:8080/path?x=y#z]", 1000 - 947),
    ("<@root> and {@admin@example.net}", 20),
    ("https://example.com/a-b_c~d?param_a=1&param-b=2", 1000 - 977),
]

@pytest.mark.parametrize("text,expected", TEST_CASES)
def test_get_status_length_against_ground_truth(text, expected):
    assert Mastodon.get_status_length(text) == expected
    assert Mastodon.get_status_length(text, "what") == expected + 4
