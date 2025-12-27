#! /usr/local/bin/python3
"""Base class for all text based format classes."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from typing import TextIO, Optional
from mformat.mformat import MultiFormat


class MultiFormatTextBased(MultiFormat):
    """Base class for all text based format classes."""

    def __init__(self, file_name: str, url_as_text: bool = False):
        """Initialize the TextBasedFormat class."""
        super().__init__(file_name=file_name, url_as_text=url_as_text)
        self.file: Optional[TextIO] = None

    def open(self) -> None:
        """Open the file."""
        self.file = open(self.file_name,  # pylint: disable=consider-using-with
                         mode='wt', encoding='utf-8')

    def close(self) -> None:
        """Close the file."""
        if self.file is None:
            return
        assert self.file is not None
        self.file.close()
        self.file = None
