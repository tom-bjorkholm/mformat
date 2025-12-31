#! /usr/local/bin/python3
"""Extension of the MultiFormat class for DOCX files."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional, Callable
from docx import Document
from docx.document import Document as DocumentObject
from docx.text.paragraph import Paragraph
from mformat.mformat import FormatterDescriptor, MultiFormat, \
    MultiFormatState


class MultiFormatDocx(MultiFormat):
    """Extension of the MultiFormat class for DOCX files."""

    def __init__(self, file_name: str, url_as_text: bool = False,
                 file_exists_callback: Optional[Callable[[str], None]] = None):
        """Initialize the MultiFormatDocx class.

        Args:
            file_name: The name of the file to write to.
            url_as_text: Format URLs as text not clickable URLs.
            file_exists_callback: A callback function to call if the file
                                  already exists. Return to allow the file to
                                  be overwritten. Raise an exception to prevent
                                  the file from being overwritten.
                                  (May for instance save existing file as
                                  backup.)
                                  (Default is to raise an exception.)
        """
        self.doc: DocumentObject = Document()
        self.current_paragraph: Optional[Paragraph] = None
        super().__init__(file_name=file_name, url_as_text=url_as_text,
                         file_exists_callback=file_exists_callback)

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

    def _close(self) -> None:
        """Close the file.

        Avoid using this method directly.
        Use as a context manager instead, using a with statement.
        """
        if self.state == MultiFormatState.EMPTY:
            return
        self.doc.save(self.file_name)

    def _start_paragraph(self) -> None:
        """Start a paragraph."""
        self.current_paragraph = self.doc.add_paragraph()

    def _end_paragraph(self) -> None:
        """End a paragraph."""
        self.current_paragraph = None

    def _write_text(self, text: str, state: MultiFormatState,
                    bold: bool, italic: bool) -> None:
        """Write text into current item (paragraph, bullet list item, etc.).

        Args:
            text: The text to write into the current item.
            state: The state of the current item.
            bold: If True, the text is bold.
            italic: If True, the text is italic.
        """
        if self.current_paragraph is None:
            raise RuntimeError('No current paragraph to write text into')
        run = self.current_paragraph.add_run(text)
        if bold:
            run.bold = True
        if italic:
            run.italic = True
