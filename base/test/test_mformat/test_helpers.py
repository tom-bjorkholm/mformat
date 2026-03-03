#! /usr/local/bin/python3
"""Shared test helper classes and functions for mformat tests."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Callable, Optional, TypeAlias
import pytest
from mformat.factory import OptArgs, create_mf
from mformat.mformat import MultiFormat
from mformat.mformat_state import Formatting, MultiFormatState
from .check_capsys import check_capsys

MethodCall: TypeAlias = tuple[str, dict[str, Any]]


class FileExistsCallbackCounter:  # pylint: disable=too-few-public-methods
    """Count callback calls for existing file checks."""

    def __init__(self) -> None:
        """Initialize callback counter."""
        self.called = 0
        self.last_file_name = ''

    def __call__(self, file_name: str) -> None:
        """Record callback invocation."""
        self.called += 1
        self.last_file_name = file_name


def run_with_context_manager(
        format_name: str,
        file_extension: str,
        test_action: Callable[[Any], None],
        args: OptArgs = None,
        url_as_text: bool = False) -> str:
    """Run test with context manager and return file contents.

    Args:
        format_name: The format name (e.g. 'html', 'md')
        file_extension: The file extension (e.g. '.html', '.md')
        test_action: A function that takes mfd and performs actions
        args: Optional arguments to pass to create_mf
        url_as_text: Whether to format URLs as text

    Returns:
        The contents of the file after the test action runs
    """
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / f'test{file_extension}')
        with create_mf(format_name=format_name, file_name=fname,
                       url_as_text=url_as_text, args=args) as mfd:
            test_action(mfd)
        with open(fname, 'rt', encoding='utf-8') as file:
            return file.read()


def check_run_with_context_manager(    # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
        format_name: str,
        file_extension: str,
        test_action: Callable[[Any], None],
        expected_text: str,
        args: OptArgs = None,
        url_as_text: bool = False,
        capsys: Optional[pytest.CaptureFixture[str]] = None,
        err_msgs: Optional[list[str]] = None,
        out_msgs: Optional[list[str]] = None) -> None:
    """Run the test action with context manager and check file contents.

    Args:
        format_name: The format name (e.g. 'html', 'md')
        file_extension: The file extension (e.g. '.html', '.md')
        test_action: A function that takes mfd and performs actions
        args: Optional arguments to pass to create_mf
        url_as_text: Whether to format URLs as text
        expected_text: The expected text in the file
    """
    txt = run_with_context_manager(format_name, file_extension,
                                   test_action, args, url_as_text)
    assert txt == expected_text
    if err_msgs is not None or out_msgs is not None:
        assert capsys is not None
    if capsys is not None:
        check_capsys(capsys, err_msgs, out_msgs)


def create_method_call_action(
        expected_type_name: str,
        method_calls: list[MethodCall]) -> Callable[[Any], None]:
    """Create test action to run formatter method calls."""

    def test_action(mfd: Any) -> None:
        assert type(mfd).__name__ == expected_type_name
        for method_name, kwargs in method_calls:
            method = getattr(mfd, method_name)
            method(**kwargs)

    return test_action


def check_method_calls_output(  # pylint: disable=too-many-arguments,too-many-positional-arguments # noqa: E501
        format_name: str,
        file_extension: str,
        expected_type_name: str,
        method_calls: list[MethodCall],
        expected_text: str,
        args: OptArgs = None,
        url_as_text: bool = False,
        capsys: Optional[pytest.CaptureFixture[str]] = None) -> None:
    """Run formatter method calls and verify emitted text."""
    test_action = create_method_call_action(expected_type_name,
                                            method_calls)
    check_run_with_context_manager(
        format_name=format_name,
        file_extension=file_extension,
        test_action=test_action,
        expected_text=expected_text,
        args=args,
        url_as_text=url_as_text,
        capsys=capsys)


# pylint: disable=too-many-arguments,too-many-positional-arguments
def run_method_calls_output(
        format_name: str,
        file_extension: str,
        expected_type_name: str,
        method_calls: list[MethodCall],
        args: OptArgs = None,
        url_as_text: bool = False) -> str:
    """Run formatter method calls and return output text."""
    test_action = create_method_call_action(expected_type_name,
                                            method_calls)
    return run_with_context_manager(
        format_name=format_name,
        file_extension=file_extension,
        test_action=test_action,
        args=args,
        url_as_text=url_as_text)
# pylint: enable=too-many-arguments,too-many-positional-arguments


def check_formatter_constructor_attributes(
        formatter_class: Callable[..., Any],
        file_extension: str,
        constructor_args: Optional[dict[str, Any]],
        expected_attrs: dict[str, Any],
        expected_file_extension: Optional[str] = None) -> None:
    """Create formatter and assert selected constructor attributes."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test{file_extension}')
        kwargs: dict[str, Any] = {'file_name': file_name}
        if constructor_args is not None:
            kwargs.update(constructor_args)
        mfd = formatter_class(**kwargs)
        if expected_file_extension is not None:
            assert mfd.file_name.endswith(expected_file_extension)
        for attr_name, expected_value in expected_attrs.items():
            assert getattr(mfd, attr_name) == expected_value


