#! /usr/local/bin/python3
"""Test the mformat_lists_impl module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Any
import pytest
from mformat.mformat_lists_impl import (ListHandlerMixin, PointListType,
                                        PointStackItem)
from mformat.mformat_state import Formatting, MultiFormatState
from .check_capsys import check_capsys


@pytest.mark.parametrize('state, in_item',
                         [(MultiFormatState.EMPTY, False),
                          (MultiFormatState.PARAGRAPH_END, False),
                          (MultiFormatState.BULLET_LIST, False),
                          (MultiFormatState.BULLET_LIST_ITEM, True),
                          (MultiFormatState.NUMBERED_LIST, False),
                          (MultiFormatState.NUMBERED_LIST_ITEM, True),
                          (MultiFormatState.TABLE, False),
                          (MultiFormatState.CODE_BLOCK, False),
                          (MultiFormatState.CLOSED, False)])
def test_is_in_item_state(capsys: pytest.CaptureFixture[str],
                          state: MultiFormatState,
                          in_item: bool) -> None:
    """Test the is_in_list_item_state method."""
    list_handler = ListHandlerMixin()
    list_handler.state = state
    # pylint: disable=protected-access
    assert list_handler._is_in_list_item_state() == in_item
    check_capsys(capsys)


@pytest.mark.parametrize('state, in_list',
                         [(MultiFormatState.EMPTY, False),
                          (MultiFormatState.PARAGRAPH_END, False),
                          (MultiFormatState.BULLET_LIST, True),
                          (MultiFormatState.BULLET_LIST_ITEM, True),
                          (MultiFormatState.NUMBERED_LIST, True),
                          (MultiFormatState.NUMBERED_LIST_ITEM, True),
                          (MultiFormatState.TABLE, False),
                          (MultiFormatState.CODE_BLOCK, False),
                          (MultiFormatState.CLOSED, False)])
def test_is_in_list_state(capsys: pytest.CaptureFixture[str],
                          state: MultiFormatState,
                          in_list: bool) -> None:
    """Test the is_in_list_state method."""
    list_handler = ListHandlerMixin()
    list_handler.state = state
    # pylint: disable=protected-access
    assert list_handler._is_in_list_state() == in_list
    check_capsys(capsys)


@pytest.mark.parametrize('pltype, list_state, item_state',
                         [(PointListType.BULLET,
                           MultiFormatState.BULLET_LIST,
                           MultiFormatState.BULLET_LIST_ITEM),
                          (PointListType.NUMBERED,
                           MultiFormatState.NUMBERED_LIST,
                           MultiFormatState.NUMBERED_LIST_ITEM)])
def test_get_states_of_pltype_ok(capsys: pytest.CaptureFixture[str],
                                 pltype: PointListType,
                                 list_state: MultiFormatState,
                                 item_state: MultiFormatState) -> None:
    """Test the get_states_of_pltype method."""
    # pylint: disable=protected-access
    assert ListHandlerMixin._get_states_of_pltype(pltype) == (list_state,
                                                              item_state)
    check_capsys(capsys)


@pytest.mark.parametrize('pltype', [5, 7])
def test_get_states_of_pltype_nok(capsys: pytest.CaptureFixture[str],
                                  pltype: int) -> None:
    """Test the get_states_of_pltype method."""
    list_handler = ListHandlerMixin()
    with pytest.raises(KeyError) as exc:
        # pylint: disable=protected-access
        list_handler._get_states_of_pltype(pltype)  # type: ignore[arg-type]
    assert isinstance(exc.value, KeyError)
    check_capsys(capsys)


@pytest.mark.parametrize('pltype, name',
                         [(PointListType.BULLET, 'bullet'),
                          (PointListType.NUMBERED, 'numbered')])
def test_get_point_list_tname_ok(capsys: pytest.CaptureFixture[str],
                                 pltype: PointListType,
                                 name: str) -> None:
    """Test the get_point_list_type_name method."""
    # pylint: disable=protected-access
    assert ListHandlerMixin._get_point_list_type_name(pltype) == name
    check_capsys(capsys)


@pytest.mark.parametrize('pltype', [5, 7])
def test_get_point_list_tname_nok(capsys: pytest.CaptureFixture[str],
                                  pltype: int) -> None:
    """Test the get_point_list_type_name method."""
    with pytest.raises(KeyError) as exc:
        # pylint: disable=protected-access
        ListHandlerMixin._get_point_list_type_name(
            pltype)  # type: ignore[arg-type]
    assert isinstance(exc.value, KeyError)
    check_capsys(capsys)


@pytest.mark.parametrize('method,args',
                         [('_end_state', ()),
                          ('_to_write', ('test', True, False)),
                          ('_write_text', ('test', MultiFormatState.PARAGRAPH,
                                           Formatting(bold=False,
                                                      italic=False))),
                          ('_start_bullet_list', [1]),
                          ('_start_numbered_list', [1]),
                          ('_end_bullet_list', [1]),
                          ('_end_numbered_list', [1]),
                          ('_start_bullet_item', [1]),
                          ('_start_numbered_item', [1, 1, '1.']),
                          ('_end_bullet_item', [1]),
                          ('_end_numbered_item', [1, 1])])
def test_abstract_methods(
        capsys: pytest.CaptureFixture[str],
        method: str,
        args: tuple[Any, ...] | list[Any]) -> None:
    """Test the abstract methods."""
    list_handler = ListHandlerMixin()
    with pytest.raises(NotImplementedError) as exc:
        getattr(list_handler, method)(*args)
    assert exc.value.args[0] == f'{method} must be overridden'
    check_capsys(capsys)


class ListHandler2(ListHandlerMixin):  # pylint: disable=too-few-public-methods
    """Class for testing the ListHandlerMixin class."""

    def __init__(self,
                 state: MultiFormatState = MultiFormatState.EMPTY) -> None:
        """Initialize the ListHandler2 class."""
        super().__init__()
        self.state = state
        self.call_list: list[str] = []
        self.call_arg_list: list[str] = []

    def _record_call(self, method: str,
                     args: tuple[Any, ...]) -> None:
        """Record a call to a method."""
        self.call_list.append(method)
        calltxt = f'{method}({", ".join([str(arg) for arg in args])})'
        self.call_arg_list.append(calltxt)

    def _end_state(self) -> None:
        """End the state."""
        self.state = MultiFormatState.PARAGRAPH_END
        self._record_call('_end_state', ())

    def _to_write(self, text: str, smart_ws: bool, in_add: bool) -> str:
        """Write the text."""
        self._record_call('_to_write', (text, smart_ws, in_add))
        return text

    def _write_text(self, text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write the text."""
        self._record_call('_write_text', (text, state, formatting))

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        self._record_call('_start_bullet_list', (level,))

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        self._record_call('_end_bullet_list', (level,))

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list."""
        self._record_call('_start_numbered_list', (level,))

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list."""
        self._record_call('_end_numbered_list', (level,))

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        self._record_call('_start_bullet_item', (level,))

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered item."""
        self._record_call('_start_numbered_item',
                          (level, num, full_number))

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item."""
        self._record_call('_end_bullet_item', (level,))

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered item."""
        self._record_call('_end_numbered_item', (level, num))


@pytest.mark.parametrize('lev, pltype, call_list, call_arg_list',
                         [(0, PointListType.BULLET,
                           ['_start_bullet_list'], ['_start_bullet_list(0)']),
                          (0, PointListType.NUMBERED,
                           ['_start_numbered_list'],
                           ['_start_numbered_list(0)']),
                          (7, PointListType.BULLET,
                           ['_start_bullet_list'], ['_start_bullet_list(7)']),
                          (5, PointListType.NUMBERED,
                           ['_start_numbered_list'],
                           ['_start_numbered_list(5)']),
                          ])
def test_disp_start_list(capsys: pytest.CaptureFixture[str],
                         lev: int,
                         pltype: PointListType,
                         call_list: list[str],
                         call_arg_list: list[str]) -> None:
    """Test the _dispatch_start_list method."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    # pylint: disable=protected-access
    list_handler._dispatch_start_list(lev, pltype)
    assert list_handler.call_list == call_list
    assert list_handler.call_arg_list == call_arg_list
    check_capsys(capsys)


