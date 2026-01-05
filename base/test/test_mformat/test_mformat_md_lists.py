#! /usr/local/bin/python3
"""Test the mformat_md module lists functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from test_helpers import (
    check_run_with_context_manager,
    action_complex_nested_bullet_structure
)


def test_single_bullet_item(capsys):
    """Test a single bullet item."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='First item')

    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text='- First item\n',
                                   capsys=capsys)


def test_multiple_bullet_items(capsys):
    """Test multiple bullet items."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_bullet_item(text='Third item')

    expected = '- First item\n- Second item\n- Third item\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_bullet_item_with_url(capsys):
    """Test bullet item with URL."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    expected = '- Check [this link](http://example.com)\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_nested_bullet_items_level2(capsys):
    """Test nested bullet items at level 2."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)

    expected = '- Level 1\n  - Level 2\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_nested_bullet_items_level3(capsys):
    """Test nested bullet items at level 3."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 3', level=3)

    expected = '- Level 1\n  - Level 2\n    - Level 3\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_bullet_list_back_to_level1(capsys):
    """Test bullet list returning to level 1."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Level 1 first', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 1 second', level=1)

    expected = ('- Level 1 first\n  - Level 2\n'
                '- Level 1 second\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_bullet_list_formatting(capsys):
    """Test bullet list with bold and italic."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Bold item', bold=True)
        mfd.start_bullet_item(text='Italic item', italic=True)
        mfd.start_bullet_item(text='Both', bold=True, italic=True)

    expected = ('- **Bold item**\n- *Italic item*\n'
                '- ***Both***\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_bullet_list(capsys):
    """Test paragraph followed by bullet list."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph(text='Intro paragraph')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    expected = '\nIntro paragraph\n- First item\n- Second item\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_bullet_list_then_paragraph(capsys):
    """Test bullet list followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_paragraph(text='Concluding paragraph')

    expected = '- First item\n- Second item\n\nConcluding paragraph\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_bullet_list(capsys):
    """Test heading followed by bullet list."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=1, text='Main Title')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    # pylint: disable=duplicate-code
    expected = '# Main Title\n- First item\n- Second item\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_complex_nested_structure(capsys):
    """Test complex nested bullet structure."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        action_complex_nested_bullet_structure(mfd)

    expected = ('- Item 1\n  - Item 1.1\n  - Item 1.2\n'
                '- Item 2\n  - Item 2.1\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


# Tests for numbered point lists


def test_single_numbered_item(capsys):
    """Test a single numbered point item."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='First item')

    expected = '1. First item\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_multiple_numbered_items(capsys):
    """Test multiple numbered point items."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')
        mfd.start_numbered_point_item(text='Third item')

    expected = '1. First item\n2. Second item\n3. Third item\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_numbered_item_with_add_text(capsys):
    """Test numbered point item with additional text."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='First item')
        mfd.add_text(text=' with more text')

    expected = '1. First item with more text\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_numbered_item_with_url(capsys):
    """Test numbered point item with URL."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    expected = '1. Check [this link](http://example.com)\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_nested_numbered_items_level2(capsys):
    """Test nested numbered point items at level 2."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='Level 1', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)

    expected = '1. Level 1\n  1. Level 2\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_nested_numbered_items_level3(capsys):
    """Test nested numbered point items at level 3."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='Level 1', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)
        mfd.start_numbered_point_item(text='Level 3', level=3)

    expected = '1. Level 1\n  1. Level 2\n    1. Level 3\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_numbered_list_back_to_level1(capsys):
    """Test numbered point list returning to level 1."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='Level 1 first', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)
        mfd.start_numbered_point_item(text='Level 1 second', level=1)

    expected = ('1. Level 1 first\n  1. Level 2\n'
                '2. Level 1 second\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_numbered_list_formatting(capsys):
    """Test numbered point list with bold and italic."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='Bold item', bold=True)
        mfd.start_numbered_point_item(text='Italic item', italic=True)
        mfd.start_numbered_point_item(text='Both', bold=True, italic=True)

    expected = ('1. **Bold item**\n2. *Italic item*\n'
                '3. ***Both***\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_numbered_list(capsys):
    """Test paragraph followed by numbered point list."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph(text='Intro paragraph')
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')

    expected = '\nIntro paragraph\n1. First item\n2. Second item\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_numbered_list_then_paragraph(capsys):
    """Test numbered point list followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')
        mfd.start_paragraph(text='Concluding paragraph')

    expected = '1. First item\n2. Second item\n\nConcluding paragraph\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_numbered_list(capsys):
    """Test heading followed by numbered point list."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=1, text='Main Title')
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')

    # pylint: disable=duplicate-code
    expected = '# Main Title\n1. First item\n2. Second item\n'
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_mixed_bullet_and_numbered_lists(capsys):
    """Test switching between bullet and numbered point lists."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Bullet 1', level=1)
        mfd.start_bullet_item(text='Bullet 2', level=1)
        mfd.start_numbered_point_item(text='Numbered 1', level=1)
        mfd.start_numbered_point_item(text='Numbered 2', level=1)

    expected = ('- Bullet 1\n- Bullet 2\n'
                '1. Numbered 1\n2. Numbered 2\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_nested_mixed_lists(capsys):
    """Test nested mixed bullet and numbered point lists."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Bullet 1', level=1)
        mfd.start_numbered_point_item(text='Numbered 1.1', level=2)
        mfd.start_numbered_point_item(text='Numbered 1.2', level=2)
        mfd.start_bullet_item(text='Bullet 2', level=1)

    expected = ('- Bullet 1\n  1. Numbered 1.1\n  2. Numbered 1.2\n'
                '- Bullet 2\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)
