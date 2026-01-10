#! /usr/local/bin/python3
"""Test table functionality in the mformat module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from test_helpers import (
    MultiFormat3,
    TABLE_DATA_3X2,
    TABLE_DATA_VARIED_WIDTHS,
    TABLE_DATA_WRONG_COLUMNS
)
from mformat.mformat_state import MultiFormatState, Formatting


class MultiFormat11(MultiFormat3):
    """Class used for testing tables."""

    def _start_table(self, num_columns: int) -> None:
        """Start a table."""
        assert isinstance(num_columns, int)
        self.inc_count('_start_table')

    def _end_table(self, num_columns: int, num_rows: int) -> None:
        """End a table."""
        assert isinstance(num_columns, int)
        assert isinstance(num_rows, int)
        self.inc_count('_end_table')

    def _write_table_first_row(self, first_row: list[str],
                               formatting: Formatting) -> None:
        """Write the first row of a table."""
        assert isinstance(first_row, list)
        assert isinstance(formatting, Formatting)
        self.inc_count('_write_table_first_row')

    def _write_table_row(self, row: list[str], formatting: Formatting,
                         row_number: int) -> None:
        """Write a row of a table."""
        assert isinstance(row, list)
        assert isinstance(formatting, Formatting)
        assert isinstance(row_number, int)
        self.inc_count('_write_table_row')

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        assert isinstance(level, int)
        self.inc_count('_start_heading')

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        assert isinstance(level, int)
        self.inc_count('_end_heading')


def test_start_table_basic(capsys):
    """Test starting a basic table."""
    mfmt = MultiFormat11(file_name='test')
    assert mfmt.state == MultiFormatState.EMPTY
    mfmt.start_table(first_row=['Col1', 'Col2'])
    assert mfmt.state == MultiFormatState.TABLE
    assert mfmt.table is not None
    assert mfmt.table.number_of_columns == 2
    assert mfmt.table.number_of_rows == 1
    assert mfmt.table.column_widths == [4, 4]
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_table': 1,
        '_write_table_first_row': 1}
    check_capsys(capsys)


def test_start_table_with_rows(capsys):
    """Test table with multiple rows."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_table(first_row=['Name', 'Age'])
    mfmt.add_table_row(row=['Alice', '30'])
    mfmt.add_table_row(row=['Bob', '25'])
    assert mfmt.state == MultiFormatState.TABLE
    assert mfmt.table.number_of_rows == 3
    assert mfmt.table.column_widths == [5, 3]
    assert mfmt.count == {
        '_encode_text': 6,
        '_write_file_prefix': 1,
        '_start_table': 1,
        '_write_table_first_row': 1,
        '_write_table_row': 2}
    check_capsys(capsys)


def test_table_column_width_expansion(capsys):
    """Test that column widths expand with longer content."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_table(first_row=['A', 'B'])
    assert mfmt.table.column_widths == [1, 1]
    mfmt.add_table_row(row=['Short', 'Text'])
    assert mfmt.table.column_widths == [5, 4]
    mfmt.add_table_row(row=['Very long text', 'X'])
    assert mfmt.table.column_widths == [14, 4]
    check_capsys(capsys)


def test_write_complete_table_basic(capsys):
    """Test write_complete_table method."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.write_complete_table(table=TABLE_DATA_3X2)
    assert mfmt.state == MultiFormatState.TABLE
    assert mfmt.table.number_of_columns == 2
    assert mfmt.table.number_of_rows == 3
    # Column widths calculated from all rows
    assert mfmt.table.column_widths == [8, 8]
    assert mfmt.count == {
        '_encode_text': 6,
        '_write_file_prefix': 1,
        '_start_table': 1,
        '_write_table_first_row': 1,
        '_write_table_row': 2}
    check_capsys(capsys)


def test_write_complete_table_with_varying_widths(capsys):
    """Test write_complete_table with varying column widths."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.write_complete_table(table=TABLE_DATA_VARIED_WIDTHS)
    # Column widths should be max from all rows
    assert mfmt.table.column_widths == [6, 14]
    check_capsys(capsys)


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_table(first_row=['X', 'Y'])
    mfmt.add_table_row(row=['1', '2'])
    mfmt.start_paragraph(text='After table')
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {
        '_encode_text': 5,
        '_write_file_prefix': 1,
        '_start_table': 1,
        '_write_table_first_row': 1,
        '_write_table_row': 1,
        '_end_table': 1,
        '_start_paragraph': 1,
        '_write_text': 1}
    check_capsys(capsys)


def test_heading_then_table(capsys):
    """Test heading followed by table."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_heading(level=1, text='Data')
    mfmt.start_table(first_row=['Col1', 'Col2'])
    assert mfmt.state == MultiFormatState.TABLE
    assert mfmt.count == {
        '_encode_text': 3,
        '_write_file_prefix': 1,
        '_start_heading': 1,
        '_write_text': 1,
        '_end_heading': 1,
        '_start_table': 1,
        '_write_table_first_row': 1}
    check_capsys(capsys)


