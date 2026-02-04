#! /usr/local/bin/python3
"""Example of using the MultiFormat class to write a bullet list."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def bullet_example(format_name: str,
                   file_name: str) -> None:
    """Write an example file with a bullet list."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to write a bullet list.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as in e01_paragraph.py.
    # We use a with statement to ensure that the file is closed properly.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.start_heading(level=1, text='Bullet list example')
        # To start a bullet list we simple start a bullet point item.
        mf.start_bullet_item('This is the first bullet point item.')
        mf.start_bullet_item('This is the second bullet point item.')
        mf.add_text('We can add text to the bullet point items with')
        mf.add_text('add_text(), just as we can add text to paragraphs.')
        mf.start_bullet_item('This is the third bullet point item.')


if __name__ == "__main__":
    example_main(example_text='Headings', function=bullet_example)
