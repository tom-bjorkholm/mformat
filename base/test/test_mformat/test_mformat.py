#! /usr/local/bin/python3
"""Test the mformat module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional
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

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   bold: bool, italic: bool) -> None:
        """Write a URL into current item.

        (paragraph, bullet list item, etc.)
        """
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        # pylint: disable=duplicate-code
        assert isinstance(url, str)
        if text is not None:
            assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        self.inc_count('_write_url')

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
                           'xyz'),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           MultiFormatState.BULLET_LIST_ITEM,
                           {'_write_text': 1},
                           'def'),
                          (MultiFormatState.NUMERIC_LIST_ITEM,
                           MultiFormatState.NUMERIC_LIST_ITEM,
                           {'_write_text': 1},
                           'ghi')])
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
                         [('abc', False, False, 'abc'),
                          ('def', True, False, 'def'),
                          ('ghi', False, True, 'ghi'),
                          ('jkl', True, True, 'jkl')])
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


class MultiFormat6(MultiFormat3):
    """Class used for testing add_url."""

    def __init__(self, file_name: str, expected_url: str,
                 expected_url_text: Optional[str] = None,
                 expected_bold: bool = False,
                 expected_italic: bool = False,
                 url_as_text: bool = False):
        """Initialize the MultiFormat6 class."""
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        super().__init__(file_name=file_name)
        self.expected_url: str = expected_url
        self.expected_url_text: Optional[str] = expected_url_text
        self.expected_bold: bool = expected_bold
        self.expected_italic: bool = expected_italic
        self.url_as_text: bool = url_as_text

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   bold: bool, italic: bool) -> None:
        """Write a URL into current item.

        (paragraph, bullet list item, etc.)
        """
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        super()._write_url(url, text, state, bold, italic)
        assert url == self.expected_url
        assert text == self.expected_url_text
        assert bold == self.expected_bold
        assert italic == self.expected_italic


@pytest.mark.parametrize('from_state, exc, msg',
                         [(MultiFormatState.PARAGRAPH_END,
                           RuntimeError,
                           'Cannot add URL to state PARAGRAPH_END'),
                          (MultiFormatState.BULLET_LIST,
                           RuntimeError,
                           'Cannot add URL to state BULLET_LIST'),
                          (MultiFormatState.EMPTY,
                           RuntimeError,
                           'Cannot add URL to state EMPTY')])
def test_add_url_error(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                       from_state, exc, msg):
    """Test that the add_url method raises an error in wrong state."""
    mfmt = MultiFormat6(file_name='test',
                        expected_url='http://example.com')
    mfmt.state = from_state
    with pytest.raises(exc) as exc2:
        mfmt.add_url(url='http://example.com')
    assert exc2.value.args[0] == msg
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected_url, expected_text',
                         [('http://example.com', None,
                           'http://example.com', None),
                          ('http://test.org', 'link text',
                           'http://test.org', 'link text'),
                          ('http://test.org', '  link text  ',
                           'http://test.org', 'link text')])
def test_add_url(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url, text, expected_url, expected_text):
    """Test that the add_url method is correct."""
    mfmt = MultiFormat6(file_name='test', expected_url=expected_url,
                        expected_url_text=expected_text)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_write_url': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected_url, '
                         'expected_text, expected_bold, expected_italic',
                         [('http://example.com', None, False, False,
                           'http://example.com', None, False, False),
                          ('http://test.org', 'link', True, False,
                           'http://test.org', 'link', True, False),
                          ('http://test.org', 'link', False, True,
                           'http://test.org', 'link', False, True),
                          ('http://test.org', 'link', True, True,
                           'http://test.org', 'link', True, True)])
def test_add_url_bold_italic(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             url, text, bold, italic, expected_url,
                             expected_text, expected_bold, expected_italic):
    """Test add_url with bold and italic parameters."""
    mfmt = MultiFormat6(file_name='test', expected_url=expected_url,
                        expected_url_text=expected_text,
                        expected_bold=expected_bold,
                        expected_italic=expected_italic)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_write_url': 1}
    check_capsys(capsys)


class MultiFormat7(MultiFormat4):
    """Class used for testing add_url with url_as_text=True."""

    def __init__(self, file_name: str, expected_text: str,
                 expected_bold: bool = False,
                 expected_italic: bool = False,
                 url_as_text: bool = True):
        """Initialize the MultiFormat7 class."""
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        super().__init__(file_name=file_name,
                         expected_text=expected_text,
                         expected_bold=expected_bold,
                         expected_italic=expected_italic)
        self.url_as_text: bool = url_as_text


@pytest.mark.parametrize('url, text, expected_text',
                         [('http://example.com', None,
                           'http://example.com'),
                          ('http://test.org', 'See here',
                           'See here http://test.org'),
                          ('http://test.org', '  See here  ',
                           'See here http://test.org')])
def test_add_url_as_text(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         url, text, expected_text):
    """Test add_url with url_as_text=True."""
    mfmt = MultiFormat7(file_name='test', expected_text=expected_text,
                        url_as_text=True)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_write_text': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected_text',
                         [('http://example.com', None, True, False,
                           'http://example.com'),
                          ('http://test.org', 'See', False, True,
                           'See http://test.org'),
                          ('http://test.org', 'Here', True, True,
                           'Here http://test.org')])
def test_add_url_as_text_formatting(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                    url, text, bold, italic, expected_text):
    """Test add_url with url_as_text=True and bold/italic."""
    mfmt = MultiFormat7(file_name='test', expected_text=expected_text,
                        expected_bold=bold, expected_italic=italic,
                        url_as_text=True)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_write_text': 1}
    check_capsys(capsys)


def test_enter_exit(capsys):
    """Test that the enter and exit methods are correct."""
    with MultiFormat5(file_name='test', expected_text='abc') as mfmt:
        assert isinstance(mfmt, MultiFormat5)
        assert mfmt.count == {'open': 1}
    assert mfmt.count == {'open': 1, '_close': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('text, expected_text, expected_ws_needed',
                         [('hello', 'hello', True),
                          ('hello ', 'hello ', False),
                          ('hello\n', 'hello\n', False),
                          ('hello\t', 'hello\t', False),
                          ('hello\r', 'hello\r', False),
                          ('', '', False),
                          ('  ', '  ', False)])
def test_start_paragraph_smart_ws_false(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                        text, expected_text,
                                        expected_ws_needed):
    """Test start_paragraph with smart_ws=False."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text)
    mfmt.start_paragraph(text=text, smart_ws=False)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.ws_needed_at_append == expected_ws_needed
    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 1,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('text, expected_text, expected_ws_needed',
                         [('world', 'world', True),
                          ('world ', 'world ', False),
                          ('world\n', 'world\n', False),
                          ('', '', False),
                          ('  spaces  ', '  spaces  ', False)])
