#! /usr/local/bin/python3
"""Example of using the MultiFormat class to write a bullet list."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def numbered_list_example(format_name: str,
                          file_name: str) -> None:
    """Write an example file with a numbered list."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to write a numbered list.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as in e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # To start a numbered list we simple start a numbered list item.
        mf.start_numbered_point_item('This is the first numbered item.')
        mf.add_text('We can add text to the numbered items with add_text(),')
        mf.add_text('just as we can add text to paragraphs.')
        mf.start_numbered_point_item('This is the second numbered item.')
        mf.start_numbered_point_item('This is the third numbered item.')


if __name__ == "__main__":
    example_main(example_text='Headings', function=numbered_list_example)
