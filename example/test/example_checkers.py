#! /usr/bin/env python3
"""Collection of checkers for use in tests of example programs."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from pathlib import Path
from typing import Callable
import sys
from tempfile import TemporaryDirectory
import pytest
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException, \
    PyMarkdownScanPathResult, PyMarkdownScanFailure, PyMarkdownPragmaError
import restructuredtext_lint
from html5lib import HTMLParser
from html5lib.html5parser import ParseError
import mammoth


def check_capsys_silent(capsys: pytest.CaptureFixture[str]) -> None:
    """Check that the captured output is silent."""
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def check_text_in_order(text: str, expected_txts: list[str]) -> None:
    """Check that the text contains expected text in the expected order."""
    for expected_txt in expected_txts:
        if expected_txt not in text:
            print(f'Expected text: "{expected_txt}" not found in text.',
                  file=sys.stderr)
            print(f'Text: "{text}"', file=sys.stderr)
        assert expected_txt in text
    start = 0
    for num, expected_txt in enumerate(expected_txts):
        pos = text.find(expected_txt, start)
        if pos == -1:
            print(f'Expected text with index {num-1} ended at '
                  f' position {start} in text.', file=sys.stderr)
            print(f'Expected text with index {num} not found in text '
                  f'starting at position {start}.', file=sys.stderr)
            print(f'Failing expected text: {expected_txt}', file=sys.stderr)
            print(f'Text from position {start}: {text[start:]}', file=sys.stderr)
        assert pos != -1
        start = pos + len(expected_txt)


def print_md_errors(scanfailures: list[PyMarkdownScanFailure],
                    pragma_errors: list[PyMarkdownPragmaError]) -> None:
    """Print the errors from a markdown scan result."""
    print(f'{len(scanfailures)} unexpected errors found',
          file=sys.stderr)
    print(f'{len(pragma_errors)} pragma errors found',
          file=sys.stderr)
    for error in scanfailures:
        print('\nMarkdown scan failure:', file=sys.stderr)
        print('  file:', error.scan_file, file=sys.stderr)
        print('  line:', error.line_number, file=sys.stderr)
        print('  column:', error.column_number, file=sys.stderr)
        print('  rule id:', error.rule_id, file=sys.stderr)
        print('  rule name:', error.rule_name, file=sys.stderr)
        print('  rule description:', error.rule_description, file=sys.stderr)
        if error.extra_error_information:
            print('  extra error information:', error.extra_error_information,
                  file=sys.stderr)
    for error in pragma_errors:
        print('\nMarkdown pragma error:', file=sys.stderr)
        print('  file:', error.file_path, file=sys.stderr)
        print('  line:', error.line_number, file=sys.stderr)
        print('  pragma error:', error.pragma_error, file=sys.stderr)
    print('\n', file=sys.stderr)


def _get_pymarkdown_config_path() -> str:
    """Get the path to the .pymarkdown config file."""
    return str(Path(__file__).parent.parent.parent / '.pymarkdown')


def check_markdown_func(func: Callable[[str, str], None],
                        expected_txt: list[str],
                        expected_error: list[str]) -> None:
    """Check that function produces expected text with expected errors.

    Args:
        func: The function to check.
        expected_txt: Fragments of the expected text in the order they
                      should appear.
        expected_error: Rules to be suppressed.
    """
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.md'
        func(format_name='md', file_name=file_name)
        try:
            config_path = _get_pymarkdown_config_path()
            scan_result: PyMarkdownScanPathResult = \
                PyMarkdownApi().configuration_file_path(config_path) \
                .log_error_and_above().scan_path(file_name)
            unexpected_errors = [error for error in scan_result.scan_failures
                                 if error.rule_id not in expected_error]
            if unexpected_errors:
                print_md_errors(unexpected_errors, scan_result.pragma_errors)
            assert not unexpected_errors
            if scan_result.pragma_errors:
                print_md_errors(unexpected_errors, scan_result.pragma_errors)
            assert not scan_result.pragma_errors
        except PyMarkdownApiException as exc:
            print(str(exc), file=sys.stderr)
            raise exc
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            check_text_in_order(text, expected_txt)


def print_rst_errors(errors: list[restructuredtext_lint.LintError]) -> None:
    """Print the errors from a restructuredtext lint result."""
    print(f'{len(errors)} unexpected errors found', file=sys.stderr)
    for error in errors:
        print('\nRestructuredtext lint error:', file=sys.stderr)
        print('  file:', error.source, file=sys.stderr)
        print('  line:', error.line, file=sys.stderr)
        print('  level:', error.level, file=sys.stderr)
        print('  type:', error.type, file=sys.stderr)
        print('  message:', error.message, file=sys.stderr)
        print('  full message:', error.full_message, file=sys.stderr)
    print('\n', file=sys.stderr)


def check_rst_func(func: Callable[[str, str], None],
                   expected_txt: list[str],
                   expected_error: list[str]) -> None:
    """Check that function produces expected text with expected errors.

    Args:
        func: The function to check.
        expected_txt: Fragments of the expected text in the order they
                      should appear.
        expected_error: Expected error messages to suppress.
    """
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.rst'
        func(format_name='rst', file_name=file_name)
        errors = restructuredtext_lint.lint_file(filepath=file_name)
        unexpected_errors = [error for error in errors
                             if error.message not in expected_error]
        if unexpected_errors:
            print_rst_errors(unexpected_errors)
            assert unexpected_errors == []
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            check_text_in_order(text, expected_txt)


def check_html_func(func: Callable[[str, str], None],
                    expected_txt: list[str]) -> None:
    """Check that function produces expected text.

    Args:
        func: The function to check.
        expected_txt: Fragments of the expected text in the order they
                      should appear.
    """
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.html'
        func(format_name='html', file_name=file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            html = file.read()
        try:
            parser = HTMLParser(strict=True)
            _ = parser.parse(html)
        except ParseError as exc:
            print(str(exc))
            assert False, 'HTML parse error'
        check_text_in_order(html, expected_txt)



COMMON_EXPECTED_DOCX_WARNINGS = [
    'Unrecognised paragraph style: No Spacing (Style ID: NoSpacing)'
]


def check_docx_func(func: Callable[[str, str], None],
                    expected_txt: list[str],
                    expected_warnings: list[str]) -> None:
    """Check that function produces expected text.

    Args:
        func: The function to check.
        expected_txt: Fragments of the expected text in the order they
                      should appear.
        expected_warnings: Expected warnings to suppress.
    """
    all_expected_warnings = COMMON_EXPECTED_DOCX_WARNINGS + expected_warnings
    with TemporaryDirectory() as tmp_dir:
        file_name = tmp_dir + '/test.docx'
        func(format_name='docx', file_name=file_name)
        with open(file_name, 'rb') as f:
            content = mammoth.convert_to_html(f)
            for msg in content.messages:
                assert msg.type == 'warning'
                if msg.message not in all_expected_warnings:
                    print(f'Unexpected warning: {msg.message}',
                          file=sys.stderr)
            for msg in content.messages:
                assert msg.message in all_expected_warnings
            check_text_in_order(content.value, expected_txt)
