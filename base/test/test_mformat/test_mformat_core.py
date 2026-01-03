#! /usr/local/bin/python3
"""Test the mformat module core functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional
import pytest
from check_capsys import check_capsys
from test_helpers import (
    MultiFormat2, MultiFormat3, MultiFormat5,
    MultiFormat8, MultiFormat9
)
from mformat.mformat import MultiFormat, MultiFormatState


@pytest.mark.parametrize('file_name, extension, res',
                         [('test', 'txt', 'test.txt'),
                          ('test.txt', 'txt', 'test.txt'),
                          ('test.txt', 'html', 'test.txt.html'),
                          ('test', 'md', 'test.md'),
                          ('test.txt', 'docx', 'test.txt.docx'),
                          ('test.txt', 'pdf', 'test.txt.pdf'),
                          ('test.txt', 'csv', 'test.txt.csv'),
                          ('test.txt', 'json', 'test.txt.json')])
def test_file_name_with_extension(file_name, extension, res):
    """Test the file_name_with_extension method."""
    assert MultiFormat.file_name_with_extension(file_name, extension) == res


def test_must_be_overridden1(capsys):
    """Test message from must_be_overridden methodr."""
    # pylint: disable=protected-access
    msg = MultiFormat._must_be_overridden('test')
    assert msg == 'test must be overridden by a subclass MultiFormat'
    check_capsys(capsys)


def test_must_be_overridden2(capsys):
    """Test that the must_be_overridden method raises an error."""
    # pylint: disable=protected-access
    msg = MultiFormat2._must_be_overridden('test')
    assert msg == 'test must be overridden by a subclass MultiFormat2'
    check_capsys(capsys)


def test_file_name_extension(capsys):
    """Test that the file_name_extension method is not overridden."""
    with pytest.raises(NotImplementedError) as exc:
        _ = MultiFormat.file_name_extension()
    assert exc.value.args[0] == 'file_name_extension must be overridden ' + \
        'by a subclass MultiFormat'
    check_capsys(capsys)


def test_get_arg_desciption(capsys):
    """Test that the get_arg_desciption method is not overridden."""
    with pytest.raises(NotImplementedError) as exc:
        _ = MultiFormat.get_arg_desciption()
    assert exc.value.args[0] == 'get_arg_desciption must be overridden ' + \
        'by a subclass MultiFormat'
    check_capsys(capsys)


def test_file_name_extension2(capsys):
    """Test that the file_name_extension method is overridden."""
    assert MultiFormat2.file_name_extension() == '.test'
    check_capsys(capsys)


def test_mft_init(capsys):
    """Test that the MultiFormat class is initialized correctly."""
    mfmt = MultiFormat2(file_name='test')
    assert mfmt.file_name == 'test.test'
    assert mfmt.state == MultiFormatState.EMPTY
    assert not mfmt.url_as_text
    check_capsys(capsys)


@pytest.mark.parametrize('method_name',
                         ['open', '_close',
                          '_write_file_prefix', '_write_file_suffix',
                          '_start_paragraph', '_end_paragraph', '_write_text',
                          '_write_url'])
def test_cls_method_not_overridden(capsys, method_name):
    """Test that the instance method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        if method_name == '_write_text':
            _ = getattr(mfmt, method_name)('test', MultiFormatState.PARAGRAPH,
                                           False, False)
        elif method_name == '_write_url':
            _ = getattr(mfmt, method_name)('http://example.com', 'text',
                                           MultiFormatState.PARAGRAPH,
                                           False, False)
        else:
            _ = getattr(mfmt, method_name)()
    assert exc.value.args[0] == f'{method_name} must be overridden by a ' + \
        'subclass MultiFormat2'
    check_capsys(capsys)


def test_write_text(capsys):
    """Test that the _write_text method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        mfmt._write_text('test',  # pylint: disable=protected-access
                         MultiFormatState.PARAGRAPH, False, False)
    assert exc.value.args[0] == '_write_text must be overridden ' + \
        'by a subclass MultiFormat2'
    check_capsys(capsys)


def test_write_url(capsys):
    """Test that the _write_url method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        # pylint: disable=protected-access
        mfmt._write_url('http://example.com', 'text',
                        MultiFormatState.PARAGRAPH, False, False)
    assert exc.value.args[0] == '_write_url must be overridden ' + \
        'by a subclass MultiFormat2'
    check_capsys(capsys)


