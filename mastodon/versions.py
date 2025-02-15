
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


def api_version(created_ver, last_changed_ver):
    """Version check decorator. Currently only checks Bigger Than."""
    def api_min_version_decorator(function):
        return_value_ver = None
        return_value_type = function.__annotations__.get("return", None)
        if return_value_type is not None:
            return_value_ver = getattr(return_value_type, "_version", None)
        def wrapper(function, self, *args, **kwargs):
            if not self.version_check_mode == "none":
                if self.version_check_mode == "created":
                    version = created_ver
                else:
                    if return_value_ver is not None:
                        version = max_version(last_changed_ver, return_value_ver)
                    else:
                        version = last_changed_ver
                major, minor, patch = parse_version_string(version)
                if major > self.mastodon_major:
                    raise MastodonVersionError(f"Version check failed (Need Mastodon instance version {version} to call this endpoint)")
                elif major == self.mastodon_major and minor > self.mastodon_minor:
                    raise MastodonVersionError(f"Version check failed (Need Mastodon instance version {version} to call this endpoint)")
                elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
                    raise MastodonVersionError(f"Version check failed (Need Mastodon instance version {version} to call this endpoint). Patch is {self.mastodon_patch}.")
            return function(self, *args, **kwargs)
        if function.__doc__:
            if return_value_ver is not None:
                function.__doc__ += f"\n\n        *Added: Mastodon v{created_ver}, last changed: Mastodon v{last_changed_ver} (parameters), Mastodon v{return_value_ver} (return value)*"
            else:
                function.__doc__ += f"\n\n        *Added: Mastodon v{created_ver}, last changed: Mastodon v{last_changed_ver}*"
        return decorate(function, wrapper)
    return api_min_version_decorator