def test_add_text_smart_ws_false(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                 text, expected_text, expected_ws_needed):
    """Test add_text with smart_ws=False."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_text(text=text, smart_ws=False)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.ws_needed_at_append == expected_ws_needed
    assert mfmt.count == {'_write_text': 1}
    check_capsys(capsys)


def test_smart_ws_false_no_space_between_texts(capsys):
    """Test that smart_ws=False does not add space between texts."""
    # First call: write 'hello' (no trailing whitespace)
    mfmt = MultiFormat4(file_name='test', expected_text='hello')
    mfmt.start_paragraph(text='hello', smart_ws=False)
    assert mfmt.ws_needed_at_append is True

    # Second call: write 'world' (should NOT get leading space)
    mfmt.expected_text = 'world'
    mfmt.add_text(text='world', smart_ws=False)
    assert mfmt.ws_needed_at_append is True
    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 2,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


def test_smart_ws_false_with_trailing_space(capsys):
    """Test smart_ws=False with text that has trailing whitespace."""
    # First call: write 'hello ' (with trailing space)
    mfmt = MultiFormat4(file_name='test', expected_text='hello ')
    mfmt.start_paragraph(text='hello ', smart_ws=False)
    assert mfmt.ws_needed_at_append is False

    # Second call: write 'world' (should NOT get leading space)
    mfmt.expected_text = 'world'
    mfmt.add_text(text='world', smart_ws=False)
    assert mfmt.ws_needed_at_append is True
    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 2,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


def test_smart_ws_false_empty_text(capsys):
    """Test smart_ws=False with empty text."""
    mfmt = MultiFormat4(file_name='test', expected_text='')
    mfmt.start_paragraph(text='', smart_ws=False)
    assert mfmt.ws_needed_at_append is False

    # Add more text after empty start
    mfmt.expected_text = 'content'
    mfmt.add_text(text='content', smart_ws=False)
    assert mfmt.ws_needed_at_append is True
    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 2,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


@pytest.mark.parametrize(
    'first_text, first_smart_ws, second_text, second_smart_ws, '
    'expected_second',
    [
        # smart_ws=False (no trailing ws) followed by smart_ws=True
        ('hello', False, 'world', True, ' world'),
        # smart_ws=False (with trailing ws) followed by smart_ws=True
        ('hello ', False, 'world', True, 'world'),
        ('hello\n', False, 'world', True, 'world'),
        # smart_ws=False (empty) followed by smart_ws=True
        ('', False, 'world', True, 'world'),
        # smart_ws=True followed by smart_ws=False (no space added)
        ('hello', True, 'world', False, 'world'),
        # smart_ws=True followed by smart_ws=True (normal behavior)
        ('hello', True, 'world', True, ' world'),
        # Multiple mixed calls
        ('text ', False, 'more', True, 'more'),
    ])
def test_mixed_smart_ws_modes(capsys,  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                              first_text, first_smart_ws, second_text,
                              second_smart_ws, expected_second):
    """Test mixing smart_ws=False and smart_ws=True."""
    # First call
    expected_first = first_text.strip() if first_smart_ws else first_text
    mfmt = MultiFormat4(file_name='test', expected_text=expected_first)
    mfmt.start_paragraph(text=first_text, smart_ws=first_smart_ws)

    # Second call
    mfmt.expected_text = expected_second
    mfmt.add_text(text=second_text, smart_ws=second_smart_ws)

    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 2,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


def test_complex_mixed_smart_ws_sequence(capsys):
    """Test a complex sequence mixing smart_ws modes."""
    # Start with smart_ws=False, text ending without whitespace
    mfmt = MultiFormat4(file_name='test', expected_text='First')
    mfmt.start_paragraph(text='First', smart_ws=False)
    assert mfmt.ws_needed_at_append is True

    # Add with smart_ws=True - should add space
    mfmt.expected_text = ' second'
    mfmt.add_text(text='second', smart_ws=True)
    assert mfmt.ws_needed_at_append is True

    # Add with smart_ws=False - should NOT add space (doesn't check state)
    mfmt.expected_text = 'third'
    mfmt.add_text(text='third', smart_ws=False)
    assert mfmt.ws_needed_at_append is True

    # Add with smart_ws=True - should add space
    mfmt.expected_text = ' fourth'
    mfmt.add_text(text='fourth', smart_ws=True)

    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 4,
                          '_write_file_prefix': 1}
    check_capsys(capsys)


def test_smart_ws_false_trailing_ws_then_smart_ws_true(capsys):
    """Test smart_ws=False with trailing whitespace, then smart_ws=True."""
    # Write text with trailing space using smart_ws=False
    mfmt = MultiFormat4(file_name='test', expected_text='Hello ')
    mfmt.start_paragraph(text='Hello ', smart_ws=False)
    assert mfmt.ws_needed_at_append is False

    # Add text with smart_ws=True - should NOT add space
    mfmt.expected_text = 'world'
    mfmt.add_text(text='world', smart_ws=True)
    assert mfmt.ws_needed_at_append is True

    assert mfmt.count == {'_start_paragraph': 1, '_write_text': 2,
                          '_write_file_prefix': 1}
    check_capsys(capsys)
