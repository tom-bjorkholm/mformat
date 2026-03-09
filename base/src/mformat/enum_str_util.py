#! /usr/local/bin/python3
"""Utility functions for working with enums and strings."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from enum import Enum
from typing import Optional, Union


type EnumStrInput = Union[Enum, str]
"""Type for an enum or string input value."""


def from_str(enumtype: type[Enum], value: EnumStrInput,
             strict: bool = True, what: Optional[str] = None) -> Enum:
    """Parse an enum value from an enum member or string.

    This function parses an enum value from a string, by matching the
    string to the enum member name. This matching is case insensitive.

    Returns:
        The parsed enum value.

    Raises:
        TypeError: If the value is not a string or an enum member.
        KeyError: If the value does not match any enum member.
                  (If strict is True and it does not match a complete
                  enum member name. If strict is False, and it does
                  not mactch the beginning of any enum member name).
        ValueError: If the value is a partial value, strict is False,
                    and there is more than one matching enum member.

    Arguments:
        enumtype: The enum type to parse the value for.
        value:  The value to parse.
        strict: If True, the value must match a complete known value.
                If False, the value may be a partial value, and if it
                matches the start of only one known value, that value
                will be returned. (Default is True.)
        what:   A meaningful name for the enum type, for use in error
                messages. If None, the enum type name will be used.
    """
    if isinstance(value, enumtype):
        return value
    if not isinstance(value, str):
        raise TypeError(f'value must be a {enumtype.__name__} or str, '
                        f'got {type(value).__name__}.')
    assert isinstance(value, str)
    if what is None:
        what = enumtype.__name__
    normalized = value.strip()
    assert isinstance(normalized, str)
    if normalized in enumtype:
        return enumtype(normalized)
    normalized = normalized.upper()
    for member in enumtype:
        if member.name.upper() == normalized:
            return member
    if strict:
        raise KeyError(f'Value "{value}" not a valid value for {what}.')
    matches = []
    for member in enumtype:
        if member.name.upper().startswith(normalized):
            matches.append(member)
    if len(matches) > 1:
        raise ValueError(f'Ambiguous value "{value}" for {what}. '
                         f'Matches: {", ".join([m.name for m in matches])}.')
    if not matches:
        raise KeyError(f'Value "{value}" does not match any allowed value '
                       f'for {what}.')
    return matches[0]


def possible_values(enumtype: type[Enum], include_capitalized: bool = True,
                    include_lower: bool = False,
                    include_upper: bool = False) -> list[str]:
    """Return a list of all possible string values for an enum type.

    This function returns a list of all possible string values for an enum
    type. The values are returned in the order of the enum members.
    Capitalized, upper case and lower case versions of the
    values are included if the corresponding include_* argument is True.
    If no include_* arguments are True, the return value will be empty.

    Arguments:
        enumtype: The enum type to get the possible values for.
        include_capitalized: Include capitalized version of values.
        include_lower: Include lower case version of values.
        include_upper: Include upper case version of values.
    """
    values = []
    for member in enumtype:
        if include_capitalized and member.name.capitalize() not in values:
            values.append(member.name.capitalize())
        if include_lower and member.name.lower() not in values:
            values.append(member.name.lower())
        if include_upper and member.name.upper() not in values:
            values.append(member.name.upper())
    return values
