#! /usr/local/bin/python3
"""Test the mformat_rtf module core functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import sys
from types import SimpleNamespace
from typing import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
import pytest
from mformat_ext.mformat_rtf import MultiFormatRtf
from mformat.mformat import FormatterDescriptor, TableInformation
from mformat.factory import create_mf, OptArgs
from mformat.paper_size import PaperSize

# Add base test helpers to path for shared test utilities
_base_test_path = (Path(__file__).parent.parent.parent.parent / 'base' /
                   'test')
sys.path.insert(0, str(_base_test_path))
# pylint: disable=wrong-import-order,wrong-import-position,import-error
from test_mformat.check_capsys import check_capsys  # noqa: E402


def silent_rtf_create(capsys: pytest.CaptureFixture[str],
                      func: Callable[[MultiFormatRtf], None],
                      args: OptArgs = None,
                      fname: str = 'test.rtf') -> str:
    """Check that ``func`` can write to an RTF file silently.

    Args:
        capsys: The pytest capsys fixture.
        func: The function to call with the MultiFormatRtf instance.
        args: Optional constructor arguments for ``create_mf``.
        fname: Name of the file to write.

    Returns:
        Full content of generated RTF file.
    """
    with TemporaryDirectory() as tmp_dir:
        fpath = str(Path(tmp_dir) / fname)
        with create_mf('rtf', file_name=fpath, args=args) as mfr:
            assert isinstance(mfr, MultiFormatRtf)
            func(mfr)
        output_file = Path(fpath)
        assert output_file.exists()
        assert output_file.stat().st_size > 0
        check_capsys(capsys)
        return output_file.read_text(encoding='utf-8')


def test_file_name_extension(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the file_name_extension method."""
    assert MultiFormatRtf.file_name_extension() == '.rtf'
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_get_arg_desciption(capsys: pytest.CaptureFixture[str]) -> None:
    """Test the get_arg_desciption method."""
    assert MultiFormatRtf.get_arg_desciption() == \
        FormatterDescriptor(name='rtf', mandatory_args=[],
                            optional_args=['paper_size'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_paragraph_and_formatting(capsys: pytest.CaptureFixture[str]) -> None:
    """Test paragraph text with formatting."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_paragraph(text='Hello')
        mfr.add_text(text=' bold', bold=True)
        mfr.add_text(text=' italic', italic=True)

    content = silent_rtf_create(capsys, func=func)
    assert 'Hello' in content
    assert r'\b' in content
    assert r'\i' in content
    assert 'bold' in content
    assert 'italic' in content


def test_unicode_and_escaping(capsys: pytest.CaptureFixture[str]) -> None:
    """Test unicode encoding and escaping of RTF special characters."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_paragraph(text='Unicode: åäö 😀 and symbols: { } \\')

    content = silent_rtf_create(capsys, func=func)
    assert r'\u229?' in content
    assert r'\u228?' in content
    assert r'\u246?' in content
    assert r'\u-10179?\u-8704?' in content
    assert r'\{' in content
    assert r'\}' in content
    assert r'\\' in content


def test_hyperlink_field(capsys: pytest.CaptureFixture[str]) -> None:
    """Test writing a clickable hyperlink field."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_paragraph(text='Read ')
        mfr.add_url(url='http://example.com', text='Example', bold=True)

    content = silent_rtf_create(capsys, func=func)
    assert 'HYPERLINK "http://example.com"' in content
    assert 'Example' in content
    assert r'\ul\cf2\b' in content


def test_lists(capsys: pytest.CaptureFixture[str]) -> None:
    """Test bullet and numbered lists."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_bullet_item(text='Bullet one')
        mfr.new_bullet_item(text='Bullet two')
        mfr.new_numbered_point_item(text='First numbered', level=1)
        mfr.new_numbered_point_item(text='Nested numbered', level=2)

    content = silent_rtf_create(capsys, func=func)
    assert r'\u8226?\tab' in content
    assert 'Bullet one' in content
    assert 'Bullet two' in content
    assert r'1.\tab' in content
    assert r'1.1.\tab' in content
    assert r'\fi-360\li360' in content
    assert r'\fi-600\li720' in content
    assert r'\tx360' in content
    assert r'\tx720' in content
    assert 'First numbered' in content
    assert 'Nested numbered' in content


def test_table_and_code_block(capsys: pytest.CaptureFixture[str]) -> None:
    """Test table and code block output."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_table(first_row=['A', 'B'], bold=True)
        mfr.add_table_row(row=['1', '2'])
        mfr.write_code_block(text='x = 1\ny = 2')

    content = silent_rtf_create(capsys, func=func)
    assert r'\trowd' in content
    assert 'A' in content
    assert 'B' in content
    assert '1' in content
    assert '2' in content
    assert 'x = 1' in content
    assert 'y = 2' in content
    assert r'\line' in content


def test_heading_then_paragraph_style_reset(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that paragraph style resets to normal after a heading."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_heading(level=3, text='Heading')
        mfr.new_paragraph(text='Paragraph after heading')

    content = silent_rtf_create(capsys, func=func)
    assert 'Heading' in content
    assert 'Paragraph after heading' in content
    assert r'\s13' in content
    assert r'\s0' in content


def test_require_current_paragraph_raises_when_missing(
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path) -> None:
    """Test missing current paragraphs raise a runtime error."""
    # pylint: disable=protected-access
    formatter = MultiFormatRtf(file_name=tmp_path / 'test.rtf')
    with pytest.raises(RuntimeError) as exc:
        formatter._require_current_paragraph('writing text')
    assert exc.value.args[0] == 'No current paragraph for writing text'
    check_capsys(capsys)


def test_require_current_table_raises_when_missing(
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path) -> None:
    """Test missing current tables raise a runtime error."""
    # pylint: disable=protected-access
    formatter = MultiFormatRtf(file_name=tmp_path / 'test.rtf')
    with pytest.raises(RuntimeError) as exc:
        formatter._require_current_table('writing row')
    assert exc.value.args[0] == 'No current table for writing row'
    check_capsys(capsys)


def test_table_column_widths_validate_column_count(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test fallback table widths validate the number of columns."""
    # pylint: disable=protected-access
    with pytest.raises(RuntimeError) as exc:
        _ = MultiFormatRtf._table_column_widths(0)
    assert exc.value.args[0] == 'Table must have at least one column'
    assert MultiFormatRtf._table_column_widths(3) == (800, 800, 800)
    check_capsys(capsys)


def test_table_target_width_uses_minimum_for_invalid_section_width(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test table target width falls back for missing page width data."""
    # pylint: disable=protected-access
    section = SimpleNamespace(Width=0)
    assert MultiFormatRtf._table_target_width(section, 2) == 1600
    check_capsys(capsys)


def test_balance_column_widths_handles_empty_and_exact_totals(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test width balancing exits cleanly for simple no-op cases."""
    # pylint: disable=protected-access
    empty_widths: list[int] = []
    MultiFormatRtf._balance_column_widths(empty_widths, 1000)
    assert not empty_widths
    exact_widths = [800, 800]
    MultiFormatRtf._balance_column_widths(exact_widths, 1600)
    assert exact_widths == [800, 800]
    check_capsys(capsys)


def test_balance_column_widths_reduces_widest_columns_first(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test balancing removes overflow from the widest columns first."""
    # pylint: disable=protected-access
    widths = [1500, 1000, 900]
    MultiFormatRtf._balance_column_widths(widths, 2500)
    assert widths == [800, 800, 900]
    check_capsys(capsys)


def test_balance_column_widths_skips_columns_at_minimum_width(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test balancing skips columns that cannot shrink any further."""
    # pylint: disable=protected-access
    widths = [800, 1000, 800]
    MultiFormatRtf._balance_column_widths(widths, 1500)
    assert widths == [800, 800, 800]
    check_capsys(capsys)


def test_scaled_widths_from_char_widths_returns_empty_for_empty_input(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test scaling helper returns an empty tuple for empty input."""
    # pylint: disable=protected-access
    assert MultiFormatRtf._scaled_widths_from_char_widths([], 2400) == tuple()
    check_capsys(capsys)


def test_dynamic_column_widths_falls_back_without_table_data(
        capsys: pytest.CaptureFixture[str],
        tmp_path: Path) -> None:
    """Test dynamic widths fall back when no table data is available."""
    # pylint: disable=protected-access
    formatter = MultiFormatRtf(file_name=tmp_path / 'test.rtf')
    assert formatter._dynamic_column_widths(2) == (800, 800)
    check_capsys(capsys)


def test_dynamic_column_widths_falls_back_when_scaling_returns_empty(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch,
        tmp_path: Path) -> None:
    """Test dynamic widths fall back when scaling yields no widths."""
    # pylint: disable=protected-access
    formatter = MultiFormatRtf(file_name=tmp_path / 'test.rtf')
    formatter.table = TableInformation()
    formatter.table.column_widths = [4, 8]
    monkeypatch.setattr(
        formatter, '_scaled_widths_from_char_widths',
        lambda char_widths, target_total: tuple())
    assert formatter._dynamic_column_widths(2) == (800, 800)
    check_capsys(capsys)


def test_table_style_not_inherited_from_heading(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test that table cells use normal style after heading."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_heading(level=1, text='Table heading')
        mfr.new_table(first_row=['Col1', 'Col2'])
        mfr.add_table_row(row=['V1', 'V2'])

    content = silent_rtf_create(capsys, func=func)
    assert 'Table heading' in content
    assert 'Col1' in content
    assert 'V1' in content
    assert r'\intbl \s0' in content


@pytest.mark.parametrize('paper_size, expected', [
    (PaperSize.A4, r'\paperw11907\paperh16838'),
    (PaperSize.A3, r'\paperw16838\paperh23811'),
    (PaperSize.LETTER, r'\paperw12240\paperh15840'),
    (PaperSize.LEGAL, r'\paperw12240\paperh20160'),
])
def test_paper_size_selection(capsys: pytest.CaptureFixture[str],
                              paper_size: PaperSize,
                              expected: str) -> None:
    """Test selecting different paper sizes for RTF output."""

    def func(mfr: MultiFormatRtf) -> None:
        mfr.new_paragraph(text='Paper size test')

    content = silent_rtf_create(capsys, func=func,
                                args={'paper_size': paper_size})
    assert expected in content
