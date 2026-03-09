#! /usr/local/bin/python3
"""Tests for document_class module."""

# Copyright (c) 2026 Tom Bjorkholm
# MIT License
#

from copy import deepcopy
import pytest
from mformat.document_class import DocumentClass


@pytest.mark.parametrize('value, strict, expected',
                         [('article', True, DocumentClass.ARTICLE),
                          ('REPORT', True, DocumentClass.REPORT),
                          (' Book ', True, DocumentClass.BOOK),
                          ('letter', True, DocumentClass.LETTER),
                          ('rep', False, DocumentClass.REPORT),
                          ('let', False, DocumentClass.LETTER)])
def test_from_str_ok(value: str, strict: bool,
                     expected: DocumentClass) -> None:
    """Test parsing supported document class values."""
    assert DocumentClass.from_str(value, strict=strict) == expected


def test_from_str_enum_passthrough() -> None:
    """Test parsing when input is already a DocumentClass."""
    assert DocumentClass.from_str(DocumentClass.BOOK) == DocumentClass.BOOK


def test_from_str_type_error() -> None:
    """Test type error for unsupported input type."""
    with pytest.raises(TypeError) as exc:
        DocumentClass.from_str(42)  # type: ignore[arg-type]
    assert 'document_class must be a DocumentClass or str' in exc.value.args[0]


def test_from_str_strict_key_error() -> None:
    """Test key error for strict parsing and unsupported value."""
    with pytest.raises(KeyError) as exc:
        DocumentClass.from_str('thesis')
    assert 'Value "thesis" not a valid value for document class' \
        in exc.value.args[0]


def test_from_str_non_strict_no_match_key_error() -> None:
    """Test key error for strict=False and unsupported value."""
    with pytest.raises(KeyError) as exc:
        DocumentClass.from_str('thesis', strict=False)
    expected = 'Value "thesis" does not match any allowed value '
    expected += 'for document class'
    assert expected in exc.value.args[0]


def test_from_str_non_strict_ambiguous() -> None:
    """Test ambiguous value error for strict=False."""
    with pytest.raises(ValueError) as exc:
        DocumentClass.from_str(' ', strict=False)
    assert 'Ambiguous value " " for document class' in exc.value.args[0]
    assert 'Matches: ARTICLE, REPORT, BOOK, LETTER' in exc.value.args[0]


@pytest.mark.parametrize('low, upp, expected',
                         [(False, False, ['Article', 'Report', 'Book',
                                          'Letter']),
                          (True, False, ['Article', 'Report', 'Book',
                                         'Letter', 'article', 'report',
                                         'book', 'letter']),
                          (False, True, ['Article', 'Report', 'Book',
                                         'Letter', 'ARTICLE', 'REPORT',
                                         'BOOK', 'LETTER']),
                          (True, True, ['Article', 'Report', 'Book',
                                        'Letter', 'article', 'report',
                                        'book', 'letter', 'ARTICLE',
                                        'REPORT', 'BOOK', 'LETTER'])])
def test_allowed_values(low: bool, upp: bool, expected: list[str]) -> None:
    """Test allowed values method."""
    vals = DocumentClass.allowed_values(include_lower=low, include_upper=upp)
    assert sorted(vals) == sorted(deepcopy(expected))


@pytest.mark.parametrize('value, expected',
                         [(DocumentClass.ARTICLE, 'article'),
                          (DocumentClass.REPORT, 'report'),
                          (DocumentClass.BOOK, 'book'),
                          (DocumentClass.LETTER, 'letter')])
def test_lower(value: DocumentClass, expected: str) -> None:
    """Test lower method."""
    assert value.lower() == expected


@pytest.mark.parametrize('value, expected',
                         [(DocumentClass.ARTICLE, 'ARTICLE'),
                          (DocumentClass.REPORT, 'REPORT'),
                          (DocumentClass.BOOK, 'BOOK'),
                          (DocumentClass.LETTER, 'LETTER')])
def test_upper(value: DocumentClass, expected: str) -> None:
    """Test upper method."""
    assert value.upper() == expected


@pytest.mark.parametrize('value, expected',
                         [(DocumentClass.ARTICLE, 'Article'),
                          (DocumentClass.REPORT, 'Report'),
                          (DocumentClass.BOOK, 'Book'),
                          (DocumentClass.LETTER, 'Letter')])
def test_normalize(value: DocumentClass, expected: str) -> None:
    """Test normalize method."""
    assert value.normalize() == expected
