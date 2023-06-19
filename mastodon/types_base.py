from typing import List, Union, Optional, Dict, Any, Tuple, Callable, get_type_hints, TypeVar, IO
from datetime import datetime, timezone
import dateutil
import dateutil.parser
from collections import OrderedDict
import inspect
import json
from mastodon.compat import PurePath

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

"""
The base type for all non-snowflake IDs. This is a union of int and str 
because while Mastodon mostly uses IDs that are ints, it doesn't guarantee
this and other implementations do not use integer IDs.

In a change from previous versions, string IDs now take precedence over ints.
This is a breaking change, and I'm sorry about it, but this will make every piece
of software using Mastodon.py more robust in the long run.
"""
PrimitiveIdType = Union[str, int]

class MaybeSnowflakeIdType(str):
    """
    Represents, maybe, a snowflake ID.

    Contains what a regular ID can contain (int or str) and will convert to int if
    containing an int or a str that naturally converts to an int (e.g. "123").

    Can *also* contain a *datetime* which gets converted to 

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
    
"""
IDs returned from Mastodon.py ar either primitive (int or str) or snowflake
(still int or str, but potentially convertible to datetime).
"""
IdType = Union[PrimitiveIdType, MaybeSnowflakeIdType]

T = TypeVar('T')
class PaginatableList(List[T]):
    """
    This is a list with pagination information attached.

    It is returned by the API when a list of items is requested, and the response contains
    a Link header with pagination information.
    """
    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError(f"Attribute not found: {attr}")

    def __setattr__(self, attr, val):
        if attr in self:
            raise AttributeError("Attribute-style access is read only")
        super(NonPaginatableList, self).__setattr__(attr, val)
    # TODO add the pagination housekeeping stuff

class NonPaginatableList(List[T]):
    """
    This is just a list. I am subclassing the regular list out of pure paranoia about
    potential oversights that might require me to add things to it later.
    """
    pass

# Lists in Mastodon.py are either regular or paginatable
EntityList = Union[NonPaginatableList[T], PaginatableList[T]]

# Backwards compat alias
AttribAccessList = EntityList

# Helper functions for typecasting attempts
def try_cast(t, value, retry = True):
    """
    Base case casting function. Handles:
    * Casting to any AttribAccessDict subclass (directly, no special handling)
    * Casting to MaybeSnowflakeIdType (directly, no special handling)
    * Casting to bool (with possible conversion from json bool strings)
    * Casting to datetime (with possible conversion from all kinds of funny date formats because unfortunately this is the world we live in)
    Gives up and returns as-is if none of the above work.
    """
    try:
        if issubclass(t, AttribAccessDict) or t is MaybeSnowflakeIdType:
            try:
                value = t(**value)
            except:
                try:
                    value = AttribAccessDict(**value)
                except:
                    pass
        elif isinstance(t, bool):
            if isinstance(value, str):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
            value = bool(value)
        elif isinstance(t, datetime):
            if isinstance(value, int):
                value = datetime.fromtimestamp(value, timezone.utc)
            elif isinstance(value, str):
                try:
                    value_int = int(value)
                    value = datetime.fromtimestamp(value_int, timezone.utc)
                except:
                    value = dateutil.parser.parse(value)
    except:
        value = try_cast(AttribAccessDict, value, False)
    return value

def try_cast_recurse(t, value):
    """
    Non-dict compound type casting function. Handles:
    * Casting to list, tuple, EntityList or (Non)PaginatableList, converting all elements to the correct type recursively
    * Casting to Union, trying all types in the union until one works
    Gives up and returns as-is if none of the above work.
    """
    try:
        orig_type = getattr(t, '__origin__')
        if orig_type in (list, tuple, EntityList, NonPaginatableList, PaginatableList):
            value_cast = []
            type_args = t.__args__
            if len(type_args) == 1:
                type_args = type_args * len(value)
            for element_type, v in zip(type_args, value):
                value_cast.append(try_cast_recurse(element_type, v))
            value = orig_type(value_cast)
        elif orig_type is Union:
            for t in t.__args__:
                value = try_cast_recurse(t, value)
                if isinstance(value, t):
                    break
    except Exception as e:
        pass
    return try_cast(t, value)

class AttribAccessDict(OrderedDict[str, Any]):
    """
    Base return object class for Mastodon.py.

    Inherits from dict, but allows access via attributes as well as if it was a dataclass.

    While the subclasses implement specific fields with proper typing, parsing and documentation,
    they all inherit from this class, and parsing is extremely permissive to allow for forward and
    backward compatibility as well as compatibility with other implementations of the Mastodon API.
    """
    def __init__(self, **kwargs):
        """
        Constructor that calls through to dict constructor and then sets attributes for all keys.
        """
        super(AttribAccessDict, self).__init__()
        if __annotations__ in self.__class__.__dict__:
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
        if attr == '__class__':
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
                raise AttributeError(f"Attribute not found: {attr}")
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
                raise AttributeError(f"Attribute not found: {attr}")
            
    def __setattr__(self, attr, val):
        """
        Attribute setter that calls through to dict setter but will throw if attribute is not in dict
        """
        if attr in self:
            self[attr] = val
        else:
            raise AttributeError(f"Attribute not found: {attr}")

    def __setitem__(self, key, val):
        """
        Dict setter that also sets attributes and tries to typecast if we have an 
        AttribAccessDict or MaybeSnowflakeIdType type hint.

        For Unions, it will try the types in order.
        """
        # Collate type hints that we may have
        type_hints = get_type_hints(self.__class__)
        init_hints = get_type_hints(self.__class__.__init__)
        type_hints.update(init_hints)

        # Do typecasting, possibly iterating over a list or tuple
        if key in type_hints:
            type_hint = type_hints[key]
            val = try_cast_recurse(type_hint, val)

        # Finally, call out to setattr and setitem proper
        super(AttribAccessDict, self).__setattr__(key, val)
        super(AttribAccessDict, self).__setitem__(key, val)

"""An entity returned by the Mastodon API is either a dict or a list"""
Entity = Union[AttribAccessDict, EntityList]

"""A type containing the parameters for a encrypting webpush data. Considered opaque / implementation detail."""
WebpushCryptoParamsPubkey = Dict[str, str]

"""A type containing the parameters for a derypting webpush data. Considered opaque / implementation detail."""
WebpushCryptoParamsPrivkey = Dict[str, str]