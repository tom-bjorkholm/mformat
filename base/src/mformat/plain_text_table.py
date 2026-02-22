#! /usr/local/bin/python3
"""Format a table as plain text with borders."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from enum import IntEnum, auto
from typing import NamedTuple, Sequence
from mformat.underline_text import wrap_text


class BorderSpec(NamedTuple):
    """Specification for plain text table borders.

    The pattern strings are used to create the borders. The patterns are
    repeated to create the borders. The patterns for vertical borders
    shall include any spacing between the border and the cell content.
    The following picture of a 3x3 table shows which patterns are used
    for which border:

    1aaaa2aaaa2aaaa3
    X    |    |    Y
    4----5----5----6
    X    |    |    Y
    4----5----5----6
    X    |    |    Y
    7cccc8cccc8cccc9

    - top is a
    - bottom is c
    - left is X
    - right is Y
    - top_left is 1
    - top_right is 3
    - bottom_left is 7
    - bottom_right is 9
    - inner_horizontal is -
    - inner_vertical is |
    - top_corner is 2
    - bottom_corner is 8
    - left_corner is 4
    - right_corner is 6
    - inner_cell_corner is 5
    """

    top: str
    """Top border pattern away from corners."""
    bottom: str
    """Bottom border pattern away from corners."""
    left: str
    """Left border pattern away from corners."""
    right: str
    """Right border pattern away from corners."""
    top_left: str
    """Top left corner pattern."""
    top_right: str
    """Top right corner pattern."""
    bottom_left: str
    """Bottom left corner pattern."""
    bottom_right: str
    """Bottom right corner pattern."""
    inner_horizontal: str
    """Inner horizontal border pattern away from cell corners."""
    inner_vertical: str
    """Inner vertical border pattern away from cell corners."""
    top_corner: str
    """Pattern for cell corner at top of table away from table corners."""
    bottom_corner: str
    """Pattern for cell corner at bottom of table away from table corners."""
    left_corner: str
    """Pattern for cell corner at left of table away from table corners."""
    right_corner: str
    """Pattern for cell corner at right of table away from table corners."""
    inner_cell_corner: str
    """Pattern for cell corner away from table edges."""


def _wrap_cell_text(text: str, width: int) -> list[str]:
    """Wrap cell text to fit within the given width.

    Handles the case where text already fits without wrapping
    (returning it without calling wrap_text). For text that
    needs wrapping, delegates to wrap_text.

    Args:
        text: The text to wrap.
        width: The maximum line width.

    Returns:
        A list of strings, one for each wrapped line.
    """
    stripped = text.strip()
    if not stripped:
        return ['']
    if len(stripped) <= width:
        return [stripped]
    return wrap_text(stripped, width)


def get_rst_like_spec() -> BorderSpec:
    """Get a specification for RST like plain text table borders."""
    return BorderSpec(
        top='-',
        bottom='-',
        left='|',
        right='|',
        top_left='+-',
        top_right='-+',
        bottom_left='+-',
        bottom_right='-+',
        inner_horizontal='-',
        inner_vertical=' | ',
        top_corner='-+-',
        bottom_corner='-+-',
        left_corner='+-',
        right_corner='-+',
        inner_cell_corner='-+-',
    )


def line_wraps_per_column_width(column_values: Sequence[str]) -> dict[int,
                                                                      int]:
    """Get the number of line wraps for different column widths.

    The number of line wraps is calculated by wrapping the column values
    at word boundaries and counting the number of lines for each column width.
    The column width is varying from the longest column value unwrapped
    to the shortest possible column width that can hold the longest word
    in the column value.

    Args:
        column_values: The values in the columns.

    Returns:
        A dictionary with the column width as key and the number of line
        wraps needed for that column width as value.
        The unit of the column width is the number of characters.
        The dictionary only holds the smallest column width needed for
        a given number of line wraps (that is if column width 50 and 51
        both need 5 line wraps, only the column width 50 is in the
        dictionary).
    """
    longest_value_length = max(len(value) for value in column_values)
    longest_word_length = max(len(word) for value in column_values
                              for word in value.split(' '))
    result: dict[int, int] = {}
    for width in reversed(range(longest_word_length,
                                longest_value_length + 1)):
        num_wraps = sum(len(_wrap_cell_text(value, width)) - 1
                        for value in column_values)
        result[width] = num_wraps
        for prev_width in range(width + 1,
                                longest_value_length + 1):
            if prev_width in result \
                    and result[prev_width] == num_wraps:
                del result[prev_width]
    return result


def _backtrack_widths(prev_dp: list[float],
                      choices: list[list[int]]) -> list[int]:
    """Find the best total used space and backtrack to widths.

    Args:
        prev_dp: The final DP cost array after processing all
            columns. prev_dp[s] is the minimum total wraps when
            exactly s total width is used.
        choices: For each column, an array where
            choices[col][s] is the width chosen for that column
            when s total width is used for columns 0..col.

    Returns:
        A list of column widths, one per column.
    """
    best_wraps = float('inf')
    best_used = 0
    for used, cost in enumerate(prev_dp):
        if cost < best_wraps:
            best_wraps = cost
            best_used = used
    num_cols = len(choices)
    result = [0] * num_cols
    remaining = best_used
    for col_idx in range(num_cols - 1, -1, -1):
        w = choices[col_idx][remaining]
        result[col_idx] = w
        remaining -= w
    return result


def _find_optimal_widths(
        possible_widths: list[dict[int, int]],
        available_space: int) -> list[int]:
    """Find column widths that minimize total line wraps.

    Uses dynamic programming to find the combination of column
    widths whose sum fits within available_space and whose total
    wrap cost is minimized.

    Args:
        possible_widths: For each column, a dict mapping column
            width to the number of line wraps at that width.
        available_space: The total space available for all columns.

    Returns:
        A list of column widths, one per column.
    """
    num_cols = len(possible_widths)
    inf = float('inf')
    prev_dp: list[float] = [inf] * (available_space + 1)
    prev_dp[0] = 0
    choices: list[list[int]] = []
    for col_idx in range(num_cols):
        curr_dp: list[float] = [inf] * (available_space + 1)
        col_choices = [0] * (available_space + 1)
        for used, cost in enumerate(prev_dp):
            if cost == inf:
                continue
            for w, wrap_cost in \
                    possible_widths[col_idx].items():
                new_used = used + w
                if new_used > available_space:
                    continue
                new_cost = cost + wrap_cost
                if new_cost < curr_dp[new_used]:
                    curr_dp[new_used] = new_cost
                    col_choices[new_used] = w
        prev_dp = curr_dp
        choices.append(col_choices)
    return _backtrack_widths(prev_dp, choices)


def select_column_widths(data: list[list[str]], border_spec: BorderSpec,
                         max_line_length: int) -> list[int]:
    """Select the column widths for a table.

    Args:
        data: The data in the table.
        border_spec: The specification for the borders.
        max_line_length: The maximum length of the lines to generate.

    Returns:
        A list of column widths that are needed to fit the data in the table
        with the given border specification and maximum line length and as
        few line wraps as possible.

    Raises:
        ValueError: If the data is empty.
        ValueError: If the data rows have different number of columns.
        ValueError: If the border specification is invalid.
        ValueError: If the maximum line length is less than 10.
        ValueError: If the data is not a list of lists of strings.
        RuntimeError: If the table cannot be formatted with the given border
                      specification and maximum line length.
    """
    if not data or not isinstance(data, list):
        raise ValueError('Data is not a list of lists of strings')
    for row in data:
        if not row or not isinstance(row, list):
            raise ValueError('Data is not a list of lists of strings')
        if len(row) != len(data[0]):
            raise ValueError('Data rows have different number of columns')
        if not all(isinstance(cell, str) for cell in row):
            raise ValueError('Data is not a list of lists of strings')
    if not border_spec:
        raise ValueError('Border specification is invalid')
    if max_line_length < 10:
        raise ValueError('Maximum line length is less than 10')
    sum_border_length = len(border_spec.left) + \
        len(border_spec.right) + \
        (len(border_spec.inner_vertical) * (len(data[0]) - 1))
    available_space = max_line_length - sum_border_length
    if available_space <= 0:
        raise RuntimeError('Maximum line length is too short to fit the '
                           'borders')
    possible_column_widths: list[dict[int, int]] = []
    for column in zip(*data):
        colwidths = line_wraps_per_column_width(column)
        possible_column_widths.append(colwidths)
    no_wrap_length: int = sum(list(col.keys())[0]
                              for col in possible_column_widths)
    if no_wrap_length <= available_space:
        return [list(colwidths.keys())[0]
                for colwidths in possible_column_widths]
    min_possible_width: int = \
        sum(list(col.keys())[-1] for col in possible_column_widths)
    if min_possible_width > available_space:
        raise RuntimeError('Maximum line length is too short to fit the '
                           'data')
    return _find_optimal_widths(
        possible_column_widths, available_space)


class TableAlignment(IntEnum):
    """Alignment of the data inside a table cell."""

    RIGHT = auto()
    LEFT = auto()
    LEFT_BUT_DIGITS_RIGHT = auto()
    CENTER = auto()
    CENTER_BUT_DIGITS_RIGHT = auto()


type TableAlignmentSpec = TableAlignment | list[TableAlignment]
"""Specification for the alignment of the data inside a table cell.

    The specification can be a single alignment or a list of alignments.
    If a list is used, the alignment is applied to the columns in the order
    of the list.
    """


def align_cell_value(value: str,  # pylint: disable=too-many-return-statements
                     alignment: TableAlignment, column_width: int) -> str:
    """Align a cell value.

    Args:
        value: The value to align.
        alignment: The alignment to use.
        column_width: The width of the column.
    """
    if alignment == TableAlignment.LEFT:
        return value.ljust(column_width)
    if alignment == TableAlignment.RIGHT:
        return value.rjust(column_width)
    if alignment == TableAlignment.LEFT_BUT_DIGITS_RIGHT:
        if all(char in '0123456789.,' for char in value):
            return value.rjust(column_width)
        return value.ljust(column_width)
    if alignment == TableAlignment.CENTER:
        return value.center(column_width)
    if alignment == TableAlignment.CENTER_BUT_DIGITS_RIGHT:
        if all(char in '0123456789.,' for char in value):
            return value.rjust(column_width)
        return value.center(column_width)
    raise ValueError(f'Invalid alignment: {alignment}')


def format_one_table_row(row: list[str], column_widths: list[int],
                         border_spec: BorderSpec,
                         alignment: list[TableAlignment]) -> str:
    """Format one table row.

    Args:
        row: The row to format.
        column_widths: The widths of the columns.
        border_spec: The specification for the borders.
        alignment: The alignment to use.
    """
    assert isinstance(alignment, list)
    assert isinstance(column_widths, list)
    assert len(alignment) == len(column_widths)
    result: str = border_spec.left
    for column_number, cell in enumerate(row):
        result += align_cell_value(cell, alignment[column_number],
                                   column_widths[column_number])
        if column_number < len(column_widths) - 1:
            result += border_spec.inner_vertical
    result += border_spec.right
    return result


def format_border_row(left: str, right: str, horizontal: str, vertical: str,
                      column_widths: list[int]) -> str:
    """Format a border row.

    Args:
        left: The left border.
        right: The right border.
        horizontal: The horizontal border.
        vertical: The vertical border.
        column_widths: The widths of the columns.
    """
    result: str = left
    for column_number, column_width in enumerate(column_widths):
        repeats = column_width // len(horizontal) + 1
        result += (horizontal * repeats)[:column_width]
        if column_number < len(column_widths) - 1:
            result += vertical
    result += right
    return result


def format_top_border(border_spec: BorderSpec,
                      column_widths: list[int]) -> str:
    """Format the top border of the table.

    Args:
        border_spec: The specification for the borders.
        column_widths: The widths of the columns.
    """
    return format_border_row(left=border_spec.top_left,
                             right=border_spec.top_right,
                             horizontal=border_spec.top,
                             vertical=border_spec.top_corner,
                             column_widths=column_widths)


def format_bottom_border(border_spec: BorderSpec,
                         column_widths: list[int]) -> str:
    """Format the bottom border of the table.

    Args:
        border_spec: The specification for the borders.
        column_widths: The widths of the columns.
    """
    return format_border_row(left=border_spec.bottom_left,
                             right=border_spec.bottom_right,
                             horizontal=border_spec.bottom,
                             vertical=border_spec.bottom_corner,
                             column_widths=column_widths)


def _wrap_row_cells(row: list[str],
                    column_widths: list[int]) -> list[list[str]]:
    """Wrap cell values in a row to fit column widths.

    Each cell is wrapped to its column width using word-boundary
    wrapping. Cells with fewer lines than the tallest cell are
    padded with empty strings.

    Args:
        row: The cell values in the row.
        column_widths: The widths of the columns.

    Returns:
        A list of sub-rows, where each sub-row is a list of cell
        values (one per column) for a single output line.
    """
    wrapped_cells: list[list[str]] = []
    max_lines = 1
    for cell, width in zip(row, column_widths):
        lines = _wrap_cell_text(cell, width)
        wrapped_cells.append(lines)
        max_lines = max(max_lines, len(lines))
    sub_rows: list[list[str]] = []
    for line_idx in range(max_lines):
        sub_row: list[str] = []
        for cell_lines in wrapped_cells:
            if line_idx < len(cell_lines):
                sub_row.append(cell_lines[line_idx])
            else:
                sub_row.append('')
        sub_rows.append(sub_row)
    return sub_rows


def get_plain_text_table(data: list[list[str]], border_spec: BorderSpec,
                         max_line_length: int,
                         alignment: TableAlignmentSpec) -> list[str]:
    """Get the plain text table as a list of lines.

    Args:
        data: The data in the table.
        border_spec: The specification for the borders.
        max_line_length: The maximum length of the lines to generate.
        alignment: The alignment specification for cell content.

    Returns:
        The plain text table including the borders as a list of lines.
        Each line to be output is one element in the list in the
        order it is to be output. The first line is the top border
        (if any), the second line is the first row of the table,
        the last line is the bottom border (if any).
    """
    column_widths: list[int] = select_column_widths(
        data, border_spec, max_line_length)
    if isinstance(alignment, TableAlignment):
        alignment = [alignment] * len(column_widths)
    assert isinstance(alignment, list)
    if len(alignment) != len(column_widths):
        raise ValueError('Alignment specification has wrong number of '
                         'elements')
    result: list[str] = []
    result.append(format_top_border(border_spec, column_widths))
    for row_number, row in enumerate(data):
        sub_rows = _wrap_row_cells(row, column_widths)
        for sub_row in sub_rows:
            result.append(format_one_table_row(
                sub_row, column_widths, border_spec, alignment))
        if row_number < len(data) - 1:
            result.append(format_border_row(
                left=border_spec.left_corner,
                right=border_spec.right_corner,
                horizontal=border_spec.inner_horizontal,
                vertical=border_spec.inner_cell_corner,
                column_widths=column_widths))
    result.append(format_bottom_border(border_spec, column_widths))
    return result
