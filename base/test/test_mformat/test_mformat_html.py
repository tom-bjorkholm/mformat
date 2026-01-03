#! /usr/local/bin/python3
"""Test the mformat_html module."""
# pylint: disable=too-many-lines

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from test_helpers import (
    run_with_context_manager,
    run_protected_method,
    action_complex_nested_bullet_structure,
    TABLE_DATA_3X2,
    TABLE_DATA_3X2_SIMPLE
)
from mformat.mformat_html import MultiFormatHtml
from mformat.mformat import FormatterDescriptor, MultiFormatState


def test_file_name_extension(capsys):
    """Test the file_name_extension method."""
    assert MultiFormatHtml.file_name_extension() == '.html'
    check_capsys(capsys)


def test_get_arg_desciption(capsys):
    """Test the get_arg_desciption method."""
    assert MultiFormatHtml.get_arg_desciption() == \
        FormatterDescriptor(name='html', mandatory_args=[],
                            optional_args=['title', 'css_file', 'lang'])
    check_capsys(capsys)


PFDT = '<!DOCTYPE html encoding="utf-8">\n<html lang="'
PTAL = '">\n<head>\n<title>'
PFAT = '</title>\n'
PFCSS = '<link rel="stylesheet" href="'
PFCSSE = '">\n'
PFLS = '</head>\n<body>\n'

SFTOT = '</body>\n</html>\n'

PF_EN_NT_NC = PFDT + 'en' + PTAL + 'HTML file' + PFAT + PFLS
PF_SV_TS_C1 = PFDT + 'sv' + PTAL + 'Something' + PFAT + PFCSS + \
    'style1.css' + PFCSSE + PFLS


@pytest.mark.parametrize('lang, title, css_file, expected',
                         [('en', None, None, PF_EN_NT_NC),
                          ('sv', 'Something', 'style1.css', PF_SV_TS_C1)])
def test_write_file_prefix(capsys, lang, title, css_file, expected):
    """Test the write_file_prefix method."""
    args = {'lang': lang}
    if title is not None:
        args['title'] = title
    if css_file is not None:
        args['css_file'] = css_file
    txt = run_protected_method('html', '.html', '_write_file_prefix',
                               args=args)
    assert txt == expected
    check_capsys(capsys)


def test_write_file_suffix(capsys):
    """Test the write_file_suffix method."""
    txt = run_protected_method('html', '.html', '_write_file_suffix')
    assert txt == SFTOT
    check_capsys(capsys)


def test_start_paragraph(capsys):
    """Test the start_paragraph method."""
    txt = run_protected_method('html', '.html', '_start_paragraph')
    assert txt == '<p>\n'
    check_capsys(capsys)


def test_end_paragraph(capsys):
    """Test the end_paragraph method."""
    txt = run_protected_method('html', '.html', '_end_paragraph')
    assert txt == '</p>\n'
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('Hello, world!', False, False, 'Hello, world!'),
                          ('Something else', False, False,
                           'Something else'),
                          ('Bold text', True, False,
                           '<strong>Bold text</strong>'),
                          ('Italic text', False, True,
                           '<em>Italic text</em>'),
                          ('Both', True, True,
                           '<em><strong>Both</strong></em>')])
def test_write_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                    text, bold, italic, expected):
    """Test the _write_text method."""
    txt = run_protected_method('html', '.html', '_write_text',
                               (text, MultiFormatState.PARAGRAPH,
                                bold, italic))
    assert txt == expected
    check_capsys(capsys)


EN_NT_NC_T1 = PF_EN_NT_NC + '<p>\nHello, world!</p>\n<p>\nBye!</p>\n' + SFTOT
SV_TS_C1_T2 = PF_SV_TS_C1 + '<p>\nSomething else</p>\n<p>\nYeah!</p>\n' + \
    SFTOT
EN_NT_NC_BOLD = PF_EN_NT_NC + '<p>\n<strong>Bold text</strong></p>\n' + SFTOT
EN_NT_NC_ITALIC = PF_EN_NT_NC + '<p>\n<em>Italic text</em></p>\n' + SFTOT
EN_NT_NC_BOTH = PF_EN_NT_NC + \
    '<p>\n<em><strong>Both styles</strong></em></p>\n' + SFTOT


