#! /usr/local/bin/python3
"""Test the mformat_odt module lists functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from typing import Any
from pathlib import Path
import pytest
from odf.text import P, List, ListItem, A  # type: ignore[import-untyped]
from mformat_ext.mformat_odt import MultiFormatOdt
from .test_mformat_odt_core import (silent_odt_create, get_elements_by_type,
                                    get_element_text, get_heading_texts,
                                    get_all_text_content, has_span_with_style)

# Add base test helpers to path for shared test utilities
_base_test_path = (Path(__file__).parent.parent.parent.parent / 'base' /
                   'test')
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from test_mformat.test_helpers import (  # noqa: E402
    action_complex_nested_bullet_structure,
)


def get_list_items_text(doc: Any) -> list[str]:
    """Get all list item texts from an ODT document.

    Args:
        doc: The ODF document.

    Returns:
        A list of text content for each list item (stripped of whitespace).
    """
    texts = []
    for item in get_elements_by_type(doc, ListItem):
        texts.append(get_element_text(item).strip())
    return texts


def get_list_count(doc: Any) -> int:
    """Get the count of top-level lists in an ODT document.

    Args:
        doc: The ODF document.

    Returns:
        The number of List elements.
    """
    return len(get_elements_by_type(doc, List))


# --- Tests for bullet lists ---


def test_single_bullet_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single bullet item."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='First item')

    doc = silent_odt_create(capsys, func=func)
    items = get_list_items_text(doc)
    assert 'First item' in items


def test_multiple_bullet_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple bullet items."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='First item')
        mfo.new_bullet_item(text='Second item')
        mfo.new_bullet_item(text='Third item')

    doc = silent_odt_create(capsys, func=func)
    items = get_list_items_text(doc)
    assert 'First item' in items
    assert 'Second item' in items
    assert 'Third item' in items


def test_bullet_item_with_add_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet item with additional text."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='First item')
        mfo.add_text(text=' with more text')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First item with more text' in all_text


def test_bullet_item_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet item with URL."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Check ')
        mfo.add_url(url='http://example.com', text='this link')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Check' in all_text
    assert 'this link' in all_text
    # Verify URL is present in list item
    url_found = False
    for item in get_elements_by_type(doc, ListItem):
        for link in item.getElementsByType(A):
            if link.getAttribute('href') == 'http://example.com':
                url_found = True
    assert url_found


def test_nested_bullet_items_level2(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested bullet items at level 2."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Level 1', level=1)
        mfo.new_bullet_item(text='Level 2', level=2)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1' in all_text
    assert 'Level 2' in all_text


def test_nested_bullet_items_level3(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested bullet items at level 3."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Level 1', level=1)
        mfo.new_bullet_item(text='Level 2', level=2)
        mfo.new_bullet_item(text='Level 3', level=3)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1' in all_text
    assert 'Level 2' in all_text
    assert 'Level 3' in all_text


def test_bullet_list_back_to_level1(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list returning to level 1."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Level 1 first', level=1)
        mfo.new_bullet_item(text='Level 2', level=2)
        mfo.new_bullet_item(text='Level 1 second', level=1)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1 first' in all_text
    assert 'Level 2' in all_text
    assert 'Level 1 second' in all_text


def test_bullet_list_bold_formatting(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list with bold formatting."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Bold item', bold=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Bold item' in all_text
    # Verify bold style
    for item in get_elements_by_type(doc, ListItem):
        if 'Bold item' in get_element_text(item):
            for para in item.getElementsByType(P):
                assert has_span_with_style(para, 'bold')


def test_bullet_list_italic_formatting(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list with italic formatting."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Italic item', italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Italic item' in all_text


def test_bullet_list_bold_italic_formatting(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list with bold and italic formatting."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Both', bold=True, italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Both' in all_text


def test_paragraph_then_bullet_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by bullet list."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_paragraph(text='Intro paragraph')
        mfo.new_bullet_item(text='First item')
        mfo.new_bullet_item(text='Second item')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Intro paragraph' in all_text
    assert 'First item' in all_text
    assert 'Second item' in all_text


def test_bullet_list_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list followed by paragraph."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='First item')
        mfo.new_bullet_item(text='Second item')
        mfo.new_paragraph(text='Concluding paragraph')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First item' in all_text
    assert 'Second item' in all_text
    assert 'Concluding paragraph' in all_text


def test_heading_then_bullet_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by bullet list."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_heading(level=1, text='Main Title')
        mfo.new_bullet_item(text='First item')
        mfo.new_bullet_item(text='Second item')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert headings[0] == (1, 'Main Title')
    all_text = get_all_text_content(doc)
    assert 'First item' in all_text
    assert 'Second item' in all_text


def test_complex_nested_structure(capsys: pytest.CaptureFixture[str]) -> None:
    """Test complex nested bullet structure."""

    def func(mfo: MultiFormatOdt) -> None:
        action_complex_nested_bullet_structure(mfo)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Item 1' in all_text
    assert 'Item 1.1' in all_text
    assert 'Item 1.2' in all_text
    assert 'Item 2' in all_text
    assert 'Item 2.1' in all_text


# --- Tests for numbered point lists ---


def test_single_numbered_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single numbered point item."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='First item')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First item' in all_text


def test_multiple_numbered_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple numbered point items."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='First item')
        mfo.new_numbered_point_item(text='Second item')
        mfo.new_numbered_point_item(text='Third item')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First item' in all_text
    assert 'Second item' in all_text
    assert 'Third item' in all_text


def test_numbered_item_with_add_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point item with additional text."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='First item')
        mfo.add_text(text=' with more text')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First item' in all_text
    assert 'with more text' in all_text


def test_numbered_item_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point item with URL."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Check ')
        mfo.add_url(url='http://example.com', text='this link')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Check' in all_text
    assert 'this link' in all_text


def test_nested_numbered_items_level2(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested numbered point items at level 2."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Level 1', level=1)
        mfo.new_numbered_point_item(text='Level 2', level=2)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1' in all_text
    assert 'Level 2' in all_text


def test_nested_numbered_items_level3(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested numbered point items at level 3."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Level 1', level=1)
        mfo.new_numbered_point_item(text='Level 2', level=2)
        mfo.new_numbered_point_item(text='Level 3', level=3)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1' in all_text
    assert 'Level 2' in all_text
    assert 'Level 3' in all_text


def test_numbered_list_back_to_level1(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list returning to level 1."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Level 1 first', level=1)
        mfo.new_numbered_point_item(text='Level 2', level=2)
        mfo.new_numbered_point_item(text='Level 1 second', level=1)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1 first' in all_text
    assert 'Level 2' in all_text
    assert 'Level 1 second' in all_text


def test_numbered_list_bold_formatting(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list with bold formatting."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Bold item', bold=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Bold item' in all_text


def test_numbered_list_italic_formatting(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list with italic formatting."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Italic item', italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Italic item' in all_text


def test_numbered_list_bold_italic_formatting(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list with bold and italic formatting."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Both', bold=True, italic=True)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Both' in all_text


def test_paragraph_then_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by numbered point list."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_paragraph(text='Intro paragraph')
        mfo.new_numbered_point_item(text='First item')
        mfo.new_numbered_point_item(text='Second item')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Intro paragraph' in all_text
    assert 'First item' in all_text
    assert 'Second item' in all_text


def test_numbered_list_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list followed by paragraph."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='First item')
        mfo.new_numbered_point_item(text='Second item')
        mfo.new_paragraph(text='Concluding paragraph')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'First item' in all_text
    assert 'Second item' in all_text
    assert 'Concluding paragraph' in all_text


def test_heading_then_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by numbered point list."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_heading(level=1, text='Main Title')
        mfo.new_numbered_point_item(text='First item')
        mfo.new_numbered_point_item(text='Second item')

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert headings[0] == (1, 'Main Title')
    all_text = get_all_text_content(doc)
    assert 'First item' in all_text
    assert 'Second item' in all_text


# --- Tests for mixed bullet and numbered lists ---


def test_mixed_bullet_and_numbered_lists(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test switching between bullet and numbered point lists."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Bullet 1', level=1)
        mfo.new_bullet_item(text='Bullet 2', level=1)
        mfo.new_numbered_point_item(text='Numbered 1', level=1)
        mfo.new_numbered_point_item(text='Numbered 2', level=1)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Bullet 1' in all_text
    assert 'Bullet 2' in all_text
    assert 'Numbered 1' in all_text
    assert 'Numbered 2' in all_text


def test_nested_mixed_lists(capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested mixed bullet and numbered point lists."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Bullet 1', level=1)
        mfo.new_numbered_point_item(text='Numbered 1.1', level=2)
        mfo.new_numbered_point_item(text='Numbered 1.2', level=2)
        mfo.new_bullet_item(text='Bullet 2', level=1)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Bullet 1' in all_text
    assert 'Numbered 1.1' in all_text
    assert 'Numbered 1.2' in all_text
    assert 'Bullet 2' in all_text


# --- Tests for special characters in lists ---


def test_special_characters_in_bullet_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test special characters in bullet list."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Special: <>&"\'')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert '<>&"\'' in all_text


def test_unicode_in_numbered_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test unicode in numbered list."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Unicode: åäö 日本語')

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'åäö' in all_text
    assert '日本語' in all_text


# --- Tests for deeply nested lists ---


def test_deeply_nested_bullet_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test deeply nested bullet list (5 levels)."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_bullet_item(text='Level 1', level=1)
        mfo.new_bullet_item(text='Level 2', level=2)
        mfo.new_bullet_item(text='Level 3', level=3)
        mfo.new_bullet_item(text='Level 4', level=4)
        mfo.new_bullet_item(text='Level 5', level=5)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1' in all_text
    assert 'Level 2' in all_text
    assert 'Level 3' in all_text
    assert 'Level 4' in all_text
    assert 'Level 5' in all_text


def test_deeply_nested_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test deeply nested numbered list (5 levels)."""

    def func(mfo: MultiFormatOdt) -> None:
        mfo.new_numbered_point_item(text='Level 1', level=1)
        mfo.new_numbered_point_item(text='Level 2', level=2)
        mfo.new_numbered_point_item(text='Level 3', level=3)
        mfo.new_numbered_point_item(text='Level 4', level=4)
        mfo.new_numbered_point_item(text='Level 5', level=5)

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Level 1' in all_text
    assert 'Level 2' in all_text
    assert 'Level 3' in all_text
    assert 'Level 4' in all_text
    assert 'Level 5' in all_text
