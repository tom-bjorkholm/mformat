#! /usr/local/bin/python3
"""Test the mformat_plaintextlike module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Callable, TypeAlias, cast
import pytest
from mformat.mformat_plaintextlike import MultiFormatPlainTextLike
from mformat.mformat_state import MultiFormatState
from .check_capsys import check_capsys
from .test_helpers import check_invalid_character_encoding_constructor


class PlainTextLikeTestImpl(  # pylint: disable=too-few-public-methods
        MultiFormatPlainTextLike):
    """Minimal concrete subclass for testing."""

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension."""
        return '.test'

    def _write_file_prefix(self) -> None:
        """Write the file prefix (no-op for testing)."""

    def _write_file_suffix(self) -> None:
        """Write the file suffix (no-op for testing)."""


FormatterCallback: TypeAlias = Callable[[PlainTextLikeTestImpl], None]


def _write_and_read(callback: FormatterCallback) -> str:
    """Create a temp file, run callback with formatter, return content.

    The callback receives the opened MultiFormatPlainTextLike
    instance. After the callback returns, state is set to
    PARAGRAPH_END so that close does not trigger abstract methods.
    """
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        with PlainTextLikeTestImpl(file_name=file_name) as mf:
            callback(cast(PlainTextLikeTestImpl, mf))
            mf.state = MultiFormatState.PARAGRAPH_END
        with open(file=file_name, mode='rt',
                  encoding='utf-8') as f:
            return f.read()


def _write_and_read_bytes(
        callback: FormatterCallback,
        character_encoding: str) -> bytes:
    """Create a temp file, run callback, and return file bytes.

    The callback receives the opened MultiFormatPlainTextLike
    instance. After the callback returns, state is set to
    PARAGRAPH_END so that close does not trigger abstract methods.
    """
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        with PlainTextLikeTestImpl(
                file_name=file_name,
                character_encoding=character_encoding) as mf:
            callback(cast(PlainTextLikeTestImpl, mf))
            mf.state = MultiFormatState.PARAGRAPH_END
        with open(file=file_name, mode='rb') as f:
            return f.read()


# =================================================================
# Init state
# =================================================================

