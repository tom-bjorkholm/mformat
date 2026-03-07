#! /usr/local/bin/python3
"""Tests for custom_build_tools/src/create_pypi_readme.py."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import pytest
_TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TEST_DIR))
# pylint: disable=wrong-import-position,wrong-import-order
from helpers_custom_build_tools import (  # noqa: E402
    load_source_module,
    write_text
)
# pylint: enable=wrong-import-position,wrong-import-order

create_pypi = load_source_module(
    'create_pypi_readme',
    'create_pypi_readme.py'
)


def _set_version_history(monkeypatch: pytest.MonkeyPatch,
                         version: str) -> None:
    """Set VERSION_HISTORY to one deterministic test release."""
    monkeypatch.setattr(
        create_pypi,
        'VERSION_HISTORY',
        [['Version', 'Date', 'Python version', 'Description'],
         [version, '01 Jan 2026', '3.12 or newer', 'Test release']]
    )


def _create_paths_for_version_check(
        root: Path,
        base_setup_version: str,
        base_pyproject_version: str,
        extend_setup_version: str,
        extend_pyproject_version: str) -> dict[str, object]:
    """Write local version files and return the corresponding paths dict."""
    write_text(
        root / 'base_setup.py',
        f'version="{base_setup_version}"\n'
    )
    write_text(
        root / 'base_pyproject.toml',
        f'version = "{base_pyproject_version}"\n'
    )
    write_text(
        root / 'ext_setup.py',
        f'version="{extend_setup_version}"\n'
    )
    write_text(
        root / 'ext_pyproject.toml',
        f'version = "{extend_pyproject_version}"\n'
    )
    return {
        'base': create_pypi.Paths(
            readme=root / 'base_README.md',
            setup=root / 'base_setup.py',
            pyproject=root / 'base_pyproject.toml'
        ),
        'extend': create_pypi.Paths(
            readme=root / 'ext_README.md',
            setup=root / 'ext_setup.py',
            pyproject=root / 'ext_pyproject.toml'
        )
    }


def test_get_paths_returns_expected_structure(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test create_pypi get_paths resolves both base and extend paths."""
    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        fake_file = (
            project_root / 'custom_build_tools' / 'src' /
            'create_pypi_readme.py'
        )
        fake_file.parent.mkdir(parents=True)
        monkeypatch.setattr(create_pypi, '__file__', str(fake_file))
        paths = create_pypi.get_paths()
    assert sorted(paths.keys()) == ['base', 'extend']
    assert paths['base'].readme == (
        (project_root / 'base' / 'README_pypi.md').resolve()
    )
    assert paths['extend'].setup == (
        (project_root / 'extend' / 'setup.py').resolve()
    )


@pytest.mark.parametrize(
    'content, expected',
    [('name = "x"\nversion = "1.2.3"\n', '1.2.3'),
     ('version="2.0.1",\n', '2.0.1'),
     ('name = "x"\n', '')]
)
def test_get_version_in_file(content: str, expected: str) -> None:
    """Test version extraction from setup.py or pyproject.toml style text."""
    with TemporaryDirectory() as tmp_dir:
        version_file = Path(tmp_dir) / 'version_file.txt'
        write_text(version_file, content)
        version = create_pypi.get_version_in_file(version_file)
    assert version == expected


def test_check_version_accepts_consistent_files(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test check_version passes when all version values are consistent."""
    _set_version_history(monkeypatch, '1.2')
    with TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        paths = _create_paths_for_version_check(
            root=root,
            base_setup_version='1.2.5',
            base_pyproject_version='1.2.5',
            extend_setup_version='1.2.5',
            extend_pyproject_version='1.2.5'
        )
        create_pypi.check_version(paths)


def test_check_version_fails_on_mismatch(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test check_version exits when version files do not match."""
    _set_version_history(monkeypatch, '1.2')
    with TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        paths = _create_paths_for_version_check(
            root=root,
            base_setup_version='1.2.5',
            base_pyproject_version='1.2.4',
            extend_setup_version='1.2.5',
            extend_pyproject_version='1.2.5'
        )
        with pytest.raises(SystemExit) as exc:
            create_pypi.check_version(paths)
    assert exc.value.code == 1
    out, err = capsys.readouterr()
    assert out == ''
    assert 'Versions are not consistent' in err


def test_create_pypi_readme_writes_markdown(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test create_pypi_readme writes file content and status output."""
    with TemporaryDirectory() as tmp_dir:
        readme_path = Path(tmp_dir) / 'README_pypi.md'
        create_pypi.create_pypi_readme(
            create_pypi.ReadmeType.BASE, readme_path
        )
        text = readme_path.read_text(encoding='utf-8')
    out, err = capsys.readouterr()
    assert out == ''
    assert '# mformat' in text
    assert '## Installing mformat (base package, this package)' in text
    assert '## Version history' in text
    assert '## Test summary' in text
    assert 'Created' in err


def test_create_pypi_readme_hook_calls_main(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test create_pypi_readme hook delegates to main."""
    called = {'count': 0}

    def fake_main() -> None:
        """Record one call."""
        called['count'] += 1

    monkeypatch.setattr(create_pypi, 'main', fake_main)
    create_pypi.create_pypi_readme_hook(object(), object())
    assert called['count'] == 1
