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
from odf.opendocument import load as odf_load
from odf.odf2xhtml import ODF2XHTML


def check_capsys_silent(capsys: pytest.CaptureFixture[str]) -> None:
    """Check that the captured output is silent."""
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def print_text(text: str) -> None:
    """Print the text."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    for line in lines[:500]:
        print(f'{line[:800]}', file=sys.stderr)


def print_line_col_of_pos(text: str, pos: int) -> None:
    """Print the line number and column number of the position in the text."""
    lines = text[:pos].split('\n')
    print(f'Position: {pos} is line: {len(lines)}, column: {len(lines[-1])}',
          file=sys.stderr)


def check_text_in_order(text: str, expected_txts: list[str]) -> None:
    """Check that the text contains expected text in the expected order."""
    for expected_txt in expected_txts:
        if expected_txt not in text:
            print(f'Expected text: "{expected_txt}" not found in text.',
                  file=sys.stderr)
            print('Text:', file=sys.stderr)
            print_text(text)
        assert expected_txt in text
    start = 0
    for num, expected_txt in enumerate(expected_txts):
        pos = text.find(expected_txt, start)
        if pos == -1:
            print(f'Expected text with index {num - 1} ended at '
                  f'position {start} in text.', file=sys.stderr)
            print(f'Expected text index {num - 1}: {expected_txts[num - 1]}',
                  file=sys.stderr)
            print(f'Expected text with index {num} not found in text '
                  f'starting at position {start}.', file=sys.stderr)
            print_line_col_of_pos(text, start)
            print(f'Failing expected text: {expected_txt}', file=sys.stderr)
            print(f'Text from position {start}:', file=sys.stderr)
            print_text(text[start:])
            print('\n\n----Complete text beginning:-------------\n',
                  file=sys.stderr)
            print_text(text)
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


def check_txt_func(func: Callable[[str, str], None],
                   expected_txt: list[str]) -> None:
    """Check that function produces expected text.

    Args:
        func: The function to check.
        expected_txt: Fragments of the expected text in the order they
                      should appear.
    """
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.txt')
        func(format_name='txt', file_name=file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            check_text_in_order(text, expected_txt)


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
        file_name = str(Path(tmp_dir) / 'test.md')
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


def print_rst_errors(errors: list['restructuredtext_lint.LintError']) -> None:
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
        file_name = str(Path(tmp_dir) / 'test.rst')
        func(format_name='reST', file_name=file_name)
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
        file_name = str(Path(tmp_dir) / 'test.html')
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
        file_name = str(Path(tmp_dir) / 'test.docx')
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


def check_odt_func(func: Callable[[str, str], None],
                   expected_txt: list[str]) -> None:
    """Check that function produces expected text.

    Args:
        func: The function to check.
        expected_txt: Fragments of the expected text in the order they
                      should appear.
    """
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.odt')
        func(format_name='odt', file_name=file_name)
        with open(file_name, 'rb') as file:
            _ = odf_load(file)  # test if loads without raising exception
            converter = ODF2XHTML()
            html = converter.odf2xhtml(file)
            check_text_in_order(html, expected_txt)


EQUIV_SEQS = [
    (['</strong>', '<strong>'], []),
    (['</em>', '<em>'], []),
    (['<strong>', '</strong>'], []),
    (['<em>', '</em>'], []),
    (['</strong>', '<em>', '<strong>'], ['<em>']),
    (['<strong>', '<em>', '</strong>'], ['<em>']),
    (['</em>', '<strong>', '<em>'], ['<strong>']),
    (['<em>', '<strong>', '</em>'], ['<strong>']),
    (['</strong>', '<p>', '<strong>'], ['<p>']),
    (['</strong>', '</p>', '<p>', '<strong>'], ['</p>', '<p>']),
    (['</em>', '<p>', '<em>'], ['<p>']),
    (['</em>', '</p>', '<p>', '<em>'], ['</p>', '<p>']),
]


def _reduce_equiv_seqs(html: list[str]) -> list[str]:
    """Reduce equivalent sequences of HTML tags.

    When the html input contains a sequence of values (tags)
    that is a key in EQUIV_SEQS, the sequence is replaced by the value.
    """
    reduced_html: list[str] = []
    idx: int = 0
    while idx < len(html):
        for seq_key, seq_value in EQUIV_SEQS:
            if html[idx:idx + len(seq_key)] == seq_key:
                reduced_html.extend(seq_value)
                idx += len(seq_key)
                continue
        reduced_html.append(html[idx])
        idx += 1
    return reduced_html


DOCX_EXCLUDE_TAGS = ('<code>', '</code>', '<pre>', '</pre>')
"""Tags to exclude from the HTML conversion to DOCX."""


def docx_version_of_html(html: list[str]) -> list[str]:
    """Convert HTML to version that we get from mammoth."""
    reduced_html = _reduce_equiv_seqs(html)
    docx_html = []
    for idx, line in enumerate(reduced_html):
        prev = reduced_html[idx - 1] if idx > 0 else None
        if line == '<strong>' and prev == '<em>':
            continue
        if line == '</strong>' and prev == '</em>':
            continue
        if line == '<em>' and prev == '<strong>':
            continue
        if line == '</em>' and prev == '</strong>':
            continue
        if line in DOCX_EXCLUDE_TAGS:
            continue
        docx_html.append(line)
    return docx_html


HTML2ODT_TAGS = {
    '<h1>': '<h1',
    '<h2>': '<h2',
    '<h3>': '<h3',
    '<h4>': '<h4',
    '<h5>': '<h5',
    '<h6>': '<h6',
    '<p>': '<p',
    '<ul>': '<ul',
    '<ol>': '<ol',
}


ODT_EXCLUDE_TAGS = DOCX_EXCLUDE_TAGS
"""Tags to exclude from the HTML conversion to ODT."""


def odt_version_of_html(html: list[str]) -> list[str]:
    """Convert HTML to version that we get from odf2xhtml."""
    odt_html = []
    for line in html:
        if line in ODT_EXCLUDE_TAGS:
            continue
        odt_html.append(line.replace('&quot;', '"'))
    for idx, line in enumerate(odt_html):
        if line in HTML2ODT_TAGS:
            odt_html[idx] = HTML2ODT_TAGS[line]
        elif line in ('<em>', '<strong>'):
            if idx > 0 and odt_html[idx - 1] == '<span':
                odt_html[idx] = ''
            else:
                odt_html[idx] = '<span'
        elif line in ('</em>', '</strong>'):
            if idx > 0 and odt_html[idx - 1] == '</span':
                odt_html[idx] = ''
            else:
                odt_html[idx] = '</span'
    return odt_html
