#! /usr/local/bin/python3
"""Tests for custom_build_tools/src/create_example_readme.py."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from typing import Callable
import pytest
_TEST_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TEST_DIR))
# pylint: disable=wrong-import-position,wrong-import-order
from helpers_custom_build_tools import (  # noqa: E402
    load_source_module,
    write_text
)
# pylint: enable=wrong-import-position,wrong-import-order

create_example = load_source_module(
    'create_example_readme',
    'create_example_readme.py'
)


@pytest.mark.parametrize(
    'docstring, expected',
    [('',
      ''),
     ('One line sentence.',
      'One line sentence.'),
     ('One sentence. Another sentence.',
      'One sentence. Another sentence.'),
     ('No period in line',
      'No period in line'),
     ('First line\nSecond line.',
      'First line')]
)
def test_extract_first_line(docstring: str, expected: str) -> None:
    """Test extraction of first line or sentence from docstrings."""
    extract_first_line: Callable[[str], str] = getattr(
        create_example, '_extract_first_line'
    )
    assert extract_first_line(docstring) == expected


def test_extract_function_docstring_prefers_class_docstring() -> None:
    """Test that class docstring is selected before function docstring."""
    with TemporaryDirectory() as tmp_dir:
        src_file = Path(tmp_dir) / 'source.py'
        write_text(
            src_file,
            'class Demo:\n'
            '    """Class summary. More details."""\n'
            '\n'
            'def run() -> None:\n'
            '    """Function summary."""\n'
            '    return None\n'
        )
        assert create_example.extract_function_docstring(src_file) == (
            'Class summary. More details.'
        )


def test_extract_function_docstring_returns_default_on_parse_error(
        capsys: pytest.CaptureFixture[str]) -> None:
    """Test parse errors produce default description and warning output."""
    with TemporaryDirectory() as tmp_dir:
        src_file = Path(tmp_dir) / 'broken.py'
        write_text(src_file, 'def broken(:\n    pass\n')
        description = create_example.extract_function_docstring(src_file)
    assert description == 'No description available.'
    out, err = capsys.readouterr()
    assert 'Warning: Could not parse' in out
    assert err == ''


def test_discover_examples_collects_results_and_descriptions() -> None:
    """Test discovery of source files, docstrings, and result files."""
    with TemporaryDirectory() as tmp_dir:
        src_dir = Path(tmp_dir) / 'src'
        result_dir = Path(tmp_dir) / 'result'
        write_text(
            src_dir / 'e01_first.py',
            'def example() -> None:\n'
            '    """First example sentence. Extra text."""\n'
            '    return None\n'
        )
        write_text(
            src_dir / 'e99_other.py',
            'def example() -> None:\n'
            '    """Another example."""\n'
            '    return None\n'
        )
        write_text(src_dir / 'ignore_me.py', 'def x() -> None:\n    pass\n')
        write_text(result_dir / 'e01_first.html', '<h1>x</h1>\n')
        write_text(result_dir / 'e01_first.md', '# x\n')
        write_text(result_dir / 'e99_other.odt', 'fake\n')
        examples = create_example.discover_examples(src_dir, result_dir)
    assert [example.name for example in examples] == ['e01_first', 'e99_other']
    assert examples[0].description == 'First example sentence. Extra text.'
    assert examples[1].description == 'Another example.'
    assert sorted(examples[0].result_files.keys()) == ['.html', '.md']
    assert sorted(examples[1].result_files.keys()) == ['.odt']


def test_group_and_order_categories() -> None:
    """Test category grouping and configured category ordering."""
    with TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        examples = [
            create_example.ExampleInfo(
                name='e01_alpha',
                source_path=root / 'e01_alpha.py',
                description='First',
                result_files={}
            ),
            create_example.ExampleInfo(
                name='e60_beta',
                source_path=root / 'e60_beta.py',
                description='Second',
                result_files={}
            ),
            create_example.ExampleInfo(
                name='z77_misc',
                source_path=root / 'z77_misc.py',
                description='Third',
                result_files={}
            )
        ]
        grouped = create_example.group_examples_by_category(examples)
        ordered = create_example.get_ordered_categories(grouped)
    assert sorted(grouped.keys()) == ['Extend with own formats', 'Other',
                                      'Paragraphs']
    assert ordered == ['Paragraphs', 'Extend with own formats', 'Other']


def test_write_readme_writes_expected_links_and_sections() -> None:
    """Test README rendering for categories, source links, and result links."""
    with TemporaryDirectory() as tmp_dir:
        root = Path(tmp_dir)
        readme_path = root / 'README.md'
        examples = [
            create_example.ExampleInfo(
                name='e01_alpha',
                source_path=root / 'src' / 'e01_alpha.py',
                description='Alpha example.',
                result_files={
                    '.md': root / 'result' / 'e01_alpha.md',
                    '.html': root / 'result' / 'e01_alpha.html'
                }
            ),
            create_example.ExampleInfo(
                name='z99_misc',
                source_path=root / 'src' / 'z99_misc.py',
                description='Misc example.',
                result_files={}
            )
        ]
        create_example.write_readme(examples, readme_path)
        text = readme_path.read_text(encoding='utf-8')
    assert '# mformat Examples' in text
    assert '## Paragraphs' in text
    assert '## Other' in text
    assert 'Alpha example.' in text
    assert 'Misc example.' in text
    assert '[e01_alpha.py](' in text
    assert '/example/src/e01_alpha.py' in text
    assert '[HTML](' in text
    assert '/example/result/e01_alpha.html' in text
    assert '[Markdown](' in text
    assert '/example/result/e01_alpha.md' in text


def test_main_reports_missing_source_dir(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main reports a missing source directory."""
    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        monkeypatch.setattr(create_example, '_project_root',
                            lambda: project_root)
        create_example.main()
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Error: Source directory not found' in out


def test_main_reports_missing_result_dir(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main reports a missing result directory."""
    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        (project_root / 'example' / 'src').mkdir(parents=True)
        monkeypatch.setattr(create_example, '_project_root',
                            lambda: project_root)
        create_example.main()
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Error: Result directory not found' in out


def test_main_generates_readme_when_examples_exist(
        capsys: pytest.CaptureFixture[str],
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main discovers examples and writes README successfully."""
    with TemporaryDirectory() as tmp_dir:
        project_root = Path(tmp_dir)
        src_dir = project_root / 'example' / 'src'
        result_dir = project_root / 'example' / 'result'
        readme_path = project_root / 'example' / 'README.md'
        write_text(
            src_dir / 'e01_paragraph.py',
            'def run() -> None:\n'
            '    """Simple paragraph example."""\n'
            '    return None\n'
        )
        write_text(result_dir / 'e01_paragraph.md', '# example\n')
        monkeypatch.setattr(create_example, '_project_root',
                            lambda: project_root)
        create_example.main()
        text = readme_path.read_text(encoding='utf-8')
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Found 1 example files.' in out
    assert 'Generated:' in out
    assert 'Simple paragraph example.' in text


def test_create_example_readme_hook_calls_main(
        monkeypatch: pytest.MonkeyPatch) -> None:
    """Test create_example_readme hook delegates to main."""
    called = {'count': 0}

    def fake_main() -> None:
        """Record one call."""
        called['count'] += 1

    monkeypatch.setattr(create_example, 'main', fake_main)
    create_example.create_example_readme_hook(object(), object())
    assert called['count'] == 1