@pytest.mark.parametrize('lev, pltype, call_list, call_arg_list',
                         [(2, PointListType.BULLET,
                           ['_end_bullet_list'], ['_end_bullet_list(2)']),
                          (4, PointListType.NUMBERED,
                           ['_end_numbered_list'],
                           ['_end_numbered_list(4)']),
                          ])
def test_disp_end_list(capsys: pytest.CaptureFixture[str],
                       lev: int,
                       pltype: PointListType,
                       call_list: list[str],
                       call_arg_list: list[str]) -> None:
    """Test the _dispatch_end_list method."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    # pylint: disable=protected-access
    list_handler._dispatch_end_list(lev, pltype)
    assert list_handler.call_list == call_list
    assert list_handler.call_arg_list == call_arg_list
    check_capsys(capsys)


@pytest.mark.parametrize('lev, pltype, call_list, call_arg_list',
                         [(4, PointListType.BULLET,
                           ['_start_bullet_item'], ['_start_bullet_item(4)']),
                          (1, PointListType.NUMBERED,
                           ['_start_numbered_item'],
                           ['_start_numbered_item(1, 1, 1.)']),
                          (3, PointListType.NUMBERED,
                           ['_start_numbered_item'],
                           ['_start_numbered_item(3, 1, 1.1.1.)']),
                          ])
def test_disp_start_item(capsys: pytest.CaptureFixture[str],
                         lev: int,
                         pltype: PointListType,
                         call_list: list[str],
                         call_arg_list: list[str]) -> None:
    """Test the _dispatch_start_item method."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    stack_item = PointStackItem(point_list_type=pltype, number_at_level=1)
    for _ in range(lev):
        list_handler.point_list_stack.append(stack_item)
    # pylint: disable=protected-access
    list_handler._dispatch_start_item(lev, pltype)
    assert list_handler.call_list == call_list
    assert list_handler.call_arg_list == call_arg_list
    check_capsys(capsys)


