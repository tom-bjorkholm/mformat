#! /usr/local/bin/python3
"""Paragraphs example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main, NO_HEADING_TEXT
from mformat.factory import create_mf


def paragraphs_bold_example(format_name: str,
                            file_name: str) -> None:
    """Write an example file with several paragraphs and bold text."""
    # This example demonstrates the basic usage of the multi format class.
    # It shows how to add bold and italic text to paragraphs.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as shown in the example file e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # Start a paragraph with first sentence in bold.
        mf.new_paragraph('With new_paragraph we can start a paragraph '
                         'with the first sentence in bold.',
                         bold=True)
        # Add some more text to the paragraph this time not in bold.
        mf.add_text('Use add_text to add text without bold to the paragraph.')
        # Add some more text to the paragraph this time in italic.
        mf.add_text('Use add_text to add text in italic to the paragraph.',
                    italic=True)
        # Add some more text to the paragraph this time in bold and italic.
        mf.add_text('Use add_text to add text in bold and italic.',
                    bold=True, italic=True)
        # Let us add a second paragraph with first sentence in italic.
        mf.new_paragraph('With new_paragraph we can start a second '
                         'paragraph with the first sentence in italic.',
                         italic=True)
        # Add some more text to the second paragraph this time not in italic.
        mf.add_text('Use add_text to add text without italic to the '
                    'second paragraph.')
        # Add some more text to the second paragraph this time in bold.
        mf.add_text('Use add_text to add text in bold to the second '
                    'paragraph.', bold=True)
        # Add some more text to the second paragraph this time
        # in italic and bold.
        mf.add_text('Use add_text to add text in italic and bold to the '
                    'second paragraph.', italic=True, bold=True)
        mf.new_paragraph(NO_HEADING_TEXT, bold=True)


if __name__ == "__main__":
    example_main(example_text='Paragraphs bold',
                 function=paragraphs_bold_example)
