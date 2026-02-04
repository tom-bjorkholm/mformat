#! /usr/local/bin/python3
"""Example of using the MultiFormat class to write a bullet list."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def numbered_nested_example(format_name: str,
                            file_name: str) -> None:
    """Write an example file with a nested numbered list."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to write a nested numbered list.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as in e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.start_heading(level=1, text='Nested numbered list example')
        # To start a numbered list we simple start a numbered list item.
        mf.start_numbered_point_item('This is the first numbered item.')
        mf.add_text('If we do not specify the level, it is at the same')
        mf.add_text('level as the previous item - and when there is no')
        mf.add_text('previous item, it is at level 1.')
        mf.start_numbered_point_item('This is the second numbered item.')
        mf.start_numbered_point_item('This is the third numbered item.',
                                     level=2)
        mf.add_text('This is the first item at level 2.')
        mf.start_numbered_point_item('Another item at level 2.',
                                     level=2)
        mf.start_numbered_point_item('And an item at level 3.',
                                     level=3)
        mf.start_numbered_point_item('The final item is back at level 1.',
                                     level=1)


if __name__ == "__main__":
    example_main(example_text='Headings', function=numbered_nested_example)