def check_formatter_constructor_raises(
        formatter_class: Callable[..., Any],
        file_extension: str,
        constructor_args: dict[str, Any],
        exception_type: type[BaseException],
        expected_message: Optional[str] = None) -> None:
    """Assert formatter constructor raises expected exception."""
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / f'test{file_extension}')
        kwargs = {'file_name': file_name}
        kwargs.update(constructor_args)
        with pytest.raises(exception_type) as exc:
            _ = formatter_class(**kwargs)
        if expected_message is not None:
            assert str(exc.value) == expected_message


def run_protected_method(
        format_name: str,
        file_extension: str,
        method_name: str,
        method_args: Optional[tuple[Any, ...]] = None,
        args: OptArgs = None) -> str:
    """Run a protected method and return file contents.

    Args:
        format_name: The format name (e.g. 'html', 'md')
        file_extension: The file extension (e.g. '.html', '.md')
        method_name: The name of the protected method to call
        method_args: Optional tuple of arguments to pass to the method
        args: Optional arguments to pass to create_mf

    Returns:
        The contents of the file after the method runs
    """
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / f'test{file_extension}')
        mfd = create_mf(format_name=format_name, file_name=fname, args=args)
        mfd.open()
        method = getattr(mfd, method_name)
        if method_args is not None:
            method(*method_args)
        else:
            method()
        mfd._close()  # pylint: disable=protected-access
        with open(fname, 'rt', encoding='utf-8') as file:
            return file.read()


def create_paragraph_file_bytes(
        formatter_class: Callable[..., Any], file_extension: str,
        character_encoding: str,
        text: str = 'Café') -> bytes:
    """Create a paragraph file via formatter constructor and return bytes.

    Args:
        formatter_class: Formatter class or constructor callable.
        file_extension: Output file extension (e.g. '.html').
        character_encoding: Character encoding argument to pass.
        text: Paragraph text to write.
    Returns:
        Raw file bytes.
    """
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / f'test{file_extension}')
        with formatter_class(file_name=fname,
                             character_encoding=character_encoding) as mfd:
            mfd.new_paragraph(text=text)
        with open(fname, 'rb') as file:
            return file.read()


def create_paragraph_file_bytes_factory(
        format_name: str, file_extension: str,
        character_encoding: str,
        text: str = 'Café') -> bytes:
    """Create a paragraph file via create_mf and return bytes.

    Args:
        format_name: Registered format name.
        file_extension: Output file extension (e.g. '.md').
        character_encoding: Character encoding argument to pass.
        text: Paragraph text to write.
    Returns:
        Raw file bytes.
    """
    args: OptArgs = {'character_encoding': character_encoding}
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / f'test{file_extension}')
        with create_mf(format_name=format_name, file_name=fname,
                       args=args) as mfd:
            mfd.new_paragraph(text=text)
        with open(fname, 'rb') as file:
            return file.read()


def check_character_encoding_bytes(
        raw_content: bytes, character_encoding: str,
        expected_text_bytes: bytes,
        expected_html_meta: bool = False) -> None:
    """Check that raw output bytes match selected character encoding.

    Args:
        raw_content: Raw file bytes to verify.
        character_encoding: Encoding used for writing.
        expected_text_bytes: Expected byte sequence for written text.
        expected_html_meta: If True, assert HTML charset meta tag.
    """
    assert expected_text_bytes in raw_content
    if expected_html_meta:
        meta = f'<meta charset="{character_encoding}">\n'
        assert meta.encode('ascii') in raw_content
    if character_encoding == 'iso-8859-1':
        with pytest.raises(UnicodeDecodeError):
            raw_content.decode('utf-8')


