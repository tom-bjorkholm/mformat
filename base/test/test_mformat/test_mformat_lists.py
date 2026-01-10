#! /usr/local/bin/python3
"""Test bullet list and numbered list functionality in the mformat module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from test_helpers import MultiFormat10
from mformat.mformat_state import MultiFormatState


def test_start_bullet_item_from_empty(capsys):
    """Test starting a bullet item from empty state."""
    mfmt = MultiFormat10(file_name='test')
    assert mfmt.state == MultiFormatState.EMPTY
    mfmt.start_bullet_item(text='First item')
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 1,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 1,
        '_write_text': 1}
    check_capsys(capsys)


def test_start_multiple_bullet_items(capsys):
    """Test starting multiple bullet items at same level."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='First item')
    mfmt.start_bullet_item(text='Second item')
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 2,
        '_end_bullet_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_start_bullet_item_nested(capsys):
    """Test starting nested bullet items."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Level 1 item', level=1)
    mfmt.start_bullet_item(text='Level 2 item', level=2)
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert len(mfmt.point_list_stack) == 2
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_bullet_list': 2,
        '_start_bullet_item': 2,
        '_end_bullet_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_start_bullet_item_nested_then_back_to_level1(capsys):
    """Test nested bullet items then returning to level 1."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Level 1 item', level=1)
    mfmt.start_bullet_item(text='Level 2 item', level=2)
    mfmt.start_bullet_item(text='Back to level 1', level=1)
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 3,
        '_write_file_prefix': 1,
        '_start_bullet_list': 2,
        '_start_bullet_item': 3,
        '_end_bullet_item': 2,
        '_end_bullet_list': 1,
        '_write_text': 3}
    check_capsys(capsys)


def test_bullet_item_with_add_text(capsys):
    """Test adding text to a bullet item."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='First item')
    mfmt.add_text(text=' more text')
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_bullet_item_with_add_url(capsys):
    """Test adding URL to a bullet item."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='First item')
    mfmt.add_url(url='http://example.com', text='link')
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 1,
        '_write_text': 2,
        '_write_url': 1}
    check_capsys(capsys)


def test_bullet_list_error_skip_level(capsys):
    """Test error when skipping a level in bullet list."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Level 1 item', level=1)
    with pytest.raises(RuntimeError) as exc:
        mfmt.start_bullet_item(text='Level 3 item', level=3)
    assert 'start_bullet_item called with level=3' in exc.value.args[0]
    assert 'but level 2 does not exist' in exc.value.args[0]
    check_capsys(capsys)


def test_bullet_list_three_levels(capsys):
    """Test bullet list with three levels."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Level 1', level=1)
    mfmt.start_bullet_item(text='Level 2', level=2)
    mfmt.start_bullet_item(text='Level 3', level=3)
    assert len(mfmt.point_list_stack) == 3
    assert mfmt.count == {
        '_encode_text': 3,
        '_write_file_prefix': 1,
        '_start_bullet_list': 3,
        '_start_bullet_item': 3,
        '_end_bullet_item': 2,
        '_write_text': 3}
    check_capsys(capsys)


def test_bullet_list_three_levels_back_to_one(capsys):
    """Test bullet list with three levels then back to level 1."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Level 1', level=1)
    mfmt.start_bullet_item(text='Level 2', level=2)
    mfmt.start_bullet_item(text='Level 3', level=3)
    mfmt.start_bullet_item(text='Back to 1', level=1)
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 4,
        '_write_file_prefix': 1,
        '_start_bullet_list': 3,
        '_start_bullet_item': 4,
        '_end_bullet_item': 3,
        '_end_bullet_list': 2,
        '_write_text': 4}
    check_capsys(capsys)


def test_bullet_list_smart_ws(capsys):
    """Test bullet list with smart_ws parameter."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='  First  ', smart_ws=True)
    assert mfmt.ws_needed_at_append is True
    mfmt.add_text(text='  more  ', smart_ws=True)
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_bullet_list_bold_italic(capsys):
    """Test bullet list with bold and italic text."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Bold', bold=True)
    mfmt.start_bullet_item(text='Italic', italic=True)
    mfmt.start_bullet_item(text='Both', bold=True, italic=True)
    assert mfmt.count == {
        '_encode_text': 3,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 3,
        '_end_bullet_item': 2,
        '_write_text': 3}
    check_capsys(capsys)


def test_paragraph_then_bullet_list(capsys):
    """Test paragraph followed by bullet list."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_paragraph(text='Paragraph')
    mfmt.start_bullet_item(text='Bullet item')
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_paragraph': 1,
        '_end_paragraph': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_bullet_list_then_paragraph(capsys):
    """Test bullet list followed by paragraph."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Bullet item')
    mfmt.start_paragraph(text='Paragraph')
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 1,
        '_end_bullet_item': 1,
        '_end_bullet_list': 1,
        '_start_paragraph': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_heading_then_bullet_list(capsys):
    """Test heading followed by bullet list."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_heading(level=1, text='Heading')
    mfmt.start_bullet_item(text='Bullet item')
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_heading': 1,
        '_end_heading': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


# Tests for numbered point lists


def test_start_numbered_item_from_empty(capsys):
    """Test starting a numbered point item from empty state."""
    mfmt = MultiFormat10(file_name='test')
    assert mfmt.state == MultiFormatState.EMPTY
    mfmt.start_numbered_point_item(text='First item')
    assert mfmt.state == MultiFormatState.NUMBERED_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 1,
        '_write_file_prefix': 1,
        '_start_numbered_list': 1,
        '_start_numbered_item': 1,
        '_write_text': 1}
    check_capsys(capsys)


