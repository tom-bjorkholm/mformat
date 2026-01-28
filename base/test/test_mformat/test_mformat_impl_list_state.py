#! /usr/local/bin/python3
"""Test the ListHandlerMixin class specifically the list state handling."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import NamedTuple
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


class ExpectedResult(NamedTuple):
    """Expected result of a test."""

    state: MultiFormatState
    calls: list[str]
    stack: list[PointListType]
    number_at_top_level: int


def check_expected_result(list_handler: ListHandler2,
                          exp: ExpectedResult) -> None:
    """Check the expected result."""
    assert list_handler.state == exp.state
    assert list_handler.call_list == exp.calls
    assert len(list_handler.point_list_stack) == len(exp.stack)
    if list_handler.point_list_stack:
        assert list_handler.point_list_stack[-1]['number_at_level'] == \
            exp.number_at_top_level
    for stack_item, exp_pltype in zip(list_handler.point_list_stack,
                                      exp.stack):
        assert stack_item['point_list_type'] == exp_pltype


@pytest.mark.parametrize('state,stack,lev,pltype,exp',
                         [(MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET], 1,
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=[],
                                          stack=[PointListType.BULLET],
                                          number_at_top_level=1)),
                          (MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET], 2,
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=['_start_bullet_list'],
                                          stack=[PointListType.BULLET,
                                                 PointListType.BULLET],
                                          number_at_top_level=0)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.NUMBERED, PointListType.BULLET,
                            PointListType.BULLET], 4,
                           PointListType.NUMBERED,
                           ExpectedResult(
                                state=MultiFormatState.NUMBERED_LIST,
                                calls=['_start_numbered_list'],
                                stack=[PointListType.NUMBERED,
                                       PointListType.BULLET,
                                       PointListType.BULLET,
                                       PointListType.NUMBERED],
                                number_at_top_level=0))])
def test_increase_list_depth(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             state, stack, lev, pltype, exp) -> None:
    """Test the _increase_list_depth method."""
    list_handler = ListHandler2(state=state)
    for item in stack:
        stack_item = PointStackItem(point_list_type=item,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    list_handler._increase_list_depth(target_level=lev,  # pylint: disable=protected-access # noqa: E501
                                      point_list_type=pltype)
    check_expected_result(list_handler, exp)
    check_capsys(capsys)


def test_increase_list_depth_nok(capsys) -> None:
    """Test the _increase_list_depth method with a not ok state."""
    list_handler = ListHandler2(state=MultiFormatState.BULLET_LIST)
    with pytest.raises(AssertionError):
        list_handler._increase_list_depth(target_level=2,  # pylint: disable=protected-access # noqa: E501
                                          point_list_type=PointListType.BULLET)
    check_capsys(capsys)


@pytest.mark.parametrize('state,stack,lev,pltype,exp',
                         [(MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET], 1,
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=[],
                                          stack=[PointListType.BULLET],
                                          number_at_top_level=1)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.NUMBERED], 1,
                           PointListType.NUMBERED,
                           ExpectedResult(state=MultiFormatState.NUMBERED_LIST,
                                          calls=[],
                                          stack=[PointListType.NUMBERED],
                                          number_at_top_level=1)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.NUMBERED], 1,
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.PARAGRAPH_END,
                                          calls=['_end_numbered_list'],
                                          stack=[],
                                          number_at_top_level=0)),
                          (MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET], 1,
                           PointListType.NUMBERED,
                           ExpectedResult(state=MultiFormatState.PARAGRAPH_END,
                                          calls=['_end_bullet_list'],
                                          stack=[],
                                          number_at_top_level=0)),
                          (MultiFormatState.NUMBERED_LIST_ITEM,
                           [PointListType.NUMBERED], 1,
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.PARAGRAPH_END,
                                          calls=['_end_numbered_item',
                                                 '_end_numbered_list'],
                                          stack=[],
                                          number_at_top_level=0)),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           [PointListType.BULLET], 1,
                           PointListType.NUMBERED,
                           ExpectedResult(state=MultiFormatState.PARAGRAPH_END,
                                          calls=['_end_bullet_item',
                                                 '_end_bullet_list'],
                                          stack=[],
                                          number_at_top_level=0)),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           [PointListType.BULLET, PointListType.BULLET], 2,
                           PointListType.NUMBERED,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=['_end_bullet_item',
                                                 '_end_bullet_list'],
                                          stack=[PointListType.BULLET],
                                          number_at_top_level=1)),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           [PointListType.BULLET, PointListType.BULLET], 1,
                           PointListType.NUMBERED,
                           ExpectedResult(
                               state=MultiFormatState.BULLET_LIST_ITEM,
                               calls=[],
                               stack=[PointListType.BULLET,
                                      PointListType.BULLET],
                               number_at_top_level=1))])
def test_end_wrong_list_type(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             state, stack, lev, pltype, exp) -> None:
    """Test the _end_wrong_list_type_at_lev method."""
    list_handler = ListHandler2(state=state)
    for item in stack:
        stack_item = PointStackItem(point_list_type=item,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    list_handler._end_wrong_list_type_at_lev(target_level=lev,  # pylint: disable=protected-access # noqa: E501
                                             point_list_type=pltype)
    check_expected_result(list_handler, exp)
    check_capsys(capsys)


@pytest.mark.parametrize('state,stack,lev,exp',
                         [(MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET], 1,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=[],
                                          stack=[PointListType.BULLET],
                                          number_at_top_level=1)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.NUMBERED], 1,
                           ExpectedResult(state=MultiFormatState.NUMBERED_LIST,
                                          calls=[],
                                          stack=[PointListType.NUMBERED],
                                          number_at_top_level=1)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.NUMBERED,
                            PointListType.BULLET,
                            PointListType.NUMBERED], 1,
                           ExpectedResult(state=MultiFormatState.NUMBERED_LIST,
                                          calls=['_end_numbered_list',
                                                 '_end_bullet_list'],
                                          stack=[PointListType.NUMBERED],
                                          number_at_top_level=1)),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           [PointListType.BULLET,
                            PointListType.NUMBERED,
                            PointListType.BULLET], 1,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=['_end_bullet_item',
                                                 '_end_bullet_list',
                                                 '_end_numbered_list'],
                                          stack=[PointListType.BULLET],
                                          number_at_top_level=1))])
def test_decrease_list_depth(capsys, state, stack, lev, exp) -> None:
    """Test the _decrease_list_depth method."""
    list_handler = ListHandler2(state=state)
    for item in stack:
        stack_item = PointStackItem(point_list_type=item,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    list_handler._decrease_list_depth(target_level=lev)  # pylint: disable=protected-access # noqa: E501
    check_expected_result(list_handler, exp)
    check_capsys(capsys)


@pytest.mark.parametrize('state,stack,exp',
                         [(MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET],
                           ExpectedResult(
                               state=MultiFormatState.BULLET_LIST_ITEM,
                               calls=['_start_bullet_item'],
                               stack=[PointListType.BULLET],
                               number_at_top_level=2)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.NUMBERED],
                           ExpectedResult(
                               state=MultiFormatState.NUMBERED_LIST_ITEM,
                               calls=['_start_numbered_item'],
                               stack=[PointListType.NUMBERED],
                               number_at_top_level=2)),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           [PointListType.BULLET],
                           ExpectedResult(
                               state=MultiFormatState.BULLET_LIST_ITEM,
                               calls=['_end_bullet_item',
                                      '_start_bullet_item'],
                               stack=[PointListType.BULLET],
                               number_at_top_level=2)),
                          (MultiFormatState.NUMBERED_LIST_ITEM,
                           [PointListType.NUMBERED],
                           ExpectedResult(
                               state=MultiFormatState.NUMBERED_LIST_ITEM,
                               calls=['_end_numbered_item',
                                      '_start_numbered_item'],
                               stack=[PointListType.NUMBERED],
                               number_at_top_level=2))])
def test_start_item_in_list(capsys, state, stack, exp) -> None:
    """Test the _start_item_in_list method."""
    list_handler = ListHandler2(state=state)
    for item in stack:
        stack_item = PointStackItem(point_list_type=item,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    list_handler._start_item_in_list(point_list_type=stack[-1])  # pylint: disable=protected-access # noqa: E501
    check_expected_result(list_handler, exp)
    check_capsys(capsys)


@pytest.mark.parametrize('state,stack,pltype,exp',
                         [(MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET],
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=['_start_bullet_list'],
                                          stack=[PointListType.BULLET,
                                                 PointListType.BULLET],
                                          number_at_top_level=0)),
                          (MultiFormatState.PARAGRAPH_END,
                           [],
                           PointListType.NUMBERED,
                           ExpectedResult(state=MultiFormatState.NUMBERED_LIST,
                                          calls=['_start_numbered_list'],
                                          stack=[PointListType.NUMBERED],
                                          number_at_top_level=0)),
                          (MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET],
                           PointListType.NUMBERED,
                           ExpectedResult(state=MultiFormatState.NUMBERED_LIST,
                                          calls=['_start_numbered_list'],
                                          stack=[PointListType.BULLET,
                                                 PointListType.NUMBERED],
                                          number_at_top_level=0)),])
def test_push_and_start_list(capsys, state, stack, pltype, exp) -> None:
    """Test the _push_and_start_list method."""
    list_handler = ListHandler2(state=state)
    for item in stack:
        stack_item = PointStackItem(point_list_type=item,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    list_handler._push_and_start_list(point_list_type=pltype)  # pylint: disable=protected-access # noqa: E501
    check_expected_result(list_handler, exp)
    check_capsys(capsys)


@pytest.mark.parametrize('state,stack,lev,pltype,exp',
                         [(MultiFormatState.BULLET_LIST,
                           [PointListType.BULLET], 1,
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=[],
                                          stack=[PointListType.BULLET],
                                          number_at_top_level=1)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.NUMBERED, PointListType.BULLET,
                            PointListType.NUMBERED], 1,
                           PointListType.BULLET,
                           ExpectedResult(state=MultiFormatState.BULLET_LIST,
                                          calls=['_end_numbered_list',
                                                 '_end_bullet_list',
                                                 '_end_numbered_list',
                                                 '_start_bullet_list'],
                                          stack=[PointListType.BULLET],
                                          number_at_top_level=0)),
                          (MultiFormatState.NUMBERED_LIST,
                           [PointListType.BULLET, PointListType.BULLET,
                            PointListType.NUMBERED], 1,
                           PointListType.NUMBERED,
                           ExpectedResult(state=MultiFormatState.NUMBERED_LIST,
                                          calls=['_end_numbered_list',
                                                 '_end_bullet_list',
                                                 '_end_bullet_list',
                                                 '_start_numbered_list'],
                                          stack=[PointListType.NUMBERED],
                                          number_at_top_level=0))])
def test_adjust_to_list_level(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                              state, stack, lev, pltype, exp) -> None:
    """Test the _adjust_to_list_level method."""
    list_handler = ListHandler2(state=state)
    for item in stack:
        stack_item = PointStackItem(point_list_type=item,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    list_handler._adjust_to_list_level(target_level=lev,  # pylint: disable=protected-access # noqa: E501
                                       point_list_type=pltype)
    check_expected_result(list_handler, exp)
    check_capsys(capsys)
