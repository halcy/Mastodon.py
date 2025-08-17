from __future__ import annotations # python < 3.9 compat
import typing
from typing import List, Union, Optional, Dict, Any, Tuple, Callable, get_type_hints, TypeVar, IO, Generic, ForwardRef
from datetime import datetime, timezone
import dateutil
import dateutil.parser
from collections import OrderedDict
from mastodon.compat import PurePath
import sys
import json
import copy

# A type representing a file name as a PurePath or string, or a file-like object, for convenience
PathOrFile = Union[str, PurePath, IO[bytes]]

BASE62_ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
def base62_to_int(base62: str) -> int:
    """
    internal helper for *oma compat: convert a base62 string to an int since
    that is what that software uses as ID type.

    we don't convert IDs in general, but this is needed for snowflake ID
    calculations.
    """
    str_len = len(base62)
    val = 0
    base62 = base62.lower()
    for idx, char in enumerate(base62):
        power = (str_len - (idx + 1))
        val += BASE62_ALPHABET.index(char) * (62 ** power)
    return val

def int_to_base62(val: int) -> str:
    """
    Internal helper to convert an int to a base62 string.
    """
    if val == 0:
        return BASE62_ALPHABET[0]

    base62 = []
    while val:
        val, digit = divmod(val, 62)
        base62.append(BASE62_ALPHABET[digit])
    return ''.join(reversed(base62))


PrimitiveIdType = Union[str, int]
"""
The base type for all non-snowflake IDs. This is a union of int and str 
because while Mastodon mostly uses IDs that are ints, it doesn't guarantee
this and other implementations do not use integer IDs.

In a change from previous versions, string IDs now take precedence over ints.
This is a breaking change, and I'm sorry about it, but this will make every piece
of software using Mastodon.py more robust in the long run.
"""

def _str_to_type(mastopy_type):
    """
    String name to internal type resolver
    """
    # See if we need to parse a sub-type (i.e. [<something>] in the type name
    sub_type = None
    if "[" in mastopy_type and "]" in mastopy_type:
        mastopy_type, sub_type = mastopy_type.split("[")
        sub_type = sub_type[:-1]
        if mastopy_type not in ["PaginatableList", "NonPaginatableList", "typing.Optional", "typing.Union"]:
            raise ValueError(f"Subtype not allowed for type {mastopy_type} and subtype {sub_type}")
    if "[" in mastopy_type or "]" in mastopy_type:
        raise ValueError(f"Invalid type {mastopy_type}")
    if sub_type is not None and ("[" in sub_type or "]" in sub_type):
        raise ValueError(f"Invalid subtype {sub_type}")
    
    # Build the actual type object. 
    from mastodon.return_types import ENTITY_NAME_MAP
    full_type = None
    if sub_type is not None:
        if not mastopy_type == "typing.Union":
            sub_type = ENTITY_NAME_MAP.get(sub_type, None)
        else:
            sub_type_list = []
            for sub_type_part in sub_type.split(","):
                sub_type_part = sub_type_part.strip()
                if sub_type_part:
                    sub_type_part_type = ENTITY_NAME_MAP.get(sub_type_part, None)
                    if sub_type_part_type is not None:
                        sub_type_list.append(sub_type_part_type)
        if mastopy_type == "PaginatableList":
            full_type = PaginatableList[sub_type]
        elif mastopy_type == "NonPaginatableList":
            full_type = NonPaginatableList[sub_type]
        elif mastopy_type == "typing.Optional":
            full_type = Optional[sub_type]
        elif mastopy_type == "typing.Union":
            full_type = Union.__getitem__(tuple(sub_type_list))
    else:
        full_type = ENTITY_NAME_MAP.get(mastopy_type, None)
    if full_type is None:
        raise ValueError(f"Unknown type {mastopy_type}")
    return full_type

