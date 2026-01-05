#! /usr/local/bin/python3
"""Test the mformat_docx module lists functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
from test_mformat_docx_core import silent_docx_create
from mformat_ext.mformat_docx import MultiFormatDocx

# Add base test helpers to path for shared test utilities
_base_test_path = (
    Path(__file__).parent.parent.parent.parent /
    'base' / 'test' / 'test_mformat'
)
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from test_helpers import action_complex_nested_bullet_structure  # noqa: E402


def test_single_bullet_item(capsys):
    """Test a single bullet item."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='First item')

    silent_docx_create(capsys, func=func)


def test_multiple_bullet_items(capsys):
    """Test multiple bullet items."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_bullet_item(text='Third item')

    silent_docx_create(capsys, func=func)


def test_bullet_item_with_add_text(capsys):
    """Test bullet item with additional text."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='First item')
        mfd.add_text(text=' with more text')

    silent_docx_create(capsys, func=func)


def test_bullet_item_with_url(capsys):
    """Test bullet item with URL."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    silent_docx_create(capsys, func=func)


def test_nested_bullet_items_level2(capsys):
    """Test nested bullet items at level 2."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)

    silent_docx_create(capsys, func=func)


def test_nested_bullet_items_level3(capsys):
    """Test nested bullet items at level 3."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 3', level=3)

    silent_docx_create(capsys, func=func)


def test_bullet_list_back_to_level1(capsys):
    """Test bullet list returning to level 1."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='Level 1 first', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 1 second', level=1)

    silent_docx_create(capsys, func=func)


def test_bullet_list_formatting(capsys):
    """Test bullet list with bold and italic."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='Bold item', bold=True)
        mfd.start_bullet_item(text='Italic item', italic=True)
        mfd.start_bullet_item(text='Both', bold=True, italic=True)

    silent_docx_create(capsys, func=func)


def test_paragraph_then_bullet_list(capsys):
    """Test paragraph followed by bullet list."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_paragraph(text='Intro paragraph')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    silent_docx_create(capsys, func=func)


def test_bullet_list_then_paragraph(capsys):
    """Test bullet list followed by paragraph."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_paragraph(text='Concluding paragraph')

    silent_docx_create(capsys, func=func)


def test_heading_then_bullet_list(capsys):
    """Test heading followed by bullet list."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=1, text='Main Title')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    silent_docx_create(capsys, func=func)


def test_complex_nested_structure(capsys):
    """Test complex nested bullet structure."""
    def func(mfd: MultiFormatDocx) -> None:
        action_complex_nested_bullet_structure(mfd)

    silent_docx_create(capsys, func=func)


# Tests for numbered point lists


def test_single_numbered_item(capsys):
    """Test a single numbered point item."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='First item')

    silent_docx_create(capsys, func=func)


def test_multiple_numbered_items(capsys):
    """Test multiple numbered point items."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')
        mfd.start_numbered_point_item(text='Third item')

    silent_docx_create(capsys, func=func)


def test_numbered_item_with_add_text(capsys):
    """Test numbered point item with additional text."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='First item')
        mfd.add_text(text=' with more text')

    silent_docx_create(capsys, func=func)


def test_numbered_item_with_url(capsys):
    """Test numbered point item with URL."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    silent_docx_create(capsys, func=func)


def test_nested_numbered_items_level2(capsys):
    """Test nested numbered point items at level 2."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='Level 1', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)

    silent_docx_create(capsys, func=func)


def test_nested_numbered_items_level3(capsys):
    """Test nested numbered point items at level 3."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='Level 1', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)
        mfd.start_numbered_point_item(text='Level 3', level=3)

    silent_docx_create(capsys, func=func)


def test_numbered_list_back_to_level1(capsys):
    """Test numbered point list returning to level 1."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='Level 1 first', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)
        mfd.start_numbered_point_item(text='Level 1 second', level=1)

    silent_docx_create(capsys, func=func)


def test_numbered_list_formatting(capsys):
    """Test numbered point list with bold and italic."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='Bold item', bold=True)
        mfd.start_numbered_point_item(text='Italic item', italic=True)
        mfd.start_numbered_point_item(text='Both', bold=True, italic=True)

    silent_docx_create(capsys, func=func)


def test_paragraph_then_numbered_list(capsys):
    """Test paragraph followed by numbered point list."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_paragraph(text='Intro paragraph')
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')

    silent_docx_create(capsys, func=func)


def test_numbered_list_then_paragraph(capsys):
    """Test numbered point list followed by paragraph."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')
        mfd.start_paragraph(text='Concluding paragraph')

    silent_docx_create(capsys, func=func)


def test_heading_then_numbered_list(capsys):
    """Test heading followed by numbered point list."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=1, text='Main Title')
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')

    silent_docx_create(capsys, func=func)


def test_mixed_bullet_and_numbered_lists(capsys):
    """Test switching between bullet and numbered point lists."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='Bullet 1', level=1)
        mfd.start_bullet_item(text='Bullet 2', level=1)
        mfd.start_numbered_point_item(text='Numbered 1', level=1)
        mfd.start_numbered_point_item(text='Numbered 2', level=1)

    silent_docx_create(capsys, func=func)


def test_nested_mixed_lists(capsys):
    """Test nested mixed bullet and numbered point lists."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_bullet_item(text='Bullet 1', level=1)
        mfd.start_numbered_point_item(text='Numbered 1.1', level=2)
        mfd.start_numbered_point_item(text='Numbered 1.2', level=2)
        mfd.start_bullet_item(text='Bullet 2', level=1)

    silent_docx_create(capsys, func=func)
