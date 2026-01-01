#! /usr/local/bin/python3
"""Test the mformat_md module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import pytest
from check_capsys import check_capsys
from test_helpers import (
    run_with_context_manager,
    run_protected_method,
    action_complex_nested_bullet_structure
)
from mformat.mformat_md import MultiFormatMd
from mformat.mformat import FormatterDescriptor, MultiFormatState
from mformat.factory import create_mf


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatMd.file_name_extension() == '.md'
    check_capsys(capsys)


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatMd.get_arg_desciption() == \
        FormatterDescriptor(name='md', mandatory_args=[],
                            optional_args=[])
    check_capsys(capsys)


@pytest.mark.parametrize('method, arg, expected',
                         [('_write_file_prefix', None, ''),
                          ('_write_file_suffix', None, ''),
                          ('_start_paragraph', None, '\n'),
                          ('_end_paragraph', None, '\n'),
                          ('_write_text',
                           ('test', MultiFormatState.PARAGRAPH,
                            False, False), 'test'),
                          ('_write_text',
                           ('test\ntest', MultiFormatState.PARAGRAPH,
                            False, False), 'test\ntest'),
                          ('_write_text',
                           ('bold', MultiFormatState.PARAGRAPH,
                            True, False), '**bold**'),
                          ('_write_text',
                           ('italic', MultiFormatState.PARAGRAPH,
                            False, True), '*italic*'),
                          ('_write_text',
                           ('both', MultiFormatState.PARAGRAPH,
                            True, True), '***both***')])
def test_methods(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                 method, arg, expected):
    """Test the trivial methods of the MultiFormatMd class."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with MultiFormatMd(file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            if arg is not None:
                if isinstance(arg, tuple):
                    getattr(mfd, method)(*arg)
                else:
                    getattr(mfd, method)(text=arg)
            else:
                getattr(mfd, method)()
            assert mfd.state == MultiFormatState.EMPTY
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)


@pytest.mark.parametrize('text, expected',
                         [('test', '\ntest\n'),
                          ('test\ntest', '\ntest\ntest\n')])
def test_start_paragraph(capsys, text, expected):
    """Test the start_paragraph method."""
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test.md'
        with create_mf('md', file_name=fname) as mfd:
            assert type(mfd).__name__ == 'MultiFormatMd'
            assert mfd.state == MultiFormatState.EMPTY
            mfd.start_paragraph(text=text)
            assert mfd.state == MultiFormatState.PARAGRAPH
        with open(fname, 'rt', encoding='utf-8') as file:
            assert file.read() == expected
        check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('bold text', True, False, '\n**bold text**\n'),
                          ('italic text', False, True, '\n*italic text*\n'),
                          ('both', True, True, '\n***both***\n')])
def test_start_paragraph_formatting(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                                    text, bold, italic, expected):
    """Test the start_paragraph method with bold and italic."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        assert mfd.state == MultiFormatState.EMPTY
        mfd.start_paragraph(text=text, bold=bold, italic=italic)
        assert mfd.state == MultiFormatState.PARAGRAPH

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected',
                         [('http://example.com', None, False, False,
                           '[http://example.com](http://example.com)'),
                          ('http://test.org', 'link text', False, False,
                           '[link text](http://test.org)'),
                          ('http://test.org', 'link', True, False,
                           '**[link](http://test.org)**'),
                          ('http://test.org', 'link', False, True,
                           '*[link](http://test.org)*'),
                          ('http://test.org', 'link', True, True,
                           '***[link](http://test.org)***')])
def test_write_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                   url, text, bold, italic, expected):
    """Test the _write_url method."""
    txt = run_protected_method('md', '.md', '_write_url',
                               (url, text, MultiFormatState.PARAGRAPH,
                                bold, italic))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           '\n[http://example.com](http://example.com)\n'),
                          ('http://test.org', 'link text',
                           '\n[link text](http://test.org)\n')])
def test_add_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url, text, expected):
    """Test the add_url method."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           '\nhttp://example.com\n'),
                          ('http://test.org', 'See here',
                           '\nSee here http://test.org\n')])
def test_add_url_as_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         url, text, expected):
    """Test the add_url method with url_as_text=True."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    txt = run_with_context_manager('md', '.md', test_action,
                                   url_as_text=True)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, expected_prefix',
                         [(1, '# '),
                          (2, '## '),
                          (3, '### '),
                          (4, '#### '),
                          (5, '##### '),
                          (6, '###### ')])
def test_start_heading(capsys, level, expected_prefix):
    """Test the _start_heading method."""
    txt = run_protected_method('md', '.md', '_start_heading', (level,))
    assert txt == expected_prefix
    check_capsys(capsys)


def test_end_heading(capsys):
    """Test the _end_heading method."""
    txt = run_protected_method('md', '.md', '_end_heading', (1,))
    assert txt == '\n'
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, expected',
                         [(1, 'Main Title', '# Main Title\n'),
                          (2, 'Subtitle', '## Subtitle\n'),
                          (3, 'Section', '### Section\n')])
def test_heading_integration(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             level, text, expected):
    """Test complete heading creation."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=level, text=text)

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, bold, italic, expected',
                         [(1, 'Bold Title', True, False,
                           '# **Bold Title**\n'),
                          (2, 'Italic Title', False, True,
                           '## *Italic Title*\n'),
                          (3, 'Both', True, True,
                           '### ***Both***\n')])