@pytest.mark.parametrize('lang, title, css_file, texts, expected',
                         [('en', None, None,
                           ['Hello, world!', 'Bye!'], EN_NT_NC_T1),
                          ('sv', 'Something', 'style1.css',
                           ['Something else', 'Yeah!'], SV_TS_C1_T2)])
def test_start_paragraph2(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                          lang, title, css_file, texts, expected):
    """Test the start_paragraph method."""
    args = {'lang': lang}
    if title is not None:
        args['title'] = title
    if css_file is not None:
        args['css_file'] = css_file

    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        for text in texts:
            mfd.start_paragraph(text)

    txt = run_with_context_manager('html', '.html', test_action, args=args)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected',
                         [('Bold text', True, False,
                           '<strong>Bold text</strong>'),
                          ('Italic text', False, True,
                           '<em>Italic text</em>'),
                          ('Both styles', True, True,
                           '<em><strong>Both styles</strong></em>')])
def test_start_paragraph_formatting(capsys,  # pylint: disable=too-many-arguments, too-many-positional-arguments # noqa: E501
                                    text, bold, italic, expected):
    """Test the start_paragraph method with bold and italic."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph(text, bold=bold, italic=italic)

    txt = run_with_context_manager('html', '.html', test_action)
    assert txt == PF_EN_NT_NC + '<p>\n' + expected + '</p>\n' + SFTOT
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected',
                         [('http://example.com', None, False, False,
                           '<a href="http://example.com">'
                           'http://example.com</a>'),
                          ('http://test.org', 'link text', False, False,
                           '<a href="http://test.org">'
                           'link text</a>'),
                          ('http://test.org', 'link', True, False,
                           '<strong><a href="http://test.org">'
                           'link</a></strong>'),
                          ('http://test.org', 'link', False, True,
                           '<em><a href="http://test.org">'
                           'link</a></em>'),
                          ('http://test.org', 'link', True, True,
                           '<em><strong><a href="http://test.org">'
                           'link</a></strong></em>')])
def test_write_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                   url, text, bold, italic, expected):
    """Test the _write_url method."""
    txt = run_protected_method('html', '.html', '_write_url',
                               (url, text, MultiFormatState.PARAGRAPH,
                                bold, italic))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           PF_EN_NT_NC +
                           '<p>\n<a href="http://example.com">'
                           'http://example.com</a></p>\n' + SFTOT),
                          ('http://test.org', 'link text',
                           PF_EN_NT_NC +
                           '<p>\n<a href="http://test.org">'
                           'link text</a></p>\n' + SFTOT)])
def test_add_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url, text, expected):
    """Test the add_url method."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    txt = run_with_context_manager('html', '.html', test_action)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected',
                         [('http://example.com', None,
                           PF_EN_NT_NC +
                           '<p>\nhttp://example.com</p>\n' + SFTOT),
                          ('http://test.org', 'See here',
                           PF_EN_NT_NC +
                           '<p>\nSee here http://test.org</p>\n' +
                           SFTOT)])
def test_add_url_as_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         url, text, expected):
    """Test the add_url method with url_as_text=True."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph('')
        mfd.add_url(url=url, text=text)

    txt = run_with_context_manager('html', '.html', test_action,
                                   url_as_text=True)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, expected',
                         [(1, '<h1>\n'),
                          (2, '<h2>\n'),
                          (3, '<h3>\n'),
                          (4, '<h4>\n'),
                          (5, '<h5>\n'),
                          (6, '<h6>\n')])
def test_start_heading(capsys, level, expected):
    """Test the _start_heading method."""
    txt = run_protected_method('html', '.html', '_start_heading', (level,))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, expected',
                         [(1, '</h1>\n'),
                          (2, '</h2>\n'),
                          (3, '</h3>\n'),
                          (4, '</h4>\n'),
                          (5, '</h5>\n'),
                          (6, '</h6>\n')])
def test_end_heading(capsys, level, expected):
    """Test the _end_heading method."""
    txt = run_protected_method('html', '.html', '_end_heading', (level,))
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, expected',
                         [(1, 'Main Title',
                           PF_EN_NT_NC + '<h1>\nMain Title</h1>\n' + SFTOT),
                          (2, 'Subtitle',
                           PF_EN_NT_NC + '<h2>\nSubtitle</h2>\n' + SFTOT),
                          (3, 'Section',
                           PF_EN_NT_NC + '<h3>\nSection</h3>\n' + SFTOT)])
def test_heading_integration(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             level, text, expected):
    """Test complete heading creation."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=level, text=text)

    txt = run_with_context_manager('html', '.html', test_action)
    assert txt == expected
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, bold, italic, expected',
                         [(1, 'Bold Title', True, False,
                           '<h1>\n<strong>Bold Title</strong></h1>\n'),
                          (2, 'Italic Title', False, True,
                           '<h2>\n<em>Italic Title</em></h2>\n'),
                          (3, 'Both', True, True,
                           '<h3>\n<em><strong>Both</strong></em></h3>\n')])
