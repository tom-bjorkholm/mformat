#! /usr/local/bin/python3
"""Example of writing a URL in a heading."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from e20_url_in_paragraph import EXAMPLES_URL
from mformat.factory import create_mf


def example_url_in_heading(format_name: str, file_name: str) -> None:
    """Show how to write a URL in a heading, both italic and bold."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.new_heading(level=1, text='URL in heading example')
        # Start a heading with a URL.
        mf.new_heading(text='A heading with a URL:', level=1)
        # Add a URL to the heading.
        mf.add_url(text='This URL link to the examples.',
                   url=EXAMPLES_URL)
        # Then another heading with a bold URL
        mf.new_heading(text='A heading with a bold URL:', level=2)
        # Add a bold URL to the heading.
        mf.add_url(text='This bold URL link to the example source code.',
                   bold=True, url=f'{EXAMPLES_URL}/src')
        # Then another heading with an italic URL
        mf.new_heading(text='A heading with an italic URL:', level=2)
        # Add an italic URL to the heading.
        mf.add_url(text='This italic URL link to the examples result.',
                   italic=True, url=f'{EXAMPLES_URL}/result')
        # Last heading with italic and bold URL
        mf.new_heading(text='And with an italic and bold URL:', level=2)
        # Add an italic and bold URL to the heading.
        mf.add_url(text='This italic and bold URL link to the examples.',
                   italic=True, bold=True, url=f'{EXAMPLES_URL}/src')
        mf.new_paragraph(text='The add_url function can be used')
        mf.add_text('to add a URL to a heading, as well as to paragraphs,')
        mf.add_text('bullet lists, and numbered point lists.')


if __name__ == '__main__':
    example_main(example_text='Writing a URL in a heading',
                 function=example_url_in_heading)
