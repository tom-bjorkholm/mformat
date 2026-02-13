#! /usr/local/bin/python3
"""Paragraphs example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main, NO_HEADING_TEXT
from mformat.factory import create_mf


def paragraphs_smart_ws_example(format_name: str,
                                file_name: str) -> None:
    """Write an example file with smart whitespace handling."""
    # This example demonstrates how to use smart whitespace handling.
    # We start by getting a formatter from the factory, using the format name
    # and the output file name as shown in the example file e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # Start a paragraph.
        # We can add all the text of the paragraph in one go in this call,
        # or we can have just a little text in this call.
        mf.new_paragraph('With new_paragraph we can start a paragraph.')
        # We can also add text to the paragraph in multiple calls
        # using add_text. The default smart whitespace handling is enabled
        # so we do not need to add whitespace between text fragments from
        # different calls to add_text or new_paragraph calls.
        mf.add_text('Thanks to smart whitespace handling, we do not need')
        mf.add_text('to add whitespace between text fragments from different')
        mf.add_text('calls to add_text ')
        # If we have extra whitespace, it will be consolidated
        # into a single space.
        mf.add_text(' or new_paragraph calls. ')
        mf.add_text(' If we have extra whitespace, it will be consolidated')
        mf.add_text('into a single space.')
        # Start a second paragraph with smart whitespace handling disabled
        # in the new_paragraph call.
        mf.new_paragraph('With new_paragraph we can start another '
                         'paragraph. ',
                         smart_ws=False)
        # We can also add text to the second paragraph in multiple calls
        # using add_text. The smart whitespace handling is disabled by setting
        # smart_ws=False so whitespace between text fragments from different
        # calls to add_text or new_paragraph calls will be preserved
        mf.add_text(' With smart_ws=False the whitespace between text ',
                    smart_ws=False)
        mf.add_text(' fragments will be preserved.', smart_ws=False)
        mf.add_text('So we can have no whitespae or multiple spaces',
                    smart_ws=False)
        mf.add_text(' between text fragments if we want to.', smart_ws=False)
        # Whenever smart_ws is not specified, it will be True as default.
        # So the following call will have smart whitespace handling enabled.
        mf.add_text('We can at any time switch on smart whitespace handling')
        mf.add_text('by ommitting the smart_ws=False argument,')
        # Naturally we can also explicitly set smart_ws=True.
        mf.add_text('or by explicitly setting smart_ws=True.', smart_ws=True)
        mf.new_paragraph(NO_HEADING_TEXT, bold=True)


if __name__ == "__main__":
    example_main(example_text='Smart whitespace',
                 function=paragraphs_smart_ws_example)