def test_heading_formatting(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                            level, text, bold, italic, expected):
    """Test heading with bold and italic formatting."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=level, text=text, bold=bold, italic=italic)

    txt = run_with_context_manager('html', '.html', test_action)
    assert txt == PF_EN_NT_NC + expected + SFTOT
    check_capsys(capsys)


def test_heading_add_text(capsys):
    """Test adding text to a heading."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=1, text='Title')
        mfd.add_text(text=' and more')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = PF_EN_NT_NC + '<h1>\nTitle and more</h1>\n' + SFTOT
    assert txt == expected
    check_capsys(capsys)


def test_heading_add_url(capsys):
    """Test adding URL to a heading."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=2, text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h2>\nCheck ' +
                '<a href="http://example.com">this link</a></h2>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_heading_then_paragraph(capsys):
    """Test heading followed by paragraph."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=1, text='Title')
        mfd.start_paragraph('Some text')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h1>\nTitle</h1>\n' +
                '<p>\nSome text</p>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_multiple_headings(capsys):
    """Test multiple headings."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=1, text='Main')
        mfd.start_heading(level=2, text='Sub')
        mfd.start_heading(level=3, text='Subsub')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h1>\nMain</h1>\n' +
                '<h2>\nSub</h2>\n<h3>\nSubsub</h3>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_heading_paragraph_heading(capsys):
    """Test heading, paragraph, then another heading."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=1, text='First Heading')
        mfd.start_paragraph('Some content here.')
        mfd.start_heading(level=2, text='Second Heading')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h1>\nFirst Heading</h1>\n' +
                '<p>\nSome content here.</p>\n' +
                '<h2>\nSecond Heading</h2>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_single_bullet_item(capsys):
    """Test a single bullet item."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='First item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = PF_EN_NT_NC + '<ul>\n<li>First item</li>\n</ul>\n' + SFTOT
    assert txt == expected
    check_capsys(capsys)


def test_multiple_bullet_items(capsys):
    """Test multiple bullet items."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_bullet_item(text='Third item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>First item</li>\n' +
                '<li>Second item</li>\n<li>Third item</li>\n</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_bullet_item_with_add_text(capsys):
    """Test bullet item with additional text."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='First item')
        mfd.add_text(text=' with more text')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>First item with more text</li>\n' +
                '</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_bullet_item_with_url(capsys):
    """Test bullet item with URL."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>Check ' +
                '<a href="http://example.com">this link</a></li>\n' +
                '</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_nested_bullet_items_level2(capsys):
    """Test nested bullet items at level 2."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>Level 1</li>\n' +
                '<ul>\n<li>Level 2</li>\n</ul>\n</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_nested_bullet_items_level3(capsys):
    """Test nested bullet items at level 3."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='Level 1', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 3', level=3)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>Level 1</li>\n' +
                '<ul>\n<li>Level 2</li>\n' +
                '<ul>\n<li>Level 3</li>\n</ul>\n</ul>\n</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_bullet_list_back_to_level1(capsys):
    """Test bullet list returning to level 1."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='Level 1 first', level=1)
        mfd.start_bullet_item(text='Level 2', level=2)
        mfd.start_bullet_item(text='Level 1 second', level=1)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>Level 1 first</li>\n' +
                '<ul>\n<li>Level 2</li>\n</ul>\n' +
                '<li>Level 1 second</li>\n</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_bullet_list_formatting(capsys):
    """Test bullet list with bold and italic."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='Bold item', bold=True)
        mfd.start_bullet_item(text='Italic item', italic=True)
        mfd.start_bullet_item(text='Both', bold=True, italic=True)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li><strong>Bold item</strong></li>\n' +
                '<li><em>Italic item</em></li>\n' +
                '<li><em><strong>Both</strong></em></li>\n</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_paragraph_then_bullet_list(capsys):
    """Test paragraph followed by bullet list."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph(text='Intro paragraph')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<p>\nIntro paragraph</p>\n' +
                '<ul>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_bullet_list_then_paragraph(capsys):
    """Test bullet list followed by paragraph."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')
        mfd.start_paragraph(text='Concluding paragraph')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>First item</li>\n' +
                '<li>Second item</li>\n</ul>\n' +
                '<p>\nConcluding paragraph</p>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_heading_then_bullet_list(capsys):
    """Test heading followed by bullet list."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=1, text='Main Title')
        mfd.start_bullet_item(text='First item')
        mfd.start_bullet_item(text='Second item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h1>\nMain Title</h1>\n' +
                '<ul>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_complex_nested_structure(capsys):
    """Test complex nested bullet structure."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        action_complex_nested_bullet_structure(mfd)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>Item 1</li>\n' +
                '<ul>\n<li>Item 1.1</li>\n<li>Item 1.2</li>\n</ul>\n' +
                '<li>Item 2</li>\n' +
                '<ul>\n<li>Item 2.1</li>\n</ul>\n</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


