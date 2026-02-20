#! /usr/local/bin/python3
"""Example of writing code in a heading and list items."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def code_in_heading_example(format_name: str, file_name: str) -> None:
    """Show how to write code in a heading and list items."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.new_heading(level=1, text='Code in heading example')
        # Write a word of code in the heading.
        mf.add_code_in_text(text='add_code_in_text()')
        # Start a new bullet list with a 2 bullet items.
        # Each bullet item contains a word of code.
        mf.new_bullet_item(text='Bullet items can also contain code:')
        mf.add_code_in_text(text='example()')
        # Start a new numbered point list with a 1 numbered point item.
        # The numbered point item contains a word of code.
        mf.new_numbered_point_item(text='Numbered items can also ' +
                                   'contain code:')
        mf.add_code_in_text(text='example()')


if __name__ == '__main__':
    example_main(example_text='Writing code in a heading',
                 function=code_in_heading_example)
