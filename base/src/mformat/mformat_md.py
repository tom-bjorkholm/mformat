#! /usr/local/bin/python3
"""Markdown format class."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from mformat.mformat_textbased import MultiFormatTextBased
from mformat.mformat import FormatterDescriptor


class MultiFormatMd(MultiFormatTextBased):
    """Markdown format class."""

    def __init__(self, file_name: str, url_as_text: bool = False):
        """Initialize the MdFormat class."""
        super().__init__(file_name=file_name, url_as_text=url_as_text)

    def file_name_extension(self) -> str:
        """Get the file name extension for the formatter."""
        return '.md'

    @classmethod
    def get_arg_desciption(cls) -> FormatterDescriptor:
        """Get the description of the arguments for the formatter."""
        return FormatterDescriptor(name='md', mandatory_args=[],
                                   optional_args=[])

    def _write_file_prefix(self) -> None:
        """Write the file prefix."""

    def _write_file_suffix(self) -> None:
        """Write the file suffix."""

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        assert self.file is not None
        self.file.write('\n')

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        assert self.file is not None
        self.file.write('\n')

    def _write_in_paragraph(self, text: str) -> None:
        """Write text into current paragraph."""
        assert self.file is not None
        self.file.write(text)
