#! /usr/local/bin/python3
"""Example of writing a forcing URLs to be shown as text."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e20_url_in_paragraph import example_url_in_paragraph
from e01_paragraph import example_main


def example_url_as_text(format_name: str, file_name: str) -> None:
    """Show how to force URLs to be shown as text."""
    # The code in e20_url_in_paragraph.py shows how to write a URL in a
    # paragraph.
    # We can force the URLs to be shown as text by passing the url_as_text
    # argument to the MultiFormat constructor as an extra argument to the
    # create_mf factoryfunction.
    # This example just passes the argument to the example_url_in_paragraph
    # function in e20_url_in_paragraph.py and it will produce text output
    # instead of a clickable links.
    extra_text = 'The URLs are shown as text instead of clickable links. '
    extra_text += 'This might be useful when you want to copy the URLs to '
    extra_text += 'the clipboard and paste them into another application. '
    extra_text += 'This is done by passing the url_as_text argument to the '
    extra_text += 'create_mf factory function.'
    example_url_in_paragraph(format_name=format_name, file_name=file_name,
                             url_as_text=True, extra_text=extra_text)


if __name__ == '__main__':
    example_main(example_text='Writing URLs as text',
                 function=example_url_as_text)
