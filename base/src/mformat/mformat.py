#! /usr/local/bin/python3
"""Base class for all multi file format classes."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from io import TextIOBase, BufferedWriter, BufferedRandom
from types import TracebackType
from enum import IntEnum, auto


type Iov = TextIOBase | BufferedWriter | BufferedRandom


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


class MultiFormat:
    """Base class for all multi file format classes."""

    def __init__(self, file: Iov):
        """Initialize the MFormat class."""
        self.file: Iov = file
        self.state: MultiFormatState = MultiFormatState.EMPTY

    def __enter__(self) -> 'MultiFormat':
        """Enter the context manager."""
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
        return exc_type is None
