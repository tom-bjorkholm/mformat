#! /usr/local/bin/python3
"""Example of nesting numbered point list with bullet points."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#
from e01_paragraph import example_main
from mformat.factory import create_mf


def example_nest_numbers_bullets(format_name: str, file_name: str) -> None:
    """Show how to nest numbered points with bullet points."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # See example e05_heading.py for how to write a heading.
        mf.start_heading(level=1, text='Nesting points example')
        # First a few numbered point list items.
        # The lists are created as needed for the items.
        mf.start_numbered_point_item('First item')
        mf.start_numbered_point_item('Second item')
        mf.add_text('with some bold text', bold=True)
        # We get nesting by specifying a level.
        mf.start_bullet_item('First bullet', level=2)
        # default level is current level, so this is also level 2.
        mf.start_bullet_item('Second bullet is italic', italic=True)
        mf.add_text('with some bold', bold=True)
        mf.add_text('and some non-bold and non-italic text')
        mf.start_numbered_point_item('First item in third level', level=3)
        mf.start_numbered_point_item('Second item in third level')
        # By specifying a lower level we end some nested lists.
        mf.start_numbered_point_item('Third item on first level.', level=1)
        mf.add_text('By specifying a lower level we end some nested lists.')


if __name__ == '__main__':
    example_main(example_text='Nesting numbered and bullet points',
                 function=example_nest_numbers_bullets)
