#! /usr/local/bin/python3
"""Example of writing a bold and italic URL in a paragraph."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from e20_url_in_paragraph import EXAMPLES_URL
from mformat.factory import create_mf


def example_url_in_paragraph_bold(format_name: str, file_name: str) -> None:
    """Show how to write a bold and italic URL in a paragraph."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    # We can pass additional arguments to the MultiFormat constructor
    # using the args parameter. This will be shown in e25_url_as_text.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.new_heading(level=1,
                       text='URL in paragraph with bold & italic example')
        # Start a paragraph.
        mf.new_paragraph(text='This is a paragraph with a URL: ')
        # add an italic URL.
        mf.add_url(text='This italic URL link to the examples', italic=True,
                   url=EXAMPLES_URL)
        # add some text between the URLs.
        mf.add_text('and')
        # add a bold URL.
        mf.add_url(text='this bold URL link to the example source code.',
                   bold=True,
                   url=f'{EXAMPLES_URL}/src')


if __name__ == '__main__':
    example_main(example_text='Writing a bold and italic URL in a paragraph',
                 function=example_url_in_paragraph_bold)
