#! /usr/local/bin/python3
"""Test the mformat_rst module list functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from rst_test_helpers import check_rst_output


def test_single_bullet_item(capsys):
    """Test a single bullet list item."""
    check_rst_output(
        capsys=capsys,
        method_calls=[('new_bullet_item', {'text': 'First item'})],
        expected_text='* First item\n')


def test_multiple_bullet_items(capsys):
    """Test multiple bullet list items."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_bullet_item', {'text': 'First'}),
            ('new_bullet_item', {'text': 'Second'}),
            ('new_bullet_item', {'text': 'Third'}),
        ],
        expected_text='* First\n* Second\n* Third\n')


def test_nested_bullet_items(capsys):
    """Test nested bullet list items."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_bullet_item', {'text': 'Level 1', 'level': 1}),
            ('new_bullet_item', {'text': 'Level 2', 'level': 2}),
            ('new_bullet_item', {'text': 'Level 3', 'level': 3}),
        ],
        expected_text='* Level 1\n\n   * Level 2\n\n      * Level 3\n\n')


def test_bullet_list_back_to_level1(capsys):
    """Test nested bullet list returning to level 1."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_bullet_item', {'text': 'Level 1 first', 'level': 1}),
            ('new_bullet_item', {'text': 'Level 2', 'level': 2}),
            ('new_bullet_item', {'text': 'Level 1 second', 'level': 1}),
        ],
        expected_text='* Level 1 first\n\n   * Level 2\n\n* Level 1 second\n')


def test_bullet_item_with_url_and_code(capsys):
    """Test adding URL and code inside bullet item."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_bullet_item', {'text': 'Check'}),
            ('add_url', {'url': 'http://example.com', 'text': 'this link'}),
            ('new_bullet_item', {'text': 'Use'}),
            ('add_code_in_text', {'text': 'cmd()'}),
        ],
        expected_text='* Check `this link <http://example.com>`_\n'
                      '* Use ``cmd()``\n')


def test_single_numbered_item(capsys):
    """Test a single numbered list item."""
    check_rst_output(
        capsys=capsys,
        method_calls=[('new_numbered_point_item', {'text': 'First item'})],
        expected_text='1. First item\n')


def test_multiple_numbered_items(capsys):
    """Test multiple numbered list items."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_numbered_point_item', {'text': 'First'}),
            ('new_numbered_point_item', {'text': 'Second'}),
            ('new_numbered_point_item', {'text': 'Third'}),
        ],
        expected_text='1. First\n2. Second\n3. Third\n')


def test_nested_numbered_items(capsys):
    """Test nested numbered list items."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_numbered_point_item', {'text': 'Level 1', 'level': 1}),
            ('new_numbered_point_item', {'text': 'Level 2', 'level': 2}),
            ('new_numbered_point_item', {'text': 'Level 3', 'level': 3}),
        ],
        expected_text='1. Level 1\n\n   1. Level 2\n\n      1. Level 3\n\n')


def test_numbered_list_back_to_level1(capsys):
    """Test nested numbered list returning to level 1."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_numbered_point_item', {'text': 'Level 1 first', 'level': 1}),
            ('new_numbered_point_item', {'text': 'Level 2', 'level': 2}),
            ('new_numbered_point_item',
             {'text': 'Level 1 second', 'level': 1}),
        ],
        expected_text='1. Level 1 first\n\n   1. Level 2\n\n2. Level 1 '
                      'second\n')


def test_heading_then_list(capsys):
    """Test heading followed by a list item."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_heading', {'level': 1, 'text': 'Title'}),
            ('new_bullet_item', {'text': 'Item'}),
        ],
        expected_text='Title\n=====\n\n* Item\n')


def test_paragraph_then_numbered_list(capsys):
    """Test paragraph followed by numbered list item."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': 'Intro'}),
            ('new_numbered_point_item', {'text': 'Item'}),
        ],
        expected_text='Intro\n\n1. Item\n')


def test_mixed_bullet_and_numbered_lists(capsys):
    """Test mixing bullet and numbered lists."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_bullet_item', {'text': 'Bullet 1'}),
            ('new_numbered_point_item', {'text': 'Number 1'}),
            ('new_bullet_item', {'text': 'Bullet 2'}),
        ],
        expected_text='* Bullet 1\n\n1. Number 1\n\n* Bullet 2\n')
