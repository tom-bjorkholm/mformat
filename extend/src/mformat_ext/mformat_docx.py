#! /usr/local/bin/python3
"""Extension of the MultiFormat class for DOCX files."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from io import BufferedWriter, BufferedRandom
from types import TracebackType
from docx import Document
from mformat.mformat import MultiFormat, Iov


class MultiFormatDocx(MultiFormat):
    """Extension of the MultiFormat class for DOCX files."""

    def __init__(self, file: Iov) -> None:
        """Initialize the MultiFormatDocx class."""
        assert isinstance(file, (BufferedWriter, BufferedRandom))
        self.doc = Document()
        self.entered = False
        super().__init__(file)

    def __enter__(self) -> 'MultiFormatDocx':
        """Enter the context manager."""
        self.entered = True
        super().__enter__()
        return self

    def __exit__(self, exc_type: type[BaseException] | None,
                 exc_value: BaseException | None,
                 traceback: TracebackType | None) -> bool:
        """Exit the context manager."""
        assert isinstance(self.file, (BufferedWriter, BufferedRandom))
        if self.entered:
            self.doc.save(self.file)
        self.entered = False
        return super().__exit__(exc_type, exc_value, traceback)
