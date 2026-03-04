#! /usr/local/bin/python3
"""Test the mformat_docx module lists functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
import pytest
from mformat_ext.mformat_docx import MultiFormatDocx
from .test_mformat_docx_core import silent_docx_create

# Add base test helpers to path for shared test utilities
_base_test_path = (Path(__file__).parent.parent.parent.parent / 'base' /
                   'test')
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from test_mformat.check_capsys import check_capsys  # noqa: E402
from test_mformat.test_helpers import (  # noqa: E402
    action_complex_nested_bullet_structure,
)


def test_single_bullet_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single bullet item."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='First item')

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert '<li>First item</li>' in html
    assert '</ul>' in html


def test_multiple_bullet_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple bullet items."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')
        mfd.new_bullet_item(text='Third item')

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html
    assert '<li>Third item</li>' in html


def test_bullet_item_with_add_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet item with additional text."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='First item')
        mfd.add_text(text=' with more text')

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert '<li>First item with more text</li>' in html


def test_bullet_item_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet item with URL."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert 'Check' in html
    assert '<a href="http://example.com">this link</a>' in html


def test_nested_bullet_items_level2(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested bullet items at level 2."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='Level 1', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert 'Level 1' in html
    assert 'Level 2' in html


def test_nested_bullet_items_level3(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested bullet items at level 3."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='Level 1', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)
        mfd.new_bullet_item(text='Level 3', level=3)

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert 'Level 1' in html
    assert 'Level 2' in html
    assert 'Level 3' in html


def test_bullet_list_back_to_level1(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list returning to level 1."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='Level 1 first', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)
        mfd.new_bullet_item(text='Level 1 second', level=1)

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert 'Level 1 first' in html
    assert 'Level 2' in html
    assert 'Level 1 second' in html


def test_bullet_list_formatting(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list with bold and italic."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='Bold item', bold=True)
        mfd.new_bullet_item(text='Italic item', italic=True)
        mfd.new_bullet_item(text='Both', bold=True, italic=True)

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert '<strong>Bold item</strong>' in html
    assert '<em>Italic item</em>' in html
    assert 'Both' in html


def test_paragraph_then_bullet_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by bullet list."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_paragraph(text='Intro paragraph')
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')

    html = silent_docx_create(capsys, func=func)
    assert '<p>Intro paragraph</p>' in html
    assert '<ul>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html


def test_bullet_list_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list followed by paragraph."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')
        mfd.new_paragraph(text='Concluding paragraph')

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html
    assert '<p>Concluding paragraph</p>' in html


def test_heading_then_bullet_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by bullet list."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=1, text='Main Title')
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')

    html = silent_docx_create(capsys, func=func)
    assert '<h1>Main Title</h1>' in html
    assert '<ul>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html


def test_complex_nested_structure(capsys: pytest.CaptureFixture[str]) -> None:
    """Test complex nested bullet structure."""

    def func(mfd: MultiFormatDocx) -> None:
        action_complex_nested_bullet_structure(mfd)

    html = silent_docx_create(capsys, func=func)
    # Verify at least the outer list structure and some content
    assert '<ul>' in html
    assert 'Item 1' in html
    assert 'Item 1.1' in html
    assert 'Item 2' in html


# Tests for numbered point lists


def test_single_numbered_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single numbered point item."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='First item')

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert '<li>First item</li>' in html
    assert '</ol>' in html


def test_multiple_numbered_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple numbered point items."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')
        mfd.new_numbered_point_item(text='Third item')

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html
    assert '<li>Third item</li>' in html
    assert '</ol>' in html


def test_numbered_item_with_add_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point item with additional text."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='First item')
        mfd.add_text(text=' with more text')

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert '<li>First item with more text</li>' in html


def test_numbered_item_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point item with URL."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert 'Check' in html
    assert '<a href="http://example.com">this link</a>' in html
    assert '</ol>' in html


def test_nested_numbered_items_level2(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested numbered point items at level 2."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='Level 1', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert 'Level 1' in html
    assert 'Level 2' in html
    assert html.count('<ol>') == 2
    assert html.count('</ol>') == 2


def test_nested_numbered_items_level3(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested numbered point items at level 3."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='Level 1', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)
        mfd.new_numbered_point_item(text='Level 3', level=3)

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert 'Level 1' in html
    assert 'Level 2' in html
    assert 'Level 3' in html
    assert html.count('<ol>') == 3
    assert html.count('</ol>') == 3


def test_numbered_list_back_to_level1(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list returning to level 1."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='Level 1 first', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)
        mfd.new_numbered_point_item(text='Level 1 second', level=1)

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert 'Level 1 first' in html
    assert 'Level 2' in html
    assert 'Level 1 second' in html


def test_numbered_list_formatting(capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list with bold and italic."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='Bold item', bold=True)
        mfd.new_numbered_point_item(text='Italic item', italic=True)
        mfd.new_numbered_point_item(text='Both', bold=True, italic=True)

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert '<strong>Bold item</strong>' in html
    assert '<em>Italic item</em>' in html
    assert 'Both' in html
    assert '</ol>' in html


def test_paragraph_then_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by numbered point list."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_paragraph(text='Intro paragraph')
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')

    html = silent_docx_create(capsys, func=func)
    assert '<p>Intro paragraph</p>' in html
    assert '<ol>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html
    assert '</ol>' in html


def test_numbered_list_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list followed by paragraph."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')
        mfd.new_paragraph(text='Concluding paragraph')

    html = silent_docx_create(capsys, func=func)
    assert '<ol>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html
    assert '</ol>' in html
    assert '<p>Concluding paragraph</p>' in html


def test_heading_then_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by numbered point list."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_heading(level=1, text='Main Title')
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')

    html = silent_docx_create(capsys, func=func)
    assert '<h1>Main Title</h1>' in html
    assert '<ol>' in html
    assert '<li>First item</li>' in html
    assert '<li>Second item</li>' in html
    assert '</ol>' in html


def test_mixed_bullet_and_numbered_lists(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test switching between bullet and numbered point lists."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='Bullet 1', level=1)
        mfd.new_bullet_item(text='Bullet 2', level=1)
        mfd.new_numbered_point_item(text='Numbered 1', level=1)
        mfd.new_numbered_point_item(text='Numbered 2', level=1)

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert '<li>Bullet 1</li>' in html
    assert '<li>Bullet 2</li>' in html
    assert '</ul>' in html
    assert '<ol>' in html
    assert '<li>Numbered 1</li>' in html
    assert '<li>Numbered 2</li>' in html
    assert '</ol>' in html


def test_nested_mixed_lists(capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested mixed bullet and numbered point lists."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='Bullet 1', level=1)
        mfd.new_numbered_point_item(text='Numbered 1.1', level=2)
        mfd.new_numbered_point_item(text='Numbered 1.2', level=2)
        mfd.new_bullet_item(text='Bullet 2', level=1)

    html = silent_docx_create(capsys, func=func)
    assert '<ul>' in html
    assert 'Bullet 1' in html
    assert '<ol>' in html
    assert '<li>Numbered 1.1</li>' in html
    assert '<li>Numbered 1.2</li>' in html
    assert '</ol>' in html
    assert 'Bullet 2' in html
    assert '</ul>' in html


def test_numbered_list_depth_limit(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that level > 5 raises RuntimeError."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_numbered_point_item(text='L1', level=1)
        mfd.new_numbered_point_item(text='L2', level=2)
        mfd.new_numbered_point_item(text='L3', level=3)
        mfd.new_numbered_point_item(text='L4', level=4)
        mfd.new_numbered_point_item(text='L5', level=5)
        mfd.new_numbered_point_item(text='L6', level=6)

    with pytest.raises(RuntimeError, match='at most 5'):
        silent_docx_create(capsys, func=func)
    check_capsys(capsys)


def test_bullet_list_depth_limit(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that bullet level > 5 raises RuntimeError."""

    def func(mfd: MultiFormatDocx) -> None:
        mfd.new_bullet_item(text='L1', level=1)
        mfd.new_bullet_item(text='L2', level=2)
        mfd.new_bullet_item(text='L3', level=3)
        mfd.new_bullet_item(text='L4', level=4)
        mfd.new_bullet_item(text='L5', level=5)
        mfd.new_bullet_item(text='L6', level=6)

    with pytest.raises(RuntimeError, match='at most 5'):
        silent_docx_create(capsys, func=func)
    check_capsys(capsys)
