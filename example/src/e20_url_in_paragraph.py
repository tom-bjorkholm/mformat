#! /usr/local/bin/python3
"""Example of writing a URL in a paragraph."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf

REPO_URL = 'https://bitbucket.org/tom-bjorkholm/mformat/src/master'
EXAMPLES_URL = f'{REPO_URL}/example'


def example_url_in_paragraph(format_name: str, file_name: str,
                             url_as_text: bool = False,
                             extra_text: str = '') -> None:
    """Show how to write a URL in a paragraph."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    # We can pass additional arguments to the MultiFormat constructor
    # using the args parameter. This will be shown in e25_url_as_text.py.
    with create_mf(format_name=format_name, file_name=file_name,
                   url_as_text=url_as_text) as mf:
        # Start a paragraph.
        mf.start_paragraph(text='This is a paragraph with a URL: ')
        # add a URL.
        mf.add_url(text='The examples are here.',
                   url=EXAMPLES_URL)
        mf.start_paragraph(text='The URL was added as a link using')
        mf.add_text('add_url(text, url)')
        mf.start_paragraph(text='By not specifying the text, '
                           'the URL is shows as text:')
        mf.add_url(url=EXAMPLES_URL)
        mf.start_paragraph('A paragraph can of course have multiple URLs.')
        mf.add_url(text='The source code of the examples are here.',
                   url=f'{EXAMPLES_URL}/src')
        mf.add_text('and')
        mf.add_url(text='The produced output files are here.',
                   url=f'{EXAMPLES_URL}/result')
        if extra_text:
            mf.start_paragraph(text=extra_text)


if __name__ == '__main__':
    example_main(example_text='Writing a URL in a paragraph',
                 function=example_url_in_paragraph)
