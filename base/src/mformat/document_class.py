#! /usr/local/bin/python3
"""Common document class enum used by output format implementations."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from enum import IntEnum, auto
from typing import Union
from mformat.enum_str_util import from_str, possible_values


type DocumentClassInput = Union['DocumentClass', str]
"""Type for a document class input value."""


class DocumentClass(IntEnum):
    """Common document classes used by at least LaTeX output format."""

    ARTICLE = auto()
    REPORT = auto()
    BOOK = auto()
    LETTER = auto()

    @classmethod
    def allowed_values(cls, include_lower: bool = False,
                       include_upper: bool = False) -> list[str]:
        """Return a list of all allowed document class values.

        Normally only the capitalized values are returned.
        As from_str() can parse lower and upper case values,
        this method can be used to get a list of all allowed
        values for use in error messages.

        Arguments:
            include_lower: Include lower case values.
            include_upper: Include upper case values.
        """
        return possible_values(enumtype=cls, include_lower=include_lower,
                               include_upper=include_upper)

    @classmethod
    def from_str(cls, document_class: DocumentClassInput,
                 strict: bool = True) -> 'DocumentClass':
        """Parse a document class enum value from an enum member or string.

        Arguments:
            document_class: The document class to parse.
                        Can be a DocumentClass enum member or a string.
                        If a string, its case will be ignored.
            strict: If True, the value must match a complete known value.
                    If False, the value may be a partial value,
                    and if it matches the start of only one known value,
                    that value will be returned. (Default is True.)
        """
        if isinstance(document_class, cls):
            return document_class
        if not isinstance(document_class, str):
            errmsg: str = 'document_class must be a DocumentClass or str, '
            errmsg += f'got {type(document_class).__name__}.'
            raise TypeError(errmsg)
        parsed = from_str(enumtype=cls, value=document_class,
                          strict=strict, what='document class')
        assert isinstance(parsed, cls)
        return parsed

    def lower(self) -> str:
        """Return the lower case name of the document class."""
        lower_name = self.name.lower()
        return lower_name

    def upper(self) -> str:
        """Return the upper case name of the document class."""
        upper_name = self.name.upper()
        return upper_name

    def normalize(self) -> str:
        """Return the normalized (capitalized) name of the document class."""
        normalized_name = self.name.capitalize()
        return normalized_name