def test_init_line_wrapping_state(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that line wrapping state is initialized."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        # pylint: disable=protected-access
        mf = PlainTextLikeTestImpl(file_name=file_name)
        assert mf._current_column == 0
        assert mf._continuation_indent == ''
        assert mf._pending_whitespace == ''
    check_capsys(capsys)


@pytest.mark.parametrize('character_encoding, expected_bytes',
                         [('utf-8', b'Caf\xc3\xa9'),
                          ('iso-8859-1', b'Caf\xe9')])
def test_init_character_encoding(
        capsys: pytest.CaptureFixture[str],
        character_encoding: str,
        expected_bytes: bytes) -> None:
    """Test that selected character encoding is used for written bytes."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Café')

    assert _write_and_read_bytes(callback, character_encoding) == \
        expected_bytes
    check_capsys(capsys)


def test_init_invalid_character_encoding(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test invalid encoding is propagated from Python open."""
    check_invalid_character_encoding_constructor(
        formatter_class=PlainTextLikeTestImpl, file_extension='.test')
    check_capsys(capsys)


# =================================================================
# _reset_line_state
# =================================================================

@pytest.mark.parametrize('indent', ['', '  ', '> ', '    '])
def test_reset_line_state(
        capsys: pytest.CaptureFixture[str],
        indent: str) -> None:
    """Test _reset_line_state resets all tracking fields."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        # pylint: disable=protected-access
        mf = PlainTextLikeTestImpl(file_name=file_name)
        mf._current_column = 42
        mf._continuation_indent = 'xxx'
        mf._pending_whitespace = 'yyy'
        mf._reset_line_state(continuation_indent=indent)
        assert mf._current_column == 0
        assert mf._continuation_indent == indent
        assert mf._pending_whitespace == ''
    check_capsys(capsys)


# =================================================================
# _write_line_break
# =================================================================

def test_write_line_break(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _write_line_break writes newline and resets state."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Hello')
        mf._pending_whitespace = '  '
        mf._current_column = 5
        mf._write_line_break()
        assert mf._pending_whitespace == ''
        assert mf._current_column == 0
    assert _write_and_read(callback) == 'Hello\n'
    check_capsys(capsys)


# =================================================================
# _empty_line_before
# =================================================================

@pytest.mark.parametrize('before, now, expected',
                         [('\n\n', 'Hello', '\n\nHello'),
                          ('', 'Hi', 'Hi'),
                          ('Hallo\n', 'Welt', 'Hallo\n\nWelt'),
                          ('Hello', 'World', 'Hello\n\nWorld')])
def test_empty_line_before(
        capsys: pytest.CaptureFixture[str],
        before: str,
        now: str,
        expected: str) -> None:
    """Test _empty_line_before ensures an empty line."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write(before)
        mf._empty_line_before()
        mf.file.write(now)
    assert _write_and_read(callback) == expected
    check_capsys(capsys)


# =================================================================
# _indent2
# =================================================================

@pytest.mark.parametrize('level, expected',
                         [(1, ''),
                          (2, '  '),
                          (3, '    '),
                          (4, '      ')])
def test_indent2(
        capsys: pytest.CaptureFixture[str],
        level: int,
        expected: str) -> None:
    """Test _indent2 returns indentation and warns as deprecated."""
    with TemporaryDirectory() as temp_dir:
        file_name = str(Path(temp_dir) / 'test.test')
        # pylint: disable=protected-access
        mf = PlainTextLikeTestImpl(file_name=file_name)
        with pytest.deprecated_call(
                match='_indent2 is deprecated. '
                'Use _indent_for_level instead.'):
            assert mf._indent2(level) == expected
        assert mf._indent_for_level(level) == expected
    check_capsys(capsys)


# =================================================================
# _wrap_and_write
# =================================================================

@pytest.mark.parametrize(
    'text, max_len, cont_indent, init_col, expected', [
        ('Hello world', 80, '', 0, 'Hello world'),
        ('Hello world', 5, '', 0, 'Hello\nworld'),
        ('a b c', 3, '', 0, 'a b\nc'),
        ('Hello world foo', 11, '  ', 0,
         'Hello world\n  foo'),
        ('', 80, '', 0, ''),
        ('word', 80, '', 0, 'word'),
    ])
def test_wrap_and_write(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
        capsys: pytest.CaptureFixture[str],
        text: str,
        max_len: int,
        cont_indent: str,
        init_col: int,
        expected: str) -> None:
    """Test _wrap_and_write wraps text at word boundaries."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        mf._reset_line_state(
            continuation_indent=cont_indent)
        mf._current_column = init_col
        mf._wrap_and_write(text, max_len)
    assert _write_and_read(callback) == expected
    check_capsys(capsys)


def test_wrap_and_write_continues_line(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test wrapping when text is added to an existing line."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Start ')
        mf._current_column = 6
        mf._wrap_and_write('more words here', 15)
    assert _write_and_read(callback) == 'Start more\nwords here'
    check_capsys(capsys)


# =================================================================
# _wrap_and_write_atomic
# =================================================================

def test_wrap_and_write_atomic_fits(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test atomic write when text fits on current line."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Hi')
        mf._current_column = 2
        mf._pending_whitespace = ' '
        mf._wrap_and_write_atomic('world', 10)
    assert _write_and_read(callback) == 'Hi world'
    check_capsys(capsys)


def test_wrap_and_write_atomic_wraps(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test atomic write wraps to new line when needed."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Hello')
        mf._current_column = 5
        mf._pending_whitespace = ' '
        mf._wrap_and_write_atomic('world_long', 10)
    assert _write_and_read(callback) == 'Hello\nworld_long'
    check_capsys(capsys)


def test_wrap_and_write_atomic_at_start(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test atomic write at start of line with long text."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        mf._current_column = 0
        mf._pending_whitespace = ''
        mf._wrap_and_write_atomic(
            'verylongword', 5)
    assert _write_and_read(callback) == 'verylongword'
    check_capsys(capsys)


# =================================================================
# _start_paragraph / _end_paragraph
# =================================================================

def test_start_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _start_paragraph adds empty line and resets state."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Previous text')
        mf._start_paragraph()
        mf.file.write('New paragraph')
    result = _write_and_read(callback)
    assert result == 'Previous text\n\nNew paragraph'
    check_capsys(capsys)


def test_start_paragraph_at_file_start(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test _start_paragraph at the beginning of file."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf._start_paragraph()
        mf.file.write('First paragraph')
    result = _write_and_read(callback)
    assert result == 'First paragraph'
    check_capsys(capsys)


def test_end_paragraph(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _end_paragraph writes line break."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Paragraph text')
        mf._end_paragraph()
    assert _write_and_read(callback) == 'Paragraph text\n'
    check_capsys(capsys)


# =================================================================
# _start_block_quote / _end_block_quote
# =================================================================

def test_start_block_quote(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _start_block_quote writes prefix and sets state."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Before')
        mf._start_block_quote()
        assert mf._continuation_indent == '> '
        assert mf._current_column == 2
        mf.file.write('Quote text')
    result = _write_and_read(callback)
    assert result == 'Before\n\n> Quote text'
    check_capsys(capsys)


def test_end_block_quote(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _end_block_quote writes line break and resets."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf._continuation_indent = '> '
        mf.file.write('> Quote')
        mf._end_block_quote()
        assert mf._continuation_indent == ''
    assert _write_and_read(callback) == '> Quote\n'
    check_capsys(capsys)


# =================================================================
# _start_bullet_list / _end_bullet_list (no-ops)
# =================================================================

def test_bullet_list_noop(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _start/_end_bullet_list do not write anything."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Before')
        mf._start_bullet_list(level=1)
        mf._end_bullet_list(level=1)
        mf.file.write('After')
    assert _write_and_read(callback) == 'BeforeAfter'
    check_capsys(capsys)


# =================================================================
# _start_numbered_list / _end_numbered_list (no-ops)
# =================================================================

def test_numbered_list_noop(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _start/_end_numbered_list do not write anything."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('Before')
        mf._start_numbered_list(level=1)
        mf._end_numbered_list(level=1)
        mf.file.write('After')
    assert _write_and_read(callback) == 'BeforeAfter'
    check_capsys(capsys)


# =================================================================
# _start_bullet_item_common / _end_bullet_item
# =================================================================

@pytest.mark.parametrize(
    'level, empty_before, marker, pre, expected', [
        (1, True, '- ', 'Before', 'Before\n\n- '),
        (2, True, '- ', 'Before', 'Before\n\n  - '),
        (1, False, '- ', 'Before\n', 'Before\n- '),
        (1, True, '* ', 'Before', 'Before\n\n* '),
        (3, True, '- ', 'Before',
         'Before\n\n    - '),
    ])
def test_start_bullet_item_common(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
        capsys: pytest.CaptureFixture[str],
        level: int,
        empty_before: bool,
        marker: str,
        pre: str,
        expected: str) -> None:
    """Test _start_bullet_item_common writes indent and marker."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write(pre)
        mf._start_bullet_item_common(
            level=level, empty_line_before=empty_before,
            marker=marker)
    assert _write_and_read(callback) == expected
    check_capsys(capsys)


def test_end_bullet_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _end_bullet_item writes line break."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('- Item text')
        mf._end_bullet_item(level=1)
    assert _write_and_read(callback) == '- Item text\n'
    check_capsys(capsys)


# =================================================================
# _start_numbered_item_common / _end_numbered_item
# =================================================================

@pytest.mark.parametrize(
    'level, num, full_num, empty_before, pre, expected', [
        (1, 1, '1.', True, 'Before', 'Before\n\n1. '),
        (2, 1, '1.1.', True, 'Before',
         'Before\n\n  1.1. '),
        (1, 3, '3.', False, 'Before\n', 'Before\n3. '),
    ])
def test_start_numbered_item_common(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
        capsys: pytest.CaptureFixture[str],
        level: int,
        num: int,
        full_num: str,
        empty_before: bool,
        pre: str,
        expected: str) -> None:
    """Test _start_numbered_item_common writes marker."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write(pre)
        mf._start_numbered_item_common(
            level=level, num=num,
            full_number=full_num,
            empty_line_before=empty_before)
    assert _write_and_read(callback) == expected
    check_capsys(capsys)


def test_end_numbered_item(capsys: pytest.CaptureFixture[str]) -> None:
    """Test _end_numbered_item writes line break."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf.file.write('1. Item text')
        mf._end_numbered_item(level=1, num=1)
    result = _write_and_read(callback)
    assert result == '1. Item text\n'
    check_capsys(capsys)


# =================================================================
# Continuation indent for bullet and numbered items
# =================================================================

def test_bullet_item_continuation_indent(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test continuation indent is set correctly for bullets."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf._start_bullet_item_common(
            level=1, empty_line_before=False,
            marker='- ')
        assert mf._continuation_indent == '  '
        assert mf._current_column == 2
    _write_and_read(callback)
    check_capsys(capsys)


def test_numbered_item_continuation_indent(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test continuation indent for numbered items."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf._start_numbered_item_common(
            level=1, num=1, full_number='1.',
            empty_line_before=False)
        assert mf._continuation_indent == '   '
        assert mf._current_column == 3
    _write_and_read(callback)
    check_capsys(capsys)


def test_nested_bullet_continuation_indent(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test continuation indent for nested bullet items."""
    # pylint: disable=protected-access
    def callback(mf: PlainTextLikeTestImpl) -> None:
        assert mf.file is not None
        mf._start_bullet_item_common(
            level=2, empty_line_before=False,
            marker='- ')
        assert mf._continuation_indent == '    '
        assert mf._current_column == 4
    _write_and_read(callback)
    check_capsys(capsys)
