#! /usr/local/bin/python3
"""Common paper size enum used by output format implementations."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from enum import IntEnum, auto
from typing import Union
from mformat.enum_str_util import from_str, possible_values


type PaperSizeInput = Union['PaperSize', str]
"""Type for a paper size input value."""


class PaperSize(IntEnum):
    """Common paper sizes supported across some output formats."""

    A3 = auto()
    A4 = auto()
    A5 = auto()
    LEGAL = auto()
    LETTER = auto()

    @classmethod
    def allowed_values(cls, include_lower: bool = False,
                       include_upper: bool = False) -> list[str]:
        """Return a list of all allowed paper size values.

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
    def from_str(cls, paper_size: PaperSizeInput,
                 strict: bool = True) -> 'PaperSize':
        """Parse a paper size enum value from an enum member or string.

        Arguments:
            paper_size: The paper size to parse.
                        Can be a PaperSize enum member or a string.
                        If a string, its case and any underscores or hyphens
                        will be ignored. If the string ends with "PAPER",
                        the "PAPER" will be ignored.
            strict: If True, the value must match a complete known value.
                    If False, the value may be a partial value,
                    and if it matches the start of only one known value,
                    that value will be returned. (Default is True.)
        """
        if isinstance(paper_size, cls):
            return paper_size
        if not isinstance(paper_size, str):
            errmsg: str = 'paper_size must be a PaperSize or str, '
            errmsg += f'got {type(paper_size).__name__}.'
            raise TypeError(errmsg)
        normalized = \
            paper_size.strip().upper().replace('_', '').replace('-', '')
        if normalized.endswith('PAPER'):
            normalized = normalized[:-5]
        ret = from_str(enumtype=cls, value=normalized,
                       strict=strict, what='paper size')
        assert isinstance(ret, cls)
        return ret

    def lower(self) -> str:
        """Return the lower case name of the paper size."""
        return self.name.lower()

    def upper(self) -> str:
        """Return the upper case name of the paper size."""
        return self.name.upper()

    def normalize(self) -> str:
        """Return the normalized (capitalized) name of the paper size."""
        return self.name.capitalize()
