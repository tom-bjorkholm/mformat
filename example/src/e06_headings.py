#! /usr/local/bin/python3
"""Example of using the MultiFormat class to write headings."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def headings_example(format_name: str,
                     file_name: str) -> None:
    """Write an example file with several headings."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to write multiple headings at different levels.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name.
    # The file extension is automatically added to the file name if not
    # present.
    # We use a with statement to ensure that the file is closed properly.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # Start a heading at level 1 just as in the example e05_heading.py.
        mf.new_heading(level=1, text='This is the first heading,')
        # We can also add text to the heading in multiple calls
        # using add_text.
        mf.add_text('it is at level 1')
        # There is no need to close the heading, it is closed automatically
        # when we start something new or when the with statement is exited.
        mf.new_heading(level=2, text='This is the second heading,')
        mf.add_text('it is at level 2')
        mf.new_heading(level=3, text='This is the third heading,')
        mf.add_text('it is at level 3')
        # We add a paragraph under this heading with some text.
        mf.new_paragraph('We can add text to headings with add_text(),')
        mf.add_text('just as we can add text to paragraphs.')
        mf.add_text('New headings can be added at any level.')
        mf.add_text('The argument smart_ws is used to control how')
        mf.add_text('whitespace is handled in headings just as in paragraphs.')
        mf.new_paragraph('new_heading() also obeys the arguments bold '
                         'and italic, just as in paragraphs.')
        mf.add_text('However, they make less sense for headings.')
        mf.add_text('Explicitly setting bold or italic on a heading may')
        mf.add_text('not produce the expected readability, as the heading')
        mf.add_text('has formatting from the heading definition that is')
        mf.add_text('specific to the output format.')
        # We add another heading at level 2 just as above.
        mf.new_heading(level=2,
                       text='The fourth heading is again at level 2')


if __name__ == "__main__":
    example_main(example_text='Headings', function=headings_example)