def test_start_multiple_numbered_items(capsys):
    """Test starting multiple numbered point items at same level."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_numbered_point_item(text='First item')
    mfmt.start_numbered_point_item(text='Second item')
    assert mfmt.state == MultiFormatState.NUMBERED_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_numbered_list': 1,
        '_start_numbered_item': 2,
        '_end_numbered_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_start_numbered_item_nested(capsys):
    """Test starting nested numbered point items."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_numbered_point_item(text='Level 1 item', level=1)
    mfmt.start_numbered_point_item(text='Level 2 item', level=2)
    assert mfmt.state == MultiFormatState.NUMBERED_LIST_ITEM
    assert len(mfmt.point_list_stack) == 2
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_numbered_list': 2,
        '_start_numbered_item': 2,
        '_end_numbered_item': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_numbered_list_back_to_level1(capsys):
    """Test numbered point list returning to level 1."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_numbered_point_item(text='Level 1 first', level=1)
    mfmt.start_numbered_point_item(text='Level 2', level=2)
    mfmt.start_numbered_point_item(text='Level 1 second', level=1)
    assert mfmt.state == MultiFormatState.NUMBERED_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 3,
        '_write_file_prefix': 1,
        '_start_numbered_list': 2,
        '_start_numbered_item': 3,
        '_end_numbered_item': 2,
        '_end_numbered_list': 1,
        '_write_text': 3}
    check_capsys(capsys)


def test_numbered_then_paragraph(capsys):
    """Test numbered point list followed by paragraph."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_numbered_point_item(text='Numbered item')
    mfmt.start_paragraph(text='Paragraph')
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_numbered_list': 1,
        '_start_numbered_item': 1,
        '_end_numbered_item': 1,
        '_end_numbered_list': 1,
        '_start_paragraph': 1,
        '_write_text': 2}
    check_capsys(capsys)


def test_mixed_bullet_and_numbered_same_level(capsys):
    """Test switching between bullet and numbered at same level."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Bullet 1', level=1)
    mfmt.start_bullet_item(text='Bullet 2', level=1)
    mfmt.start_numbered_point_item(text='Numbered 1', level=1)
    mfmt.start_numbered_point_item(text='Numbered 2', level=1)
    assert mfmt.state == MultiFormatState.NUMBERED_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 4,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 2,
        '_end_bullet_item': 2,
        '_end_bullet_list': 1,
        '_start_numbered_list': 1,
        '_start_numbered_item': 2,
        '_end_numbered_item': 1,
        '_write_text': 4}
    check_capsys(capsys)


def test_nested_mixed_bullet_then_numbered(capsys):
    """Test nested list with bullet at level 1 and numbered at level 2."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_bullet_item(text='Bullet 1', level=1)
    mfmt.start_numbered_point_item(text='Numbered 1.1', level=2)
    mfmt.start_numbered_point_item(text='Numbered 1.2', level=2)
    mfmt.start_bullet_item(text='Bullet 2', level=1)
    assert mfmt.state == MultiFormatState.BULLET_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 4,
        '_write_file_prefix': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 2,
        '_end_bullet_item': 1,
        '_start_numbered_list': 1,
        '_start_numbered_item': 2,
        '_end_numbered_item': 2,
        '_end_numbered_list': 1,
        '_write_text': 4}
    check_capsys(capsys)


def test_nested_mixed_numbered_then_bullet(capsys):
    """Test nested list with numbered at level 1 and bullet at level 2."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_numbered_point_item(text='Numbered 1', level=1)
    mfmt.start_bullet_item(text='Bullet 1.1', level=2)
    mfmt.start_bullet_item(text='Bullet 1.2', level=2)
    mfmt.start_numbered_point_item(text='Numbered 2', level=1)
    assert mfmt.state == MultiFormatState.NUMBERED_LIST_ITEM
    assert len(mfmt.point_list_stack) == 1
    assert mfmt.count == {
        '_encode_text': 4,
        '_write_file_prefix': 1,
        '_start_numbered_list': 1,
        '_start_numbered_item': 2,
        '_end_numbered_item': 1,
        '_start_bullet_list': 1,
        '_start_bullet_item': 2,
        '_end_bullet_item': 2,
        '_end_bullet_list': 1,
        '_write_text': 4}
    check_capsys(capsys)


def test_three_level_nested_numbered(capsys):
    """Test three-level nested numbered point lists."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_numbered_point_item(text='Level 1', level=1)
    mfmt.start_numbered_point_item(text='Level 2', level=2)
    mfmt.start_numbered_point_item(text='Level 3', level=3)
    assert mfmt.state == MultiFormatState.NUMBERED_LIST_ITEM
    assert len(mfmt.point_list_stack) == 3
    assert mfmt.count == {
        '_encode_text': 3,
        '_write_file_prefix': 1,
        '_start_numbered_list': 3,
        '_start_numbered_item': 3,
        '_end_numbered_item': 2,
        '_write_text': 3}
    check_capsys(capsys)


def test_numbered_list_error_skip_level(capsys):
    """Test error when skipping a level in numbered point list."""
    mfmt = MultiFormat10(file_name='test')
    mfmt.start_numbered_point_item(text='Level 1', level=1)
    with pytest.raises(RuntimeError,
                       match='start_numbered_item called with level=3'):
        mfmt.start_numbered_point_item(text='Level 3', level=3)
    check_capsys(capsys)
