#! /usr/local/bin/python3
"""Shared helpers for reST formatter tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from typing import Any
from mformat.factory import OptArgs
from .test_helpers import (MethodCall, check_method_calls_output,
                           run_method_calls_output)

RST_FORMAT_NAME = 'reST'
RST_FILE_EXTENSION = '.rst'
RST_FORMATTER_TYPE_NAME = 'MultiFormatRst'


def check_rst_output(
        capsys: Any,
        method_calls: list[MethodCall],
        expected_text: str,
        args: OptArgs = None,
        url_as_text: bool = False) -> None:
    """Run reST method calls and compare output."""
    check_method_calls_output(
        format_name=RST_FORMAT_NAME,
        file_extension=RST_FILE_EXTENSION,
        expected_type_name=RST_FORMATTER_TYPE_NAME,
        method_calls=method_calls,
        expected_text=expected_text,
        args=args,
        url_as_text=url_as_text,
        capsys=capsys)


def run_rst_output(
        method_calls: list[MethodCall],
        args: OptArgs = None,
        url_as_text: bool = False) -> str:
    """Run reST method calls and return output text."""
    return run_method_calls_output(
        format_name=RST_FORMAT_NAME,
        file_extension=RST_FILE_EXTENSION,
        expected_type_name=RST_FORMATTER_TYPE_NAME,
        method_calls=method_calls,
        args=args,
        url_as_text=url_as_text)
