#! /usr/local/bin/python3
"""Extension of the MultiFormat class for DOCX files."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from docx import Document
from mformat.mformat import FormatterDescriptor, MultiFormat, \
    MultiFormatState


class MultiFormatDocx(MultiFormat):
    """Extension of the MultiFormat class for DOCX files."""

    def __init__(self, file_name: str, url_as_text: bool = False) -> None:
        """Initialize the MultiFormatDocx class."""
        self.doc = Document()
        super().__init__(file_name=file_name, url_as_text=url_as_text)

    @classmethod
    def file_name_extension(cls) -> str:
        """Get the file name extension for the formatter."""
        return '.docx'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='docx', mandatory_args=[],
                                   optional_args=[])

    def open(self) -> None:
        """Open the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        self.doc.save(self.file_name)

    def close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        if self.state == MultiFormatState.EMPTY:
            return
        self.doc.save(self.file_name)