def test_multiple_tables(capsys):
    """Test multiple tables in sequence."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_table(first_row=['A', 'B'])
    mfmt.add_table_row(row=['1', '2'])
    mfmt.start_paragraph(text='Between')
    mfmt.start_table(first_row=['X', 'Y', 'Z'])
    mfmt.add_table_row(row=['3', '4', '5'])
    assert mfmt.state == MultiFormatState.TABLE
    assert mfmt.table.number_of_columns == 3
    assert mfmt.count == {
        '_encode_text': 11,
        '_write_file_prefix': 1,
        '_start_table': 2,
        '_write_table_first_row': 2,
        '_write_table_row': 2,
        '_end_table': 1,
        '_end_paragraph': 1,
        '_start_paragraph': 1,
        '_write_text': 1}
    check_capsys(capsys)


def test_table_error_wrong_column_count(capsys):
    """Test error when row has wrong number of columns."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_table(first_row=['A', 'B'])
    with pytest.raises(RuntimeError, match='Row has 3 columns'):
        mfmt.add_table_row(row=['1', '2', '3'])
    check_capsys(capsys)


def test_write_complete_table_error_empty(capsys):
    """Test error when table is empty."""
    mfmt = MultiFormat11(file_name='test')
    with pytest.raises(RuntimeError, match='must have at least one row'):
        mfmt.write_complete_table(table=[])
    check_capsys(capsys)


def test_write_complete_table_error_empty_first_row(capsys):
    """Test error when first row is empty."""
    mfmt = MultiFormat11(file_name='test')
    with pytest.raises(RuntimeError,
                       match='must have at least one column'):
        mfmt.write_complete_table(table=[[]])
    check_capsys(capsys)


def test_write_complete_table_error_inconsistent_columns(capsys):
    """Test error when rows have inconsistent column counts."""
    mfmt = MultiFormat11(file_name='test')
    with pytest.raises(RuntimeError,
                       match='Row 1 has 3 columns.*2 columns'):
        mfmt.write_complete_table(table=TABLE_DATA_WRONG_COLUMNS)
    check_capsys(capsys)


def test_table_with_single_column(capsys):
    """Test table with single column."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_table(first_row=['Column'])
    mfmt.add_table_row(row=['Value1'])
    mfmt.add_table_row(row=['Value2'])
    assert mfmt.table.number_of_columns == 1
    assert mfmt.table.number_of_rows == 3
    assert mfmt.table.column_widths == [6]
    check_capsys(capsys)


def test_table_with_many_columns(capsys):
    """Test table with many columns."""
    mfmt = MultiFormat11(file_name='test')
    first_row = ['C1', 'C2', 'C3', 'C4', 'C5']
    mfmt.start_table(first_row=first_row)
    mfmt.add_table_row(row=['1', '2', '3', '4', '5'])
    assert mfmt.table.number_of_columns == 5
    assert mfmt.table.column_widths == [2, 2, 2, 2, 2]
    check_capsys(capsys)


def test_write_complete_table_then_start_table(capsys):
    """Test write_complete_table followed by start_table."""
    mfmt = MultiFormat11(file_name='test')
    # First table using write_complete_table
    mfmt.write_complete_table(table=[['A', 'B'], ['1', '2']])
    assert mfmt.table.column_widths == [1, 1]
    # Start a new table
    mfmt.start_paragraph(text='Between')
    mfmt.start_table(first_row=['Long', 'Short'])
    assert mfmt.table.column_widths == [4, 5]
    mfmt.add_table_row(row=['A', 'B'])
    # New table should have its own column widths
    assert mfmt.table.column_widths == [4, 5]
    assert mfmt.table.number_of_columns == 2
    check_capsys(capsys)


def test_table_row_in_paragraph(capsys):
    """Test table row in paragraph."""
    mfmt = MultiFormat11(file_name='test')
    mfmt.start_paragraph(text='A')
    with pytest.raises(RuntimeError) as exc:
        mfmt.add_table_row(row=['1', '2'])
    assert exc.value.args[0] == 'Cannot add table row to state PARAGRAPH'
    check_capsys(capsys)
