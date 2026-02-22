#! /usr/local/bin/python3
"""Underline row(s) of text in a text based format."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import NamedTuple
from copy import deepcopy


class UnderlineSpec(NamedTuple):
    """Specification for underlining text."""

    pattern: str
    """Pattern to use repeatedly to underline the text."""
    empty_lines_between: int
    """Number of empty lines to insert between each row of underlined text."""
    empty_lines_after: int
    """Number of empty lines after the last row of underlined text."""


def wrap_text(text: str, max_line_length: int) -> list[str]:
    """Wrap text into rows of length max_line_length.

    Wraps text at word boundaries to keep lines within the specified
    maximum length. Handles whitespace at wrap points by collapsing
    multiple spaces/newlines into the line break. Trying to preserve
    any multiple spaces that are present in the text away from the
    wrap points. If a single word is longer than max_line_length, it
    will be alone at a line of its own that is longer than max_line_length.

    Args:
        text: The text to wrap. May not contain newlines.
        max_line_length: The maximum length of the lines to generate.

    Returns:
        A list of strings, one for each row limited to max_line_length.
    """
    if '\n' in text:
        err = 'Text arguement to wrap_text may not contain newlines'
        raise ValueError(err)
    if max_line_length <= 10:
        err = 'max_line_length must be greater than 10'
        raise ValueError(err)
    textleft = deepcopy(text)
    rows: list[str] = []
    textleft = textleft.strip()
    while len(textleft) > max_line_length:
        pos = textleft.rfind(' ', 0, max_line_length + 1)
        if pos == -1:
            pos = textleft.find(' ')
            if pos == -1:
                pos = len(textleft)
        rows.append(textleft[:pos].strip())
        textleft = textleft[pos:].strip()
    if textleft:
        rows.append(textleft.strip())
    return rows


def underline_text(text: str, underline_spec: UnderlineSpec,
                   max_line_length: int) -> list[str]:
    """Underline text according to the specification.

    Args:
        text: The text to underline. This will be wrapped into rows of length
              max_line_length and each row will be underlined. If a single word
              is longer than max_line_length, that word will be alone at a line
              of its own that is longer than max_line_length. If the text is
              empty, no rows will be generated. No newlines are allowed in the
              text argument.
        underline_spec: The specification for the underlining.
        max_line_length: The maximum length of the lines to generate.

    Returns:
        A list of strings, one for each row to pass to output function.
        This will contain also the underlining pattern and the empty lines
        between and after the text rows.
    """
    if not underline_spec.pattern:
        raise ValueError('underline_spec.pattern must not be empty')
    rows: list[str] = wrap_text(text=text, max_line_length=max_line_length)
    ret: list[str] = []
    for i, row in enumerate(rows):
        ret.append(row)
        num_patterns = len(row) // len(underline_spec.pattern) + 1
        underline = underline_spec.pattern * num_patterns
        ret.append(underline[:len(row)])
        if i < len(rows) - 1:
            for _ in range(underline_spec.empty_lines_between):
                ret.append('')
        if i == len(rows) - 1:
            for _ in range(underline_spec.empty_lines_after):
                ret.append('')
    return ret