class MaybeSnowflakeIdType(str):
    """
    Represents, maybe, a snowflake ID.

    Contains what a regular ID can contain (int or str) and will convert to int if
    containing an int or a str that naturally converts to an int (e.g. "123").

    Can *also* contain a *datetime* which gets converted to a  timestamp.

    It's also just *maybe* a snowflake ID, because some implementations may not use those.

    This may seem annoyingly complex, but the goal here is:
    1) If constructed with some ID, return that ID unchanged, so equality and hashing work
    2) Allow casting to int and str, just like a regular ID
    3) Halfway transparently convert to and from datetime with the correct format for the server we're talking to
    """
    def __new__(cls, value, *args, **kwargs):
        try:
            return super(cls, cls).__new__(cls, value)
        except:
            return object.__new__(cls)

    def __init__(self, val: Union[PrimitiveIdType, datetime], assume_pleroma: bool = False):
        try:
            super(MaybeSnowflakeIdType, self).__init__()
        except:
            pass
        if isinstance(val, (int, str)):
            self.__val = val
        elif isinstance(val, datetime):
            self.__val = (int(val.timestamp()) << 16) * 1000
            if assume_pleroma:
                self.__val = int_to_base62(self.__val)
        else:
            raise TypeError(f"Expected int or str, got {type(val).__name__}")
        self.assume_pleroma = assume_pleroma
        
    def to_datetime(self) -> Optional[datetime]:
        """
        Convert to datetime. This *can* fail because not every implementation of
        the masto API is guaranteed to actually use snowflake IDs where masto uses
        snowflake IDs, so it can in fact return None.
        """
        val = self.__val
        try:
            # Pleroma ID compat. First, try to just cast to int. If that fails *or*
            # if we are told to assume Pleroma, try to convert from base62.
            if isinstance(self.__val, str):
                try_base62 = False
                try:
                    val = int(self.__val)
                except:
                    try_base62 = True
                if try_base62 or self.assume_pleroma:
                    val = base62_to_int(self.__val)
        except:
            return None
        
        # TODO: This matches the masto approach, whether this matches the
        # Pleroma approach is to be verified.
        timestamp_s = int(int(val) / 1000) >> 16
        return datetime.fromtimestamp(timestamp_s)

    def __str__(self) -> str:
        """
        Return as string representation.
        """
        return str(self.__val)

    def __int__(self) -> int:
        """
        Return as int representation.

        This is not guaranteed to work, because the ID might be a string,
        though on Mastodon it is generally going to be an int.
        """
        if isinstance(self.__val, str):
            return int(self.__val)
        return self.__val
    
    def __repr__(self) -> str:
        """
        Overriden so that the integer representation doesn't take precedence
        """
        return str(self.__val)

# Forward reference resolution for < 3.9
if sys.version_info < (3, 9):
    def resolve_type(t):
        # I'm sorry about this, but I cannot think of another way to make this work properly in versions below 3.9 that
        # cannot resolve forward references in a sane way
        from mastodon.return_types import Account, AccountField, Role, CredentialAccountSource, \
            Status, Quote, ShallowQuote, StatusEdit, FilterResult, StatusMention, \
            ScheduledStatus, ScheduledStatusParams, Poll, PollOption, Conversation, Tag, \
            TagHistory, CustomEmoji, Application, Relationship, Filter, FilterV2, \
            Notification, Context, UserList, MediaAttachment, MediaAttachmentMetadataContainer, MediaAttachmentImageMetadata, \
            MediaAttachmentVideoMetadata, MediaAttachmentAudioMetadata, MediaAttachmentFocusPoint, MediaAttachmentColors, PreviewCard, TrendingLinkHistory, \
            PreviewCardAuthor, Search, SearchV2, Instance, InstanceConfiguration, InstanceURLs, \
            InstanceV2, InstanceIcon, InstanceConfigurationV2, InstanceVapidKey, InstanceURLsV2, InstanceThumbnail, \
            InstanceThumbnailVersions, InstanceStatistics, InstanceUsage, InstanceUsageUsers, RuleTranslation, Rule, \
            InstanceRegistrations, InstanceContact, InstanceAccountConfiguration, InstanceStatusConfiguration, InstanceTranslationConfiguration, InstanceMediaConfiguration, \
            InstancePollConfiguration, Nodeinfo, NodeinfoSoftware, NodeinfoServices, NodeinfoUsage, NodeinfoUsageUsers, \
            NodeinfoMetadata, Activity, Report, AdminReport, WebPushSubscription, WebPushSubscriptionAlerts, \
            PushNotification, Preferences, FeaturedTag, Marker, Announcement, Reaction, \
            StreamReaction, FamiliarFollowers, AdminAccount, AdminIp, AdminMeasure, AdminMeasureData, \
            AdminDimension, AdminDimensionData, AdminRetention, AdminCohort, AdminDomainBlock, AdminCanonicalEmailBlock, \
            AdminDomainAllow, AdminEmailDomainBlock, AdminEmailDomainBlockHistory, AdminIpBlock, DomainBlock, ExtendedDescription, \
            FilterKeyword, FilterStatus, IdentityProof, StatusSource, Suggestion, Translation, \
            AccountCreationError, AccountCreationErrorDetails, AccountCreationErrorDetailsField, NotificationPolicy, NotificationPolicySummary, RelationshipSeveranceEvent, \
            GroupedNotificationsResults, PartialAccountWithAvatar, NotificationGroup, AccountWarning, UnreadNotificationsCount, Appeal, \
            NotificationRequest, SupportedLocale, OAuthServerInfo, OAuthUserInfo, TermsOfService
        if isinstance(t, ForwardRef):
            try:
                t = t._evaluate(globals(), locals(), frozenset())
            except:
                t = t._evaluate(globals(), locals())
        return t