def check_invalid_character_encoding_constructor(
        formatter_class: Callable[..., Any], file_extension: str,
        invalid_encoding: str = 'invalid-encoding') -> None:
    """Check constructor path propagates invalid encoding LookupError.

    Args:
        formatter_class: Formatter class or constructor callable.
        file_extension: Output file extension for temporary file.
        invalid_encoding: Invalid encoding name to test.
    """
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / f'test{file_extension}')
        with pytest.raises(LookupError) as exc:
            with formatter_class(file_name=fname,
                                 character_encoding=invalid_encoding):
                pass
        assert invalid_encoding in str(exc.value)


def check_invalid_character_encoding_factory(
        format_name: str, file_extension: str,
        invalid_encoding: str = 'invalid-encoding') -> None:
    """Check factory path propagates invalid encoding LookupError.

    Args:
        format_name: Registered format name.
        file_extension: Output file extension for temporary file.
        invalid_encoding: Invalid encoding name to test.
    """
    args: OptArgs = {'character_encoding': invalid_encoding}
    with TemporaryDirectory() as tmp_dir:
        fname = str(Path(tmp_dir) / f'test{file_extension}')
        with pytest.raises(LookupError) as exc:
            with create_mf(format_name=format_name, file_name=fname,
                           args=args):
                pass
        assert invalid_encoding in str(exc.value)


def check_formatter_character_encoding(
        formatter_class: Callable[..., Any],
        file_extension: str, character_encoding: str,
        expected_text_bytes: bytes,
        expected_html_meta: bool = False) -> None:
    """Check selected encoding output for formatter constructor path.

    Args:
        formatter_class: Formatter class or constructor callable.
        file_extension: Output file extension.
        character_encoding: Encoding passed to formatter.
        expected_text_bytes: Expected byte sequence for paragraph text.
        expected_html_meta: If True, verify HTML charset meta tag.
    """
    raw_content = create_paragraph_file_bytes(
        formatter_class=formatter_class,
        file_extension=file_extension,
        character_encoding=character_encoding)
    check_character_encoding_bytes(
        raw_content=raw_content,
        character_encoding=character_encoding,
        expected_text_bytes=expected_text_bytes,
        expected_html_meta=expected_html_meta)


