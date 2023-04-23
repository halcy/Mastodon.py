# compat.py - backwards compatible optional imports

IMPL_HAS_CRYPTO = True
try:
    import cryptography
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import serialization
except:
    IMPL_HAS_CRYPTO = False
    cryptography = None
    default_backend = None
    ec = None
    serialization = None

IMPL_HAS_ECE = True
try:
    import http_ece
except:
    IMPL_HAS_ECE = False
    http_ece = None

IMPL_HAS_BLURHASH = True
try:
    import blurhash
except:
    IMPL_HAS_BLURHASH = False
    blurhash = None

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    import magic
except ImportError:
    magic = None

try:
    from pathlib import PurePath, Path
except:
    class PurePath:
        pass
    class Path:
        pass

