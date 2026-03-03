#! /usr/local/bin/python3
"""Test the mformat module core functionality."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from typing import Optional
import pytest
from mformat.mformat import MultiFormat
from mformat.mformat_lists_impl import PointStackItem
from mformat.mformat_state import Formatting, MultiFormatState
from .check_capsys import check_capsys
from .test_helpers import (MultiFormat2, MultiFormat3, MultiFormat4,
                           MultiFormat5, MultiFormat8, MultiFormat9)


@pytest.mark.parametrize('file_name, extension, res',
                         [('test', 'txt', 'test.txt'),
                          ('test.txt', 'txt', 'test.txt'),
                          ('test.txt', 'html', 'test.txt.html'),
                          ('test', 'md', 'test.md'),
                          ('test.txt', 'docx', 'test.txt.docx'),
                          ('test.txt', 'pdf', 'test.txt.pdf'),
                          ('test.txt', 'csv', 'test.txt.csv'),
                          ('test.txt', 'json', 'test.txt.json')])
def test_file_name_with_extension(file_name, extension, res) -> None:
    """Test the file_name_with_extension method."""
    assert MultiFormat.file_name_with_extension(file_name, extension) == res


@pytest.mark.parametrize('file_name, extension, res',
                         [(Path('test'), 'txt', 'test.txt'),
                          (Path('test.txt'), 'txt', 'test.txt'),
                          (Path('test.txt'), 'html', 'test.txt.html'),
                          (Path('test'), 'md', 'test.md'),
                          (Path('test.txt'), 'docx', 'test.txt.docx'),
                          (Path('test.txt'), 'pdf', 'test.txt.pdf'),
                          (Path('test.txt'), 'csv', 'test.txt.csv'),
                          (Path('test.txt'), 'json', 'test.txt.json'),
                          (Path(__file__).parent / 'test.txt', 'txt',
                           str(Path(__file__).parent / 'test.txt'))])
def test_file_name_with_extension2(file_name, extension, res) -> None:
    """Test the file_name_with_extension method."""
    assert MultiFormat.file_name_with_extension(file_name, extension) == res


def test_must_be_overridden1(capsys: pytest.capturefixture[str]) -> None:
    """Test message from must_be_overridden methodr."""
    # pylint: disable=protected-access
    msg = MultiFormat._must_be_overridden('test')
    assert msg == 'test must be overridden by a subclass MultiFormat'
    check_capsys(capsys)


def test_must_be_overridden2(capsys: pytest.capturefixture[str]) -> None:
    """Test that the must_be_overridden method raises an error."""
    # pylint: disable=protected-access
    msg = MultiFormat2._must_be_overridden('test')
    assert msg == 'test must be overridden by a subclass MultiFormat2'
    check_capsys(capsys)


def test_file_name_extension(capsys: pytest.capturefixture[str]) -> None:
    """Test that the file_name_extension method is not overridden."""
    with pytest.raises(NotImplementedError) as exc:
        _ = MultiFormat.file_name_extension()
    assert exc.value.args[0] == 'file_name_extension must be overridden ' + \
        'by a subclass MultiFormat'
    check_capsys(capsys)


def test_get_arg_desciption(capsys: pytest.capturefixture[str]) -> None:
    """Test that the get_arg_desciption method is not overridden."""
    with pytest.raises(NotImplementedError) as exc:
        _ = MultiFormat.get_arg_desciption()
    assert exc.value.args[0] == 'get_arg_desciption must be overridden ' + \
        'by a subclass MultiFormat'
    check_capsys(capsys)


def test_file_name_extension2(capsys: pytest.capturefixture[str]) -> None:
    """Test that the file_name_extension method is overridden."""
    assert MultiFormat2.file_name_extension() == '.test'
    check_capsys(capsys)


def test_mft_init(capsys: pytest.capturefixture[str]) -> None:
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
                          '_write_url',
                          '_start_block_quote', '_end_block_quote'])
def test_cls_method_not_overridden(capsys: pytest.capturefixture[str],
                                   method_name: str) -> None:
    """Test that the instance method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        formatting = Formatting(bold=False, italic=False)
        if method_name == '_write_text':
            _ = getattr(mfmt, method_name)('test', MultiFormatState.PARAGRAPH,
                                           formatting)
        elif method_name == '_write_url':
            _ = getattr(mfmt, method_name)('http://example.com', 'text',
                                           MultiFormatState.PARAGRAPH,
                                           formatting)
        else:
            _ = getattr(mfmt, method_name)()
    assert exc.value.args[0] == f'{method_name} must be overridden by a ' + \
        'subclass MultiFormat2'
    check_capsys(capsys)


