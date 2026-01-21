#! /usr/local/bin/python3
"""Example of writing a table in one call."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#
from e01_paragraph import example_main
from mformat.factory import create_mf


def example_table_at_once(format_name: str, file_name: str) -> None:
    """Show how to write a complete table in one call."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # The table data
        table_data: list[list[str]] = [
            ['Name', 'Age', 'City'],
            ['John', '25', 'New York'],
            ['Jane', '30', 'Los Angeles'],
            ['Jim', '35', 'Chicago'],
        ]
        # Write the table
        mf.write_complete_table(table=table_data)


if __name__ == '__main__':
    example_main(example_text='Writing a table in one call',
                 function=example_table_at_once)
