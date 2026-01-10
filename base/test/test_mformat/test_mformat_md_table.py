#! /usr/local/bin/python3
"""Test the mformat_md module table functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from test_helpers import (
    check_run_with_context_manager,
    run_with_context_manager,
    TABLE_DATA_3X2,
    TABLE_DATA_3X2_SIMPLE
)
from check_capsys import check_capsys
from mformat.mformat_state import Formatting


def test_simple_table(capsys):
    """Test a simple table."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])
        mfd.add_table_row(row=['C', 'D'])

    expected = ('\n| Col1 | Col2 |\n'
                '|------|------|\n'
                '| A    | B    |\n'
                '| C    | D    |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_with_bold_header(capsys):
    """Test a table with bold header."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['Name', 'Age'], bold=True)
        mfd.add_table_row(row=['Alice', '30'])
        mfd.add_table_row(row=['Bob', '25'])

    expected = ('\n| **Name** | **Age** |\n'
                '|----------|---------|\n'
                '| Alice    | 30      |\n'
                '| Bob      | 25      |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_with_italic_header(capsys):
    """Test a table with italic header."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['Name', 'Age'], italic=True)
        mfd.add_table_row(row=['Alice', '30'])

    expected = ('\n| *Name* | *Age* |\n'
                '|--------|-------|\n'
                '| Alice  | 30    |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_with_varied_column_widths(capsys):
    """Test a table with varied column widths."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['Short', 'Longer'])
        mfd.add_table_row(row=['A', 'Very long text'])
        mfd.add_table_row(row=['B', 'Short'])

    # Note: separator width is based on first row only
    expected = ('\n| Short | Longer |\n'
                '|-------|--------|\n'
                '| A     | Very long text |\n'
                '| B     | Short          |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_write_complete_table(capsys):
    """Test write_complete_table method."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_complete_table(table=TABLE_DATA_3X2)

    expected = ('\n| Header1  | Header2  |\n'
                '|----------|----------|\n'
                '| Row1Col1 | Row1Col2 |\n'
                '| Row2Col1 | Row2Col2 |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_write_complete_table_with_bold_header(capsys):
    """Test write_complete_table with bold first row."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.write_complete_table(
            table=TABLE_DATA_3X2_SIMPLE, bold_first_row=True)

    expected = ('\n| **Name** | **Value** |\n'
                '|----------|-----------|\n'
                '| Alpha    | 1         |\n'
                '| Beta     | 2         |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph(text='Here is a table:')
        mfd.start_table(first_row=['A', 'B'])
        mfd.add_table_row(row=['1', '2'])

    expected = ('Here is a table:\n'
                '\n| A | B |\n'
                '|---|---|\n'
                '| 1 | 2 |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['X', 'Y'])
        mfd.add_table_row(row=['1', '2'])
        mfd.start_paragraph(text='That was the table.')

    expected = ('\n| X | Y |\n'
                '|---|---|\n'
                '| 1 | 2 |\n'
                '\nThat was the table.\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_heading_then_table(capsys):
    """Test heading followed by table."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=2, text='Data Table')
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])

    expected = ('## Data Table\n'
                '\n| Col1 | Col2 |\n'
                '|------|------|\n'
                '| A    | B    |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_with_three_columns(capsys):
    """Test a table with three columns."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['Name', 'Age', 'City'])
        mfd.add_table_row(row=['Alice', '30', 'NYC'])
        mfd.add_table_row(row=['Bob', '25', 'LA'])

    # Note: separator width based on first row widths [4, 3, 4]
    # Subsequent rows can be wider
    expected = ('\n| Name | Age | City |\n'
                '|------|-----|------|\n'
                '| Alice | 30  | NYC  |\n'
                '| Bob   | 25  | LA   |\n\n')
    check_run_with_context_manager('md', '.md', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_different_num_cols(capsys):
    """Test a table with different number of columns."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['Name', 'Age', 'City'])
        mfd.add_table_row(row=['Alice', '30'])
        mfd.add_table_row(row=['Bob', '25', 'LA'])

    with pytest.raises(RuntimeError) as exc:
        _ = run_with_context_manager('md', '.md', test_action)
    assert exc.value.args[0] == 'Row has 2 columns, but table has 3 columns'
    check_capsys(capsys)


def test_table_different_num_cols2(capsys):
    """Test a table with different number of columns."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_table(first_row=['Name', 'Age', 'City'])
        mfd._write_table_row(row=['Alice', '30'],  # pylint: disable=protected-access # noqa: E501
                             formatting=Formatting(bold=False, italic=False),
                             row_number=2)
        mfd.add_table_row(row=['Bob', '25', 'LA'])

    with pytest.raises(ValueError) as exc:
        _ = run_with_context_manager('md', '.md', test_action)
    assert exc.value.args[0] == 'Row 2 has 2 columns, but table has 3 columns.'
    check_capsys(capsys)
