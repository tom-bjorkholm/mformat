#! /usr/local/bin/python3
"""Tests for paper_size module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from copy import deepcopy
import pytest
from mformat.paper_size import PaperSize


@pytest.mark.parametrize('value, strict, expected',
                         [('A3', True, PaperSize.A3),
                          ('a4', True, PaperSize.A4),
                          ('a5paper', True, PaperSize.A5),
                          ('a4paper ', True, PaperSize.A4),
                          ('letter', True, PaperSize.LETTER),
                          ('legalpaper', True, PaperSize.LEGAL),
                          ('A4_PAPER', True, PaperSize.A4),
                          ('A4-PAPER', True, PaperSize.A4),
                          ('Legal', True, PaperSize.LEGAL),
                          ('Legal', False, PaperSize.LEGAL),
                          ('Let', False, PaperSize.LETTER)])
def test_from_str_ok(value: str, strict: bool, expected: PaperSize) -> None:
    """Test parsing supported paper size values."""
    assert PaperSize.from_str(value, strict=strict) == expected


def test_from_str_enum_passthrough() -> None:
    """Test parsing when input is already a PaperSize."""
    assert PaperSize.from_str(PaperSize.A4) == PaperSize.A4


def test_from_str_type_error() -> None:
    """Test type error for unsupported input type."""
    with pytest.raises(TypeError) as exc:
        PaperSize.from_str(42)  # type: ignore[arg-type]
    assert 'paper_size must be a PaperSize or str' in exc.value.args[0]


def test_from_str_value_error() -> None:
    """Test value error for unsupported paper size text."""
    with pytest.raises(KeyError) as exc:
        PaperSize.from_str('A2')
    assert 'Value "A2" not a valid value for paper size' in exc.value.args[0]


def test_from_str_value_error2() -> None:
    """Test value error for unsupported paper size text."""
    with pytest.raises(ValueError) as exc:
        PaperSize.from_str('Le', strict=False)
    assert 'Ambiguous value "LE" for paper size' in exc.value.args[0]
    assert 'Matches: LEGAL, LETTER' in exc.value.args[0]


def test_from_str_value_error3() -> None:
    """Test value error for strict=False and no match."""
    with pytest.raises(KeyError) as exc:
        PaperSize.from_str('A2', strict=False)
    assert 'Value "A2" does not match any allowed value for paper size' \
        in exc.value.args[0]


@pytest.mark.parametrize('low, upp, expected',
                         [(False, False, ['A3', 'A4', 'A5', 'Legal',
                                          'Letter']),
                          (True, False, ['A3', 'A4', 'A5', 'Legal', 'Letter',
                                         'a3', 'a4', 'a5', 'legal', 'letter']),
                          (False, True, ['A3', 'A4', 'A5', 'Legal', 'Letter',
                                         'LEGAL', 'LETTER']),
                          (True, True, ['A3', 'A4', 'A5', 'Legal', 'Letter',
                                        'a3', 'a4', 'a5', 'legal', 'letter',
                                        'LEGAL', 'LETTER'])])
def test_allowed_values(low: bool, upp: bool, expected: list[str]) -> None:
    """Test allowed values method."""
    vals = PaperSize.allowed_values(include_lower=low, include_upper=upp)
    assert sorted(vals) == sorted(deepcopy(expected))


@pytest.mark.parametrize('value, expected',
                         [(PaperSize.A3, 'a3'),
                          (PaperSize.A4, 'a4'),
                          (PaperSize.A5, 'a5'),
                          (PaperSize.LEGAL, 'legal'),
                          (PaperSize.LETTER, 'letter')])
def test_lower(value: PaperSize, expected: str) -> None:
    """Test lower method."""
    assert value.lower() == expected


@pytest.mark.parametrize('value, expected',
                         [(PaperSize.A3, 'A3'),
                          (PaperSize.A4, 'A4'),
                          (PaperSize.A5, 'A5'),
                          (PaperSize.LEGAL, 'LEGAL'),
                          (PaperSize.LETTER, 'LETTER')])
def test_upper(value: PaperSize, expected: str) -> None:
    """Test upper method."""
    assert value.upper() == expected


@pytest.mark.parametrize('value, expected',
                         [(PaperSize.A3, 'A3'),
                          (PaperSize.A4, 'A4'),
                          (PaperSize.A5, 'A5'),
                          (PaperSize.LEGAL, 'Legal'),
                          (PaperSize.LETTER, 'Letter')])
def test_normalize(value: PaperSize, expected: str) -> None:
    """Test normalize method."""
    assert value.normalize() == expected
