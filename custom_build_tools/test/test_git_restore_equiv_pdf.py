#! /usr/local/bin/python3
"""Tests for custom_build_tools/src/git_restore_equiv_pdf.py."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import pytest
_TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TEST_DIR))
# pylint: disable=wrong-import-position,wrong-import-order
from helpers_custom_build_tools import (  # noqa: E402
    init_git_repo,
    load_source_module,
    run_git,
    write_bytes,
)
# pylint: enable=wrong-import-position,wrong-import-order

restore_equiv_pdf = load_source_module(
    'git_restore_equiv_pdf',
    'git_restore_equiv_pdf.py'
)


def _write_pdf(file_name: Path, text: str, title: str,
               creation_date: str) -> None:
    """Write one small PDF file with deterministic visible content."""
    file_name.parent.mkdir(parents=True, exist_ok=True)
    pdf_document = restore_equiv_pdf.pymupdf.open()
    page = pdf_document.new_page()
    page.insert_text((72, 72), text)
    pdf_document.set_toc([[1, 'Heading', 1]])
    metadata = pdf_document.metadata
    metadata['title'] = title
    metadata['creationDate'] = creation_date
    metadata['modDate'] = creation_date
    pdf_document.set_metadata(metadata)
    pdf_document.save(file_name)
    pdf_document.close()


def test_are_pdf_files_equivalent_ignores_creation_and_mod_dates() -> None:
    """Test PDF equivalence ignores creation and modification timestamps."""
    with TemporaryDirectory() as tmp_dir:
        file_a = Path(tmp_dir) / 'a.pdf'
        file_b = Path(tmp_dir) / 'b.pdf'
        _write_pdf(file_a, 'Hello PDF', 'Sample',
                   "D:20260101000000+00'00'")
        _write_pdf(file_b, 'Hello PDF', 'Sample',
                   "D:20260202000000+00'00'")
        assert restore_equiv_pdf.are_pdf_files_equivalent(file_a, file_b)


def test_are_pdf_files_equivalent_detects_other_metadata_changes() -> None:
    """Test PDF equivalence detects metadata differences beyond dates."""
    with TemporaryDirectory() as tmp_dir:
        file_a = Path(tmp_dir) / 'a.pdf'
        file_b = Path(tmp_dir) / 'b.pdf'
        _write_pdf(file_a, 'Hello PDF', 'Sample A',
                   "D:20260101000000+00'00'")
        _write_pdf(file_b, 'Hello PDF', 'Sample B',
                   "D:20260202000000+00'00'")
        assert not restore_equiv_pdf.are_pdf_files_equivalent(file_a, file_b)


def test_are_pdf_files_equivalent_detects_text_changes() -> None:
    """Test PDF equivalence detects differences in visible page content."""
    with TemporaryDirectory() as tmp_dir:
        file_a = Path(tmp_dir) / 'a.pdf'
        file_b = Path(tmp_dir) / 'b.pdf'
        _write_pdf(file_a, 'Hello PDF', 'Sample',
                   "D:20260101000000+00'00'")
        _write_pdf(file_b, 'Hello changed PDF', 'Sample',
                   "D:20260202000000+00'00'")
        assert not restore_equiv_pdf.are_pdf_files_equivalent(file_a, file_b)


def test_list_unchanged_files_filters_using_status_and_comparison(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test list_unchanged_files only returns modified equivalent PDFs."""
    with TemporaryDirectory() as tmp_dir:
        repo_root = Path(tmp_dir) / 'repo'
        result_dir = repo_root / 'example' / 'result'
        write_bytes(result_dir / 'a.pdf', b'a')
        write_bytes(result_dir / 'b.pdf', b'b')
        fake_file = (
            repo_root / 'custom_build_tools' / 'src' /
            'git_restore_equiv_pdf.py'
        )
        fake_file.parent.mkdir(parents=True, exist_ok=True)
        modified_files = {(result_dir / 'a.pdf').resolve()}
        equivalent_files = {(result_dir / 'a.pdf').resolve()}

        def fake_compare(file_path: Path, committed_file: Path) -> bool:
            """Return if the modified file is equivalent."""
            _ = committed_file
            return file_path.resolve() in equivalent_files

        monkeypatch.setattr(restore_equiv_pdf, '__file__', str(fake_file))
        monkeypatch.setattr(
            restore_equiv_pdf,
            'is_git_status_modified',
            lambda file_path: file_path.resolve() in modified_files
        )
        monkeypatch.setattr(
            restore_equiv_pdf,
            'get_committed_file',
            lambda file_path, temp_dir: file_path
        )
        monkeypatch.setattr(
            restore_equiv_pdf,
            'PATTERN_DISPATCH',
            {'*.pdf': fake_compare}
        )
        unchanged = restore_equiv_pdf.list_unchanged_files()
    assert len(unchanged) == 1
    assert Path(unchanged[0]).resolve() == (result_dir / 'a.pdf').resolve()


def test_restore_unchanged_files_restores_in_sorted_order(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test restore_unchanged_files restores files in sorted order."""
    calls: list[list[str]] = []

    def fake_list_unchanged() -> list[str]:
        """Return unsorted unchanged file list."""
        return ['/tmp/z.pdf', '/tmp/a.pdf']

    def fake_restore_sorted_files(unchanged_files: list[str]) -> None:
        """Record unchanged file list passed to shared restore helper."""
        calls.append(unchanged_files)
        for file in sorted(unchanged_files):
            print(f'git restored {file}')
        print(f'Restored {len(unchanged_files)} unchanged files.')

    monkeypatch.setattr(restore_equiv_pdf, 'list_unchanged_files',
                        fake_list_unchanged)
    monkeypatch.setattr(restore_equiv_pdf, 'restore_sorted_files',
                        fake_restore_sorted_files)
    restore_equiv_pdf.restore_unchanged_files()
    out, err = capsys.readouterr()
    assert err == ''
    assert calls == [['/tmp/z.pdf', '/tmp/a.pdf']]
    assert 'git restored /tmp/a.pdf' in out
    assert 'git restored /tmp/z.pdf' in out
    assert 'Restored 2 unchanged files.' in out


def test_restore_equiv_pdf_main_calls_restore(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test module main delegates to restore_unchanged_files."""
    called = {'count': 0}

    def fake_restore() -> None:
        """Record one call."""
        called['count'] += 1

    monkeypatch.setattr(restore_equiv_pdf, 'restore_unchanged_files',
                        fake_restore)
    restore_equiv_pdf.main()
    assert called['count'] == 1


def test_list_unchanged_files_uses_latest_committed_pdf_content() -> None:
    """Test committed PDF content is used when comparing modified files."""
    with TemporaryDirectory() as tmp_dir:
        repo_dir = Path(tmp_dir) / 'repo'
        init_git_repo(repo_dir)
        tracked_file = repo_dir / 'example' / 'result' / 'item.pdf'
        _write_pdf(tracked_file, 'Committed text', 'Sample',
                   "D:20260101000000+00'00'")
        run_git(repo_dir, ['add', '.'])
        run_git(repo_dir, ['commit', '-m', 'initial commit'])
        _write_pdf(tracked_file, 'Committed text', 'Sample',
                   "D:20260202000000+00'00'")
        assert restore_equiv_pdf.are_pdf_files_equivalent(
            tracked_file,
            restore_equiv_pdf.get_committed_file(
                tracked_file,
                Path(tmp_dir) / 'copy'
            )
        )
