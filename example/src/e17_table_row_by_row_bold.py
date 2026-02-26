#! /usr/local/bin/python3
"""Example of writing a table row by row with bold and italic text."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#
from e01_paragraph import example_main
from e16_table_row_by_row import NOTE
from mformat.factory import create_mf


def example_table_row_by_row_bold(format_name: str, file_name: str) -> None:
    """Show how to write a table row by row with bold and italic text."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.new_heading(level=1,
                       text='Table row by row with bold & italic example')
        # Start first row of table with bold first line.
        # Plain text output has no visible bold/italic, but this code
        # still runs. Bold/italic are visible in other formats.
        mf.new_table(first_row=['City', 'Country', 'Size'], bold=True)
        # Add a row.
        mf.add_table_row(row=['Mariehamn', 'Finland', 'Small'])
        mf.add_table_row(row=['Copenhagen', 'Denmark', 'Large'], italic=True)
        mf.add_table_row(row=['Tokyo', 'Japan', 'Huge'], bold=True,
                         italic=True)
        # Table is automatically ended when the context manager is exited,
        # or when we start something else, like another table.
        mf.new_table(first_row=['Capital', 'Country', 'Continent'],
                     italic=True)
        mf.add_table_row(row=['Oslo', 'Norway', 'Europe'])
        mf.add_table_row(row=['Tokyo', 'Japan', 'Asia'])
        mf.add_table_row(row=['Berlin', 'Germany', 'Europe'], bold=True)
        mf.add_table_row(row=['Kairo', 'Egypt', 'Africa'])
        mf.add_table_row(row=['Brussels', 'Belgium', 'Europe'], bold=True,
                         italic=True)
        mf.new_paragraph(text=NOTE)


if __name__ == '__main__':
    example_main(example_text='Writing a table row by row (bold and italic)',
                 function=example_table_row_by_row_bold)
