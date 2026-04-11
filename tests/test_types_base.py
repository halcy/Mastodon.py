import pytest
from datetime import datetime, timezone
from mastodon.types_base import base62_to_int, int_to_base62, MaybeSnowflakeIdType, _str_to_type, PaginatableList, NonPaginatableList
from typing import Optional, Union

def test_base62_to_int_zero():
    assert base62_to_int('0') == 0

def test_base62_to_int_single_digit():
    assert base62_to_int('a') == 10
    assert base62_to_int('z') == 35
    assert base62_to_int('A') == 36
    assert base62_to_int('Z') == 61

def test_base62_to_int_multidigit():
    assert base62_to_int('10') == 62
    assert base62_to_int('100') == 62 * 62

def test_int_to_base62_zero():
    assert int_to_base62(0) == '0'

def test_int_to_base62_small():
    assert int_to_base62(10) == 'a'
    assert int_to_base62(61) == 'Z'
    assert int_to_base62(62) == '10'

def test_base62_roundtrip():
    for val in [0, 1, 61, 62, 100, 999999, 2**48]:
        assert base62_to_int(int_to_base62(val)) == val

def test_base62_roundtrip_from_string():
    for s in ['0', '1', 'abc', 'ZZZ', '10']:
        assert int_to_base62(base62_to_int(s)) == s

def test_to_datetime_mastodon_snowflake_string():
    snowflake = MaybeSnowflakeIdType("109404970108594430")
    dt = snowflake.to_datetime()
    assert dt is not None
    assert isinstance(dt, datetime)
    assert dt.year == 2022

def test_to_datetime_mastodon_snowflake_int():
    snowflake = MaybeSnowflakeIdType(109404970108594430)
    dt = snowflake.to_datetime()
    assert dt is not None
    assert dt.year == 2022

def test_to_datetime_pleroma_base62():
    known_int = 109404970108594430
    base62_str = int_to_base62(known_int)
    snowflake = MaybeSnowflakeIdType(base62_str, assume_pleroma=True)
    dt = snowflake.to_datetime()
    assert dt is not None
    assert dt.year == 2022

def test_to_datetime_non_numeric_string():
    base62_str = int_to_base62(109404970108594430)
    snowflake = MaybeSnowflakeIdType(base62_str)
    dt = snowflake.to_datetime()
    assert dt is not None

def test_to_datetime_roundtrip():
    original = datetime(2023, 6, 15, 12, 0, 0)
    snowflake = MaybeSnowflakeIdType(original)
    result = snowflake.to_datetime()
    assert result is not None
    assert abs((result - original).total_seconds()) < 2

def test_to_datetime_roundtrip_pleroma():
    original = datetime(2023, 6, 15, 12, 0, 0)
    snowflake = MaybeSnowflakeIdType(original, assume_pleroma=True)
    result = snowflake.to_datetime()
    assert result is not None
    assert abs((result - original).total_seconds()) < 2

def test_str_to_type_simple():
    from mastodon.return_types import Status
    assert _str_to_type("Status") is Status

def test_str_to_type_paginatable_list():
    from mastodon.return_types import Status
    assert _str_to_type("PaginatableList[Status]") == PaginatableList[Status]

def test_str_to_type_non_paginatable_list():
    from mastodon.return_types import Status
    assert _str_to_type("NonPaginatableList[Status]") == NonPaginatableList[Status]

def test_str_to_type_optional():
    from mastodon.return_types import Status
    assert _str_to_type("typing.Optional[Status]") == Optional[Status]

def test_str_to_type_union():
    from mastodon.return_types import Status, Account
    assert _str_to_type("typing.Union[Status, Account]") == Union[Status, Account]

def test_str_to_type_unknown():
    with pytest.raises(ValueError, match="Unknown type"):
        _str_to_type("TotallyFakeType")

def test_str_to_type_invalid_subtype_container():
    with pytest.raises(ValueError, match="Subtype not allowed"):
        _str_to_type("Status[Account]")

def test_str_to_type_dangling_open_bracket():
    with pytest.raises(ValueError, match="Invalid type"):
        _str_to_type("PaginatableList[")

def test_str_to_type_dangling_close_bracket():
    with pytest.raises(ValueError, match="Invalid type"):
        _str_to_type("Status]")
