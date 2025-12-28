#! /usr/local/bin/python3
"""Base class for all multi file format classes."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from types import TracebackType
from enum import IntEnum, auto
from typing import NamedTuple


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
                 url_as_text: bool = False):
        """Initialize the MFormat class."""
        self.file_name: str = \
            self.file_name_with_extension(file_name,
                                          self.file_name_extension())
        self.state: MultiFormatState = MultiFormatState.EMPTY
        self.url_as_text: bool = url_as_text

    def __enter__(self) -> 'MultiFormat':
        """Enter the context manager."""
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
                                   optional_args=[])

    def file_name_extension(self) -> str:
        """Get the file name extension for the formatter.

        Must be overridden by subclasses.
        """
        err = self._must_be_overridden('file_name_extension')
        raise NotImplementedError(err)
        # pylint: disable=unreachable
        return ''

    def open(self) -> None:
        """Open the file."""
        err = self._must_be_overridden('open')
        raise NotImplementedError(err)

    def close(self) -> None:
        """Close the file."""
        err = self._must_be_overridden('close')
        raise NotImplementedError(err)

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""
        err = self._must_be_overridden('write_file_prefix')
        raise NotImplementedError(err)

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""
        err = self._must_be_overridden('write_file_suffix')
        raise NotImplementedError(err)

    def write_paragraph(self, text: str,
                        how: NewOrAppend = NewOrAppend.APPEND_IF_EXISTS
                        ) -> None:
        """Write text in a paragraph."""
        if self.state == MultiFormatState.PARAGRAPH:
            if how == NewOrAppend.NEW:
                self._end_paragraph()
                self._start_paragraph()
        elif how == NewOrAppend.MUST_APPEND:
            err = f'Paragraph append required, but state is {self.state.name}'
            raise RuntimeError(err)
        elif self.state == MultiFormatState.PARAGRAPH_END:
            self._start_paragraph()
        elif self.state not in (MultiFormatState.PARAGRAPH,
                                MultiFormatState.PARAGRAPH_END):
            self._end_state()
            self._start_paragraph()
        self._write_in_paragraph(text)
        self.state = MultiFormatState.PARAGRAPH

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
        err = self._must_be_overridden('start_paragraph')
        raise NotImplementedError(err)

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        err = self._must_be_overridden('end_paragraph')
        raise NotImplementedError(err)

    def _write_in_paragraph(self, text: str) -> None:
        """Write text into current paragraph."""
        assert isinstance(text, str)
        err = self._must_be_overridden('write_paragraph')
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
        """Raise an error if the function is not overridden by a subclass."""
        return f'{func_name} must be overridden by a ' + \
            f'subclass {cls.__name__}'