@pytest.mark.parametrize('lev, pltype, call_list, call_arg_list',
                         [(4, PointListType.BULLET,
                           ['_end_bullet_item'], ['_end_bullet_item(4)']),
                          (1, PointListType.NUMBERED,
                           ['_end_numbered_item'],
                           ['_end_numbered_item(1, 1)']),
                          (3, PointListType.NUMBERED,
                           ['_end_numbered_item'],
                           ['_end_numbered_item(3, 1)']),
                          ])
def test_disp_end_item(capsys: pytest.CaptureFixture[str],
                       lev: int,
                       pltype: PointListType,
                       call_list: list[str],
                       call_arg_list: list[str]) -> None:
    """Test the _dispatch_end_item method."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    stack_item = PointStackItem(point_list_type=pltype, number_at_level=1)
    for _ in range(lev):
        list_handler.point_list_stack.append(stack_item)
    # pylint: disable=protected-access
    list_handler._dispatch_end_item(lev, pltype)
    assert list_handler.call_list == call_list
    assert list_handler.call_arg_list == call_arg_list
    check_capsys(capsys)


@pytest.mark.parametrize('pltype', [PointListType.BULLET,
                                    PointListType.NUMBERED])
@pytest.mark.parametrize('lev, on_stack',
                         [(1, []),
                          (2, [PointListType.BULLET]),
                          (1, [PointListType.BULLET,
                               PointListType.NUMBERED,
                               PointListType.BULLET])])
def test_val_list_level_ok(capsys: pytest.CaptureFixture[str],
                           lev: int,
                           on_stack: list[PointListType],
                           pltype: PointListType) -> None:
    """Test the validate_list_level method for OK cases."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    for item in on_stack:
        stack_item = PointStackItem(point_list_type=item, number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    # pylint: disable=protected-access
    list_handler._validate_list_level(lev, pltype)
    check_capsys(capsys)


@pytest.mark.parametrize('pltype', [PointListType.BULLET,
                                    PointListType.NUMBERED])
@pytest.mark.parametrize('lev, on_stack',
                         [(4, [PointListType.BULLET]),
                          (2, [])])
def test_val_list_level_nok(capsys: pytest.CaptureFixture[str],
                            lev: int,
                            on_stack: list[PointListType],
                            pltype: PointListType) -> None:
    """Test the validate_list_level method for NOK cases."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    for item in on_stack:
        stack_item = PointStackItem(point_list_type=item, number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    # pylint: disable=protected-access
    with pytest.raises(RuntimeError) as exc:
        list_handler._validate_list_level(lev, pltype)
    assert f'called with level={lev}, but level {lev-1}' in exc.value.args[0]
    check_capsys(capsys)


@pytest.mark.parametrize('pltype', [PointListType.BULLET,
                                    PointListType.NUMBERED])
@pytest.mark.parametrize('num_at_lev, full_num',
                         [([2, 4, 5], '2.4.5.'),
                          ([1, 2, 3], '1.2.3.'),
                          ([1], '1.')])
def test_ful_nu_of_list_item_ok(capsys: pytest.CaptureFixture[str],
                                pltype: PointListType,
                                num_at_lev: list[int],
                                full_num: str) -> None:
    """Test the full_number_of_list_item method."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    for num in num_at_lev:
        stack_item = PointStackItem(point_list_type=pltype,
                                    number_at_level=num)
        list_handler.point_list_stack.append(stack_item)
    # pylint: disable=protected-access
    ret = list_handler._full_number_of_list_item(num=num_at_lev[-1])
    assert ret == full_num
    check_capsys(capsys)


@pytest.mark.parametrize('pltype', [PointListType.BULLET,
                                    PointListType.NUMBERED])
def test_ful_nu_of_list_item_nok(capsys: pytest.CaptureFixture[str],
                                 pltype: PointListType) -> None:
    """Test the full_number_of_list_item method."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    list_handler.point_list_stack.append(PointStackItem(point_list_type=pltype,
                                                        number_at_level=1))
    with pytest.raises(AssertionError) as _:
        # pylint: disable=protected-access
        list_handler._full_number_of_list_item(num=2)
    check_capsys(capsys)


@pytest.mark.parametrize('pltype, depth, expected',
                         [(PointListType.BULLET, 3,
                           MultiFormatState.BULLET_LIST),
                          (PointListType.NUMBERED, 2,
                           MultiFormatState.NUMBERED_LIST),
                          (PointListType.BULLET, 0,
                           MultiFormatState.PARAGRAPH_END),
                          (PointListType.NUMBERED, 0,
                           MultiFormatState.PARAGRAPH_END)])
def test_state_from_pl_stack(capsys: pytest.CaptureFixture[str],
                             pltype: PointListType,
                             depth: int,
                             expected: MultiFormatState) -> None:
    """Test the _state_from_point_list method."""
    list_handler = ListHandler2(MultiFormatState.EMPTY)
    for _ in range(depth):
        stack_item = PointStackItem(point_list_type=pltype,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    # pylint: disable=protected-access
    list_handler._state_from_point_list()
    assert list_handler.state == expected
    check_capsys(capsys)


@pytest.mark.parametrize('depth, state',
                         [(0, MultiFormatState.BULLET_LIST),
                          (0, MultiFormatState.NUMBERED_LIST),
                          (0, MultiFormatState.BULLET_LIST_ITEM),
                          (0, MultiFormatState.NUMBERED_LIST_ITEM),
                          (3, MultiFormatState.PARAGRAPH_END),
                          (2, MultiFormatState.PARAGRAPH),
                          (1, MultiFormatState.HEADING)])
def test_end_list_state_nok(capsys: pytest.CaptureFixture[str],
                            depth: int,
                            state: MultiFormatState) -> None:
    """Test the _end_list_state method for NOK cases."""
    list_handler = ListHandler2(state)
    for _ in range(depth):
        stack_item = PointStackItem(point_list_type=PointListType.BULLET,
                                    number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    with pytest.raises(AssertionError) as _:
        # pylint: disable=protected-access
        list_handler._end_list_state()
    check_capsys(capsys)


@pytest.mark.parametrize('stack, state, exp_state, exp_calls',
                         [([PointListType.BULLET],
                           MultiFormatState.BULLET_LIST_ITEM,
                           MultiFormatState.PARAGRAPH_END,
                           ['_end_bullet_item',
                            '_end_bullet_list']),
                          ([PointListType.BULLET],
                           MultiFormatState.BULLET_LIST,
                           MultiFormatState.PARAGRAPH_END,
                           ['_end_bullet_list']),
                          ([PointListType.NUMBERED],
                           MultiFormatState.NUMBERED_LIST_ITEM,
                           MultiFormatState.PARAGRAPH_END,
                           ['_end_numbered_item',
                            '_end_numbered_list']),
                          ([PointListType.NUMBERED],
                           MultiFormatState.NUMBERED_LIST,
                           MultiFormatState.PARAGRAPH_END,
                           ['_end_numbered_list']),
                          ([PointListType.NUMBERED,
                            PointListType.BULLET],
                           MultiFormatState.BULLET_LIST_ITEM,
                           MultiFormatState.NUMBERED_LIST,
                           ['_end_bullet_item',
                            '_end_bullet_list']),
                          ([PointListType.BULLET,
                            PointListType.NUMBERED],
                           MultiFormatState.NUMBERED_LIST,
                           MultiFormatState.BULLET_LIST,
                           ['_end_numbered_list'])])
def test_end_list_state_ok(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                           stack: list[PointListType],
                           state: MultiFormatState,
                           exp_state: MultiFormatState,
                           exp_calls: list[str]) -> None:
    """Test the _end_list_state method for OK cases."""
    list_handler = ListHandler2(state)
    for item in stack:
        stack_item = PointStackItem(point_list_type=item, number_at_level=1)
        list_handler.point_list_stack.append(stack_item)
    # pylint: disable=protected-access
    list_handler._end_list_state()
    assert list_handler.state == exp_state
    assert list_handler.call_list == exp_calls
    check_capsys(capsys)
