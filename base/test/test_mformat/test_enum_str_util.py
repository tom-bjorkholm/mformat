#! /usr/local/bin/python3
"""Tests for enum_str_util module."""

# Copyright (c) 2026 Tom Bjorkholm
# MIT License
#

from enum import Enum, IntEnum, auto
import pytest
from mformat.enum_str_util import from_str, possible_values


class Color(Enum):
    """Test enum with string values."""

    RED = 'stop'
    GREEN = 'go'
    YELLOW = 'wait'


class Level(IntEnum):
    """Test enum with integer values."""

    LOW = auto()
    LONG = auto()
    HIGH = auto()


class ShortName(IntEnum):
    """Test enum for duplicate output variants."""

    A = auto()
    A1 = auto()


def test_from_str_enum_passthrough() -> None:
    """Test parsing when value is already an enum member."""
    assert from_str(Level, Level.HIGH) == Level.HIGH


def test_from_str_exact_name_case_insensitive() -> None:
    """Test parsing by member name, case-insensitive."""
    assert from_str(Level, 'high') == Level.HIGH


def test_from_str_name_with_surrounding_whitespace() -> None:
    """Test parsing by member name with surrounding whitespace."""
    assert from_str(Level, ' HIGH ') == Level.HIGH


def test_from_str_by_string_value() -> None:
    """Test parsing by enum value for string-valued enum."""
    assert from_str(Color, 'go') == Color.GREEN


def test_from_str_type_error() -> None:
    """Test type error for unsupported input type."""
    with pytest.raises(TypeError) as exc:
        from_str(Level, 42)  # type: ignore[arg-type]
    assert 'value must be a Level or str' in exc.value.args[0]


def test_from_str_key_error_default_what() -> None:
    """Test strict key error with default what value."""
    with pytest.raises(KeyError) as exc:
        from_str(Level, 'missing')
    assert 'Value "missing" not a valid value for Level' in exc.value.args[0]


def test_from_str_key_error_custom_what() -> None:
    """Test strict key error with custom what value."""
    with pytest.raises(KeyError) as exc:
        from_str(Level, 'missing', what='level')
    assert 'Value "missing" not a valid value for level' in exc.value.args[0]


def test_from_str_non_strict_unique_prefix() -> None:
    """Test non-strict parsing with one unique match."""
    assert from_str(Level, 'hi', strict=False) == Level.HIGH


def test_from_str_non_strict_ambiguous_prefix() -> None:
    """Test non-strict parsing with ambiguous prefix."""
    with pytest.raises(ValueError) as exc:
        from_str(Level, 'lo', strict=False)
    assert 'Ambiguous value "lo" for Level' in exc.value.args[0]
    assert 'Matches: LOW, LONG' in exc.value.args[0]


def test_from_str_non_strict_no_match() -> None:
    """Test non-strict parsing with no match."""
    with pytest.raises(KeyError) as exc:
        from_str(Level, 'ZZ', strict=False)
    assert 'Value "ZZ" does not match any allowed value for Level' \
        in exc.value.args[0]


def test_possible_values_defaults() -> None:
    """Test possible values defaults to capitalized names."""
    assert possible_values(Level) == ['Low', 'Long', 'High']


def test_possible_values_lower_only() -> None:
    """Test possible values with lower-case only output."""
    assert possible_values(Level, include_capitalized=False,
                           include_lower=True) == ['low', 'long', 'high']


def test_possible_values_empty() -> None:
    """Test possible values when no variants are requested."""
    assert not possible_values(Level, include_capitalized=False,
                               include_lower=False, include_upper=False)


def test_possible_values_no_duplicates() -> None:
    """Test that output variants are deduplicated."""
    assert possible_values(ShortName, include_lower=True,
                           include_upper=True) == ['A', 'a', 'A1', 'a1']
