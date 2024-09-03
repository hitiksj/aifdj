"""Tests for dict helpers."""

from sqlfluff.core.helpers.dict import (
    dict_diff,
    iter_records_from_nested_dict,
    nested_combine,
)


def test__helpers_dict__nested_combine():
    """Test combination of two config dicts."""
    a = {"a": {"b": {"c": 123, "d": 456}}}
    b = {"b": {"b": {"c": 123, "d": 456}}}
    c = {"a": {"b": {"c": 234, "e": 456}}}
    r = nested_combine(a, b, c)
    assert r == {
        "a": {"b": {"c": 234, "e": 456, "d": 456}},
        "b": {"b": {"c": 123, "d": 456}},
    }


def test__helpers_dict__dict_diff():
    """Test diffs between two config dicts."""
    a = {"a": {"b": {"c": 123, "d": 456, "f": 6}}}
    b = {"b": {"b": {"c": 123, "d": 456}}}
    c = {"a": {"b": {"c": 234, "e": 456, "f": 6}}}
    assert dict_diff(a, b) == a
    assert dict_diff(a, c) == {"a": {"b": {"c": 123, "d": 456}}}
    assert dict_diff(c, a) == {"a": {"b": {"c": 234, "e": 456}}}


def test__config__iter_records_from_nested_dict():
    """Test conversion from nested dict to records."""
    c = iter_records_from_nested_dict({"a": {"b": {"c": 123, "d": 456}, "f": 6}})
    assert list(c) == [
        (("a", "b", "c"), 123),
        (("a", "b", "d"), 456),
        (("a", "f"), 6),
    ]
