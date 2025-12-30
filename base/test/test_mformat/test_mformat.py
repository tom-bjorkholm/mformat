#! /usr/local/bin/python3
"""Test the mformat module."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from mformat.mformat import MultiFormat, MultiFormatState, NewOrAppend


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
                          '_start_paragraph', '_end_paragraph'])
def test_cls_method_not_overridden(capsys, method_name):
    """Test that the instance method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        _ = getattr(mfmt, method_name)()
    assert exc.value.args[0] == f'{method_name} must be overridden by a ' + \
        'subclass MultiFormat2'
    check_capsys(capsys)


def test_write_in_paragraph(capsys):
    """Test that the write_in_paragraph method is not overridden."""
    mfmt = MultiFormat2(file_name='test')
    with pytest.raises(NotImplementedError) as exc:
        mfmt._write_in_paragraph('test')  # pylint: disable=protected-access
    assert exc.value.args[0] == '_write_in_paragraph must be overridden ' + \
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

    def _write_in_paragraph(self, text: str) -> None:
        """Write text into current paragraph."""
        assert isinstance(text, str)
        self.inc_count('_write_in_paragraph')

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

    def __init__(self, file_name: str, expected_text: str):
        """Initialize the MultiFormat4 class."""
        super().__init__(file_name=file_name)
        self.expected_text: str = expected_text

    def _write_in_paragraph(self, text: str) -> None:
        """Write text into current paragraph."""
        super()._write_in_paragraph(text)
        assert text == self.expected_text


@pytest.mark.parametrize('from_state, to_state, count, how, text',
                         [(MultiFormatState.EMPTY,
                           MultiFormatState.PARAGRAPH,
                           {'_start_paragraph': 1, '_write_in_paragraph': 1,
                            '_write_file_prefix': 1},
                           NewOrAppend.NEW, 'abc'),
                          (MultiFormatState.PARAGRAPH_END,
                           MultiFormatState.PARAGRAPH,
                           {'_start_paragraph': 1, '_write_in_paragraph': 1},
                           NewOrAppend.NEW, 'abc'),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.PARAGRAPH,
                           {'_write_in_paragraph': 1},
                           NewOrAppend.APPEND_IF_EXISTS, 'abc'),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.PARAGRAPH,
                           {'_write_in_paragraph': 1},
                           NewOrAppend.MUST_APPEND, 'abc'),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.PARAGRAPH,
                           {'_end_paragraph': 1, '_start_paragraph': 1,
                            '_write_in_paragraph': 1},
                           NewOrAppend.NEW, 'abc')])
def test_write_paragraph(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         from_state, to_state, count, how, text):
    """Test that the write_paragraph method is correct."""
    mfmt = MultiFormat4(file_name='test', expected_text=text)
    mfmt.state = from_state
    mfmt.write_paragraph(text=text, how=how)
    assert mfmt.state == to_state
    assert mfmt.count == count
    check_capsys(capsys)


@pytest.mark.parametrize('from_state, to_state, how, text, exc, msg',
                         [(MultiFormatState.PARAGRAPH_END,
                           MultiFormatState.PARAGRAPH_END,
                           NewOrAppend.MUST_APPEND, 'abc',
                           RuntimeError,
                           'Paragraph append required, ' +
                           'but state is PARAGRAPH_END'),
                          (MultiFormatState.BULLET_LIST,
                           MultiFormatState.BULLET_LIST,
                           NewOrAppend.MUST_APPEND, 'abc',
                           RuntimeError,
                           'Paragraph append required, ' +
                           'but state is BULLET_LIST')])
def test_write_paragraph_error(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                               from_state, to_state, how, text, exc, msg):
    """Test that the write_paragraph method raises an error."""
    mfmt = MultiFormat4(file_name='test', expected_text=text)
    mfmt.state = from_state
    with pytest.raises(exc) as exc2:
        mfmt.write_paragraph(text=text, how=how)
    assert exc2.value.args[0] == msg
    assert mfmt.state == to_state
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
