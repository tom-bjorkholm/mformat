#! /usr/local/bin/python3
"""Test the ListHandlerMixin class specifically the list state handling."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from test_mformat_lists_impl import ListHandler2
from check_capsys import check_capsys
from mformat.mformat_state import MultiFormatState
from mformat.mformat_lists_impl import (
    PointStackItem, PointListType)


@pytest.mark.parametrize('state,stack,exp_state,exp_calls',
                         [(MultiFormatState.BULLET_LIST_ITEM, [],
                           MultiFormatState.BULLET_LIST_ITEM, []),
                          (MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET],
                           MultiFormatState.BULLET_LIST, []),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           [PointListType.NUMBERED, PointListType.BULLET],
                           MultiFormatState.BULLET_LIST, ['_end_bullet_item']),
                          (MultiFormatState.NUMBERED_LIST_ITEM,
                           [PointListType.BULLET, PointListType.NUMBERED],
                           MultiFormatState.NUMBERED_LIST,
                           ['_end_numbered_item'])])
def test_end_item_before_nesting(capsys, state, stack,
                                 exp_state, exp_calls) -> None:
    """Test the end_item_before_nesting method."""
    list_handler = ListHandler2()
    for item in stack:
        stack_item = PointStackItem(point_list_type=item,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    list_handler.state = state
    list_handler._end_item_before_nesting()  # pylint: disable=protected-access # noqa: E501
    assert list_handler.state == exp_state
    assert list_handler.call_list == exp_calls
    check_capsys(capsys)