class MultiFormat2(MultiFormat):
    """Class used for testing."""

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.test'


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
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, bullet list item, etc.)."""
        assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        assert isinstance(formatting, Formatting)
        self.inc_count('_write_text')

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item.

        (paragraph, bullet list item, etc.)
        """
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        # pylint: disable=duplicate-code
        assert isinstance(url, str)
        if text is not None:
            assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        assert isinstance(formatting, Formatting)
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

    def _encode_text(self, text: str) -> str:
        """Encode text (escape special characters)."""
        self.inc_count('_encode_text')
        return text


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
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, bullet list item, etc.)."""
        super()._write_text(text, state, formatting)
        assert text == self.expected_text
        assert formatting.bold == self.expected_bold
        assert formatting.italic == self.expected_italic


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
                   formatting: Formatting) -> None:
        """Write a URL into current item.

        (paragraph, bullet list item, etc.)
        """
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        super()._write_url(url, text, state, formatting)
        assert url == self.expected_url
        assert text == self.expected_url_text
        assert formatting.bold == self.expected_bold
        assert formatting.italic == self.expected_italic


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


class MultiFormat8(MultiFormat3):
    """Class used for testing new_heading."""

    def __init__(self, file_name: str, expected_text: str,
                 expected_level: int,
                 expected_bold: bool = False,
                 expected_italic: bool = False):
        """Initialize the MultiFormat8 class."""
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        super().__init__(file_name=file_name)
        self.expected_text: str = expected_text
        self.expected_level: int = expected_level
        self.expected_bold: bool = expected_bold
        self.expected_italic: bool = expected_italic

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        self.inc_count('_start_heading')
        assert level == self.expected_level

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        self.inc_count('_end_heading')
        # Note: We don't assert on level here because _end_heading
        # is called automatically when transitioning to other states

    def _write_text(self, text: str, state: MultiFormatState,
                    formatting: Formatting) -> None:
        """Write text into current item (paragraph, bullet list item, etc.)."""
        super()._write_text(text, state, formatting)
        assert text == self.expected_text
        assert formatting.bold == self.expected_bold
        assert formatting.italic == self.expected_italic


class MultiFormat9(MultiFormat8):
    """Class used for testing add_url in headings."""

    def __init__(self, file_name: str, expected_url: str,
                 expected_url_text: Optional[str] = None,
                 expected_level: int = 1,
                 expected_bold: bool = False,
                 expected_italic: bool = False):
        """Initialize the MultiFormat9 class."""
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        super().__init__(file_name=file_name,
                         expected_text='',
                         expected_level=expected_level)
        self.expected_url: str = expected_url
        self.expected_url_text: Optional[str] = expected_url_text
        self.expected_bold: bool = expected_bold
        self.expected_italic: bool = expected_italic

    def _write_url(self, url: str, text: Optional[str],
                   state: MultiFormatState,
                   formatting: Formatting) -> None:
        """Write a URL into current item.

        (paragraph, bullet list item, etc.)
        """
        # pylint: disable=too-many-arguments,too-many-positional-arguments
        super()._write_url(url, text, state, formatting)
        assert url == self.expected_url
        assert text == self.expected_url_text
        assert formatting.bold == self.expected_bold
        assert formatting.italic == self.expected_italic


class MultiFormat10(MultiFormat3):
    """Class used for testing bullet lists."""

    def _start_bullet_list(self, level: int) -> None:
        """Start a bullet list."""
        assert isinstance(level, int)
        self.inc_count('_start_bullet_list')

    def _end_bullet_list(self, level: int) -> None:
        """End a bullet list."""
        assert isinstance(level, int)
        self.inc_count('_end_bullet_list')

    def _start_bullet_item(self, level: int) -> None:
        """Start a bullet item."""
        assert isinstance(level, int)
        self.inc_count('_start_bullet_item')

    def _end_bullet_item(self, level: int) -> None:
        """End a bullet item."""
        assert isinstance(level, int)
        self.inc_count('_end_bullet_item')

    def _start_numbered_list(self, level: int) -> None:
        """Start a numbered list."""
        assert isinstance(level, int)
        self.inc_count('_start_numbered_list')

    def _end_numbered_list(self, level: int) -> None:
        """End a numbered list."""
        assert isinstance(level, int)
        self.inc_count('_end_numbered_list')

    def _start_numbered_item(self, level: int, num: int,
                             full_number: str) -> None:
        """Start a numbered item."""
        assert isinstance(level, int)
        assert isinstance(num, int)
        assert isinstance(full_number, str)
        self.inc_count('_start_numbered_item')

    def _end_numbered_item(self, level: int, num: int) -> None:
        """End a numbered item."""
        assert isinstance(level, int)
        assert isinstance(num, int)
        self.inc_count('_end_numbered_item')

    def _start_heading(self, level: int) -> None:
        """Start a heading."""
        assert isinstance(level, int)
        self.inc_count('_start_heading')

    def _end_heading(self, level: int) -> None:
        """End a heading."""
        assert isinstance(level, int)
        self.inc_count('_end_heading')


# Common test action functions that can be reused across format tests


def action_complex_nested_bullet_structure(mfd: Any) -> None:
    """Create a complex nested bullet structure.

    This is a common test pattern used across multiple format tests.
    Creates a structure like:
    - Item 1
      - Item 1.1
      - Item 1.2
    - Item 2
      - Item 2.1
    """
    mfd.new_bullet_item(text='Item 1', level=1)
    mfd.new_bullet_item(text='Item 1.1', level=2)
    mfd.new_bullet_item(text='Item 1.2', level=2)
    mfd.new_bullet_item(text='Item 2', level=1)
    mfd.new_bullet_item(text='Item 2.1', level=2)


# Common table data for tests to avoid code duplication

TABLE_DATA_3X2 = [
    ['Header1', 'Header2'],
    ['Row1Col1', 'Row1Col2'],
    ['Row2Col1', 'Row2Col2']
]

TABLE_DATA_3X2_SIMPLE = [
    ['Name', 'Value'],
    ['Alpha', '1'],
    ['Beta', '2']
]

TABLE_DATA_VARIED_WIDTHS = [
    ['Short', 'Longer'],
    ['A', 'Very long text'],
    ['Medium', 'X']
]

TABLE_DATA_WRONG_COLUMNS = [
    ['A', 'B'],
    ['1', '2', '3']  # Wrong number of columns
]