@pytest.mark.parametrize('from_state, to_state, count',
                         [(MultiFormatState.EMPTY,
                           MultiFormatState.PARAGRAPH_END,
                           {'_write_file_prefix': 1}),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.PARAGRAPH_END,
                           {'_end_paragraph': 1}),
                          (MultiFormatState.PARAGRAPH_END,
                           MultiFormatState.PARAGRAPH_END,
                           {})])
def test_end_state(capsys, from_state, to_state, count):
    """Test that the end_state method is correct."""
    mfmt = MultiFormat3(file_name='test')
    mfmt.state = from_state
    mfmt._end_state()  # pylint: disable=protected-access
    assert mfmt.state == to_state
    assert mfmt.count == count
    check_capsys(capsys)


def test_enter_exit(capsys):
    """Test that the enter and exit methods are correct."""
    with MultiFormat5(file_name='test', expected_text='abc') as mfmt:
        assert isinstance(mfmt, MultiFormat5)
        assert mfmt.count == {'open': 1}
    assert mfmt.count == {'open': 1, '_close': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('from_state, to_state, count, level, text',
                         [(MultiFormatState.EMPTY,
                           MultiFormatState.HEADING,
                           {'_start_heading': 1, '_write_text': 1,
                            '_write_file_prefix': 1},
                           1, 'Main Heading'),
                          (MultiFormatState.PARAGRAPH_END,
                           MultiFormatState.HEADING,
                           {'_start_heading': 1, '_write_text': 1},
                           2, 'Subheading'),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.HEADING,
                           {'_end_paragraph': 1, '_start_heading': 1,
                            '_write_text': 1},
                           3, 'Sub-subheading')])
def test_start_heading(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                       from_state, to_state, count, level, text):
    """Test that the start_heading method is correct."""
    mfmt = MultiFormat8(file_name='test', expected_text=text,
                        expected_level=level)
    mfmt.state = from_state
    mfmt.start_heading(level=level, text=text)
    assert mfmt.state == to_state
    assert mfmt.heading_level == level
    assert mfmt.count == count
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, bold, italic',
                         [(1, 'Heading', False, False),
                          (2, 'Bold Heading', True, False),
                          (3, 'Italic Heading', False, True),
                          (4, 'Both Heading', True, True)])
