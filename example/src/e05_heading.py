#! /usr/local/bin/python3
"""Example of using the MultiFormat class to write a heading."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def heading_example(format_name: str,
                    file_name: str) -> None:
    """Write an example file with a heading."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to start a heading and add text to it.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name.
    # The file extension is automatically added to the file name if not
    # present.
    # We use a with statement to ensure that the file is closed properly.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # Start a heading.
        # We can add all the text of the heading in one go in this call,
        # or we can have just a little text in this call.
        # The level 1 heading is the main heading of the document.
        # The level 2 heading is a subheading of the main heading.
        # (For the markdown output to be accepted by markdownlint without
        # warning, the document should start with a level 1 heading.)
        mf.new_heading(level=1, text='This is a heading,')
        # We can also add text to the heading in multiple calls
        # using add_text.
        mf.add_text('at level 1')
        # There is no need to close the heading, it is closed automatically
        # when we start something new or when the with statement is exited.


if __name__ == "__main__":
    example_main(example_text='Heading', function=heading_example)
