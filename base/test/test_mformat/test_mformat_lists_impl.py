#! /usr/local/bin/python3
"""Test the mformat_lists_impl module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from mformat.mformat_state import MultiFormatState, Formatting
from mformat.mformat_lists_impl import ListHandlerMixin


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
def test_is_in_item_state(capsys, state: MultiFormatState,
                          in_item: bool) -> None:
    """Test the is_in_list_item_state method."""
    list_handler = ListHandlerMixin()
    list_handler.state = state
    # pylint: disable=protected-access
    assert list_handler._is_in_list_item_state() == in_item
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
def test_abstract_methods(capsys, method: str, args: tuple[int, ...]) -> None:
    """Test the abstract methods."""
    list_handler = ListHandlerMixin()
    with pytest.raises(NotImplementedError) as exc:
        getattr(list_handler, method)(*args)
    assert exc.value.args[0] == f'{method} must be overridden'
    check_capsys(capsys)
