#! venv/bin/python3
"""Script to restore equivalent DOCX and ODT files from the result folder.

The version control system git will detect changes in ODT files and DOCX files
every time they are regenerated, even though the actual content is unchanged.
When this script is run it will compare the content of the current (not
committed) version of each ODT and DOCX file in example/result with the
content of the latest committed version of that file. If the content is
unchanged the script will use 'git restore' to restore the already
committed version of the file.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from enum import IntEnum, auto
from typing import Callable
from pathlib import Path
from tempfile import TemporaryDirectory
from git_restore_equiv_common import (
    exit_for_missing_venv_dependency,
    get_committed_file,
    is_git_status_modified,
    list_equivalent_files,
    restore_sorted_files,
)
try:
    import mammoth  # type: ignore
    from odf.opendocument import load as odf_load  # type: ignore
    from odf.odf2xhtml import ODF2XHTML  # type: ignore
    from htmlcompare import compare_html  # type: ignore
    from mformat.factory import create_mf
except ImportError as exc:
    exit_for_missing_venv_dependency(exc)


def are_docx_files_equivalent(file1: Path, file2: Path) -> bool:
    """Check if two DOCX files are equivalent."""
    #  print(f'comparing: {file1} and {file2}')
    with open(file1, 'rb') as f:
        content1 = mammoth.convert_to_html(f)
    with open(file2, 'rb') as f:
        content2 = mammoth.convert_to_html(f)
    ret = content1.value == content2.value
    assert isinstance(ret, bool)
    return ret


def are_odt_files_equivalent(file1: Path, file2: Path) -> bool:
    """Check if two ODT files are equivalent."""
    #  print(f'comparing: {file1} and {file2}')
    converter = ODF2XHTML()
    html1 = ''
    html2 = ''
    with open(file1, 'rb') as f1:
        _ = odf_load(f1)
        html1a = converter.odf2xhtml(f1)
        title_pos = html1a.find('</head>')
        html1 = html1a[title_pos:]
    with open(file2, 'rb') as f2:
        _ = odf_load(f2)
        html2a = converter.odf2xhtml(f2)
        title_pos = html2a.find('</head>')
        html2 = html2a[title_pos:]
    result = compare_html(html1, html2)
    diffs = [d for d in result.differences if 'anchor' not in d.expected]
    if diffs:
        #  print(f'diffs: {diffs}')
        return False
    return True


def test_odt_files_equivalent() -> None:
    """Test ODT files equivalence."""
    with TemporaryDirectory() as temp_dir:
        fname1 = Path(temp_dir) / 'test.odt'
        fname2 = Path(temp_dir) / 'test2.odt'
        fname3 = Path(temp_dir) / 'test3.odt'
        fname4 = Path(temp_dir) / 'test4.odt'
        head1 = 'A great heading for testing'
        para1 = 'This is a paragraph for testing'
        with create_mf(format_name='odt', file_name=str(fname1)) as mf:
            mf.new_heading(level=1, text=head1)
            mf.new_paragraph(text=para1)
        with create_mf(format_name='odt', file_name=str(fname2)) as mf:
            mf.new_heading(level=1, text=head1)
            mf.new_paragraph(text=para1)
        assert are_odt_files_equivalent(fname1, fname2)
        with create_mf(format_name='odt', file_name=str(fname3)) as mf:
            mf.new_heading(level=1, text=head1)
            mf.new_paragraph(text=para1 + ' extra')
        assert not are_odt_files_equivalent(fname1, fname3)
        assert not are_odt_files_equivalent(fname2, fname3)
        assert are_odt_files_equivalent(fname3, fname3)
        with create_mf(format_name='odt', file_name=str(fname4)) as mf:
            mf.new_heading(level=1, text=head1 + ' extra')
            mf.new_paragraph(text=para1)
        assert not are_odt_files_equivalent(fname1, fname4)


class FileType(IntEnum):
    """Type of file."""

    DOCX = auto()
    ODT = auto()


EQUIV_DISPATCH: dict[FileType, Callable[[Path, Path], bool]] = {
    FileType.DOCX: are_docx_files_equivalent,
    FileType.ODT: are_odt_files_equivalent,
}
PATTERN_DISPATCH: dict[str, Callable[[Path, Path], bool]] = {
    '*.docx': are_docx_files_equivalent,
    '*.odt': are_odt_files_equivalent,
}


def is_unchanged_file(file: Path, file_type: FileType,
                      temp_dir: Path) -> bool:
    """Check if the file is unchanged."""
    committed_file = get_committed_file(file, temp_dir)
    return EQUIV_DISPATCH[file_type](file, committed_file)


def list_unchanged_files() -> list[str]:
    """Find unchanged files in example/result/*.docx, example/result/*.odt."""
    return list_equivalent_files(
        __file__,
        PATTERN_DISPATCH,
        is_git_status_modified,
        get_committed_file
    )


def restore_unchanged_files() -> None:
    """Restore unchanged files."""
    restore_sorted_files(list_unchanged_files())


def main() -> None:
    """Restore unchanged DOCX and ODT files."""
    restore_unchanged_files()


if __name__ == "__main__":
    main()
