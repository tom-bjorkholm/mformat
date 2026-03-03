#! /usr/local/bin/python3
"""Test the mformat_txt module list functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from .test_helpers import check_run_with_context_manager


def test_single_bullet_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single bullet list item."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_bullet_item(text='First item')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text='- First item\n',
                                   capsys=capsys)


def test_multiple_bullet_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple bullet list items."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_bullet_item(text='First')
        mfd.new_bullet_item(text='Second')
        mfd.new_bullet_item(text='Third')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=('- First\n'
                                                  '- Second\n'
                                                  '- Third\n'),
                                   capsys=capsys)


def test_nested_bullet_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested bullet list items."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_bullet_item(text='Level 1', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)
        mfd.new_bullet_item(text='Level 3', level=3)

    expected = '- Level 1\n  - Level 2\n    - Level 3\n'
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_bullet_item_with_url_and_code(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test adding URL and code inside bullet item."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_bullet_item(text='Check')
        mfd.add_url(url='http://example.com', text='this link')
        mfd.new_bullet_item(text='Use')
        mfd.add_code_in_text(text='cmd()')

    expected = ('- Check this link http://example.com\n'
                '- Use cmd()\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_single_numbered_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test a single numbered list item."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_numbered_point_item(text='First item')

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text='1. First item\n',
                                   capsys=capsys)


def test_multiple_numbered_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test multiple numbered list items."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_numbered_point_item(text='First')
        mfd.new_numbered_point_item(text='Second')
        mfd.new_numbered_point_item(text='Third')

    expected = '1. First\n2. Second\n3. Third\n'
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_nested_numbered_items(capsys: pytest.CaptureFixture[str]) -> None:
    """Test nested numbered list items."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_numbered_point_item(text='Level 1', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)
        mfd.new_numbered_point_item(text='Level 3', level=3)

    expected = ('1. Level 1\n'
                '  1.1. Level 2\n'
                '    1.1.1. Level 3\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_list(capsys: pytest.CaptureFixture[str]) -> None:
    """Test heading followed by a list item."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_heading(level=1, text='Title')
        mfd.new_bullet_item(text='Item')

    expected = 'Title\n*****\n\n- Item\n'
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_numbered_list(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph followed by numbered list item."""
    def test_action(mfd) -> None:
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text='Intro')
        mfd.new_numbered_point_item(text='Item')

    expected = 'Intro\n1. Item\n'
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)
