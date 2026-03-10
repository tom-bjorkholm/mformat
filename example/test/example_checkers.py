#! /usr/bin/env python3
"""Collection of checkers for use in tests of example programs."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Callable
import html as html_lib
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import pytest
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException, \
    PyMarkdownScanPathResult, PyMarkdownScanFailure, PyMarkdownPragmaError
import restructuredtext_lint  # type: ignore[import-untyped]
from html5lib import HTMLParser
from html5lib.html5parser import ParseError
import mammoth  # type: ignore[import-untyped]
from odf.opendocument import load as odf_load  # type: ignore[import-untyped]
from odf.odf2xhtml import ODF2XHTML  # type: ignore[import-untyped]
from mformat_ext.rtf_codec import encode_rtf_text


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
    for scan_failure in scanfailures:
        print('\nMarkdown scan failure:', file=sys.stderr)
        print('  file:', scan_failure.scan_file, file=sys.stderr)
        print('  line:', scan_failure.line_number, file=sys.stderr)
        print('  column:', scan_failure.column_number, file=sys.stderr)
        print('  rule id:', scan_failure.rule_id, file=sys.stderr)
        print('  rule name:', scan_failure.rule_name, file=sys.stderr)
        print('  rule description:', scan_failure.rule_description,
              file=sys.stderr)
        if scan_failure.extra_error_information:
            print('  extra error information:',
                  scan_failure.extra_error_information,
                  file=sys.stderr)
    for pragma_error in pragma_errors:
        print('\nMarkdown pragma error:', file=sys.stderr)
        print('  file:', pragma_error.file_path, file=sys.stderr)
        print('  line:', pragma_error.line_number, file=sys.stderr)
        print('  pragma error:', pragma_error.pragma_error, file=sys.stderr)
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
        func('txt', file_name)
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
        func('md', file_name)
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
        func('reST', file_name)
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
        func('html', file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            html = file.read()
        try:
            parser = HTMLParser(strict=True)
            _ = parser.parse(html)
        except ParseError as exc:
            print(str(exc))
            assert False, 'HTML parse error'
        check_text_in_order(html, expected_txt)


@dataclass(frozen=True)
class LatexToolchainStatus:
    """Result from probing local LaTeX compile support."""

    available: bool
    compiler_path: str
    message: str


def _latex_smoke_test_text() -> str:
    """Return a small LaTeX document for toolchain smoke testing."""
    return (
        '\\documentclass[a4paper]{report}\n'
        '\\usepackage{hyperref}\n'
        '\\usepackage{booktabs}\n'
        '\\usepackage{xurl}\n'
        '\\begin{document}\n'
        '\\chapter{Smoke test}\n'
        'See \\href{https://example.com/test\\_a}{Example link} and '
        '\\url{https://example.com/test\\_b}.\n'
        '\\begin{quote}\n'
        'Quoted text.\n'
        '\\end{quote}\n'
        '\\noindent\n'
        '\\begin{tabular}{lll}\n'
        '\\toprule\n'
        'A1 & B2 & C3 \\\\\n'
        '\\cmidrule(lr){1-2}\n'
        'x & y & z \\\\\n'
        '\\bottomrule\n'
        '\\end{tabular}\n'
        '\\par\\medskip\n'
        '\\begin{verbatim}\n'
        'code line\n'
        '\\end{verbatim}\n'
        '\\end{document}\n'
    )


def _latex_compile_command(compiler_path: str, file_name: str) -> list[str]:
    """Build the pdflatex command for compiling a LaTeX file."""
    return [compiler_path, '-interaction=nonstopmode', '-halt-on-error',
            '-file-line-error', file_name]


def _trim_process_output(text: str, max_lines: int = 60) -> str:
    """Trim captured process output to a manageable number of lines."""
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    if len(lines) <= max_lines:
        return '\n'.join(lines)
    return '\n'.join(lines[:max_lines]) + '\n...'


def _compile_latex_file(tex_file: Path,
                        compiler_path: str) -> tuple[bool, str]:
    """Compile a LaTeX file and return success flag and details."""
    command = _latex_compile_command(compiler_path=compiler_path,
                                     file_name=tex_file.name)
    try:
        process = subprocess.run(command, cwd=tex_file.parent, check=False,
                                 capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return False, (
            f'LaTeX compile timed out for {tex_file.name} using '
            f'{compiler_path}.'
        )
    except OSError as exc:
        return False, (
            f'LaTeX compile could not start for {tex_file.name} using '
            f'{compiler_path}: {exc}'
        )
    output = _trim_process_output(process.stdout + '\n' + process.stderr)
    if process.returncode != 0:
        message = (
            f'LaTeX compile failed for {tex_file.name} using '
            f'{compiler_path}. Return code: {process.returncode}.'
        )
        if output:
            message += '\nCompiler output:\n' + output
        return False, message
    pdf_file = tex_file.with_suffix('.pdf')
    if not pdf_file.exists():
        message = (
            f'LaTeX compile reported success for {tex_file.name} using '
            f'{compiler_path}, but {pdf_file.name} was not created.'
        )
        if output:
            message += '\nCompiler output:\n' + output
        return False, message
    return True, (
        f'LaTeX compile succeeded for {tex_file.name} using '
        f'{compiler_path}.'
    )


@cache
def get_latex_toolchain_status() -> LatexToolchainStatus:
    """Probe local pdflatex support once per test session."""
    compiler_path = shutil.which('pdflatex')
    if compiler_path is None:
        message = (
            'LaTeX example checks require pdflatex on PATH. '
            'Install a working TeX distribution to enable LaTeX example '
            'integration tests.'
        )
        return LatexToolchainStatus(available=False, compiler_path='',
                                    message=message)
    with TemporaryDirectory() as tmp_dir:
        file_name = Path(tmp_dir) / 'latex_toolchain_smoke_test.tex'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(_latex_smoke_test_text())
        success, message = _compile_latex_file(file_name, compiler_path)
    if not success:
        return LatexToolchainStatus(available=False,
                                    compiler_path=compiler_path,
                                    message=message)
    return LatexToolchainStatus(available=True, compiler_path=compiler_path,
                                message=message)


def check_latex_toolchain() -> None:
    """Fail once with a clear message if pdflatex support is unavailable."""
    status = get_latex_toolchain_status()
    if not status.available:
        pytest.fail(status.message)


def _skip_if_latex_toolchain_unavailable() -> LatexToolchainStatus:
    """Skip current LaTeX test when dedicated toolchain test should report."""
    status = get_latex_toolchain_status()
    if not status.available:
        pytest.skip(
            'LaTeX toolchain unavailable. See test_00_latex_toolchain for '
            'details.'
        )
    return status


def check_latex_func(func: Callable[[str, str], None],
                     expected_txt: list[str]) -> None:
    """Check that function produces compilable LaTeX with expected text.

    Args:
        func: The function to check.
        expected_txt: Fragments of the expected LaTeX source text in the
                      order they should appear.
    """
    status = _skip_if_latex_toolchain_unavailable()
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.tex')
        func('LaTeX', file_name)
        success, message = _compile_latex_file(Path(file_name),
                                               status.compiler_path)
        if not success:
            pytest.fail(message)
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
        check_text_in_order(text, expected_txt)


def _is_escaped_char(text: str, pos: int) -> bool:
    """Check if character at pos is escaped with backslashes."""
    num_backslashes = 0
    idx = pos - 1
    while idx >= 0 and text[idx] == '\\':
        num_backslashes += 1
        idx -= 1
    return num_backslashes % 2 == 1


def _check_rtf_group_balance(rtf: str) -> None:
    """Check that unescaped RTF groups are balanced."""
    nesting_level = 0
    for pos, char in enumerate(rtf):
        if char not in '{}':
            continue
        if _is_escaped_char(rtf, pos):
            continue
        if char == '{':
            nesting_level += 1
            continue
        nesting_level -= 1
        if nesting_level < 0:
            print('Unexpected closing brace in RTF output.', file=sys.stderr)
            print_line_col_of_pos(rtf, pos)
            assert False
    if nesting_level != 0:
        print(f'RTF group nesting ends at {nesting_level}.',
              file=sys.stderr)
        assert False


def _check_basic_rtf_structure(rtf: str) -> None:
    """Check that generated RTF has expected basic structure."""
    if not rtf.startswith('{\\rtf1'):
        print('RTF header "{\\\\rtf1" is missing at file start.',
              file=sys.stderr)
        print_text(rtf[:400])
    assert rtf.startswith('{\\rtf1')
    for marker in ('\\fonttbl', '\\stylesheet'):
        if marker not in rtf:
            print(f'RTF marker "{marker}" was not found.',
                  file=sys.stderr)
        assert marker in rtf
    _check_rtf_group_balance(rtf)


HTML_TAG_RE = re.compile(r'<[^>]*>')
RTF_SKIP_TEXTS = {'HTML file'}


def _rtf_fragments_from_html_token(token: str) -> list[str]:
    """Convert one expected HTML token to RTF fragments."""
    stripped_token = token.strip()
    if stripped_token.startswith('<') and '>' not in stripped_token:
        return []
    plain_text = HTML_TAG_RE.sub('', token)
    plain_text = html_lib.unescape(plain_text)
    fragments: list[str] = []
    for line in plain_text.split('\n'):
        stripped = line.strip()
        if stripped == '' or stripped in RTF_SKIP_TEXTS:
            continue
        fragments.append(encode_rtf_text(stripped))
    return fragments


def rtf_version_of_html(html_text: list[str]) -> list[str]:
    """Convert expected HTML fragments to expected RTF text fragments."""
    rtf_text: list[str] = []
    for token in html_text:
        rtf_text.extend(_rtf_fragments_from_html_token(token))
    return rtf_text


def check_rtf_func(func: Callable[[str, str], None],
                   expected_txt: list[str]) -> None:
    """Check that function produces expected RTF text.

    Args:
        func: The function to check.
        expected_txt: Fragments of expected text to check in order.
    """
    with TemporaryDirectory() as tmp_dir:
        file_name = str(Path(tmp_dir) / 'test.rtf')
        func('rtf', file_name)
        with open(file_name, 'r', encoding='utf-8') as file:
            rtf = file.read()
        _check_basic_rtf_structure(rtf)
        expected_rtf_txt = rtf_version_of_html(expected_txt)
        check_text_in_order(rtf, expected_rtf_txt)


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
        func('docx', file_name)
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
        func('odt', file_name)
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
