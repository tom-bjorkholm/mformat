#! /usr/local/bin/python3
"""Base class for all multi file format classes."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from types import TracebackType
from enum import IntEnum, auto
from typing import NamedTuple, Callable, Optional
import sys
import os


class FormatterDescriptor(NamedTuple):
    """Descriptor for a formatter."""

    name: str
    mandatory_args: list[str]
    optional_args: list[str]


class MultiFormatState(IntEnum):
    """Enum for the state of the multi file format."""

    EMPTY = auto()
    H1 = auto()
    H2 = auto()
    H3 = auto()
    H4 = auto()
    PARAGRAPH = auto()
    PARAGRAPH_END = auto()
    BULLET_LIST = auto()
    BULLET_LIST_ITEM = auto()
    BULLET_LIST_ITEM_END = auto()
    BULLET_LIST_END = auto()
    NUMERIC_LIST = auto()
    NUMERIC_LIST_ITEM = auto()
    NUMERIC_LIST_ITEM_END = auto()
    NUMERIC_LIST_END = auto()
    CLOSED = auto()


class NewOrAppend(IntEnum):
    """Enum for whether to start new section or append to existing section."""

    NEW = auto()
    MUST_APPEND = auto()
    APPEND_IF_EXISTS = auto()


class MultiFormat:
    """Base class for all multi file format classes."""

    def __init__(self, file_name: str,
                 url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]]
                 = None):
        """Initialize the MultiFormat class.

        Args:
            file_name: The name of the file to write to.
            url_as_text: Format URLs as text not clickable URLs.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to
                                  prevent the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        self.file_exists_callback: Optional[Callable[[str], None]] = \
            file_exists_callback
        self.file_name: str = \
            self.file_name_with_extension(file_name,
                                          self.file_name_extension())
        self.state: MultiFormatState = MultiFormatState.EMPTY
        self.url_as_text: bool = url_as_text
        self._file_exists_check()

    def __enter__(self) -> 'MultiFormat':
        """Enter the context manager."""
        self._file_exists_check()
        self.open()
        return self

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """Exit the context manager.

        Args:
            exc_type: The type of the exception.
            exc_value: The value of the exception.
            traceback: The traceback of the exception.
        Returns:
            True if the exception was handled, False otherwise.
        """
        self.close()
        return exc_type is None

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter.

        Must be overridden by subclasses.
        """
        err = cls._must_be_overridden('get_arg_desciption')
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return FormatterDescriptor(name='', mandatory_args=[],
                                   optional_args=['file_exists_callback'])

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter.

        Must be overridden by subclasses.
        """
        err = cls._must_be_overridden('file_name_extension')
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return ''

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        err = self._must_be_overridden('open')
        raise NotImplementedError(err)

    def close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use MultiFormat as a context manager instead, using a with statement.
        """
        if self.state != MultiFormatState.EMPTY:
            self._end_state()
            self._write_file_suffix()
        self._close()

    def _close(self) -> None:
        """Close the file.

        Must be overridden by subclasses.
        """
        err = self._must_be_overridden('_close')
        raise NotImplementedError(err)

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""
        err = self._must_be_overridden('_write_file_prefix')
        raise NotImplementedError(err)

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""
        err = self._must_be_overridden('_write_file_suffix')
        raise NotImplementedError(err)

    def start_paragraph(self, text: str, smart_ws: bool = True,
                        bold: bool = False, italic: bool = False) -> None:
        """Start a new paragraph.

        Args:
            text: The text to write in the paragraph.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      start_paragraph or add_text).
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        if self.state != MultiFormatState.PARAGRAPH_END:
            self._end_state()
        self._start_paragraph()
        self.state = MultiFormatState.PARAGRAPH
        self._write_text(text.strip() if smart_ws else text,
                         self.state, bold, italic)

    def add_text(self, text: str, smart_ws: bool = True,
                 bold: bool = False, italic: bool = False) -> None:
        """Add text to the current item (paragraph, bullet list item, etc.).

        Args:
            text: The text to add to the current item.
            smart_ws: If True, leading and trailing whitespace are collapsed
                      and a single space is inserted between texts (from
                      start_paragraph, start_bullet, ... or add_text).
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        if self.state not in (MultiFormatState.PARAGRAPH,
                              MultiFormatState.BULLET_LIST_ITEM,
                              MultiFormatState.NUMERIC_LIST_ITEM):
            err = f'Cannot add text to state {self.state.name}'
            raise RuntimeError(err)
        self._write_text(' ' + text.strip() if smart_ws else text,
                         self.state, bold, italic)

    def _end_state(self) -> None:
        """End the current state."""
        if self.state == MultiFormatState.EMPTY:
            self._write_file_prefix()
            self.state = MultiFormatState.PARAGRAPH_END
        elif self.state == MultiFormatState.PARAGRAPH:
            self._end_paragraph()
            self.state = MultiFormatState.PARAGRAPH_END

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        err = self._must_be_overridden('_start_paragraph')
        raise NotImplementedError(err)

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        err = self._must_be_overridden('_end_paragraph')
        raise NotImplementedError(err)

    def _write_text(self, text: str, state: MultiFormatState,
                    bold: bool, italic: bool) -> None:
        """Write text into current item (paragraph, bullet list item...)."""
        assert isinstance(text, str)
        assert isinstance(state, MultiFormatState)
        assert isinstance(bold, bool)
        assert isinstance(italic, bool)
        err = self._must_be_overridden('_write_text')
        raise NotImplementedError(err)

    @staticmethod
    def file_name_with_extension(file_name: str, extension: str) -> str:
        """Get the file name with the extension."""
        if not extension.startswith('.'):
            extension = f'.{extension}'
        if file_name.endswith(extension):
            return file_name
        return f'{file_name}{extension}'

    @classmethod
    def _must_be_overridden(cls, func_name: str) -> str:
        """Error message if the function is not overridden by a subclass."""
        return f'{func_name} must be overridden by a ' + \
            f'subclass {cls.__name__}'

    def _file_exists_check(self) -> None:
        """Check if the file exists and handle it accordingly."""
        if os.path.exists(self.file_name):
            if self.file_exists_callback is not None:
                self.file_exists_callback(self.file_name)
            else:
                msg = 'Cowardly refusing to overwrite existing file '
                msg += f'{self.file_name}.\n\n'
                msg += '(Use a different file name or provide a '
                msg += 'file_exists_callback \n'
                msg += ' function to allow the file to be overwritten.)\n'
                print(msg, file=sys.stderr)
                raise FileExistsError(msg)