@pytest.mark.parametrize('method_name',
                         ['_start_heading', '_end_heading',
                          '_start_bullet_list', '_end_bullet_list',
                          '_start_numbered_list', '_end_numbered_list',
                          '_start_bullet_item', '_end_bullet_item',
                          '_start_table'])
def test_cls_method_not_overridden2(capsys: pytest.capturefixture[str],
                                    method_name: str) -> None:
    """Test that the class method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        _ = getattr(mfmt, method_name)(2)
    assert exc.value.args[0] == f'{method_name} must be overridden by a ' + \
        'subclass MultiFormat2'
    check_capsys(capsys)


@pytest.mark.parametrize('method_name',
                         ['_end_table', '_end_numbered_item'])
def test_cls_method_not_overridden3(capsys: pytest.capturefixture[str],
                                    method_name: str) -> None:
    """Test that the class method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        _ = getattr(mfmt, method_name)(2, 7)
    assert exc.value.args[0] == f'{method_name} must be overridden by a ' + \
        'subclass MultiFormat2'
    check_capsys(capsys)


def test_encode_not_overridden(capsys: pytest.capturefixture[str]) -> None:
    """Test error that the _encode_text method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        _ = mfmt._encode_text(text='test')  # pylint: disable=protected-access # noqa: E501
    assert exc.value.args[0] == '_encode_text must be overridden by a ' + \
        'subclass MultiFormat2'
    check_capsys(capsys)


def test_start_num_item_not_impl(capsys: pytest.capturefixture[str]) -> None:
    """Test that the _start_numbered_item method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        # pylint: disable=protected-access
        mfmt._start_numbered_item(2, 7, '1.7')
    assert exc.value.args[0] == '_start_numbered_item must be ' + \
        'overridden by a subclass MultiFormat2'
    check_capsys(capsys)


def test_write_table_row_not_impl(capsys: pytest.capturefixture[str]) -> None:
    """Test that the write_table_row method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        mfmt._write_table_row(  # pylint: disable=protected-access
                              row=['X', 'Y'],
                              formatting=Formatting(bold=False, italic=False),
                              row_number=2)
    assert exc.value.args[0] == '_write_table_row must be ' + \
        'overridden by a subclass MultiFormat2'
    check_capsys(capsys)


def test_write_table_frow_not_impl(capsys: pytest.capturefixture[str]) -> None:
    """Test that the write_table_first_row method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        mfmt._write_table_first_row(  # pylint: disable=protected-access
                                    first_row=['X', 'Y'],
                                    formatting=Formatting(bold=False,
                                                          italic=False))
    assert exc.value.args[0] == '_write_table_first_row must ' + \
        'be overridden by a subclass MultiFormat2'
    check_capsys(capsys)


@pytest.mark.parametrize('method_name',
                         ['_start_code_block', '_end_code_block'])
def test_cls_method_not_overridden5(capsys: pytest.capturefixture[str],
                                    method_name: str) -> None:
    """Test that the class method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        _ = getattr(mfmt, method_name)(programming_language='python')
    assert exc.value.args[0] == f'{method_name} must be overridden by a ' + \
        'subclass MultiFormat2'
    check_capsys(capsys)


def test_write_code_block_not_impl(capsys: pytest.capturefixture[str]) -> None:
    """Test that the write_code_block method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        mfmt._write_code_block(text='test',  # pylint: disable=protected-access # noqa: E501
                               programming_language='python')
    assert exc.value.args[0] == '_write_code_block must be ' + \
        'overridden by a subclass MultiFormat2'
    check_capsys(capsys)


