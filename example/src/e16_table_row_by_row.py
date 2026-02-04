#! /usr/local/bin/python3
"""Example of writing a table row by row."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#
from e01_paragraph import example_main
from mformat.factory import create_mf


NOTE = '''
Note: As the rows are added and written one by one, the library
cannot know the width of columns in future rows, this will
make markdown formatted output look a bit odd when reading
the markdown file, however any further formatting from markdown
will hide this and make the table look as expected.
'''.replace('\n', ' ')


def example_table_row_by_row(format_name: str, file_name: str) -> None:
    """Show how to write a table row by row."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.start_heading(level=1, text='Table row by row example')
        # Start a table.
        mf.start_table(first_row=['Name', 'Age', 'City'])
        # Add a row.
        mf.add_table_row(row=['John', '25', 'New York'])
        # Add a row.
        mf.add_table_row(row=['Jane', '30', 'Los Angeles'])
        # Add a row.
        mf.add_table_row(row=['Jim', '35', 'Chicago'])
        # Table is automatically ended when the context manager is exited,
        # or when we start something else.
        mf.start_paragraph(text=NOTE)


if __name__ == '__main__':
    example_main(example_text='Writing a table row by row',
                 function=example_table_row_by_row)