else:
    def resolve_type(t):
        return t

# Type to string that is more robust than repr
def stringify_type(tp):
    try:
        origin = typing.get_origin(tp)
        args = typing.get_args(tp)
        if origin is not None:
            origin_module = origin.__module__
            origin_name = origin.__qualname__
            if origin in [list, EntityList, PaginatableList, NonPaginatableList]:
                if origin_module in ("mastodon.return_types", "mastodon.types_base"):
                    type_str = origin_name
                else:
                    type_str = f"{origin_module}.{origin_name}"
                if args:
                    arg_strs = [stringify_type(arg) for arg in args]
                    type_str += f"[{', '.join(arg_strs)}]"
            elif origin in [Union, Optional]:
                type_str = stringify_type(args[0])
            return type_str
        else:
            module = getattr(tp, "__module__", "")
            qualname = getattr(tp, "__qualname__", str(tp))
            if module in ("mastodon.return_types", "mastodon.types_base"):
                return qualname
            return f"{module}.{qualname}"
    except Exception:
        return str(tp)

# Function that gets a type class but doesn't break in lower python versions as much
def get_type_class(typ):
    try:
        return typ.__extra__
    except AttributeError:
        try:
            return typ.__origin__
        except AttributeError:
            pass
    return typ

# Restore behaviour that was removed from python for mysterious reasons
def real_issubclass(type1, type2orig):
    type1 = get_type_class(type1)
    type2 = get_type_class(type2orig)
    valid_types = []
    if type2 is Union:
        valid_types = type2orig.__args__
    elif type2 is Generic:
        valid_types = [type2orig.__args__[0]]
    else:
        valid_types = [type2]
    return issubclass(type1, tuple(valid_types))

