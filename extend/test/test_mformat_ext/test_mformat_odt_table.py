#! /usr/local/bin/python3
"""Test the mformat_odt module table functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from typing import Any
from odf.table import Table, TableRow, TableCell
from odf.text import P
from mformat_ext.mformat_odt import MultiFormatOdt
from test_mformat_odt_core import (
    silent_odt_create, get_elements_by_type, get_element_text,
    get_heading_texts, get_all_text_content, has_span_with_style
)


def get_table_data(doc: Any) -> list[list[str]]:
    """Extract all table data from an ODT document.

    Args:
        doc: The ODF document.

    Returns:
        A list of tables, each containing a list of rows,
        each containing a list of cell texts.
    """
    tables_data = []
    for table in get_elements_by_type(doc, Table):
        table_rows = []
        for row in table.getElementsByType(TableRow):
            row_cells = []
            for cell in row.getElementsByType(TableCell):
                cell_text = get_element_text(cell).strip()
                row_cells.append(cell_text)
            if row_cells:  # Skip empty rows
                table_rows.append(row_cells)
        if table_rows:  # Skip empty tables
            tables_data.append(table_rows)
    return tables_data


def get_table_count(doc: Any) -> int:
    """Get the count of tables in an ODT document.

    Args:
        doc: The ODF document.

    Returns:
        The number of Table elements.
    """
    return len(get_elements_by_type(doc, Table))


def has_bold_in_cell(cell: TableCell) -> bool:
    """Check if a table cell contains bold text.

    Args:
        cell: The table cell to check.

    Returns:
        True if the cell contains bold-styled text.
    """
    for para in cell.getElementsByType(P):
        if has_span_with_style(para, 'bold'):
            return True
    return False


def has_italic_in_cell(cell: TableCell) -> bool:
    """Check if a table cell contains italic text.

    Args:
        cell: The table cell to check.

    Returns:
        True if the cell contains italic-styled text.
    """
    for para in cell.getElementsByType(P):
        if has_span_with_style(para, 'italic'):
            return True
    return False


# --- Tests for basic tables ---


def test_simple_table(capsys):
    """Test a simple table."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Col1', 'Col2'])
        mfo.add_table_row(row=['A', 'B'])
        mfo.add_table_row(row=['C', 'D'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    table = tables[0]
    assert len(table) == 3  # 1 header + 2 data rows
    assert table[0] == ['Col1', 'Col2']
    assert table[1] == ['A', 'B']
    assert table[2] == ['C', 'D']


def test_table_with_bold_header(capsys):
    """Test a table with bold header."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Name', 'Age'], bold=True)
        mfo.add_table_row(row=['Alice', '30'])
        mfo.add_table_row(row=['Bob', '25'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['Name', 'Age']
    assert tables[0][1] == ['Alice', '30']
    assert tables[0][2] == ['Bob', '25']
    # Verify bold formatting in header row
    table = get_elements_by_type(doc, Table)[0]
    first_row = table.getElementsByType(TableRow)[0]
    for cell in first_row.getElementsByType(TableCell):
        assert has_bold_in_cell(cell)


def test_table_with_italic_header(capsys):
    """Test a table with italic header."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Name', 'Age'], italic=True)
        mfo.add_table_row(row=['Alice', '30'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['Name', 'Age']
    # Verify italic formatting in header row
    table = get_elements_by_type(doc, Table)[0]
    first_row = table.getElementsByType(TableRow)[0]
    for cell in first_row.getElementsByType(TableCell):
        assert has_italic_in_cell(cell)


def test_write_complete_table(capsys):
    """Test write_complete_table method."""
    def func(mfo: MultiFormatOdt) -> None:
        table_data = [
            ['Header1', 'Header2'],
            ['Row1Col1', 'Row1Col2'],
            ['Row2Col1', 'Row2Col2']
        ]
        mfo.write_complete_table(table=table_data)

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['Header1', 'Header2']
    assert tables[0][1] == ['Row1Col1', 'Row1Col2']
    assert tables[0][2] == ['Row2Col1', 'Row2Col2']


def test_write_complete_table_with_bold_header(capsys):
    """Test write_complete_table with bold first row."""
    def func(mfo: MultiFormatOdt) -> None:
        table_data = [
            ['Name', 'Value'],
            ['Alpha', '1'],
            ['Beta', '2']
        ]
        mfo.write_complete_table(table=table_data, bold_first_row=True)

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['Name', 'Value']
    # Verify bold formatting in header row
    table = get_elements_by_type(doc, Table)[0]
    first_row = table.getElementsByType(TableRow)[0]
    for cell in first_row.getElementsByType(TableCell):
        assert has_bold_in_cell(cell)


# --- Tests for table transitions ---


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_paragraph(text='Here is a table:')
        mfo.start_table(first_row=['A', 'B'])
        mfo.add_table_row(row=['1', '2'])

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'Here is a table:' in all_text
    tables = get_table_data(doc)
    assert len(tables) == 1


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['X', 'Y'])
        mfo.add_table_row(row=['1', '2'])
        mfo.start_paragraph(text='That was the table.')

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    all_text = get_all_text_content(doc)
    assert 'That was the table.' in all_text


def test_heading_then_table(capsys):
    """Test heading followed by table."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_heading(level=2, text='Data Table')
        mfo.start_table(first_row=['Col1', 'Col2'])
        mfo.add_table_row(row=['A', 'B'])

    doc = silent_odt_create(capsys, func=func)
    headings = get_heading_texts(doc)
    assert len(headings) == 1
    assert headings[0] == (2, 'Data Table')
    tables = get_table_data(doc)
    assert len(tables) == 1


# --- Tests for tables with different column counts ---


def test_table_with_three_columns(capsys):
    """Test a table with three columns."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Name', 'Age', 'City'])
        mfo.add_table_row(row=['Alice', '30', 'NYC'])
        mfo.add_table_row(row=['Bob', '25', 'LA'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['Name', 'Age', 'City']
    assert tables[0][1] == ['Alice', '30', 'NYC']
    assert tables[0][2] == ['Bob', '25', 'LA']


def test_table_with_single_column(capsys):
    """Test a table with a single column."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Items'])
        mfo.add_table_row(row=['Apple'])
        mfo.add_table_row(row=['Banana'])
        mfo.add_table_row(row=['Cherry'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['Items']
    assert tables[0][1] == ['Apple']
    assert tables[0][2] == ['Banana']
    assert tables[0][3] == ['Cherry']


def test_table_with_many_columns(capsys):
    """Test a table with many columns."""
    def func(mfo: MultiFormatOdt) -> None:
        headers = ['A', 'B', 'C', 'D', 'E', 'F']
        row1 = ['1', '2', '3', '4', '5', '6']
        mfo.start_table(first_row=headers)
        mfo.add_table_row(row=row1)

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['A', 'B', 'C', 'D', 'E', 'F']
    assert tables[0][1] == ['1', '2', '3', '4', '5', '6']


# --- Tests for multiple tables ---


def test_multiple_tables(capsys):
    """Test multiple tables in one document."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Table1Col1', 'Table1Col2'])
        mfo.add_table_row(row=['A', 'B'])
        mfo.start_table(first_row=['Table2Col1', 'Table2Col2'])
        mfo.add_table_row(row=['C', 'D'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 2
    assert tables[0][0] == ['Table1Col1', 'Table1Col2']
    assert tables[1][0] == ['Table2Col1', 'Table2Col2']


def test_tables_separated_by_paragraph(capsys):
    """Test tables separated by a paragraph."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['First', 'Table'])
        mfo.add_table_row(row=['1', '2'])
        mfo.start_paragraph(text='Between tables')
        mfo.start_table(first_row=['Second', 'Table'])
        mfo.add_table_row(row=['3', '4'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 2
    all_text = get_all_text_content(doc)
    assert 'Between tables' in all_text


# --- Tests for special characters in tables ---


def test_special_characters_in_table(capsys):
    """Test special characters in table cells."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Special', 'Chars'])
        mfo.add_table_row(row=['<>&', '"\''])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][1] == ['<>&', '"\'']


def test_unicode_in_table(capsys):
    """Test unicode characters in table cells."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Language', 'Text'])
        mfo.add_table_row(row=['Swedish', 'åäö'])
        mfo.add_table_row(row=['Japanese', '日本語'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][1] == ['Swedish', 'åäö']
    assert tables[0][2] == ['Japanese', '日本語']


# --- Tests for empty cells ---


def test_table_with_empty_cells(capsys):
    """Test table with empty cells."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Col1', 'Col2'])
        mfo.add_table_row(row=['', 'B'])
        mfo.add_table_row(row=['C', ''])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    # Empty cells might be empty strings or might be omitted
    assert len(tables[0]) >= 2


# --- Tests for header-only table ---


def test_header_only_table(capsys):
    """Test table with only header row."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Header1', 'Header2'])

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    assert tables[0][0] == ['Header1', 'Header2']


# --- Tests for table then list ---


def test_table_then_bullet_list(capsys):
    """Test table followed by bullet list."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_table(first_row=['Col1', 'Col2'])
        mfo.add_table_row(row=['A', 'B'])
        mfo.start_bullet_item(text='List item 1')
        mfo.start_bullet_item(text='List item 2')

    doc = silent_odt_create(capsys, func=func)
    tables = get_table_data(doc)
    assert len(tables) == 1
    all_text = get_all_text_content(doc)
    assert 'List item 1' in all_text
    assert 'List item 2' in all_text


def test_bullet_list_then_table(capsys):
    """Test bullet list followed by table."""
    def func(mfo: MultiFormatOdt) -> None:
        mfo.start_bullet_item(text='List item 1')
        mfo.start_bullet_item(text='List item 2')
        mfo.start_table(first_row=['Col1', 'Col2'])
        mfo.add_table_row(row=['A', 'B'])

    doc = silent_odt_create(capsys, func=func)
    all_text = get_all_text_content(doc)
    assert 'List item 1' in all_text
    assert 'List item 2' in all_text
    tables = get_table_data(doc)
    assert len(tables) == 1