# Tests for numbered point lists


def test_single_numbered_item(capsys):
    """Test a single numbered point item."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='First item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = PF_EN_NT_NC + '<ol>\n<li>First item</li>\n</ol>\n' + SFTOT
    assert txt == expected
    check_capsys(capsys)


def test_multiple_numbered_items(capsys):
    """Test multiple numbered point items."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')
        mfd.start_numbered_point_item(text='Third item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li>First item</li>\n' +
                '<li>Second item</li>\n<li>Third item</li>\n</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_numbered_item_with_add_text(capsys):
    """Test numbered point item with additional text."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='First item')
        mfd.add_text(text=' with more text')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li>First item with more text</li>\n' +
                '</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_numbered_item_with_url(capsys):
    """Test numbered point item with URL."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='Check ')
        mfd.add_url(url='http://example.com', text='this link')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li>Check ' +
                '<a href="http://example.com">this link</a></li>\n' +
                '</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_nested_numbered_items_level2(capsys):
    """Test nested numbered point items at level 2."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='Level 1', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li>Level 1</li>\n' +
                '<ol>\n<li>Level 2</li>\n</ol>\n</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_nested_numbered_items_level3(capsys):
    """Test nested numbered point items at level 3."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='Level 1', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)
        mfd.start_numbered_point_item(text='Level 3', level=3)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li>Level 1</li>\n' +
                '<ol>\n<li>Level 2</li>\n' +
                '<ol>\n<li>Level 3</li>\n</ol>\n</ol>\n</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_numbered_list_back_to_level1(capsys):
    """Test numbered point list returning to level 1."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='Level 1 first', level=1)
        mfd.start_numbered_point_item(text='Level 2', level=2)
        mfd.start_numbered_point_item(text='Level 1 second', level=1)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li>Level 1 first</li>\n' +
                '<ol>\n<li>Level 2</li>\n</ol>\n' +
                '<li>Level 1 second</li>\n</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_numbered_list_formatting(capsys):
    """Test numbered point list with bold and italic."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='Bold item', bold=True)
        mfd.start_numbered_point_item(text='Italic item', italic=True)
        mfd.start_numbered_point_item(text='Both', bold=True, italic=True)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li><strong>Bold item</strong></li>\n' +
                '<li><em>Italic item</em></li>\n' +
                '<li><em><strong>Both</strong></em></li>\n</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_paragraph_then_numbered_list(capsys):
    """Test paragraph followed by numbered point list."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph(text='Intro paragraph')
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<p>\nIntro paragraph</p>\n' +
                '<ol>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_numbered_list_then_paragraph(capsys):
    """Test numbered point list followed by paragraph."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')
        mfd.start_paragraph(text='Concluding paragraph')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ol>\n<li>First item</li>\n' +
                '<li>Second item</li>\n</ol>\n' +
                '<p>\nConcluding paragraph</p>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_heading_then_numbered_list(capsys):
    """Test heading followed by numbered point list."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=1, text='Main Title')
        mfd.start_numbered_point_item(text='First item')
        mfd.start_numbered_point_item(text='Second item')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h1>\nMain Title</h1>\n' +
                '<ol>\n<li>First item</li>\n<li>Second item</li>\n' +
                '</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_mixed_bullet_and_numbered_lists(capsys):
    """Test switching between bullet and numbered point lists."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='Bullet 1', level=1)
        mfd.start_bullet_item(text='Bullet 2', level=1)
        mfd.start_numbered_point_item(text='Numbered 1', level=1)
        mfd.start_numbered_point_item(text='Numbered 2', level=1)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>Bullet 1</li>\n<li>Bullet 2</li>\n'
                '</ul>\n<ol>\n<li>Numbered 1</li>\n<li>Numbered 2</li>\n'
                '</ol>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_nested_mixed_lists(capsys):
    """Test nested mixed bullet and numbered point lists."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_bullet_item(text='Bullet 1', level=1)
        mfd.start_numbered_point_item(text='Numbered 1.1', level=2)
        mfd.start_numbered_point_item(text='Numbered 1.2', level=2)
        mfd.start_bullet_item(text='Bullet 2', level=1)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<ul>\n<li>Bullet 1</li>\n' +
                '<ol>\n<li>Numbered 1.1</li>\n<li>Numbered 1.2</li>\n' +
                '</ol>\n<li>Bullet 2</li>\n</ul>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


# Tests for code blocks


def test_simple_code_block(capsys):
    """Test a simple code block."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='print("Hello, World!")')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<pre><code>\nprint("Hello, World!")' +
                '</code></pre>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_code_block_with_language(capsys):
    """Test a code block with programming language."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='print("Hello")',
                             programming_language='python')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<pre><code>\n' +
                '<span class="language-python">print("Hello")</span>\n' +
                '</code></pre>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_code_block_multiline(capsys):
    """Test a multiline code block."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        code = 'def hello():\n    print("Hello")\n    return True'
        mfd.write_code_block(text=code, programming_language='python')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<pre><code>\n' +
                '<span class="language-python">def hello():\n' +
                '    print("Hello")\n    return True</span>\n' +
                '</code></pre>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_code_block_with_special_chars(capsys):
    """Test a code block with special characters."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        code = 'x = "test <>&"\ny = \'another\''
        mfd.write_code_block(text=code)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<pre><code>\nx = "test <>&"\n' +
                'y = \'another\'</code></pre>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_paragraph_then_code_block(capsys):
    """Test paragraph followed by code block."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph(text='Here is some code:')
        mfd.write_code_block(text='x = 42', programming_language='python')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<p>\nHere is some code:</p>\n' +
                '<pre><code>\n<span class="language-python">x = 42' +
                '</span>\n</code></pre>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_code_block_then_paragraph(capsys):
    """Test code block followed by paragraph."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='x = 42')
        mfd.start_paragraph(text='That was the code.')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<pre><code>\nx = 42</code></pre>\n' +
                '<p>\nThat was the code.</p>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_heading_then_code_block(capsys):
    """Test heading followed by code block."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=2, text='Code Example')
        mfd.write_code_block(text='example()', programming_language='python')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h2>\nCode Example</h2>\n' +
                '<pre><code>\n<span class="language-python">example()' +
                '</span>\n</code></pre>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_multiple_code_blocks(capsys):
    """Test multiple code blocks."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_code_block(text='x = 1', programming_language='python')
        mfd.write_code_block(text='y = 2', programming_language='python')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<pre><code>\n' +
                '<span class="language-python">x = 1</span>\n' +
                '</code></pre>\n<pre><code>\n' +
                '<span class="language-python">y = 2</span>\n' +
                '</code></pre>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


# Tests for tables


def test_simple_table(capsys):
    """Test a simple table."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])
        mfd.add_table_row(row=['C', 'D'])

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>Col1</td>\n<td>Col2</td>\n'
                '</tr>\n<tr>\n<td>A</td>\n<td>B</td>\n</tr>\n<tr>\n'
                '<td>C</td>\n<td>D</td>\n</tr>\n</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_table_with_bold_header(capsys):
    """Test a table with bold header."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Name', 'Age'], bold=True)
        mfd.add_table_row(row=['Alice', '30'])
        mfd.add_table_row(row=['Bob', '25'])

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td><strong>Name</strong></td>\n'
                '<td><strong>Age</strong></td>\n</tr>\n<tr>\n<td>Alice</td>\n'
                '<td>30</td>\n</tr>\n<tr>\n<td>Bob</td>\n<td>25</td>\n</tr>\n'
                '</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_table_with_italic_header(capsys):
    """Test a table with italic header."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Name', 'Age'], italic=True)
        mfd.add_table_row(row=['Alice', '30'])

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td><em>Name</em></td>\n'
                '<td><em>Age</em></td>\n</tr>\n<tr>\n<td>Alice</td>\n'
                '<td>30</td>\n</tr>\n</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_write_complete_table(capsys):
    """Test write_complete_table method."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_complete_table(table=TABLE_DATA_3X2)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>Header1</td>\n'
                '<td>Header2</td>\n</tr>\n<tr>\n<td>Row1Col1</td>\n'
                '<td>Row1Col2</td>\n</tr>\n<tr>\n<td>Row2Col1</td>\n'
                '<td>Row2Col2</td>\n</tr>\n</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_write_complete_table_with_bold_header(capsys):
    """Test write_complete_table with bold first row."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.write_complete_table(
            table=TABLE_DATA_3X2_SIMPLE, bold_first_row=True)

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td><strong>Name</strong></td>\n'
                '<td><strong>Value</strong></td>\n</tr>\n<tr>\n'
                '<td>Alpha</td>\n<td>1</td>\n</tr>\n<tr>\n<td>Beta</td>\n'
                '<td>2</td>\n</tr>\n</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_paragraph(text='Here is a table:')
        mfd.start_table(first_row=['A', 'B'])
        mfd.add_table_row(row=['1', '2'])

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<p>\nHere is a table:</p>\n<table>\n<tr>\n'
                '<td>A</td>\n<td>B</td>\n</tr>\n<tr>\n<td>1</td>\n'
                '<td>2</td>\n</tr>\n</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['X', 'Y'])
        mfd.add_table_row(row=['1', '2'])
        mfd.start_paragraph(text='That was the table.')

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>X</td>\n<td>Y</td>\n</tr>\n'
                '<tr>\n<td>1</td>\n<td>2</td>\n</tr>\n</table>\n'
                '<p>\nThat was the table.</p>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_heading_then_table(capsys):
    """Test heading followed by table."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_heading(level=2, text='Data Table')
        mfd.start_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', 'B'])

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<h2>\nData Table</h2>\n<table>\n<tr>\n'
                '<td>Col1</td>\n<td>Col2</td>\n</tr>\n<tr>\n<td>A</td>\n'
                '<td>B</td>\n</tr>\n</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)


def test_table_with_three_columns(capsys):
    """Test a table with three columns."""
    def test_action(mfd):
        assert isinstance(mfd, MultiFormatHtml)
        mfd.start_table(first_row=['Name', 'Age', 'City'])
        mfd.add_table_row(row=['Alice', '30', 'NYC'])
        mfd.add_table_row(row=['Bob', '25', 'LA'])

    txt = run_with_context_manager('html', '.html', test_action)
    expected = (PF_EN_NT_NC + '<table>\n<tr>\n<td>Name</td>\n<td>Age</td>\n'
                '<td>City</td>\n</tr>\n<tr>\n<td>Alice</td>\n<td>30</td>\n'
                '<td>NYC</td>\n</tr>\n<tr>\n<td>Bob</td>\n<td>25</td>\n'
                '<td>LA</td>\n</tr>\n</table>\n' + SFTOT)
    assert txt == expected
    check_capsys(capsys)
