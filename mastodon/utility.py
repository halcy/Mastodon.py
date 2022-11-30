# utility.py - utility functions, externally usable

import re
from decorator import decorate
from .error import MastodonVersionError, MastodonAPIError
import dateutil
import datetime

# Module level:

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


# Class level:
class Mastodon():
    def set_language(self, lang):
        """
        Set the locale Mastodon will use to generate responses. Valid parameters are all ISO 639-1 (two letter) or, for languages that do
        not have one, 639-3 (three letter) language codes. This affects some error messages (those related to validation) and trends.
        """
        self.lang = lang
            
    def retrieve_mastodon_version(self):
        """
        Determine installed Mastodon version and set major, minor and patch (not including RC info) accordingly.

        Returns the version string, possibly including rc info.
        """
        try:
            version_str = self.__normalize_version_string(self.__instance()["version"])
            self.version_check_worked = True
        except:
            # instance() was added in 1.1.0, so our best guess is 1.0.0.
            version_str = "1.0.0"
            self.version_check_worked = False

        self.mastodon_major, self.mastodon_minor, self.mastodon_patch = parse_version_string(version_str)
        return version_str

    def verify_minimum_version(self, version_str, cached=False):
        """
        Update version info from server and verify that at least the specified version is present.

        If you specify "cached", the version info update part is skipped.

        Returns True if version requirement is satisfied, False if not.
        """
        if not cached:
            self.retrieve_mastodon_version()
        major, minor, patch = parse_version_string(version_str)
        if major > self.mastodon_major:
            return False
        elif major == self.mastodon_major and minor > self.mastodon_minor:
            return False
        elif major == self.mastodon_major and minor == self.mastodon_minor and patch > self.mastodon_patch:
            return False
        return True
    
    def get_approx_server_time(self):
        """
        Retrieve the approximate server time

        We parse this from the hopefully present "Date" header, but make no effort to compensate for latency.
        """
        response = self.__api_request("HEAD", "/", return_response_object=True)
        if 'Date' in response.headers:
            server_time_datetime = dateutil.parser.parse(response.headers['Date'])

            # Make sure we're in local time
            epoch_time = self.__datetime_to_epoch(server_time_datetime)
            return datetime.datetime.fromtimestamp(epoch_time)
        else:
            raise MastodonAPIError("No server time in response.")