def test_write_code_int_not_impl(capsys: pytest.capturefixture[str]) -> None:
    """Test that the write_code_in_text method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        mfmt._write_code_in_text(text='test',  # pylint: disable=protected-access # noqa: E501
                                 state=MultiFormatState.PARAGRAPH)
    assert exc.value.args[0] == '_write_code_in_text must be ' + \
        'overridden by a subclass MultiFormat2'
    check_capsys(capsys)


def test_write_text(capsys: pytest.capturefixture[str]) -> None:
    """Test that the _write_text method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        mfmt._write_text('test',  # pylint: disable=protected-access
                         MultiFormatState.PARAGRAPH,
                         Formatting(bold=False, italic=False))
    assert exc.value.args[0] == '_write_text must be overridden ' + \
        'by a subclass MultiFormat2'
    check_capsys(capsys)


def test_write_url(capsys: pytest.capturefixture[str]) -> None:
    """Test that the _write_url method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        # pylint: disable=protected-access
        mfmt._write_url('http://example.com', 'text',
                        MultiFormatState.PARAGRAPH,
                        Formatting(bold=False, italic=False))
    assert exc.value.args[0] == '_write_url must be overridden ' + \
        'by a subclass MultiFormat2'
    check_capsys(capsys)


def test_to_write_optional_none(capsys: pytest.capturefixture[str]) -> None:
    """Test that the to_write_optional method handles None."""
    mfmt = MultiFormat2(file_name='test')
    assert mfmt._to_write_optional(None,  # pylint: disable=protected-access
                                   smart_ws=True, in_add=False) is None
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
def test_end_state(capsys: pytest.capturefixture[str],
                   from_state: MultiFormatState,
                   to_state: MultiFormatState,
                   count: dict[str, int]) -> None:
    """Test that the end_state method is correct."""
    mfmt = MultiFormat3(file_name='test')
    mfmt.state = from_state
    mfmt._end_state()  # pylint: disable=protected-access
    assert mfmt.state == to_state
    assert mfmt.count == count
    check_capsys(capsys)


def test_enter_exit(capsys: pytest.capturefixture[str]) -> None:
    """Test that the enter and exit methods are correct."""
    with MultiFormat5(file_name='test', expected_text='abc') as mfmt:
        assert isinstance(mfmt, MultiFormat5)
        assert mfmt.count == {'open': 1}
    assert isinstance(mfmt, MultiFormat5)
    assert mfmt.count == {'open': 1, '_close': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('from_state, to_state, count, level, text',
                         [(MultiFormatState.EMPTY,
                           MultiFormatState.HEADING,
                           {'_encode_text': 1, '_start_heading': 1,
                            '_write_text': 1, '_write_file_prefix': 1},
                           1, 'Main Heading'),
                          (MultiFormatState.PARAGRAPH_END,
                           MultiFormatState.HEADING,
                           {'_encode_text': 1, '_start_heading': 1,
                            '_write_text': 1},
                           2, 'Subheading'),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.HEADING,
                           {'_encode_text': 1, '_end_paragraph': 1,
                            '_start_heading': 1, '_write_text': 1},
                           3, 'Sub-subheading')])
def test_new_heading(capsys: pytest.capturefixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                     from_state, to_state, count, level, text) -> None:
    """Test that the new_heading method is correct."""
    mfmt = MultiFormat8(file_name='test', expected_text=text,
                        expected_level=level)
    mfmt.state = from_state
    mfmt.new_heading(level=level, text=text)
    assert mfmt.state == to_state
    assert mfmt.heading_level == level
    assert mfmt.count == count
    check_capsys(capsys)


@pytest.mark.parametrize('level, text, bold, italic',
                         [(1, 'Heading', False, False),
                          (2, 'Bold Heading', True, False),
                          (3, 'Italic Heading', False, True),
                          (4, 'Both Heading', True, True)])
def test_new_heading_bold_italic(capsys: pytest.capturefixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                 level, text, bold, italic) -> None:
    """Test new_heading with bold and italic parameters."""
    mfmt = MultiFormat8(file_name='test', expected_text=text,
                        expected_level=level,
                        expected_bold=bold, expected_italic=italic)
    mfmt.new_heading(level=level, text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.HEADING
    assert mfmt.heading_level == level
    assert mfmt.count == {'_encode_text': 1, '_start_heading': 1,
                          '_write_text': 1, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_heading_add_text(capsys: pytest.capturefixture[str]) -> None:
    """Test adding text to a heading."""
    mfmt = MultiFormat8(file_name='test', expected_text='More text',
                        expected_level=1)
    mfmt.state = MultiFormatState.HEADING
    mfmt.heading_level = 1
    mfmt.add_text(text='More text')
    assert mfmt.state == MultiFormatState.HEADING
    assert mfmt.count == {'_encode_text': 1, '_write_text': 1}
    check_capsys(capsys)


def test_heading_add_url(capsys: pytest.capturefixture[str]) -> None:
    """Test adding URL to a heading."""
    mfmt = MultiFormat9(file_name='test',
                        expected_url='http://example.com',
                        expected_url_text='Example')
    mfmt.state = MultiFormatState.HEADING
    mfmt.heading_level = 1
    mfmt.add_url(url='http://example.com', text='Example')
    assert mfmt.state == MultiFormatState.HEADING
    assert mfmt.count == {'_encode_text': 1, '_write_url': 1}
    check_capsys(capsys)


def test_end_state_heading(capsys: pytest.capturefixture[str]) -> None:
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


def test_heading_then_paragraph(capsys: pytest.capturefixture[str]) -> None:
    """Test heading followed by paragraph."""
    mfmt = MultiFormat8(file_name='test', expected_text='Title',
                        expected_level=1)
    mfmt.new_heading(level=1, text='Title')
    assert mfmt.state.name == 'HEADING'
    # Now start a paragraph - should end the heading
    # Note: We don't check expected_level for the paragraph
    mfmt.expected_text = 'Paragraph text'
    mfmt.new_paragraph(text='Paragraph text')
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.heading_level is None
    assert mfmt.count == {'_encode_text': 2, '_start_heading': 1,
                          '_write_text': 2, '_write_file_prefix': 1,
                          '_end_heading': 1, '_start_paragraph': 1}
    check_capsys(capsys)


def test_multiple_headings(capsys: pytest.capturefixture[str]) -> None:
    """Test multiple headings in sequence."""
    mfmt = MultiFormat8(file_name='test', expected_text='First',
                        expected_level=1)
    mfmt.new_heading(level=1, text='First')
    assert mfmt.heading_level == 1
    # Start another heading - should end the first
    mfmt.expected_text = 'Second'
    mfmt.expected_level = 2
    mfmt.new_heading(level=2, text='Second')
    assert mfmt.heading_level == 2
    assert mfmt.count == {'_encode_text': 2, '_start_heading': 2,
                          '_write_text': 2, '_write_file_prefix': 1,
                          '_end_heading': 1}
    check_capsys(capsys)


def test_heading_with_smart_ws(capsys: pytest.capturefixture[str]) -> None:
    """Test heading with smart_ws parameter."""
    mfmt = MultiFormat8(file_name='test', expected_text='Heading',
                        expected_level=1)
    mfmt.new_heading(level=1, text='  Heading  ', smart_ws=True)
    assert mfmt.ws_needed_at_append is True
    mfmt.expected_text = ' more'
    mfmt.add_text(text='  more  ', smart_ws=True)
    assert mfmt.count == {'_encode_text': 2, '_start_heading': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)


# Tests for code blocks


class MultiFormat12(MultiFormat4):
    """Class used for testing code blocks and code in text."""

    def __init__(self,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 expected_code: str,
                 expected_text: str = '',
                 expected_bold: bool = False,
                 expected_italic: bool = False,
                 file_name: str = 'test',
                 code_in: bool = False):
        """Initialize the MultiFormat11 class."""
        super().__init__(file_name=file_name, expected_text=expected_text,
                         expected_bold=expected_bold,
                         expected_italic=expected_italic)
        self.expected_code: str = expected_code
        self.code_in: bool = code_in

    def _write_code_in_text(self, text: str, state: MultiFormatState) -> None:
        """Write code into text."""
        assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        self.inc_count('_write_code_in_text')
        assert text == self.expected_code

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
        if self.code_in:
            assert text in self.expected_code
        else:
            assert text == self.expected_code

    def _start_block_quote(self) -> None:
        """Start a block quote."""
        self.inc_count('_start_block_quote')

    def _end_block_quote(self) -> None:
        """End a block quote."""
        self.inc_count('_end_block_quote')


def test_write_code_block_basic(capsys: pytest.capturefixture[str]) -> None:
    """Test basic code block writing."""
    txt = 'print("Hello")'
    mfmt = MultiFormat12(file_name='test', expected_code=txt)
    assert mfmt.state.name == 'EMPTY'
    mfmt.write_code_block(text=txt)
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_encode_text': 1,
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_write_code_block_with_language(
        capsys: pytest.capturefixture[str]) -> None:
    """Test code block with programming language."""
    txt = 'x = 42'
    mfmt = MultiFormat12(file_name='test', expected_code=txt)
    mfmt.write_code_block(text=txt, programming_language='python')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_encode_text': 1,
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_paragraph_then_code_block(capsys: pytest.capturefixture[str]) -> None:
    """Test paragraph followed by code block."""
    code = 'code here'
    text = 'Here is code:'
    mfmt = MultiFormat12(file_name='test',
                         expected_code=code, expected_text=text)
    mfmt.new_paragraph(text=text)
    mfmt.write_code_block(text=code)
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_paragraph': 1,
        '_write_text': 1,
        '_end_paragraph': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_code_block_then_paragraph(capsys: pytest.capturefixture[str]) -> None:
    """Test code block followed by paragraph."""
    code = 'code'
    text = 'After code'
    mfmt = MultiFormat12(file_name='test',
                         expected_code=code, expected_text=text)
    mfmt.write_code_block(text=code)
    mfmt.new_paragraph(text=text)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1,
        '_start_paragraph': 1,
        '_write_text': 1}
    check_capsys(capsys)


def test_multiple_code_blocks(capsys: pytest.capturefixture[str]) -> None:
    """Test multiple code blocks in sequence."""
    mfmt = MultiFormat12(file_name='test',
                         expected_code='first, second', code_in=True)
    mfmt.write_code_block(text='first', programming_language='python')
    mfmt.write_code_block(text='second', programming_language='javascript')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_code_block': 2,
        '_write_code_block': 2,
        '_end_code_block': 2}
    check_capsys(capsys)


def test_code_block_multiline(capsys: pytest.capturefixture[str]) -> None:
    """Test code block with multiline text."""
    code = 'def hello() -> None:\n    print("Hello")\n    return True'
    mfmt = MultiFormat12(file_name='test', expected_code=code)
    mfmt.write_code_block(text=code, programming_language='python')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_encode_text': 1,
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_code_block_empty(capsys: pytest.capturefixture[str]) -> None:
    """Test code block with empty text."""
    mfmt = MultiFormat12(file_name='test', expected_code='')
    mfmt.write_code_block(text='')
    assert mfmt.state == MultiFormatState.PARAGRAPH_END
    assert mfmt.count == {
        '_encode_text': 1,
        '_write_file_prefix': 1,
        '_start_code_block': 1,
        '_write_code_block': 1,
        '_end_code_block': 1}
    check_capsys(capsys)


def test_invalid_state_plist(capsys: pytest.capturefixture[str]) -> None:
    """Test the handling of invalid state for point lists."""
    mfmt = MultiFormat12(file_name='test', expected_code='')
    mfmt.state = MultiFormatState.BULLET_LIST_ITEM
    with pytest.raises(KeyError):
        psi = PointStackItem(
            point_list_type=17,  # type: ignore[typeddict-item]
            number_at_level=1
        )
        mfmt.point_list_stack.append(psi)
        mfmt._state_from_point_list()  # pylint: disable=protected-access # noqa: E501
    check_capsys(capsys)


def test_code_in_text(capsys: pytest.capturefixture[str]) -> None:
    """Test code in text."""
    code = ' print("Hello")'
    text = 'Here is code:'
    mfmt = MultiFormat12(file_name='test', expected_code=code,
                         expected_text=text)
    mfmt.new_paragraph(text=text)
    mfmt.add_code_in_text(text=code)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {
        '_encode_text': 2,
        '_write_file_prefix': 1,
        '_start_paragraph': 1,
        '_write_text': 1,
        '_write_code_in_text': 1}
    check_capsys(capsys)


def test_code_in_text_nok1(capsys: pytest.capturefixture[str]) -> None:
    """Test error that the code in text is not allowed with line breaks."""
    code = 'print("Hello")\nprint("World")'
    text = 'Here is code:'
    mfmt = MultiFormat12(file_name='test', expected_code=code,
                         expected_text=text)
    mfmt.new_paragraph(text=text)
    with pytest.raises(RuntimeError) as exc:
        mfmt.add_code_in_text(text=code)
    assert exc.value.args[0] == \
        'Cannot add code in text with line breaks. ' + \
        'Use write_code_block for that.'
    check_capsys(capsys)


def test_code_in_text_nok2(capsys: pytest.capturefixture[str]) -> None:
    """Test error that code in text is done in an invalid state."""
    code = 'print("Hello")'
    text = 'Here is code:'
    mfmt = MultiFormat12(file_name='test', expected_code=code,
                         expected_text=text)
    mfmt.state = MultiFormatState.BULLET_LIST
    with pytest.raises(RuntimeError) as exc:
        mfmt.add_code_in_text(text=code)
    assert exc.value.args[0] == 'Cannot add code in text to state ' + \
        'BULLET_LIST'
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic',
                         [('Here is text', False, False),
                          ('Something else', True, False),
                          ('Third string', False, True),
                          ('Fourth text', True, True)])
def test_block_quote_1(capsys: pytest.capturefixture[str],
                       text: str, bold: bool, italic: bool) -> None:
    """Test block quote."""
    mfmt = MultiFormat12(file_name='test', expected_text=text,
                         expected_bold=bold, expected_italic=italic,
                         code_in=False, expected_code='')
    mfmt.new_block_quote(text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.BLOCK_QUOTE
    assert mfmt.count == {'_encode_text': 1, '_start_block_quote': 1,
                          '_write_text': 1, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_block_quote_2(capsys: pytest.capturefixture[str]) -> None:
    """Test block quote."""
    mfmt = MultiFormat12(file_name='test', expected_text='Block quote',
                         expected_bold=False, expected_italic=False,
                         code_in=False, expected_code='')
    mfmt.new_block_quote(text='Block quote')
    assert mfmt.state == MultiFormatState.BLOCK_QUOTE
    mfmt.expected_text = ' More text'
    mfmt.add_text(text='More text')
    assert mfmt.state == MultiFormatState.BLOCK_QUOTE
    assert mfmt.count == {'_encode_text': 2, '_start_block_quote': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_block_quote_3(capsys: pytest.capturefixture[str]) -> None:
    """Test block quote."""
    mfmt = MultiFormat12(file_name='test', expected_text='Block quote',
                         expected_bold=False, expected_italic=False,
                         code_in=False, expected_code='')
    mfmt.new_block_quote(text='Block quote')
    assert mfmt.state == MultiFormatState.BLOCK_QUOTE
    mfmt.expected_text = 'Paragraph text'
    mfmt.new_paragraph(text='Paragraph text')
    assert mfmt.count == {'_end_block_quote': 1, '_encode_text': 2,
                          '_start_block_quote': 1, '_start_paragraph': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_block_quote_4(capsys: pytest.capturefixture[str]) -> None:
    """Test block quote."""
    mfmt = MultiFormat12(file_name='test', expected_text='Block quote 1',
                         expected_bold=False, expected_italic=False,
                         code_in=False, expected_code='')
    mfmt.new_block_quote(text='Block quote 1')
    assert mfmt.state == MultiFormatState.BLOCK_QUOTE
    mfmt.expected_text = 'Next block quote'
    mfmt.new_block_quote(text='Next block quote')
    assert mfmt.count == {'_end_block_quote': 1, '_encode_text': 2,
                          '_start_block_quote': 2,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)