# Helper functions for typecasting attempts
def try_cast(t, value, retry = True, union_specializer = None):
    """
    Base case casting function. Handles:
    * Casting to any AttribAccessDict subclass (directly, no special handling)
    * Casting to bool (with possible conversion from json bool strings)
    * Casting to datetime (with possible conversion from all kinds of funny date formats because unfortunately this is the world we live in)
    * Casting to whatever t is
    * Trying once again to AttribAccessDict as a fallback
    Gives up and returns as-is if none of the above work.
    """
    if value is None: # None early out
        return value
    t = resolve_type(t)
    if type(t) == TypeVar: # TypeVar early out with an attempt at coercing dicts
        if isinstance(value, dict):
            return try_cast(AttribAccessDict, value, False, union_specializer)
        else:
            return value
    try:
        if real_issubclass(t, AttribAccessDict):
            if union_specializer is not None:
                value["__union_specializer"] = union_specializer
            value = t(**value)

            # Did we have type arguments on the dict? If so, we need to try to cast the values
            # This will not work in 3.7 and 3.8, which is unfortunate, but them's the breaks of using
            # very old versions.
            if hasattr(t, '__args__') and len(t.__args__) > 1:
                value_cast_type = t.__args__[1]
                for key, val in value.items():
                    value[key] = try_cast_recurse(value_cast_type, val, union_specializer)
        elif real_issubclass(t, bool):
            if isinstance(value, str):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                else:
                    # Invalid values are None'd
                    value = None
            # We assume that if it's not a string, it validly converts to bool
            # this is a potentially foolish assumption, but :shrug:
            value = bool(value)
        elif real_issubclass(t, datetime):
            if isinstance(value, int):
                value = datetime.fromtimestamp(value, timezone.utc)
            elif isinstance(value, str):
                try:
                    value_int = int(value)
                    value = datetime.fromtimestamp(value_int, timezone.utc)
                except:
                    try:
                        value = dateutil.parser.parse(value)
                    except:
                        # Invalid values are, once again, None'd
                        value = None
        elif real_issubclass(t, int):
            try:
                value = int(value)
            except:
                # You know the drill
                value = None
        elif real_issubclass(t, float):
            try:
                value = float(value)
            except:
                # One last time
                value = None   
        elif real_issubclass(t, list):
            if not t in [PaginatableList, NonPaginatableList]:
                # we never want base case lists
                t = NonPaginatableList
            value = t(value)
        else:
            if real_issubclass(value.__class__, dict):
                value = t(**value)
            else:
                value = t(value)
    except Exception as e:
        # Failures are silently ignored, usually.
        # import traceback
        # traceback.print_exc()
        if retry and isinstance(value, dict):
            value = try_cast(AttribAccessDict, value, False, union_specializer)
    return value

def try_cast_recurse(t, value, union_specializer=None):
    """
    Non-dict compound type casting function. Handles:
    * Casting to list, tuple, EntityList or (Non)PaginatableList, converting all elements to the correct type recursively
    * Casting to Union, use union_specializer to special case the union type to the correct one
    * Casting to Union, special case out Quote vs ShallowQuote by the presence of "quoted_status" or "quoted_status_id" in the value
    * Casting to Union, trying all types in the union until one works
    Gives up and returns as-is if none of the above work.
    """
    if type(t) == str:
        t = _str_to_type(t)
    if value is None:
        return value
    t = resolve_type(t)
    real_type = None
    use_real_type = False
    try:
        if hasattr(t, '__origin__') or hasattr(t, '__extra__'):
            orig_type = get_type_class(t)
            if orig_type in (list, tuple, EntityList, NonPaginatableList, PaginatableList):
                if orig_type == list:
                    orig_type = NonPaginatableList
                value_cast = []
                type_args = t.__args__
                if len(type_args) == 1:
                    type_args = type_args * len(value)
                for element_type, v in zip(type_args, value):
                    value_cast.append(try_cast_recurse(element_type, v, union_specializer))
                value = orig_type(value_cast)
            elif orig_type is Union:
                if union_specializer is not None:
                    from mastodon.return_types import MediaAttachmentImageMetadata, MediaAttachmentVideoMetadata, MediaAttachmentAudioMetadata
                    real_type = {
                        "image": MediaAttachmentImageMetadata,
                        "video": MediaAttachmentVideoMetadata,
                        "audio": MediaAttachmentAudioMetadata,
                        "gifv": MediaAttachmentVideoMetadata,
                    }.get(union_specializer, None)
                if isinstance(value, dict) and "quoted_status_id" in value:
                    from mastodon.return_types import ShallowQuote
                    real_type = ShallowQuote
                elif isinstance(value, dict) and "quoted_status" in value:
                    from mastodon.return_types import Quote
                    real_type = Quote
                if real_type in t.__args__:
                    value = try_cast_recurse(real_type, value, union_specializer)
                    use_real_type = True
                    testing_t = real_type
                    if hasattr(t, '__origin__') or hasattr(t, '__extra__'):
                        testing_t = get_type_class(real_type)
                else:
                    for sub_t in t.__args__:
                        value = try_cast_recurse(sub_t, value, union_specializer)
                        testing_t = sub_t
                        if hasattr(t, '__origin__') or hasattr(t, '__extra__'):
                            testing_t = get_type_class(sub_t)
                        if isinstance(value, testing_t):
                            break
            else:
                # uhhh I don't know how we got here but try to cast to the type anyways
                value = try_cast(t, value, True, union_specializer)
        else:
            value = try_cast(t, value, True, union_specializer)
    except Exception as e:
        # Failures are silently ignored. We care about maximum not breaking here.
        # import traceback
        # traceback.print_exc()
        pass

    if real_issubclass(value.__class__, AttribAccessDict) or real_issubclass(value.__class__, PaginatableList) or real_issubclass(value.__class__, NonPaginatableList) or real_issubclass(value.__class__, MaybeSnowflakeIdType):
        save_type = t
        if real_type is not None and use_real_type:
            save_type = real_type
        try:
            value._mastopy_type = stringify_type(save_type)
        except Exception as e:
            try:
                # If the new robust method doesn't work, try the old and less robust method
                value._mastopy_type = repr(save_type)
            except:
                # Failures are silently ignored. We care about maximum not breaking here.
                pass
        value._mastopy_type = value._mastopy_type.replace("mastodon.return_types.", "").replace("mastodon.types_base.", "")
        if value._mastopy_type.startswith("<class '") and value._mastopy_type.endswith("'>"):
            value._mastopy_type = value._mastopy_type[8:-2]
    return value

