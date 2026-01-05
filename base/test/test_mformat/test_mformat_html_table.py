#! /usr/local/bin/python3
"""Test the mformat_html module table functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#


from test_helpers import (
    check_run_with_context_manager,
    TABLE_DATA_3X2,
    TABLE_DATA_3X2_SIMPLE
)
from test_mformat_html_core import PF_EN_NT_NC, SFTOT
from mformat.mformat_html import MultiFormatHtml


def test_simple_table(capsys):
    """Test a simple table."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])
        mfd.add_table_row(row=['C', 'D'])

    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>Col1</td>\n<td>Col2</td>\n'
                '</tr>\n<tr>\n<td>A</td>\n<td>B</td>\n</tr>\n<tr>\n'
                '<td>C</td>\n<td>D</td>\n</tr>\n</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_table_with_bold_header(capsys):
    """Test a table with bold header."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Name', 'Age'], bold=True)
        mfd.add_table_row(row=['Alice', '30'])
        mfd.add_table_row(row=['Bob', '25'])

    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td><strong>Name</strong></td>\n'
                '<td><strong>Age</strong></td>\n</tr>\n<tr>\n<td>Alice</td>\n'
                '<td>30</td>\n</tr>\n<tr>\n<td>Bob</td>\n<td>25</td>\n</tr>\n'
                '</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_table_with_italic_header(capsys):
    """Test a table with italic header."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Name', 'Age'], italic=True)
        mfd.add_table_row(row=['Alice', '30'])

    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td><em>Name</em></td>\n'
                '<td><em>Age</em></td>\n</tr>\n<tr>\n<td>Alice</td>\n'
                '<td>30</td>\n</tr>\n</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_write_complete_table(capsys):
    """Test write_complete_table method."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_complete_table(table=TABLE_DATA_3X2)

    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>Header1</td>\n'
                '<td>Header2</td>\n</tr>\n<tr>\n<td>Row1Col1</td>\n'
                '<td>Row1Col2</td>\n</tr>\n<tr>\n<td>Row2Col1</td>\n'
                '<td>Row2Col2</td>\n</tr>\n</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_write_complete_table_with_bold_header(capsys):
    """Test write_complete_table with bold first row."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_complete_table(
            table=TABLE_DATA_3X2_SIMPLE, bold_first_row=True)

    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td><strong>Name</strong></td>\n'
                '<td><strong>Value</strong></td>\n</tr>\n<tr>\n'
                '<td>Alpha</td>\n<td>1</td>\n</tr>\n<tr>\n<td>Beta</td>\n'
                '<td>2</td>\n</tr>\n</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph(text='Here is a table:')
        mfd.start_table(first_row=['A', 'B'])
        mfd.add_table_row(row=['1', '2'])

    expected = (PF_EN_NT_NC + '<p>\nHere is a table:</p>\n<table>\n<tr>\n'
                '<td>A</td>\n<td>B</td>\n</tr>\n<tr>\n<td>1</td>\n'
                '<td>2</td>\n</tr>\n</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['X', 'Y'])
        mfd.add_table_row(row=['1', '2'])
        mfd.start_paragraph(text='That was the table.')

    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>X</td>\n<td>Y</td>\n</tr>\n'
                '<tr>\n<td>1</td>\n<td>2</td>\n</tr>\n</table>\n'
                '<p>\nThat was the table.</p>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_heading_then_table(capsys):
    """Test heading followed by table."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=2, text='Data Table')
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])

    expected = (PF_EN_NT_NC + '<h2>\nData Table</h2>\n<table>\n<tr>\n'
                '<td>Col1</td>\n<td>Col2</td>\n</tr>\n<tr>\n<td>A</td>\n'
                '<td>B</td>\n</tr>\n</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)


def test_table_with_three_columns(capsys):
    """Test a table with three columns."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Name', 'Age', 'City'])
        mfd.add_table_row(row=['Alice', '30', 'NYC'])
        mfd.add_table_row(row=['Bob', '25', 'LA'])

    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>Name</td>\n<td>Age</td>\n'
                '<td>City</td>\n</tr>\n<tr>\n<td>Alice</td>\n<td>30</td>\n'
                '<td>NYC</td>\n</tr>\n<tr>\n<td>Bob</td>\n<td>25</td>\n'
                '<td>LA</td>\n</tr>\n</table>\n' + SFTOT)
    check_run_with_context_manager('html', '.html', test_action,
                                   expected_text=expected, capsys=capsys)
