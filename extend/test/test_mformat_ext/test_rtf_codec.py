#! /usr/local/bin/python3
"""Test the rtf_codec module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from mformat_ext.rtf_codec import encode_rtf_field_instruction, \
    encode_rtf_text


def test_encode_rtf_text_handles_tabs_and_carriage_returns() -> None:
    """Test text encoding converts tabs and skips carriage returns."""
    assert encode_rtf_text('a\tb\rc') == r'a\tab bc'


def test_encode_rtf_field_instruction_escapes_special_chars() -> None:
    """Test field instruction encoding escapes control chars and unicode."""
    encoded = encode_rtf_field_instruction('x\\"{}\r\né')
    assert encoded.startswith(r'x\\\"\{\} ')
    assert encoded.endswith(r'\u233?')