def test_heading_formatting(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                            level, text, bold, italic, expected):
    """Test heading with bold and italic formatting."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=level, text=text, bold=bold, italic=italic)

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == expected
    check_capsys(capsys)


def test_heading_add_text(capsys):
    """Test adding text to a heading."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=1, text='Title')
        mfd.add_text(text=' and more')

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == '# Title and more\n'
    check_capsys(capsys)


def test_heading_add_url(capsys):
    """Test adding URL to a heading."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=2, text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == '## Check [this link](http://example.com)\n'
    check_capsys(capsys)


def test_heading_then_paragraph(capsys):
    """Test heading followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=1, text='Title')
        mfd.start_paragraph('Some text')

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == '# Title\n\nSome text\n'
    check_capsys(capsys)


def test_multiple_headings(capsys):
    """Test multiple headings."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=1, text='Main')
        mfd.start_heading(level=2, text='Sub')
        mfd.start_heading(level=3, text='Subsub')

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == '# Main\n## Sub\n### Subsub\n'
    check_capsys(capsys)


def test_heading_paragraph_heading(capsys):
    """Test heading, paragraph, then another heading."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=1, text='First Heading')
        mfd.start_paragraph('Some content here.')
        mfd.start_heading(level=2, text='Second Heading')

    txt = run_with_context_manager('md', '.md', test_action)
    expected = '# First Heading\n\nSome content here.\n## Second Heading\n'
    assert txt == expected
    check_capsys(capsys)


def test_single_bullet_item(capsys):
    """Test a single bullet item."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='First item')

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == '- First item\n'
    check_capsys(capsys)


def test_multiple_bullet_items(capsys):
    """Test multiple bullet items."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_bullet_item(text='Third item')

    txt = run_with_context_manager('md', '.md', test_action)
    expected = '- First item\n- Second item\n- Third item\n'
    assert txt == expected
    check_capsys(capsys)


def test_bullet_item_with_add_text(capsys):
    """Test bullet item with additional text."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='First item')
        mfd.add_text(text=' with more text')

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == '- First item with more text\n'
    check_capsys(capsys)


def test_bullet_item_with_url(capsys):
    """Test bullet item with URL."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    txt = run_with_context_manager('md', '.md', test_action)
    assert txt == '- Check [this link](http://example.com)\n'
    check_capsys(capsys)


def test_nested_bullet_items_level2(capsys):
    """Test nested bullet items at level 2."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)

    txt = run_with_context_manager('md', '.md', test_action)
    expected = '- Level 1\n  - Level 2\n'
    assert txt == expected
    check_capsys(capsys)


def test_nested_bullet_items_level3(capsys):
    """Test nested bullet items at level 3."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 3', level=3)

    txt = run_with_context_manager('md', '.md', test_action)
    expected = '- Level 1\n  - Level 2\n    - Level 3\n'
    assert txt == expected
    check_capsys(capsys)


def test_bullet_list_back_to_level1(capsys):
    """Test bullet list returning to level 1."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Level 1 first', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 1 second', level=1)

    txt = run_with_context_manager('md', '.md', test_action)
    expected = ('- Level 1 first\n  - Level 2\n'
                '- Level 1 second\n')
    assert txt == expected
    check_capsys(capsys)


def test_bullet_list_formatting(capsys):
    """Test bullet list with bold and italic."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='Bold item', bold=True)
        mfd.start_bullet_item(text='Italic item', italic=True)
        mfd.start_bullet_item(text='Both', bold=True, italic=True)

    txt = run_with_context_manager('md', '.md', test_action)
    expected = ('- **Bold item**\n- *Italic item*\n'
                '- ***Both***\n')
    assert txt == expected
    check_capsys(capsys)


def test_paragraph_then_bullet_list(capsys):
    """Test paragraph followed by bullet list."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_paragraph(text='Intro paragraph')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    txt = run_with_context_manager('md', '.md', test_action)
    expected = '\nIntro paragraph\n- First item\n- Second item\n'
    assert txt == expected
    check_capsys(capsys)


def test_bullet_list_then_paragraph(capsys):
    """Test bullet list followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_paragraph(text='Concluding paragraph')

    txt = run_with_context_manager('md', '.md', test_action)
    expected = '- First item\n- Second item\n\nConcluding paragraph\n'
    assert txt == expected
    check_capsys(capsys)


def test_heading_then_bullet_list(capsys):
    """Test heading followed by bullet list."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        mfd.start_heading(level=1, text='Main Title')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    txt = run_with_context_manager('md', '.md', test_action)
    expected = '# Main Title\n- First item\n- Second item\n'
    assert txt == expected
    check_capsys(capsys)


def test_complex_nested_structure(capsys):
    """Test complex nested bullet structure."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatMd'
        action_complex_nested_bullet_structure(mfd)

    txt = run_with_context_manager('md', '.md', test_action)
    expected = ('- Item 1\n  - Item 1.1\n  - Item 1.2\n'
                '- Item 2\n  - Item 2.1\n')
    assert txt == expected
    check_capsys(capsys)
