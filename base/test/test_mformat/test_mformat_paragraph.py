#! /usr/local/bin/python3
"""Test paragraph, text, and URL functionality in the mformat module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest
from mformat.mformat_state import MultiFormatState
from .check_capsys import check_capsys
from .test_helpers import MultiFormat4, MultiFormat6, MultiFormat7


@pytest.mark.parametrize('from_state, to_state, count, text',
                         [(MultiFormatState.EMPTY,
                           MultiFormatState.PARAGRAPH,
                           {'_encode_text': 1, '_start_paragraph': 1,
                            '_write_text': 1, '_write_file_prefix': 1},
                           'abc'),
                          (MultiFormatState.PARAGRAPH_END,
                           MultiFormatState.PARAGRAPH,
                           {'_encode_text': 1, '_start_paragraph': 1,
                            '_write_text': 1},
                           'abc'),
                          (MultiFormatState.PARAGRAPH,
                           MultiFormatState.PARAGRAPH,
                           {'_encode_text': 1, '_end_paragraph': 1,
                            '_start_paragraph': 1, '_write_text': 1},
                           'def')])
def test_new_paragraph(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                       from_state: MultiFormatState,
                       to_state: MultiFormatState,
                       count: dict[str, int],
                       text: str) -> None:
    """Test that the new_paragraph method is correct."""
    mfmt = MultiFormat4(file_name='test', expected_text=text)
    mfmt.state = from_state
    mfmt.new_paragraph(text=text)
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
def test_add_text_error(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                        from_state: MultiFormatState,
                        text: str,
                        exc: type[RuntimeError],
                        msg: str) -> None:
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
                           {'_encode_text': 1, '_write_text': 1},
                           'xyz'),
                          (MultiFormatState.BULLET_LIST_ITEM,
                           MultiFormatState.BULLET_LIST_ITEM,
                           {'_encode_text': 1, '_write_text': 1},
                           'def'),
                          (MultiFormatState.NUMBERED_LIST_ITEM,
                           MultiFormatState.NUMBERED_LIST_ITEM,
                           {'_encode_text': 1, '_write_text': 1},
                           'ghi')])
def test_add_text(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                  from_state: MultiFormatState,
                  to_state: MultiFormatState,
                  count: dict[str, int],
                  text: str) -> None:
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
def test_new_paragraph_bold_italic(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                   text: str,
                                   bold: bool,
                                   italic: bool,
                                   expected_text: str) -> None:
    """Test new_paragraph with bold and italic parameters."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text,
                        expected_bold=bold, expected_italic=italic)
    mfmt.new_paragraph(text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_encode_text': 1, '_start_paragraph': 1,
                          '_write_text': 1, '_write_file_prefix': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('text, bold, italic, expected_text',
                         [('abc', False, False, 'abc'),
                          ('def', True, False, 'def'),
                          ('ghi', False, True, 'ghi'),
                          ('jkl', True, True, 'jkl')])
def test_add_text_bold_italic(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                              text: str,
                              bold: bool,
                              italic: bool,
                              expected_text: str) -> None:
    """Test add_text with bold and italic parameters."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text,
                        expected_bold=bold, expected_italic=italic)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_text(text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.count == {'_encode_text': 1, '_write_text': 1}
    check_capsys(capsys)


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
def test_add_url_error(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                       from_state: MultiFormatState,
                       exc: type[RuntimeError],
                       msg: str) -> None:
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
def test_add_url(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                 url: str,
                 text: str | None,
                 expected_url: str,
                 expected_text: str | None) -> None:
    """Test that the add_url method is correct."""
    mfmt = MultiFormat6(file_name='test', expected_url=expected_url,
                        expected_url_text=expected_text)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    if text is not None:
        assert mfmt.count == {'_encode_text': 1, '_write_url': 1}
    else:
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
def test_add_url_bold_italic(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                             url: str,
                             text: str | None,
                             bold: bool,
                             italic: bool,
                             expected_url: str,
                             expected_text: str | None,
                             expected_bold: bool,
                             expected_italic: bool) -> None:
    """Test add_url with bold and italic parameters."""
    mfmt = MultiFormat6(file_name='test', expected_url=expected_url,
                        expected_url_text=expected_text,
                        expected_bold=expected_bold,
                        expected_italic=expected_italic)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    if text is not None:
        assert mfmt.count == {'_encode_text': 1, '_write_url': 1}
    else:
        assert mfmt.count == {'_write_url': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, expected_text',
                         [('http://example.com', None,
                           'http://example.com'),
                          ('http://test.org', 'See here',
                           'See here http://test.org'),
                          ('http://test.org', '  See here  ',
                           'See here http://test.org')])
def test_add_url_as_text(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                         url: str,
                         text: str | None,
                         expected_text: str) -> None:
    """Test add_url with url_as_text=True."""
    mfmt = MultiFormat7(file_name='test', expected_text=expected_text,
                        url_as_text=True)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    if text is not None:
        assert mfmt.count == {'_encode_text': 1, '_write_text': 1}
    else:
        assert mfmt.count == {'_write_text': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('url, text, bold, italic, expected_text',
                         [('http://example.com', None, True, False,
                           'http://example.com'),
                          ('http://test.org', 'See', False, True,
                           'See http://test.org'),
                          ('http://test.org', 'Here', True, True,
                           'Here http://test.org')])
def test_add_url_as_text_formatting(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                    url: str, text: str, bold: bool,
                                    italic: bool, expected_text: str) -> None:
    """Test add_url with url_as_text=True and bold/italic."""
    mfmt = MultiFormat7(file_name='test', expected_text=expected_text,
                        expected_bold=bold, expected_italic=italic,
                        url_as_text=True)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url=url, text=text, bold=bold, italic=italic)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    if text is not None:
        assert mfmt.count == {'_encode_text': 1, '_write_text': 1}
    else:
        assert mfmt.count == {'_write_text': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('text, expected_text, expected_ws_needed',
                         [('hello', 'hello', True),
                          ('hello ', 'hello ', False),
                          ('hello\n', 'hello\n', False),
                          ('hello\t', 'hello\t', False),
                          ('hello\r', 'hello\r', False),
                          ('', '', False),
                          ('  ', '  ', False)])
def test_new_paragraph_smart_ws_false(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                      text: str,
                                      expected_text: str,
                                      expected_ws_needed: bool) -> None:
    """Test new_paragraph with smart_ws=False."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text)
    mfmt.new_paragraph(text=text, smart_ws=False)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.ws_needed_at_append == expected_ws_needed
    assert mfmt.count == {'_encode_text': 1, '_start_paragraph': 1,
                          '_write_text': 1, '_write_file_prefix': 1}
    check_capsys(capsys)


@pytest.mark.parametrize('text, expected_text, expected_ws_needed',
                         [('world', 'world', True),
                          ('world ', 'world ', False),
                          ('world\n', 'world\n', False),
                          ('', '', False),
                          ('  spaces  ', '  spaces  ', False)])
def test_add_text_smart_ws_false(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                                 text: str, expected_text: str,
                                 expected_ws_needed: bool) -> None:
    """Test add_text with smart_ws=False."""
    mfmt = MultiFormat4(file_name='test', expected_text=expected_text)
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_text(text=text, smart_ws=False)
    assert mfmt.state == MultiFormatState.PARAGRAPH
    assert mfmt.ws_needed_at_append == expected_ws_needed
    assert mfmt.count == {'_encode_text': 1, '_write_text': 1}
    check_capsys(capsys)


def test_smart_ws_false_no_space_between_texts(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that smart_ws=False does not add space between texts."""
    # First call: write 'hello' (no trailing whitespace)
    mfmt = MultiFormat4(file_name='test', expected_text='hello')
    mfmt.new_paragraph(text='hello', smart_ws=False)
    assert mfmt.ws_needed_at_append is True
    # Second call: write 'world' (should NOT get leading space)
    mfmt.expected_text = 'world'
    mfmt.add_text(text='world', smart_ws=False)
    assert mfmt.ws_needed_at_append is True
    assert mfmt.count == {'_encode_text': 2, '_start_paragraph': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_smart_ws_false_with_trailing_space(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test smart_ws=False with text that has trailing whitespace."""
    # First call: write 'hello ' (with trailing space)
    mfmt = MultiFormat4(file_name='test', expected_text='hello ')
    mfmt.new_paragraph(text='hello ', smart_ws=False)
    assert mfmt.ws_needed_at_append is False
    # Second call: write 'world' (should NOT get leading space)
    mfmt.expected_text = 'world'
    mfmt.add_text(text='world', smart_ws=False)
    assert mfmt.ws_needed_at_append is True
    assert mfmt.count == {'_encode_text': 2, '_start_paragraph': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_smart_ws_false_empty_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test smart_ws=False with empty text."""
    mfmt = MultiFormat4(file_name='test', expected_text='')
    mfmt.new_paragraph(text='', smart_ws=False)
    assert mfmt.ws_needed_at_append is False
    # Add more text after empty start
    mfmt.expected_text = 'content'
    mfmt.add_text(text='content', smart_ws=False)
    assert mfmt.ws_needed_at_append is True
    assert mfmt.count == {'_encode_text': 2, '_start_paragraph': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
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
def test_mixed_smart_ws_modes(capsys: pytest.CaptureFixture[str],  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
                              first_text: str,
                              first_smart_ws: bool,
                              second_text: str,
                              second_smart_ws: bool,
                              expected_second: str) -> None:
    """Test mixing smart_ws=False and smart_ws=True."""
    # First call
    expected_first = first_text.strip() if first_smart_ws else first_text
    mfmt = MultiFormat4(file_name='test', expected_text=expected_first)
    mfmt.new_paragraph(text=first_text, smart_ws=first_smart_ws)
    # Second call
    mfmt.expected_text = expected_second
    mfmt.add_text(text=second_text, smart_ws=second_smart_ws)
    assert mfmt.count == {'_encode_text': 2, '_start_paragraph': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_complex_mixed_smart_ws_sequence(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test a complex sequence mixing smart_ws modes."""
    # Start with smart_ws=False, text ending without whitespace
    mfmt = MultiFormat4(file_name='test', expected_text='First')
    mfmt.new_paragraph(text='First', smart_ws=False)
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
    assert mfmt.count == {'_encode_text': 4, '_start_paragraph': 1,
                          '_write_text': 4, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_smart_ws_false_trailing_ws_then_smart_ws_true(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test smart_ws=False with trailing whitespace, then smart_ws=True."""
    # Write text with trailing space using smart_ws=False
    mfmt = MultiFormat4(file_name='test', expected_text='Hello ')
    mfmt.new_paragraph(text='Hello ', smart_ws=False)
    assert mfmt.ws_needed_at_append is False
    # Add text with smart_ws=True - should NOT add space
    mfmt.expected_text = 'world'
    mfmt.add_text(text='world', smart_ws=True)
    assert mfmt.ws_needed_at_append is True
    assert mfmt.count == {'_encode_text': 2, '_start_paragraph': 1,
                          '_write_text': 2, '_write_file_prefix': 1}
    check_capsys(capsys)


def test_url_then_text_spacing(capsys: pytest.CaptureFixture[str]) -> None:
    """Test that add_text after add_url gets proper spacing."""
    mfmt = MultiFormat6(file_name='test',
                        expected_url='http://example.com',
                        expected_url_text='link')
    mfmt.state = MultiFormatState.PARAGRAPH
    mfmt.add_url(url='http://example.com', text='link')
    assert mfmt.ws_needed_at_append is True
    # Now add text - it should get a leading space
    mfmt2 = MultiFormat4(file_name='test', expected_text=' more text')
    mfmt2.state = MultiFormatState.PARAGRAPH
    mfmt2.ws_needed_at_append = True
    mfmt2.add_text(text='more text', smart_ws=True)
    assert mfmt2.count == {'_encode_text': 1, '_write_text': 1}
    check_capsys(capsys)


def test_url_then_text_no_spacing_when_smart_ws_false(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test add_text after add_url without smart_ws."""
    mfmt = MultiFormat6(file_name='test',
                        expected_url='http://example.com',
                        expected_url_text='link')
    mfmt.state = MultiFormatState.PARAGRAPH
    # URL text ends without whitespace
    mfmt.add_url(url='http://example.com', text='link', smart_ws=False)
    assert mfmt.ws_needed_at_append is True

    # Add text with smart_ws=False - no space added
    mfmt2 = MultiFormat4(file_name='test', expected_text='more')
    mfmt2.state = MultiFormatState.PARAGRAPH
    mfmt2.add_text(text='more', smart_ws=False)
    assert mfmt2.count == {'_encode_text': 1, '_write_text': 1}
    check_capsys(capsys)
