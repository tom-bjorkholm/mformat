#! /usr/local/bin/python3
"""Example of writing a URL in a numbered point list."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from e20_url_in_paragraph import EXAMPLES_URL
from mformat.factory import create_mf


def example_url_in_numbered_list(format_name: str, file_name: str) -> None:
    """Show how to write a URL in a numbered point list."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.new_heading(level=1, text='URL in numbered point list example')
        # Start a numbered point list with an item containing a URL.
        mf.new_numbered_point_item(text='A numbered point with a URL:')
        # Add a URL to the item.
        mf.add_url(text='This URL link to the examples.',
                   url=f'{EXAMPLES_URL}/src')
        # Then another numbered point with a bold URL
        mf.new_numbered_point_item(text='A numbered point with a bold URL:')
        # Plain text output has no visible bold/italic, but this code
        # still runs. Bold/italic are visible in other formats.
        # Add a bold URL to the item.
        mf.add_url(text='This bold URL link to the example source code.',
                   bold=True, url=f'{EXAMPLES_URL}/src')
        # Then another numbered point with an italic URL
        mf.new_numbered_point_item(text='And with an italic URL:')
        # Add an italic URL to the item.
        mf.add_url(text='This italic URL link to the examples result.',
                   italic=True, url=f'{EXAMPLES_URL}/result')
        # Last numbered point with italic and bold URL
        mf.new_numbered_point_item(text='And with an italic and bold URL:')
        # Add an italic and bold URL to the item.
        mf.add_url(text='This italic and bold URL link to the examples.',
                   italic=True, bold=True, url=f'{EXAMPLES_URL}/src')
        # The numbered point list is automatically ended when the
        # context manager is exited.


if __name__ == '__main__':
    example_main(example_text='Writing a URL in a numbered point list',
                 function=example_url_in_numbered_list)
