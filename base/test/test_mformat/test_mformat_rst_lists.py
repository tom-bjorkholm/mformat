#! /usr/local/bin/python3
"""Test the mformat_rst module list functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#
# pylint: disable=duplicate-code

from test_helpers import check_run_with_context_manager


def test_single_bullet_item(capsys):
    """Test a single bullet list item."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_bullet_item(text='First item')

    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text='* First item\n',
                                   capsys=capsys)


def test_multiple_bullet_items(capsys):
    """Test multiple bullet list items."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_bullet_item(text='First')
        mfd.new_bullet_item(text='Second')
        mfd.new_bullet_item(text='Third')

    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=('* First\n'
                                                  '* Second\n'
                                                  '* Third\n'),
                                   capsys=capsys)


def test_nested_bullet_items(capsys):
    """Test nested bullet list items."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_bullet_item(text='Level 1', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)
        mfd.new_bullet_item(text='Level 3', level=3)

    expected = ('* Level 1\n'
                '\n'
                '   * Level 2\n'
                '\n'
                '      * Level 3\n'
                '\n')
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_bullet_list_back_to_level1(capsys):
    """Test nested bullet list returning to level 1."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_bullet_item(text='Level 1 first', level=1)
        mfd.new_bullet_item(text='Level 2', level=2)
        mfd.new_bullet_item(text='Level 1 second', level=1)

    expected = ('* Level 1 first\n'
                '\n'
                '   * Level 2\n'
                '\n'
                '* Level 1 second\n')
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_bullet_item_with_url_and_code(capsys):
    """Test adding URL and code inside bullet item."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_bullet_item(text='Check')
        mfd.add_url(url='http://example.com', text='this link')
        mfd.new_bullet_item(text='Use')
        mfd.add_code_in_text(text='cmd()')

    expected = ('* Check `this link <http://example.com>`_\n'
                '* Use ``cmd()``\n')
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_single_numbered_item(capsys):
    """Test a single numbered list item."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_numbered_point_item(text='First item')

    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text='1. First item\n',
                                   capsys=capsys)


def test_multiple_numbered_items(capsys):
    """Test multiple numbered list items."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_numbered_point_item(text='First')
        mfd.new_numbered_point_item(text='Second')
        mfd.new_numbered_point_item(text='Third')

    expected = '1. First\n2. Second\n3. Third\n'
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_nested_numbered_items(capsys):
    """Test nested numbered list items."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_numbered_point_item(text='Level 1', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)
        mfd.new_numbered_point_item(text='Level 3', level=3)

    expected = ('1. Level 1\n'
                '\n'
                '   1. Level 2\n'
                '\n'
                '      1. Level 3\n'
                '\n')
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_numbered_list_back_to_level1(capsys):
    """Test nested numbered list returning to level 1."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_numbered_point_item(text='Level 1 first', level=1)
        mfd.new_numbered_point_item(text='Level 2', level=2)
        mfd.new_numbered_point_item(text='Level 1 second', level=1)

    expected = ('1. Level 1 first\n'
                '\n'
                '   1. Level 2\n'
                '\n'
                '2. Level 1 second\n')
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_list(capsys):
    """Test heading followed by a list item."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_heading(level=1, text='Title')
        mfd.new_bullet_item(text='Item')

    expected = 'Title\n=====\n\n* Item\n'
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_numbered_list(capsys):
    """Test paragraph followed by numbered list item."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_paragraph(text='Intro')
        mfd.new_numbered_point_item(text='Item')

    expected = 'Intro\n\n1. Item\n'
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_mixed_bullet_and_numbered_lists(capsys):
    """Test mixing bullet and numbered lists."""

    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatRst'
        mfd.new_bullet_item(text='Bullet 1')
        mfd.new_numbered_point_item(text='Number 1')
        mfd.new_bullet_item(text='Bullet 2')

    expected = ('* Bullet 1\n'
                '\n'
                '1. Number 1\n'
                '\n'
                '* Bullet 2\n')
    check_run_with_context_manager('reST', '.rst', test_action,
                                   expected_text=expected,
                                   capsys=capsys)
