#! /usr/local/bin/python3
"""Example of using the MultiFormat class to write nested bullet lists."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def bullets_example(format_name: str,
                    file_name: str) -> None:
    """Write an example file with a nestedbullet list."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to write nested bullet lists.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as in e01_paragraph.py.
    # We use a with statement to ensure that the file is closed properly.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.new_heading(level=1, text='Nested bullet list example')
        # To start a bullet list we simple start a bullet point item.
        mf.new_bullet_item('This is the first bullet point item')
        mf.add_text('at level 1.')
        # We can specify the level of the bullet point item.
        # If we do not specify the level, it is at the same level as the
        # previous item.
        # By specifying the level, we can create nested bullet lists.
        mf.new_bullet_item('This is the second bullet point item.', level=2)
        mf.add_text('This time at level 2.')
        mf.new_bullet_item('Another point item without specifying level.')
        mf.add_text('This means that it is at the same level as the previous'
                    ' item.')
        mf.new_bullet_item('This is a bullet point item at level 3.',
                           level=3)
        mf.new_bullet_item('This is final bullet point item.',
                           level=1)
        mf.add_text('This time at level 1')


if __name__ == "__main__":
    example_main(example_text='Nested bullet list', function=bullets_example)
