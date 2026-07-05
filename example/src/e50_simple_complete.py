#! /usr/local/bin/python3
"""Simple complete example."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf


def multi_format_example(format_name: str,  # pylint: disable=too-many-statements # noqa: E501
                         file_name: str) -> None:
    """Write an example file with most features of the multi format class."""
    # This example demonstrates the usage of the multi format class.
    # It shows how to write headings, paragraphs, URLs, bold and italic text,
    # bullet lists, and code blocks.
    # It also shows how to add URLs to text, and how to format URLs as text.
    # It also shows how to add tables.
    # It also shows how to add code blocks.
    # It also shows how to add bullet and numberedlists.
    #
    # Use the MultiFormat class as a context manager, using a with statement.
    # This ensures that the file is closed properly.
    #
    # The MultiFormat class has methods for starting a new type of item.
    # We never end an item type, instead we start a new item type.
    #
    # We start by getting a formatter from the factory, using the format name
    # and the file name.
    with create_mf(format_name=format_name, file_name=file_name) as mf:
        # Write a main heading.
        mf.new_heading(level=1, text='Main heading of example')
        # Start a paragraph. This automatically closes the heading.
        mf.new_paragraph('With new_paragraph we can start a paragraph.')
        # Add text to the paragraph.
        mf.add_text('With add_text we can add text to the paragraph.')
        # Write a sub heading.
        mf.new_heading(level=2, text='Sub heading of example')
        # Add text to the sub heading.
        mf.add_text('where add_text adds text to the sub heading')
        # Start a new paragraph.
        mf.new_paragraph('Whenever we start a new item type the')
        # Add text to the paragraph.
        mf.add_text('previous item type is automatically closed.')
        mf.add_text('Add text does not automatically close the previous')
        mf.add_text('item type, instead it just adds text to that item.')
        # For any text we can add bold and italic formatting.
        # Plain text output has no visible bold/italic, but this code
        # still runs. Bold/italic are visible in other formats.
        mf.add_text('There is never a need to close an item type.',
                    bold=True, italic=True)
        # Starting a heading automatically closes the paragraph.
        mf.new_heading(level=2, text='Heading with URL to')
        # Add a URL to the heading.
        url = 'https://github.com/tom-bjorkholm/mformat/blob/master/'
        url += 'example/src/e50_simple_complete.py'
        mf.add_url(url=url, text='the example file')
        # Start a new paragraph.
        mf.new_paragraph('As you can see, we can add URLs to both')
        mf.add_text('headings and paragraphs.')
        mf.add_text('It is also possible to add URLs to text,')
        mf.add_text('for instance the URL to the example file is added')
        mf.add_text('here.')
        # Add a URL to the text.
        mf.add_url(url=url, text='The same example file')
        mf.new_paragraph('URLs can (depending on the format) be formatted ' +
                         'as clickable URLs or as text.')
        mf.add_text('To force URLs to be formatted as text, ' +
                    'set url_as_text=True.')
        mf.new_paragraph('You may have noticed that we have not worried')
        mf.add_text('about about the whitespace between text.')
        mf.add_text('This is because we use a smart whitespace handling.')
        # We can disable smart whitespace handling by setting smart_ws=False.
        mf.add_text('If we disable smart whitespace handling,', smart_ws=False)
        mf.add_text('we need to handle whitespace manually, ', smart_ws=False)
        mf.add_text(' which can be cumbersome as shown here.', smart_ws=False)
        # Headubg for lists
        mf.new_heading(level=2, text='Bullet lists and numbered lists')
        # Start a bullet list.
        # If we do not specify a level, it will be the current level
        # or a new list is started if there is no current level.
        mf.new_bullet_item('Item 1')
        mf.new_bullet_item('Item 2')
        # If we specify a level, item will on that level
        # Use this to created nested lists.
        mf.new_bullet_item('Item 2.1', level=2)
        mf.new_bullet_item('Item 2.2')
        # To move up one or several levels in a nested list
        # we need to specify the level.
        mf.new_bullet_item('Item 3', level=1)
        # Start a numbered list.
        mf.new_numbered_point_item('Item 1')
        mf.new_numbered_point_item('Item 2 with some more text.')
        mf.add_text('Naturally more text can be added in the same ' +
                    'item using add_text.')
        mf.new_numbered_point_item('Item 3')
        mf.new_numbered_point_item('Item 3.1', level=2)
        # Numbered and bullet lists can be nested.
        mf.new_bullet_item('Item 3.1.1', level=3)
        # If we do not specify a level, it will be the current level
        mf.new_bullet_item('Item 3.1.1')
        mf.new_numbered_point_item('Item 4', level=1)
        # Then a simple demo of a table, written row by row.
        mf.new_heading(level=2, text='A simple table')
        mf.new_table(first_row=['Full Name', 'Street and Number',
                                'City or Town'],
                     bold=True)
        mf.add_table_row(['John Doe', '123 Main St', 'Anytown'],
                         italic=True)
        mf.add_table_row(['Jane Doe', '456 Main St', 'Anytown'])
        mf.add_table_row(['Jim Doe', '789 Main St', 'The Village'])
        mf.new_heading(level=3, text='Another table')
        # We can also write a table all at once.
        table: list[list[str]] = [['Name', 'Age', 'Gender'],
                                  ['John Doe', '30', 'Male'],
                                  ['Jane Doe', '25', 'Female'],
                                  ['Jim Doe', '35', 'Male']]
        mf.write_complete_table(table=table,
                                bold_first_row=True)
        mf.new_heading(level=2, text='Finally code blocks')
        mf.new_paragraph('Code blocks are written with write_code_block.')
        # We can also write a code block.
        code = 'def my_function(x: int) -> int:\n'
        code += '    return x + 1\n\n'
        code += 'print(my_function(1))'
        mf.write_code_block(text=code, programming_language='python')


if __name__ == "__main__":
    example_main(example_text='Simple complete',
                 function=multi_format_example)
