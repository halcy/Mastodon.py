
# versions.py - versioning of return values

import re
from decorator import decorate
from mastodon.errors import MastodonVersionError

###
# Version check functions, including decorator and parser
###
def parse_version_string(version_string):
    """Parses a semver version string, stripping off "rc" stuff if present."""
    string_parts = version_string.split(".")
    version_parts = (
        int(re.match("([0-9]*)", string_parts[0]).group(0)), # type: ignore
        int(re.match("([0-9]*)", string_parts[1]).group(0)), # type: ignore
        int(re.match("([0-9]*)", string_parts[2]).group(0)) # type: ignore
    )
    return version_parts


def max_version(*version_strings):
    """Returns the maximum version of all provided version strings."""
    return max(version_strings, key=parse_version_string)


def api_version(created_ver, last_changed_ver, return_value_ver):
    """Version check decorator. Currently only checks Bigger Than."""
    def api_min_version_decorator(function):
        def wrapper(function, self, *args, **kwargs):
            if not self.version_check_mode == "none":
                if self.version_check_mode == "created":
                    version = created_ver
                else:
                    version = max_version(last_changed_ver, return_value_ver)
                major, minor, patch = parse_version_string(version)
                if major > self.mastodon_major:
                    raise MastodonVersionError(f"Version check failed (Need version {version})")
                elif major == self.mastodon_major and minor > self.mastodon_minor:
                    raise MastodonVersionError(f"Version check failed (Need version {version})")
                elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
                    raise MastodonVersionError(f"Version check failed (Need version {version}, patch is {self.mastodon_patch})")
            return function(self, *args, **kwargs)
        function.__doc__ += f"\n\n        *Added: Mastodon v{created_ver}, last changed: Mastodon v{last_changed_ver}*"
        return decorate(function, wrapper)
    return api_min_version_decorator


###
# Dict versions
# TODO: Get rid of these
###
_DICT_VERSION_APPLICATION = "2.7.2"
_DICT_VERSION_MENTION = "1.0.0"
_DICT_VERSION_MEDIA = "3.2.0"
_DICT_VERSION_ACCOUNT = "3.3.0"
_DICT_VERSION_POLL = "2.8.0"
_DICT_VERSION_STATUS = max_version("3.1.0", _DICT_VERSION_MEDIA, _DICT_VERSION_ACCOUNT, _DICT_VERSION_APPLICATION, _DICT_VERSION_MENTION, _DICT_VERSION_POLL)
_DICT_VERSION_INSTANCE = max_version("3.4.0", _DICT_VERSION_ACCOUNT)
_DICT_VERSION_HASHTAG = "2.3.4"
_DICT_VERSION_EMOJI = "3.0.0"
_DICT_VERSION_RELATIONSHIP = "3.3.0"
_DICT_VERSION_NOTIFICATION = max_version("3.5.0",  _DICT_VERSION_ACCOUNT, _DICT_VERSION_STATUS)
_DICT_VERSION_CONTEXT = max_version("1.0.0",  _DICT_VERSION_STATUS)
_DICT_VERSION_LIST = "2.1.0"
_DICT_VERSION_CARD = "3.2.0"
_DICT_VERSION_SEARCHRESULT = max_version("1.0.0", _DICT_VERSION_ACCOUNT, _DICT_VERSION_STATUS, _DICT_VERSION_HASHTAG)
_DICT_VERSION_ACTIVITY = "2.1.2"
_DICT_VERSION_REPORT = "2.9.1"
_DICT_VERSION_PUSH = "2.4.0"
_DICT_VERSION_PUSH_NOTIF = "2.4.0"
_DICT_VERSION_FILTER = "2.4.3"
_DICT_VERSION_CONVERSATION = max_version("2.6.0", _DICT_VERSION_ACCOUNT, _DICT_VERSION_STATUS)
_DICT_VERSION_SCHEDULED_STATUS = max_version("2.7.0", _DICT_VERSION_STATUS)
_DICT_VERSION_PREFERENCES = "2.8.0"
_DICT_VERSION_ADMIN_ACCOUNT = max_version("4.0.0", _DICT_VERSION_ACCOUNT)
_DICT_VERSION_FEATURED_TAG = "3.0.0"
_DICT_VERSION_MARKER = "3.0.0"
_DICT_VERSION_REACTION = "3.1.0"
_DICT_VERSION_ANNOUNCEMENT = max_version("3.1.0", _DICT_VERSION_REACTION)
_DICT_VERSION_STATUS_EDIT = "3.5.0"
_DICT_VERSION_FAMILIAR_FOLLOWERS = max_version("3.5.0", _DICT_VERSION_ACCOUNT)
_DICT_VERSION_ADMIN_DOMAIN_BLOCK = "4.0.0"
_DICT_VERSION_ADMIN_MEASURE = "3.5.0"
_DICT_VERSION_ADMIN_DIMENSION = "3.5.0"
_DICT_VERSION_ADMIN_RETENTION = "3.5.0"

