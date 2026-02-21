#! /usr/local/bin/python3
"""Example of writing block quotes."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def block_quote_example(format_name: str, file_name: str) -> None:
    """Show how to write block quotes."""
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        mf.new_heading(level=1, text='Block Quote Example')
        mf.new_paragraph(text='Block quotes are used to highlight quoted text '
                         'or to draw attention to important information.')
        mf.new_heading(level=2, text='Simple Block Quote')
        mf.new_block_quote(text='This is a simple block quote. Block quotes '
                           'are visually distinguished from regular text '
                           'with indentation and/or styling depending on '
                           'the output format.')
        mf.new_heading(level=2, text='Block Quote with Formatting')
        mf.new_block_quote(text='Block quotes can have ', bold=False)
        mf.add_text(text='bold', bold=True)
        mf.add_text(text=' and ')
        mf.add_text(text='italic', italic=True)
        mf.add_text(text=' text just like paragraphs.')
        mf.new_heading(level=2, text='Block Quote with URL')
        mf.new_block_quote(text='For more information, visit ')
        mf.add_url(url='http://example.com', text='Example Website')
        mf.add_text(text=' for details.')
        mf.new_heading(level=2, text='Block Quote with Code')
        mf.new_block_quote(text='The function ')
        mf.add_code_in_text(text='new_block_quote()')
        mf.add_text(text=' starts a new block quote, and ')
        mf.add_code_in_text(text='add_text()')
        mf.add_text(text=' adds more text to it.')
        mf.new_paragraph(text='Block quotes cannot be nested. Starting a new '
                         'block quote while inside one ends the current quote '
                         'and starts a fresh one.')


if __name__ == '__main__':
    example_main(example_text='Block quote',
                 function=block_quote_example)
