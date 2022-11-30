# utility.py - utility functions, externally usable

import re
from decorator import decorate
from .error import MastodonVersionError

###
# Version check functions, including decorator and parser
###
def parse_version_string(version_string):
    """Parses a semver version string, stripping off "rc" stuff if present."""
    string_parts = version_string.split(".")
    version_parts = (
        int(re.match("([0-9]*)", string_parts[0]).group(0)),
        int(re.match("([0-9]*)", string_parts[1]).group(0)),
        int(re.match("([0-9]*)", string_parts[2]).group(0))
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
                    raise MastodonVersionError("Version check failed (Need version " + version + ")")
                elif major == self.mastodon_major and minor > self.mastodon_minor:
                    raise MastodonVersionError("Version check failed (Need version " + version + ")")
                elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
                    raise MastodonVersionError("Version check failed (Need version " + version + ", patch is " + str(self.mastodon_patch) + ")")
            return function(self, *args, **kwargs)
        function.__doc__ = function.__doc__ + "\n\n        *Added: Mastodon v" + \
            created_ver + ", last changed: Mastodon v" + last_changed_ver + "*"
        return decorate(function, wrapper)
    return api_min_version_decorator

###
# Dict helper class.
# Defined at top level so it can be pickled.
###
class AttribAccessDict(dict):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("Attribute not found: " + str(attr))

    def __setattr__(self, attr, val):
        if attr in self:
            raise AttributeError("Attribute-style access is read only")
        super(AttribAccessDict, self).__setattr__(attr, val)


###
# List helper class.
# Defined at top level so it can be pickled.
###
class AttribAccessList(list):
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError("Attribute not found: " + str(attr))

    def __setattr__(self, attr, val):
        if attr in self:
            raise AttributeError("Attribute-style access is read only")
        super(AttribAccessList, self).__setattr__(attr, val)