class Entity():
    """
    Base class for everything returned by the API. This is a union of :class:`AttribAccessDict` and :class:`EntityList`.

    Defines two methods: to_json(), and (static) from_json(), for serializing and deserializing to/from JSON.
    """
    def __init__(self):
        self._mastopy_type = None
    
    def to_json(self, pretty=True) -> str:
        """
        Serialize to JSON.

        The returned JSON data includes type information and a version field.
        """
        mastopy_data = copy.deepcopy(self)

        # Recursively walk through the object, find every object with a class that has a _rename_map, and remove the renamed fields
        def remove_renamed_fields(obj):
            if isinstance(obj, dict):
                if hasattr(obj.__class__, "_rename_map"):
                    for field in getattr(obj.__class__, "_rename_map").values():
                        if field in obj:
                            del obj[field]
                for key in obj:
                    remove_renamed_fields(obj[key])
            elif isinstance(obj, list):
                for item in obj:
                    remove_renamed_fields(item)
        remove_renamed_fields(mastopy_data)

        serialize_data = {
            "_mastopy_version": "2.0.1",
            "_mastopy_type": self._mastopy_type,
            "_mastopy_data": mastopy_data,
            "_mastopy_extra_data": {}
        }

        if hasattr(self, "_pagination_next") and self._pagination_next is not None:
            serialize_data["_mastopy_extra_data"]["_pagination_next"] = self._pagination_next
        if hasattr(self, "_pagination_prev") and self._pagination_prev is not None:
            serialize_data["_mastopy_extra_data"]["_pagination_prev"] = self._pagination_prev

        def json_serial(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()

        if pretty:
            return json.dumps(serialize_data, default=json_serial, indent=4)
        else:
            return json.dumps(serialize_data, default=json_serial)

    @staticmethod
    def from_json(json_str: str) -> Entity:
        """
        Deserialize from JSON.

        Parse a JSON string and cast to the to the appropriate type
        by using a special field that is added by serialization.

        This `should` be safe to call on any JSON string (no less safe than json.loads), 
        but I would still recommend to be very careful when using this on untrusted data 
        and to check that the returned value matches your expectations.

        There is currently a bug on specifically python 3.7 and 3.8 where the return value
        is not guaranteed to be of the right type. I will probably not fix this, since the versions
        are out of support, anyways. However, the data will still be loaded correctly.
        """
        # First, parse json normally. Can end up as a dict or a list.
        json_result = json.loads(json_str)

        # Read _mastopy_version field, throw error if not present
        # Not currently used, but we make sure it is there
        if "_mastopy_version" not in json_result:
            raise ValueError("JSON does not contain _mastopy_version field, refusing to parse.")
        
        # Read _mastopy_type field, throw error if not present
        if "_mastopy_type" not in json_result:
            raise ValueError("JSON does not contain _mastopy_type field, refusing to parse.")
        mastopy_type = json_result["_mastopy_type"]
        full_type = _str_to_type(mastopy_type)

        # Finally, try to cast to the generated type
        return_data = try_cast_recurse(full_type, json_result["_mastopy_data"])

        # Fill in pagination information if it is present in the persisted data
        if "_mastopy_extra_data" in json_result:
            if "_pagination_next" in json_result["_mastopy_extra_data"]:
                return_data._pagination_next = try_cast_recurse(PaginationInfo, json_result["_mastopy_extra_data"]["_pagination_next"])
                response_type = return_data._pagination_next.get("_mastopy_type", None)
                if response_type is not None:
                    return_data._pagination_next["_mastopy_type"] = _str_to_type(response_type)
            if "_pagination_prev" in json_result["_mastopy_extra_data"]:
                return_data._pagination_prev = try_cast_recurse(PaginationInfo, json_result["_mastopy_extra_data"]["_pagination_prev"])
                response_type = return_data._pagination_prev.get("_mastopy_type", None)
                if response_type is not None:
                    return_data._pagination_prev["_mastopy_type"] = _str_to_type(response_type)

        return return_data


class PaginationInfo(OrderedDict):
    """
    Pagination info

    Not likely to change, but very much implementation (Mastodon.py) and implementation (Mastodon server) defined. It would be best
    if you treated this as opaque.
    """
    pass

IdType = Union[PrimitiveIdType, MaybeSnowflakeIdType, datetime]
"""
IDs returned from Mastodon.py ar either primitive (int or str) or snowflake
(still int or str, but potentially convertible to datetime), but also
a datetime (which will get converted to a snowflake id).
"""

T = TypeVar('T')
class PaginatableList(List[T], Entity):
    """
    This is a list with pagination information attached.

    It is returned by the API when a list of items is requested, and the response contains
    a Link header with pagination information.
    """
    _pagination_next: Optional[PaginationInfo]
    _pagination_prev: Optional[PaginationInfo]

    def __init__(self, *args, **kwargs):
        """
        Initializes basic list and adds empty pagination information.
        """
        super(PaginatableList, self).__init__(*args, **kwargs)
        self._pagination_next = None
        self._pagination_prev = None 

class NonPaginatableList(List[T], Entity):
    """
    This is just a list, without pagination information but
    annotated for serialization and deserialization.
    """
    def __init__(self, *args, **kwargs):
        super(NonPaginatableList, self).__init__(*args, **kwargs)

EntityList = Union[NonPaginatableList[T], PaginatableList[T]]
"""Lists in Mastodon.py are either regular or paginatable, so this is a union of
   :class:`NonPaginatableList` and :class:`PaginatableList`."""

try:
    OrderedStrDict = OrderedDict[str, Any]
except:
    OrderedStrDict = OrderedDict

class AttribAccessDict(OrderedStrDict, Entity):
    """
    Base return object class for Mastodon.py.

    Inherits from dict, but allows access via attributes as well as if it was a dataclass.

    While the subclasses implement specific fields with proper typing, parsing and documentation,
    they all inherit from this class, and parsing is extremely permissive to allow for forward and
    backward compatibility as well as compatibility with other implementations of the Mastodon API.

    This class can ALSO have pagination information attached, for paginating lists *inside* the object,
    because that's what Mastodon 4.3.0 does for groupee notifications. This is special cased in the class
    definition, though.
    """
    def __init__(self, **kwargs):
        """
        Constructor that calls through to dict constructor and then sets attributes for all keys.
        """
        super(AttribAccessDict, self).__init__()
        if "__union_specializer" in kwargs:
            self.__union_specializer = kwargs["__union_specializer"]
            del kwargs["__union_specializer"]
        if "__annotations__" in self.__class__.__dict__:
            for attr, _ in self.__class__.__annotations__.items():
                attr_name = attr
                if hasattr(self.__class__, "_rename_map"):
                    attr_name = getattr(self.__class__, "_rename_map").get(attr, attr)
                    if attr_name in kwargs:
                        self[attr] = kwargs[attr_name]
                        assert not attr in kwargs, f"Duplicate attribute {attr}"
                elif attr in kwargs:
                    self[attr] = kwargs[attr]
                else:
                    self[attr] = None
        for attr in kwargs:
            if not attr in self:
                self[attr] = kwargs[attr]
                
    def __getattribute__(self, attr):
        """
        Override to force access of normal attributes to go through __getattr__
        """
        if attr in ["_AttribAccessDict__union_specializer", "_mastopy_type", "__class__"]:
            return super(AttribAccessDict, self).__getattribute__(attr)
        if attr in self.__class__.__annotations__:
            return self.__getattr__(attr)
        return super(AttribAccessDict, self).__getattribute__(attr)

    def __getattr__(self, attr):
        """
        Basic attribute getter that throws if attribute is not in dict and supports redirecting access.
        """        
        if not hasattr(self.__class__, "_access_map"):
            # Base case: no redirecting
            if attr in self:
                return self[attr]
            else:
                return super(AttribAccessDict, self).__getattribute__(attr)
        else:
            if attr in self and self[attr] is not None:
                return self[attr]
            elif attr in getattr(self.__class__, "_access_map"):
                try:
                    attr_path = getattr(self.__class__, "_access_map")[attr].split('.')
                    cur_attr = self
                    for attr_path_part in attr_path:
                        cur_attr = getattr(cur_attr, attr_path_part)
                    return cur_attr
                except:
                    raise AttributeError(f"Attribute not found: {attr}")
            else:
                return super(AttribAccessDict, self).__getattribute__(attr)
            
    def __setattr__(self, attr, val):
        """
        Attribute setter that calls through to dict setter but will throw if attribute is not in dict
        """
        if attr in self or attr in ["_AttribAccessDict__union_specializer", "_mastopy_type"]:
            if attr == "_mastopy_type":
                super(AttribAccessDict, self).__setattr__(attr, val)
            else:
                self[attr] = val
        else:
            raise AttributeError(f"Attribute not found: {attr}")

    def __setitem__(self, key, val):
        """
        Dict setter that also sets attributes and tries to typecast if we have an 
        AttribAccessDict, EntityList or MaybeSnowflakeIdType type hint.

        For Unions, we special case explicitly to specialize.
        """
        # If we're already an AttribAccessDict subclass, skip all the casting
        if not isinstance(val, AttribAccessDict):
            # Collate type hints that we may have
            type_hints = {}
            try:
                type_hints = get_type_hints(self.__class__)
            except:
                pass
            init_hints = {}
            try:
                init_hints = get_type_hints(self.__class__.__init__)
            except:
                pass
            type_hints.update(init_hints)

            # Ugly hack: We have to specialize unions by hand because you can't just guess by content generally
            # Note for developers: This means type MUST be set before meta. fortunately, we can enforce this via
            # the type hints (assuming that the order of annotations is not changed, which python does not guarantee,
            # if it ever does: we'll have to add another hack to the constructor)
            from mastodon.return_types import MediaAttachment
            if type(self) == MediaAttachment and key == "type":
                self.__union_specializer = val

            # Do we have a union specializer attribute?
            union_specializer = None
            if hasattr(self, "_AttribAccessDict__union_specializer"):
                union_specializer = self.__union_specializer

            # Do typecasting, possibly iterating over a list or tuple
            if key in type_hints:
                type_hint = type_hints[key]
                val = try_cast_recurse(type_hint, val, union_specializer)
            else:
                if isinstance(val, dict):
                    val = try_cast_recurse(AttribAccessDict, val, union_specializer)
                elif isinstance(val, list):
                    val = try_cast_recurse(EntityList, val, union_specializer)

        # Finally, call out to setattr and setitem proper
        super(AttribAccessDict, self).__setattr__(key, val)
        super(AttribAccessDict, self).__setitem__(key, val)

        # Remove union specializer if we have one
        if "_AttribAccessDict__union_specializer" in self:
            del self["_AttribAccessDict__union_specializer"]

    def __eq__(self, other):
        """
        Equality checker with casting
        """
        if isinstance(other, self.__class__):
            return super(AttribAccessDict, self).__eq__(other)
        else:
            try:
                casted = try_cast_recurse(self.__class__, other)
                if isinstance(casted, self.__class__):
                    return super(AttribAccessDict, self).__eq__(casted)
                else:
                    return False
            except Exception as e:
                pass
        return False

WebpushCryptoParamsPubkey = Dict[str, str]
"""A type containing the parameters for a encrypting webpush data. Considered opaque / implementation detail."""

WebpushCryptoParamsPrivkey = Dict[str, str]
"""A type containing the parameters for a derypting webpush data. Considered opaque / implementation detail."""

AttribAccessList = PaginatableList
"""Backwards compatibility alias"""
