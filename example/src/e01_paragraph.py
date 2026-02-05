#! /usr/local/bin/python3
"""Paragraph example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Callable
import argparse
from mformat.factory import create_mf, list_registered_mf


NO_HEADING_TEXT = '(As this example does not have a heading the ' \
    'generated markdown file will not have a heading. If markdownlint ' \
    'is used on the generated markdown file it will report an error ' \
    'for the missing heading.)'


def paragraph_example(format_name: str,
                      file_name: str) -> None:
    """Write an example file with a paragraph."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to start a paragraph and add text to it.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name.
    # The file extension is automatically added to the file name if not
    # present.
    # We use a with statement to ensure that the file is closed properly.
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
        mf.add_text(NO_HEADING_TEXT)
        # There is no need to close the paragraph, it is closed automatically
        # when we start something new or when the with statement is exited.


def example_all(file_name: str, function: Callable[[str, str], None]) -> None:
    """Write example files for all formats using the multi format class."""
    #
    # This demonstrates that the same code can be used to write to
    # different formats, only by changing the format name.
    # list_registered_mf() returns a list of all registered format names.
    # In mformat package we currectly have formats "html" and "md".
    # If mformat-ext package is installed we will also have formats
    # "docx" and "odt".
    #
    for format_name in list_registered_mf():
        function(format_name, file_name)


def example_main(example_text: str,
                 function: Callable[[str, str], None]) -> None:
    """Parse command line arguments and run the example."""
    desc = f'{example_text} example of using package mformat.'
    parser = argparse.ArgumentParser(description=desc)
    # Show the correct case for the format names in the help message.
    help_choices = list_registered_mf()
    help_choices.append('all')
    format_help = 'The name of the format to use. Available formats: ' + \
        ', '.join(help_choices)
    # Allow user to also use lower case or upper case format names in the
    # command line.
    choices = list_registered_mf(lower=True, upper=True)
    choices.append('all')
    parser.add_argument('-f', '--format', type=str,
                        help=format_help,
                        required=True, choices=choices)
    parser.add_argument('-o', '--output', type=str,
                        help='The name of the output file to write to.',
                        required=True)
    args = parser.parse_args()
    if args.format == 'all':
        example_all(args.output, function)
    else:
        function(args.format, args.output)


if __name__ == "__main__":
    example_main(example_text='Paragraph', function=paragraph_example)