def test_start_heading_bold_italic(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                   level, text, bold, italic):
    """Test start_heading with bold and italic parameters."""
    mfmt = MultiFormat8(file_name='test', expected_text=text,
                        expected_level=level,
                        expected_bold=bold, expected_italic=italic)
    mfmt.start_heading(level=level, text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.HEADING
    assert mfmt.heading_level == level
    assert mfmt.count == {'_start_heading': 1, '_write_text': 1,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


def test_heading_add_text(capsys):
    """Test adding text to a heading."""
    mfmt = MultiFormat8(file_name='test', expected_text='More text',
                        expected_level=1)
    mfmt.state = MultiFormatState.HEADING
    mfmt.heading_level = 1
    mfmt.add_text(text='More text')
    assert mfmt.state == MultiFormatState.HEADING
    assert mfmt.count == {'_write_text': 1}
    check_capsys(capsys)


def test_heading_add_url(capsys):
    """Test adding URL to a heading."""
    mfmt = MultiFormat9(file_name='test',
                        expected_url='http://example.com',
                        expected_url_text='Example')
    mfmt.state = MultiFormatState.HEADING
    mfmt.heading_level = 1
    mfmt.add_url(url='http://example.com', text='Example')
    assert mfmt.state == MultiFormatState.HEADING
    assert mfmt.count == {'_write_url': 1}
    check_capsys(capsys)


def test_end_state_heading(capsys):
    """Test ending a heading state."""
    mfmt = MultiFormat8(file_name='test', expected_text='Test',
                        expected_level=2)
    mfmt.state = MultiFormatState.HEADING
    mfmt.heading_level = 2
    mfmt._end_state()  # pylint: disable=protected-access
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.heading_level is None
    assert mfmt.count == {'_end_heading': 1}
    check_capsys(capsys)


def test_heading_then_paragraph(capsys):
    """Test heading followed by paragraph."""
    mfmt = MultiFormat8(file_name='test', expected_text='Title',
                        expected_level=1)
    mfmt.start_heading(level=1, text='Title')
    assert mfmt.state == MultiFormatState.HEADING

    # Now start a paragraph - should end the heading
    # Note: We don't check expected_level for the paragraph
    mfmt.expected_text = 'Paragraph text'
    mfmt.start_paragraph(text='Paragraph text')
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.heading_level is None
    assert mfmt.count == {'_start_heading': 1, '_write_text': 2,
                          '_write_file_prefix': 1,
                          '_end_heading': 1, '_start_paragraph': 1}
    check_capsys(capsys)


def test_multiple_headings(capsys):
    """Test multiple headings in sequence."""
    mfmt = MultiFormat8(file_name='test', expected_text='First',
                        expected_level=1)
    mfmt.start_heading(level=1, text='First')
    assert mfmt.heading_level == 1

    # Start another heading - should end the first
    mfmt.expected_text = 'Second'
    mfmt.expected_level = 2
    mfmt.start_heading(level=2, text='Second')
    assert mfmt.heading_level == 2
    assert mfmt.count == {'_start_heading': 2, '_write_text': 2,
                          '_write_file_prefix': 1,
                          '_end_heading': 1}
    check_capsys(capsys)


def test_heading_with_smart_ws(capsys):
    """Test heading with smart_ws parameter."""
    mfmt = MultiFormat8(file_name='test', expected_text='Heading',
                        expected_level=1)
    mfmt.start_heading(level=1, text='  Heading  ', smart_ws=True)
    assert mfmt.ws_needed_at_append is True

    mfmt.expected_text = ' more'
    mfmt.add_text(text='  more  ', smart_ws=True)
    assert mfmt.count == {'_start_heading': 1, '_write_text': 2,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


# Tests for code blocks


class MultiFormat12(MultiFormat3):
    """Class used for testing code blocks."""

    def _start_code_block(self, programming_language: Optional[str]) -> None:
        """Start a code block."""
        if programming_language is not None:
            assert isinstance(programming_language, str)
        self.inc_count('_start_code_block')

    def _end_code_block(self, programming_language: Optional[str]) -> None:
        """End a code block."""
        if programming_language is not None:
            assert isinstance(programming_language, str)
        self.inc_count('_end_code_block')

    def _write_code_block(self, text: str,
                          programming_language: Optional[str]) -> None:
        """Write a code block."""
        assert isinstance(text, str)
        if programming_language is not None:
            assert isinstance(programming_language, str)
        self.inc_count('_write_code_block')


def test_write_code_block_basic(capsys):
    """Test basic code block writing."""
    mfmt = MultiFormat12(file_name='test')
    assert mfmt.state == MultiFormatState.EMPTY
    mfmt.write_code_block(text='print("Hello")')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_write_code_block_with_language(capsys):
    """Test code block with programming language."""
    mfmt = MultiFormat12(file_name='test')
    mfmt.write_code_block(text='x = 42', programming_language='python')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_paragraph_then_code_block(capsys):
    """Test paragraph followed by code block."""
    mfmt = MultiFormat12(file_name='test')
    mfmt.start_paragraph(text='Here is code:')
    mfmt.write_code_block(text='code here')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_write_file_prefix': 1,
        '_start_paragraph': 1,
        '_write_text': 1,
        '_end_paragraph': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_code_block_then_paragraph(capsys):
    """Test code block followed by paragraph."""
    mfmt = MultiFormat12(file_name='test')
    mfmt.write_code_block(text='code')
    mfmt.start_paragraph(text='After code')
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1,
        '_start_paragraph': 1,
        '_write_text': 1}
    check_capsys(capsys)


def test_multiple_code_blocks(capsys):
    """Test multiple code blocks in sequence."""
    mfmt = MultiFormat12(file_name='test')
    mfmt.write_code_block(text='first', programming_language='python')
    mfmt.write_code_block(text='second', programming_language='javascript')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_write_file_prefix': 1,
        '_start_code_block': 2,
        '_write_code_block': 2,
        '_end_code_block': 2}
    check_capsys(capsys)


def test_code_block_multiline(capsys):
    """Test code block with multiline text."""
    mfmt = MultiFormat12(file_name='test')
    code = 'def hello():\n    print("Hello")\n    return True'
    mfmt.write_code_block(text=code, programming_language='python')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_code_block_empty(capsys):
    """Test code block with empty text."""
    mfmt = MultiFormat12(file_name='test')
    mfmt.write_code_block(text='')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)
