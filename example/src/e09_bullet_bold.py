#! /usr/local/bin/python3
"""Example of using the MultiFormat class to write a bullet list."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def bullet_bold_example(format_name: str,
                        file_name: str) -> None:
    """Write an example file with a bullet list with bold text."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to write a bullet list with bold and italic text.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as in e01_paragraph.py.
    # We use a with statement to ensure that the file is closed properly.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # To start a bullet list we simple start a bullet point item.
        # It will not be bold or italic unless we specify it.
        mf.start_bullet_item('This is the first bullet point item.')
        mf.add_text('This is not bold or italic.')
        mf.add_text('However, this bold text is added to it.', bold=True)
        mf.add_text('And this italic text is added to it.', italic=True)
        mf.start_bullet_item('This is the bold bullet point item.', bold=True)
        mf.add_text('This non-bold text is added to it.')
        mf.start_bullet_item('This is the italic bullet point item.',
                             italic=True)
        mf.add_text('This non-italic text is added to it.')
        mf.start_bullet_item('This is the bold and italic bullet point item.',
                             bold=True, italic=True)
        mf.add_text('This non-bold and non-italic text is added to it.')
        mf.start_bullet_item('This is in item in a nested bullet list.',
                             level=2)
        mf.add_text('Bold text added to it.', bold=True)
        mf.add_text('And italic text added to it.', italic=True)
        mf.start_bullet_item('Second nested bullet point item.', bold=True,
                             italic=True)
        mf.add_text('This non-bold and non-italic text is added to it.')
        mf.add_text('And bold', bold=True)
        mf.add_text('and italic text added to it.', italic=True)


if __name__ == "__main__":
    example_main(example_text='Headings', function=bullet_bold_example)
