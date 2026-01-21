#! /usr/local/bin/python3
"""Example of writing code blocks."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def example_code_blocks(format_name: str, file_name: str) -> None:
    """Show how to write code blocks."""
    # We start by getting the MultiFormat class from the factory
    # as a context manager as we did in exampe e01_paragraph.py.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # First a paragraph to show the difference between code blocks and
        # paragraphs.
        mf.start_paragraph(text='This is a normal paragraph with some text.')
        mf.add_text('Paragraphs are not useable for showing code')
        mf.add_text('as the text is usually shown in variable width fonts,')
        mf.add_text('and line wrapping is not easy to control.')
        mf.add_text('Code blocks on the other hand are designed to show code')
        mf.add_text('in a monospace font, and line wrapping is easy to')
        mf.add_text('control.')
        mf.start_paragraph(text='Code blocks are written using the')
        mf.add_text('write_code_block() method.')
        # Then write a code block with Python code.
        code = '''
def hello_world() -> int:
    print("Hello, World!")
    print("This is another line of code.")
    return 42
'''
        mf.write_code_block(text=code, programming_language='python')
        # The complete code block is written with one function call.
        # It is not possible to add text to a code block. You have
        # to have the complete text of the code block when calling
        # write_code_block().


if __name__ == '__main__':
    example_main(example_text='Writing code blocks',
                 function=example_code_blocks)
