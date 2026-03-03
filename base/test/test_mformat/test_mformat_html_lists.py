#! /usr/local/bin/python3
"""Test the mformat_html module lists functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from mformat.mformat_html import MultiFormatHtml
from .test_helpers import (action_complex_nested_bullet_structure,
                           check_run_with_context_manager)
from .test_mformat_html_core import PF_EN_NT_NC, SFTOT


def test_single_bullet_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single bullet item."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='First item')

    expected = PF_EN_NT_NC + '<ul>\n<li>First item</li>\n</ul>\n' + SFTOT
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_multiple_bullet_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple bullet items."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')
        mfd.new_bullet_item(text='Third item')

    expected = (PF_EN_NT_NC + '<ul>\n<li>First item</li>\n' +
                '<li>Second item</li>\n<li>Third item</li>\n</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_bullet_item_with_add_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet item with additional text."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='First item')
        mfd.add_text(text=' with more text')

    expected = (PF_EN_NT_NC + '<ul>\n<li>First item with more text</li>\n' +
                '</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_bullet_item_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet item with URL."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    expected = (PF_EN_NT_NC + '<ul>\n<li>Check ' +
                '<a href="http://example.com">this link</a></li>\n' +
                '</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_nested_bullet_items_level2(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested bullet items at level 2."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='Level 1', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)

    expected = (PF_EN_NT_NC + '<ul>\n<li>Level 1</li>\n' +
                '<ul>\n<li>Level 2</li>\n</ul>\n</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_nested_bullet_items_level3(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested bullet items at level 3."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='Level 1', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)
        mfd.new_bullet_item(text='Level 3', level=3)

    expected = (PF_EN_NT_NC + '<ul>\n<li>Level 1</li>\n' +
                '<ul>\n<li>Level 2</li>\n' +
                '<ul>\n<li>Level 3</li>\n</ul>\n</ul>\n</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_bullet_list_back_to_level1(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list returning to level 1."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='Level 1 first', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)
        mfd.new_bullet_item(text='Level 1 second', level=1)

    expected = (PF_EN_NT_NC + '<ul>\n<li>Level 1 first</li>\n' +
                '<ul>\n<li>Level 2</li>\n</ul>\n' +
                '<li>Level 1 second</li>\n</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_bullet_list_formatting(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list with bold and italic."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='Bold item', bold=True)
        mfd.new_bullet_item(text='Italic item', italic=True)
        mfd.new_bullet_item(text='Both', bold=True, italic=True)

    expected = (PF_EN_NT_NC + '<ul>\n<li><strong>Bold item</strong></li>\n' +
                '<li><em>Italic item</em></li>\n' +
                '<li><em><strong>Both</strong></em></li>\n</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_paragraph_then_bullet_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by bullet list."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_paragraph(text='Intro paragraph')
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')

    expected = (PF_EN_NT_NC + '<p>\nIntro paragraph</p>\n' +
                '<ul>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_bullet_list_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet list followed by paragraph."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')
        mfd.new_paragraph(text='Concluding paragraph')

    expected = (PF_EN_NT_NC + '<ul>\n<li>First item</li>\n' +
                '<li>Second item</li>\n</ul>\n' +
                '<p>\nConcluding paragraph</p>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_heading_then_bullet_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by bullet list."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=1, text='Main Title')
        mfd.new_bullet_item(text='First item')
        mfd.new_bullet_item(text='Second item')

    expected = (PF_EN_NT_NC + '<h1>\nMain Title</h1>\n' +
                '<ul>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_complex_nested_structure(capsys: pytest.CaptureFixture[str]) -> None:
    """Test complex nested bullet structure."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        action_complex_nested_bullet_structure(mfd)

    expected = (PF_EN_NT_NC + '<ul>\n<li>Item 1</li>\n' +
                '<ul>\n<li>Item 1.1</li>\n<li>Item 1.2</li>\n</ul>\n' +
                '<li>Item 2</li>\n' +
                '<ul>\n<li>Item 2.1</li>\n</ul>\n</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


# Tests for numbered point lists

def test_multiple_numbered_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple numbered items."""

    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')
        mfd.new_numbered_point_item(text='Third item')

    expected = (PF_EN_NT_NC + '<ol>\n<li>First item</li>\n' +
                '<li>Second item</li>\n<li>Third item</li>\n</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_numbered_item_with_add_text(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point item with additional text."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='First item')
        mfd.add_text(text=' with more text')

    expected = (PF_EN_NT_NC + '<ol>\n<li>First item with more text</li>\n' +
                '</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_numbered_item_with_url(capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point item with URL."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    expected = (PF_EN_NT_NC + '<ol>\n<li>Check ' +
                '<a href="http://example.com">this link</a></li>\n' +
                '</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_nested_numbered_items_level2(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested numbered point items at level 2."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='Level 1', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)

    expected = (PF_EN_NT_NC + '<ol>\n<li>Level 1</li>\n' +
                '<ol>\n<li>Level 2</li>\n</ol>\n</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_nested_numbered_items_level3(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested numbered point items at level 3."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='Level 1', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)
        mfd.new_numbered_point_item(text='Level 3', level=3)

    expected = (PF_EN_NT_NC + '<ol>\n<li>Level 1</li>\n' +
                '<ol>\n<li>Level 2</li>\n' +
                '<ol>\n<li>Level 3</li>\n</ol>\n</ol>\n</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_numbered_list_back_to_level1(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list returning to level 1."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='Level 1 first', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)
        mfd.new_numbered_point_item(text='Level 1 second', level=1)

    expected = (PF_EN_NT_NC + '<ol>\n<li>Level 1 first</li>\n' +
                '<ol>\n<li>Level 2</li>\n</ol>\n' +
                '<li>Level 1 second</li>\n</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_numbered_list_formatting(capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list with bold and italic."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='Bold item', bold=True)
        mfd.new_numbered_point_item(text='Italic item', italic=True)
        mfd.new_numbered_point_item(text='Both', bold=True, italic=True)

    expected = (PF_EN_NT_NC + '<ol>\n<li><strong>Bold item</strong></li>\n' +
                '<li><em>Italic item</em></li>\n' +
                '<li><em><strong>Both</strong></em></li>\n</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_paragraph_then_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by numbered point list."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_paragraph(text='Intro paragraph')
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')

    expected = (PF_EN_NT_NC + '<p>\nIntro paragraph</p>\n' +
                '<ol>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_numbered_list_then_paragraph(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test numbered point list followed by paragraph."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')
        mfd.new_paragraph(text='Concluding paragraph')

    expected = (PF_EN_NT_NC + '<ol>\n<li>First item</li>\n' +
                '<li>Second item</li>\n</ol>\n' +
                '<p>\nConcluding paragraph</p>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_heading_then_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by numbered point list."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_heading(level=1, text='Main Title')
        mfd.new_numbered_point_item(text='First item')
        mfd.new_numbered_point_item(text='Second item')

    expected = (PF_EN_NT_NC + '<h1>\nMain Title</h1>\n' +
                '<ol>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_mixed_bullet_and_numbered_lists(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test switching between bullet and numbered point lists."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='Bullet 1', level=1)
        mfd.new_bullet_item(text='Bullet 2', level=1)
        mfd.new_numbered_point_item(text='Numbered 1', level=1)
        mfd.new_numbered_point_item(text='Numbered 2', level=1)

    expected = (PF_EN_NT_NC + '<ul>\n<li>Bullet 1</li>\n<li>Bullet 2</li>\n'
                '</ul>\n<ol>\n<li>Numbered 1</li>\n<li>Numbered 2</li>\n'
                '</ol>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_nested_mixed_lists(capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested mixed bullet and numbered point lists."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_bullet_item(text='Bullet 1', level=1)
        mfd.new_numbered_point_item(text='Numbered 1.1', level=2)
        mfd.new_numbered_point_item(text='Numbered 1.2', level=2)
        mfd.new_bullet_item(text='Bullet 2', level=1)

    expected = (PF_EN_NT_NC + '<ul>\n<li>Bullet 1</li>\n' +
                '<ol>\n<li>Numbered 1.1</li>\n<li>Numbered 1.2</li>\n' +
                '</ol>\n<li>Bullet 2</li>\n</ul>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_single_numbered_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single numbered point item."""
    def test_action(mfd) -> None:
        assert isinstance(mfd, MultiFormatHtml)
        mfd.new_numbered_point_item(text='First item')

    expected = PF_EN_NT_NC + '<ol>\n<li>First item</li>\n</ol>\n' + SFTOT
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)
