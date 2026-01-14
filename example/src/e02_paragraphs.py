#! /usr/local/bin/python3
"""Paragraphs example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def paragraphs_example(format_name: str,
                       file_name: str) -> None:
    """Write an example file with several paragraphs."""
    # This example shows how to start several paragraphs and add text to them.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as shown in the example file e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # Start a paragraph.
        # We can add all the text of the paragraph in one go in this call,
        # or we can have just a little text in this call.
        mf.start_paragraph('With start_paragraph we can start a paragraph.')
        # We can also add text to the paragraph in multiple calls
        # using add_text.
        mf.add_text('With add_text we can add text to the paragraph.')
        mf.add_text('We can also add text to the paragraph in multiple calls')
        mf.add_text('using add_text.')
        # There is no need to close the paragraph, it is closed automatically
        # when we start something new or when the with statement is exited.
        # Start a second paragraph - this automatically closes the first paragraph.
        mf.start_paragraph('With start_paragraph we can start a second paragraph.')
        # We can also add text to the second paragraph in multiple calls
        # using add_text.
        mf.add_text('With add_text we can add text to the second paragraph.')
        mf.add_text('just as we did with the first paragraph.')
        # There is no need to close the second paragraph, it is closed automatically
        # when we start something new or when the with statement is exited.


if __name__ == "__main__":
    example_main(example_text='Paragraphs', function=paragraphs_example)
