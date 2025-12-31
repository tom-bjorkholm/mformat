#! /usr/local/bin/python3
"""Test the mformat module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
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


class MultiFormat2(MultiFormat):
    """Class used for testing."""

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.test'


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
                          '_start_paragraph', '_end_paragraph', '_write_text'])
def test_cls_method_not_overridden(capsys, method_name):
    """Test that the instance method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        if method_name == '_write_text':
            _ = getattr(mfmt, method_name)('test', MultiFormatState.PARAGRAPH,
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


class MultiFormat3(MultiFormat2):
    """Class used for testing."""

    def __init__(self, file_name: str):
        """Initialize the MultiFormat3 class."""
        super().__init__(file_name=file_name)
        self.count: dict[str, int] = {}

    def inc_count(self, func_name: str) -> None:
        """Increment the count for the function name."""
        if func_name not in self.count:
            self.count[func_name] = 1
        else:
            self.count[func_name] += 1

    def _write_text(self, text: str, state: MultiFormatState,
                    bold: bool, italic: bool) -> None:
        """Write text into current item (paragraph, bullet list item, etc.)."""
        assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        self.inc_count('_write_text')

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self.inc_count('_start_paragraph')

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        self.inc_count('_end_paragraph')

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""
        self.inc_count('_write_file_prefix')

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""
        self.inc_count('_write_file_suffix')


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


class MultiFormat4(MultiFormat3):
    """Class used for testing."""

    def __init__(self, file_name: str, expected_text: str,
                 expected_bold: bool = False,
                 expected_italic: bool = False):
        """Initialize the MultiFormat4 class."""
        super().__init__(file_name=file_name)
        self.expected_text: str = expected_text
        self.expected_bold: bool = expected_bold
        self.expected_italic: bool = expected_italic

    def _write_text(self, text: str, state: MultiFormatState,
                    bold: bool, italic: bool) -> None:
        """Write text into current item (paragraph, bullet list item, etc.)."""
        super()._write_text(text, state, bold, italic)
        assert text == self.expected_text
        assert bold == self.expected_bold
        assert italic == self.expected_italic


@pytest.mark.parametrize('from_state, to_state, count, text',
                         [(MultiFormatState.EMPTY,
                           MultiFormatState.PARAGRAPH,
                           {'_start_paragraph': 1, '_write_text': 1,
                            '_write_file_prefix': 1},
                           'abc'),
                          (MultiFormatState.PARAGRAPH_END,
                           MultiFormatState.PARAGRAPH,
                           {'_start_paragraph': 1, '_write_text': 1},
                           'abc'),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.PARAGRAPH,
                           {'_end_paragraph': 1, '_start_paragraph': 1,
                            '_write_text': 1},
                           'def')])
def test_start_paragraph(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         from_state, to_state, count, text):
    """Test that the start_paragraph method is correct."""
    mfmt = MultiFormat4(file_name='test', expected_text=text)
    mfmt.state = from_state
    mfmt.start_paragraph(text=text)
    assert mfmt.state == to_state
    assert mfmt.count == count
    check_capsys(capsys)


@pytest.mark.parametrize('from_state, text, exc, msg',
                         [(MultiFormatState.PARAGRAPH_END,
                           'abc',
                           RuntimeError,
                           'Cannot add text to state PARAGRAPH_END'),
                          (MultiFormatState.BULLET_LIST,
                           'abc',
                           RuntimeError,
                           'Cannot add text to state BULLET_LIST'),
                          (MultiFormatState.EMPTY,
                           'abc',
                           RuntimeError,
                           'Cannot add text to state EMPTY')])
def test_add_text_error(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                        from_state, text, exc, msg):
    """Test that the add_text method raises an error in wrong state."""
    mfmt = MultiFormat4(file_name='test', expected_text=text)
    mfmt.state = from_state
    with pytest.raises(exc) as exc2:
        mfmt.add_text(text=text)
    assert exc2.value.args[0] == msg
    check_capsys(capsys)


@pytest.mark.parametrize('from_state, to_state, count, text',
                         [(MultiFormatState.PARAGRAPH,
                           MultiFormatState.PARAGRAPH,
                           {'_write_text': 1},
                           ' xyz'),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           MultiFormatState.BULLET_LIST_ITEM,
                           {'_write_text': 1},
                           ' def'),
                          (MultiFormatState.NUMERIC_LIST_ITEM,
                           MultiFormatState.NUMERIC_LIST_ITEM,
                           {'_write_text': 1},
                           ' ghi')])
def test_add_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                  from_state, to_state, count, text):
    """Test that the add_text method is correct."""
    mfmt = MultiFormat4(file_name='test', expected_text=text)
    mfmt.state = from_state
    mfmt.add_text(text=text)
    assert mfmt.state == to_state
    assert mfmt.count == count
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected_text',
                         [('abc', False, False, 'abc'),
                          ('def', True, False, 'def'),
                          ('ghi', False, True, 'ghi'),
                          ('jkl', True, True, 'jkl')])
def test_start_paragraph_bold_italic(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                     text, bold, italic, expected_text):
    """Test start_paragraph with bold and italic parameters."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text,
                        expected_bold=bold, expected_italic=italic)
    mfmt.start_paragraph(text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 1,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected_text',
                         [('abc', False, False, ' abc'),
                          ('def', True, False, ' def'),
                          ('ghi', False, True, ' ghi'),
                          ('jkl', True, True, ' jkl')])
def test_add_text_bold_italic(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                              text, bold, italic, expected_text):
    """Test add_text with bold and italic parameters."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text,
                        expected_bold=bold, expected_italic=italic)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_text(text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_write_text': 1}
    check_capsys(capsys)


class MultiFormat5(MultiFormat4):
    """Class used for testing."""

    def open(self) -> None:
        """Open the file."""
        self.inc_count('open')

    def _close(self) -> None:
        """Close the file."""
        self.inc_count('_close')


def test_enter_exit(capsys):
    """Test that the enter and exit methods are correct."""
    with MultiFormat5(file_name='test', expected_text='abc') as mfmt:
        assert isinstance(mfmt, MultiFormat5)
        assert mfmt.count == {'open': 1}
    assert mfmt.count == {'open': 1, '_close': 1}
    check_capsys(capsys)
