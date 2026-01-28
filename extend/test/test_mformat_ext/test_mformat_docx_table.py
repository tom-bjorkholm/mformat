#! /usr/local/bin/python3
"""Test the mformat_docx module table functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import sys
from pathlib import Path
from test_mformat_docx_core import silent_docx_create
from mformat_ext.mformat_docx import MultiFormatDocx

# Add base test helpers to path for shared test utilities
_base_test_path = (
    Path(__file__).parent.parent.parent.parent /
    'base' / 'test' / 'test_mformat'
)
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error


def test_simple_table(capsys):
    """Test a simple table."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])
        mfd.add_table_row(row=['C', 'D'])

    html = silent_docx_create(capsys, func=func)
    assert '<table>' in html
    assert '<tr>' in html
    assert '<td>' in html
    assert 'Col1' in html
    assert 'Col2' in html
    assert 'A' in html
    assert 'B' in html
    assert 'C' in html
    assert 'D' in html


def test_table_with_bold_header(capsys):
    """Test a table with bold header."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_table(first_row=['Name', 'Age'], bold=True)
        mfd.add_table_row(row=['Alice', '30'])
        mfd.add_table_row(row=['Bob', '25'])

    html = silent_docx_create(capsys, func=func)
    assert '<table>' in html
    assert '<strong>Name</strong>' in html
    assert '<strong>Age</strong>' in html
    assert 'Alice' in html
    assert '30' in html
    assert 'Bob' in html
    assert '25' in html


def test_table_with_italic_header(capsys):
    """Test a table with italic header."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_table(first_row=['Name', 'Age'], italic=True)
        mfd.add_table_row(row=['Alice', '30'])

    html = silent_docx_create(capsys, func=func)
    assert '<table>' in html
    assert '<em>Name</em>' in html
    assert '<em>Age</em>' in html
    assert 'Alice' in html
    assert '30' in html


def test_write_complete_table(capsys):
    """Test write_complete_table method."""
    def func(mfd: MultiFormatDocx) -> None:
        table_data = [
            ['Header1', 'Header2'],
            ['Row1Col1', 'Row1Col2'],
            ['Row2Col1', 'Row2Col2']
        ]
        mfd.write_complete_table(table=table_data)

    html = silent_docx_create(capsys, func=func)
    assert '<table>' in html
    assert 'Header1' in html
    assert 'Header2' in html
    assert 'Row1Col1' in html
    assert 'Row1Col2' in html
    assert 'Row2Col1' in html
    assert 'Row2Col2' in html


def test_write_complete_table_with_bold_header(capsys):
    """Test write_complete_table with bold first row."""
    def func(mfd: MultiFormatDocx) -> None:
        table_data = [
            ['Name', 'Value'],
            ['Alpha', '1'],
            ['Beta', '2']
        ]
        mfd.write_complete_table(table=table_data, bold_first_row=True)

    html = silent_docx_create(capsys, func=func)
    assert '<table>' in html
    assert '<strong>Name</strong>' in html
    assert '<strong>Value</strong>' in html
    assert 'Alpha' in html
    assert '1' in html
    assert 'Beta' in html
    assert '2' in html


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_paragraph(text='Here is a table:')
        mfd.start_table(first_row=['A', 'B'])
        mfd.add_table_row(row=['1', '2'])

    html = silent_docx_create(capsys, func=func)
    assert '<p>Here is a table:</p>' in html
    assert '<table>' in html
    assert 'A' in html
    assert 'B' in html
    assert '1' in html
    assert '2' in html


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_table(first_row=['X', 'Y'])
        mfd.add_table_row(row=['1', '2'])
        mfd.start_paragraph(text='That was the table.')

    html = silent_docx_create(capsys, func=func)
    assert '<table>' in html
    assert 'X' in html
    assert 'Y' in html
    assert '1' in html
    assert '2' in html
    assert '<p>That was the table.</p>' in html


def test_heading_then_table(capsys):
    """Test heading followed by table."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_heading(level=2, text='Data Table')
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])

    html = silent_docx_create(capsys, func=func)
    assert '<h2>Data Table</h2>' in html
    assert '<table>' in html
    assert 'Col1' in html
    assert 'Col2' in html
    assert 'A' in html
    assert 'B' in html


def test_table_with_three_columns(capsys):
    """Test a table with three columns."""
    def func(mfd: MultiFormatDocx) -> None:
        mfd.start_table(first_row=['Name', 'Age', 'City'])
        mfd.add_table_row(row=['Alice', '30', 'NYC'])
        mfd.add_table_row(row=['Bob', '25', 'LA'])

    html = silent_docx_create(capsys, func=func)
    assert '<table>' in html
    assert 'Name' in html
    assert 'Age' in html
    assert 'City' in html
    assert 'Alice' in html
    assert '30' in html
    assert 'NYC' in html
    assert 'Bob' in html
    assert '25' in html
    assert 'LA' in html
