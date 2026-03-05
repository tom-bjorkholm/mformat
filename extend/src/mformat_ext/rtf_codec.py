#! /usr/local/bin/python3
"""Helper functions for RTF text and field encoding."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#


def _to_signed_16bit(value: int) -> int:
    """Convert a 16-bit unsigned value to signed representation."""
    if value < 0x8000:
        return value
    return value - 0x10000


def _unicode_char_to_rtf(char: str) -> str:
    r"""Encode one Unicode character as one or more RTF ``\u`` codes."""
    utf16_data = char.encode('utf-16-le')
    encoded_parts: list[str] = []
    for index in range(0, len(utf16_data), 2):
        code_unit = int.from_bytes(
            utf16_data[index:index + 2], byteorder='little')
        encoded_parts.append(f'\\u{_to_signed_16bit(code_unit)}?')
    return ''.join(encoded_parts)


def encode_rtf_text(text: str) -> str:
    """Encode plain text so it is safe to insert in an RTF text run."""
    encoded_parts: list[str] = []
    for char in text:
        if char == '\\':
            encoded_parts.append(r'\\')
        elif char == '{':
            encoded_parts.append(r'\{')
        elif char == '}':
            encoded_parts.append(r'\}')
        elif char == '\t':
            encoded_parts.append(r'\tab ')
        elif char == '\r':
            continue
        elif char == '\n':
            encoded_parts.append('\n')
        elif 0x20 <= ord(char) <= 0x7e:
            encoded_parts.append(char)
        else:
            encoded_parts.append(_unicode_char_to_rtf(char))
    return ''.join(encoded_parts)


def encode_rtf_field_instruction(text: str) -> str:
    """Encode text for an RTF field instruction string."""
    encoded_parts: list[str] = []
    for char in text:
        if char == '\\':
            encoded_parts.append(r'\\')
        elif char == '"':
            encoded_parts.append(r'\"')
        elif char == '{':
            encoded_parts.append(r'\{')
        elif char == '}':
            encoded_parts.append(r'\}')
        elif char == '\r':
            continue
        elif char == '\n':
            encoded_parts.append(' ')
        elif 0x20 <= ord(char) <= 0x7e:
            encoded_parts.append(char)
        else:
            encoded_parts.append(_unicode_char_to_rtf(char))
    return ''.join(encoded_parts)
