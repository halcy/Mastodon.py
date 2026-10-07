import pytest
from datetime import datetime, timezone
from mastodon.types_base import base62_to_int, int_to_base62, MaybeSnowflakeIdType, _str_to_type, PaginatableList, NonPaginatableList, AttribAccessDict, _get_cached_type_hints
from typing import Optional, Union


class AnnualReportDataV2(AttribAccessDict):
    current: int


class AnnualReportDataV1(AttribAccessDict):
    previous: int


class AnnualReport(AttribAccessDict):
    data: Union[AnnualReportDataV2, AnnualReportDataV1, AttribAccessDict]
    schema_version: int


def test_base62_to_int_zero():
    assert base62_to_int('0') == 0

def test_base62_to_int_single_digit():
    assert base62_to_int('A') == 10
    assert base62_to_int('Z') == 35
    assert base62_to_int('a') == 36
    assert base62_to_int('z') == 61

def test_base62_to_int_multidigit():
    assert base62_to_int('10') == 62
    assert base62_to_int('100') == 62 * 62

def test_int_to_base62_zero():
    assert int_to_base62(0) == '0'

def test_int_to_base62_small():
    assert int_to_base62(10) == 'A'
    assert int_to_base62(61) == 'z'
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

def test_to_datetime_pleroma_family_flake():
    snowflake = MaybeSnowflakeIdType("9n2ciuz1wdesFnrGJU")
    dt = snowflake.to_datetime()
    assert dt is not None
    assert dt.timestamp() == pytest.approx(1568795327.357)

@pytest.mark.parametrize("misskey_id", [
    "9abcdefgh0",
    "9abcdefgh0abcdef",
    "01941f297c00123456789abc",
    "g1941f297c00123456789abc",
    "67748580123456789abcdef0",
    "01JGFJJ0000123456789ABCDEF",
])
def test_to_datetime_rejects_misskey_ids(misskey_id):
    assert MaybeSnowflakeIdType(misskey_id).to_datetime() is None

def test_to_datetime_rejects_implausible_base62_id():
    assert MaybeSnowflakeIdType("zzzzzzzzzzzzzzzzzz").to_datetime() is None

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
    assert snowflake == str(snowflake)

def test_id_numeric_comparison():
    assert MaybeSnowflakeIdType(9) < MaybeSnowflakeIdType(80)
    assert MaybeSnowflakeIdType("9") <= 9
    assert 80 > MaybeSnowflakeIdType("9")
    assert MaybeSnowflakeIdType("9") != 9
    assert hash(MaybeSnowflakeIdType("9")) == hash("9")

def test_pleroma_id_comparison_is_cached(monkeypatch):
    older = MaybeSnowflakeIdType("9n2ciuz1wdesFnrGJU")
    newer = MaybeSnowflakeIdType(datetime(2023, 6, 15), assume_pleroma=True)

    monkeypatch.setattr("mastodon.types_base._pleroma_id_to_int", lambda value: None)

    assert older < newer

def test_id_numeric_comparison_rejects_non_numeric_values():
    for value in (True, "opaque"):
        with pytest.raises(TypeError, match=f"ID {value!r} is not comparable with IDs"):
            MaybeSnowflakeIdType(9) < value

def test_statuses_sort_by_mixed_id_types():
    from mastodon.return_types import Status

    timestamp = 1609459200
    snowflake = lambda seconds: (seconds << 16) * 1000
    oldest = Status(id=datetime.fromtimestamp(timestamp, timezone.utc))
    naive_datetime = Status(id=datetime.fromtimestamp(timestamp + 1))
    middle = Status(id=str(snowflake(timestamp + 2)))
    pleroma = Status(id=MaybeSnowflakeIdType(
        datetime.fromtimestamp(timestamp + 2.5, timezone.utc),
        assume_pleroma=True,
    ))
    newest = Status(id=snowflake(timestamp + 3))

    assert sorted([newest, pleroma, oldest, middle, naive_datetime], key=lambda status: status.id) == [
        oldest, naive_datetime, middle, pleroma, newest
    ]

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

def test_type_hints_failure_returns_empty_dict():
    class DynamicEntity(AttribAccessDict):
        value: "MissingType"

    assert _get_cached_type_hints(DynamicEntity) == {}

def test_str_to_type_dangling_open_bracket():
    with pytest.raises(ValueError, match="Invalid type"):
        _str_to_type("PaginatableList[")

def test_str_to_type_dangling_close_bracket():
    with pytest.raises(ValueError, match="Invalid type"):
        _str_to_type("Status]")

@pytest.mark.parametrize("schema_version, expected_type", [
    (2, AnnualReportDataV2),
    ("2", AnnualReportDataV2),
    (1, AnnualReportDataV1),
    ("1", AnnualReportDataV1),
])
def test_annual_report_union_specialization(schema_version, expected_type):
    report = AnnualReport(data={"value": 1}, schema_version=schema_version)

    assert type(report.data) is expected_type

@pytest.mark.parametrize("schema_version", [None, 3, "future"])
def test_annual_report_union_specialization_falls_back(schema_version):
    report = AnnualReport(data={"future_value": 1}, schema_version=schema_version)

    assert type(report.data) is AttribAccessDict

def test_media_union_specialization():
    from mastodon.return_types import MediaAttachment, MediaAttachmentImageMetadata, MediaAttachmentVideoMetadata

    image = MediaAttachment(type="image", meta={"original": {}, "small": {}})
    video = MediaAttachment(type="video", meta={"original": {}, "small": {}})
    reassigned = MediaAttachment()
    reassigned.type = "video"
    reassigned.meta = {"original": {}, "small": {}}

    assert type(image.meta.original) is MediaAttachmentImageMetadata
    assert type(video.meta.original) is MediaAttachmentVideoMetadata
    assert type(reassigned.meta.original) is MediaAttachmentVideoMetadata
