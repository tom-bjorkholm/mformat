#! /usr/local/bin/python3
"""Tests for custom_build_tools/src/git_restore_equiv_docx_odt.py."""

from dataclasses import dataclass
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import BinaryIO
import pytest
_TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TEST_DIR))
# pylint: disable=wrong-import-position,wrong-import-order
from helpers_custom_build_tools import (  # noqa: E402
    init_git_repo,
    load_source_module,
    run_git,
    write_bytes,
    write_text
)
# pylint: enable=wrong-import-position,wrong-import-order

restore_equiv = load_source_module(
    'git_restore_equiv_docx_odt',
    'git_restore_equiv_docx_odt.py'
)


@dataclass
class FakeHtmlResult:
    """Store fake HTML content."""

    value: str


@dataclass
class FakeDifference:
    """Store one fake HTML difference."""

    expected: str


@dataclass
class FakeCompareResult:
    """Store fake HTML compare result."""

    differences: list[FakeDifference]


def test_are_docx_files_equivalent_uses_converted_html(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test DOCX equivalence compares converted HTML values."""
    def fake_convert_to_html(file_obj: BinaryIO) -> FakeHtmlResult:
        """Convert bytes to lowercased fake HTML text."""
        return FakeHtmlResult(value=file_obj.read().decode('utf-8').lower())

    monkeypatch.setattr(restore_equiv.mammoth, 'convert_to_html',
                        fake_convert_to_html)
    with TemporaryDirectory() as tmp_dir:
        file_a = Path(tmp_dir) / 'a.docx'
        file_b = Path(tmp_dir) / 'b.docx'
        file_c = Path(tmp_dir) / 'c.docx'
        write_bytes(file_a, b'Alpha')
        write_bytes(file_b, b'ALPHA')
        write_bytes(file_c, b'Beta')
        assert restore_equiv.are_docx_files_equivalent(file_a, file_b)
        assert not restore_equiv.are_docx_files_equivalent(file_a, file_c)


@pytest.mark.parametrize(
    'expected_values, expected_result',
    [(['anchor only'], True),
     (['anchor first', 'paragraph diff'], False)]
)
def test_are_odt_files_equivalent_filters_anchor_differences(
        monkeypatch: pytest.MonkeyPatch,
        expected_values: list[str],
        expected_result: bool) -> None:
    """Test ODT equivalence ignores anchor differences only."""
    class FakeConverter:  # pylint: disable=too-few-public-methods
        """Create deterministic HTML output from file bytes."""

        def odf2xhtml(self, file_obj: BinaryIO) -> str:
            """Return fake HTML with a head section."""
            body = file_obj.read().decode('utf-8')
            return f'<html><head>h</head><body>{body}</body></html>'

    def fake_compare_html(html1: str, html2: str) -> FakeCompareResult:
        """Return configured differences regardless of input html."""
        _ = html1
        _ = html2
        differences = [FakeDifference(expected=value)
                       for value in expected_values]
        return FakeCompareResult(differences=differences)

    def fake_odf_load(file_obj: BinaryIO) -> object:
        """Pretend to load ODT and keep caller behavior unchanged."""
        _ = file_obj
        return object()

    monkeypatch.setattr(restore_equiv, 'ODF2XHTML', FakeConverter)
    monkeypatch.setattr(restore_equiv, 'compare_html', fake_compare_html)
    monkeypatch.setattr(restore_equiv, 'odf_load', fake_odf_load)
    with TemporaryDirectory() as tmp_dir:
        file_a = Path(tmp_dir) / 'a.odt'
        file_b = Path(tmp_dir) / 'b.odt'
        write_bytes(file_a, b'First')
        write_bytes(file_b, b'Second')
        result = restore_equiv.are_odt_files_equivalent(file_a, file_b)
    assert result is expected_result


def test_get_committed_file_reads_content_from_latest_commit() -> None:
    """Test extraction of the committed file content into temp directory."""
    with TemporaryDirectory() as tmp_dir:
        repo_dir = Path(tmp_dir) / 'repo'
        init_git_repo(repo_dir)
        tracked_file = repo_dir / 'example' / 'result' / 'item.docx'
        write_bytes(tracked_file, b'old-content')
        run_git(repo_dir, ['add', '.'])
        run_git(repo_dir, ['commit', '-m', 'initial commit'])
        write_bytes(tracked_file, b'new-content')
        commit_copy_dir = Path(tmp_dir) / 'copy'
        commit_copy_dir.mkdir()
        committed_file = restore_equiv.get_committed_file(
            tracked_file, commit_copy_dir
        )
        committed_text = committed_file.read_bytes()
    assert committed_file == commit_copy_dir / 'item.docx'
    assert committed_text == b'old-content'


def test_is_unchanged_file_uses_dispatcher(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test unchanged check delegates to dispatched compare function."""
    calls: list[tuple[Path, Path]] = []

    def fake_get_committed_file(file_path: Path, temp_dir: Path) -> Path:
        """Return deterministic committed file path."""
        _ = file_path
        _ = temp_dir
        return Path('/fake/committed.docx')

    def fake_compare(file_path: Path, committed: Path) -> bool:
        """Record compared paths and return true."""
        calls.append((file_path, committed))
        return True

    monkeypatch.setattr(restore_equiv, 'get_committed_file',
                        fake_get_committed_file)
    monkeypatch.setitem(restore_equiv.EQUIV_DISPATCH,
                        restore_equiv.FileType.DOCX,
                        fake_compare)
    result = restore_equiv.is_unchanged_file(
        Path('/fake/current.docx'),
        restore_equiv.FileType.DOCX,
        Path('/tmp/sandbox')
    )
    assert result is True
    assert calls == [
        (Path('/fake/current.docx'), Path('/fake/committed.docx'))
    ]


def test_is_git_status_modified_in_local_repo(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test git status check in a temporary local repository."""
    with TemporaryDirectory() as tmp_dir:
        repo_dir = Path(tmp_dir) / 'repo'
        init_git_repo(repo_dir)
        tracked_file = repo_dir / 'item.odt'
        write_text(tracked_file, 'original')
        run_git(repo_dir, ['add', '.'])
        run_git(repo_dir, ['commit', '-m', 'initial'])
        monkeypatch.chdir(repo_dir)
        assert not restore_equiv.is_git_status_modified(Path('item.odt'))
        write_text(tracked_file, 'updated')
        assert restore_equiv.is_git_status_modified(Path('item.odt'))


def test_is_git_status_modified_raises_runtime_error_on_bad_return_code(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test runtime error when git status command returns non-zero code."""
    class FakeResult:  # pylint: disable=too-few-public-methods
        """Store fake command result."""

        def __init__(self) -> None:
            """Set fake process data."""
            self.returncode = 1
            self.stdout = b''

    def fake_run(command: str, shell: bool, stdout: int,
                 check: bool) -> FakeResult:
        """Return non-zero fake process result."""
        _ = command
        _ = shell
        _ = stdout
        _ = check
        return FakeResult()

    monkeypatch.setattr(restore_equiv.subprocess, 'run', fake_run)
    with pytest.raises(RuntimeError) as exc:
        _ = restore_equiv.is_git_status_modified(Path('any.file'))
    assert 'Failed to check if any.file is modified in the git status' == (
        str(exc.value)
    )


def test_list_unchanged_files_filters_using_status_and_comparison(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test list_unchanged_files only returns modified and equivalent files."""
    with TemporaryDirectory() as tmp_dir:
        repo_root = Path(tmp_dir) / 'repo'
        result_dir = repo_root / 'example' / 'result'
        write_bytes(result_dir / 'a.docx', b'a')
        write_bytes(result_dir / 'b.docx', b'b')
        write_bytes(result_dir / 'c.odt', b'c')
        write_bytes(result_dir / 'd.odt', b'd')
        fake_file = (
            repo_root / 'custom_build_tools' / 'src' /
            'git_restore_equiv_docx_odt.py'
        )
        fake_file.parent.mkdir(parents=True, exist_ok=True)
        modified_files = {
            (result_dir / 'a.docx').resolve(),
            (result_dir / 'c.odt').resolve()
        }
        equivalent_files = {(result_dir / 'a.docx').resolve()}

        def fake_status(file_path: Path) -> bool:
            """Return if file is marked as modified."""
            return file_path.resolve() in modified_files

        def fake_unchanged(file_path: Path, file_type: object,
                           temp_dir: Path) -> bool:
            """Return if modified file is equivalent to committed version."""
            _ = file_type
            _ = temp_dir
            return file_path.resolve() in equivalent_files

        monkeypatch.setattr(restore_equiv, '__file__', str(fake_file))
        monkeypatch.setattr(restore_equiv, 'is_git_status_modified',
                            fake_status)
        monkeypatch.setattr(restore_equiv, 'is_unchanged_file',
                            fake_unchanged)
        unchanged = restore_equiv.list_unchanged_files()
    assert len(unchanged) == 1
    assert Path(unchanged[0]).resolve() == (result_dir / 'a.docx').resolve()


def test_restore_unchanged_files_restores_in_sorted_order(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test restore_unchanged_files calls git restore in sorted order."""
    commands: list[str] = []

    def fake_list_unchanged() -> list[str]:
        """Return unsorted unchanged file list."""
        return ['/tmp/z.docx', '/tmp/a.odt']

    def fake_run(command: str, shell: bool, check: bool) -> object:
        """Record restore commands."""
        assert shell
        assert check
        commands.append(command)
        return object()

    monkeypatch.setattr(restore_equiv, 'list_unchanged_files',
                        fake_list_unchanged)
    monkeypatch.setattr(restore_equiv.subprocess, 'run', fake_run)
    restore_equiv.restore_unchanged_files()
    out, err = capsys.readouterr()
    assert err == ''
    assert commands == ['git restore /tmp/a.odt', 'git restore /tmp/z.docx']
    assert 'git restored /tmp/a.odt' in out
    assert 'git restored /tmp/z.docx' in out
    assert 'Restored 2 unchanged files.' in out


def test_restore_equiv_main_calls_restore(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test module main delegates to restore_unchanged_files."""
    called = {'count': 0}

    def fake_restore() -> None:
        """Record one call."""
        called['count'] += 1

    monkeypatch.setattr(restore_equiv, 'restore_unchanged_files',
                        fake_restore)
    restore_equiv.main()
    assert called['count'] == 1
