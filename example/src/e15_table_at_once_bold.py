#! /usr/local/bin/python3
"""Example of writing a table in one call with bold text in first row."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#
from e01_paragraph import example_main
from mformat.factory import create_mf


def example_table_at_once_bold(format_name: str, file_name: str) -> None:
    """Show how to write a complete table in one call with bold first row."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # The table data
        table_data: list[list[str]] = [
            ['Name', 'Age', 'City'],
            ['Janet', '25', 'New York'],
            ['Jacob', '30', 'Los Angeles'],
            ['Jill', '35', 'Chicago'],
        ]
        # Write explanation before the table.
        mf.start_paragraph('This is a table with bold text in first row.')
        # Write the table
        mf.write_complete_table(table=table_data, bold_first_row=True)
        # Now we show italics and bold in the first row.
        mf.start_paragraph('Now a table with italics and bold in the '
                           'first row.')
        mf.write_complete_table(table=table_data, bold_first_row=True,
                                italic_first_row=True)


if __name__ == '__main__':
    example_main(example_text='Writing a table in one call (bold first row)',
                 function=example_table_at_once_bold)
