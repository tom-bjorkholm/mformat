#! venv/bin/python3
"""Script to restore equivalent DOCX and ODT files from the result folder.

The version control system git will detect changes in ODT files and DOCX files
every time they are regenerated, even though the actual content is unchanged.
When this script is run it will compare the content of the current (not
committed) version of each ODT and DOCX file in example/result with the
content of the latest committed version of that file. If the content is
unchanged the script will use 'git restore' to restore the already 
committed version of the file."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from enum import IntEnum, auto
from typing import Callable
import sys
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
try:
    import mammoth
    from odf.opendocument import load as odf_load
    from odf.odf2xhtml import ODF2XHTML
except ImportError as exc:
    print('You need to run this with venv activated.')
    print(f'str(exc): {str(exc)}')
    sys.exit(1)


def are_docx_files_equivalent(file1: Path, file2: Path) -> bool:
    """Check if two DOCX files are equivalent."""
    #  print(f'comparing: {file1} and {file2}')
    with open(file1, 'rb') as f:
        content1 = mammoth.convert_to_html(f)
    with open(file2, 'rb') as f:
        content2 = mammoth.convert_to_html(f)
    return content1.value == content2.value


def are_odt_files_equivalent(file1: Path, file2: Path) -> bool:
    """Check if two ODT files are equivalent."""
    #  print(f'comparing: {file1} and {file2}')
    converter = ODF2XHTML()
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
    return html1 == html2


class FileType(IntEnum):
    """Type of file."""
    DOCX = auto()
    ODT = auto()


EQUIV_DISPATCH: dict[FileType, Callable[[Path, Path], bool]] = {
    FileType.DOCX: are_docx_files_equivalent,
    FileType.ODT: are_odt_files_equivalent,
}


def get_committed_file(file: Path, temp_dir: Path) -> Path:
    """Get the committed version of the file."""
    committed_file = temp_dir / file.name
    git_str = f'cd {file.parent} >/dev/null 2>/dev/null; '
    git_str += f'git show HEAD:./{file.name}'
    with open(committed_file, 'wb') as f:
        cpi = subprocess.run(git_str, shell=True, stdout=f,
                             check=True)
        cpi.check_returncode()
    return committed_file


def is_unchanged_file(file: Path, file_type: FileType,
                      temp_dir: Path) -> bool:
    """Check if the file is unchanged."""
    committed_file = get_committed_file(file, temp_dir)
    return EQUIV_DISPATCH[file_type](file, committed_file)


def is_git_status_modified(file: Path) -> bool:
    """Check if the file is modified in the git status."""
    git_str = f'git status --short {file}'
    cpi = subprocess.run(git_str, shell=True, stdout=subprocess.PIPE,
                         check=True)
    if cpi.returncode != 0:
        raise RuntimeError(f'Failed to check if {file} is modified in the git status')
    return cpi.stdout.decode('utf-8').strip() != ''


def list_unchanged_files() -> list[str]:
    """Find unchanged files in example/result/*.docx, example/result/*.odt."""
    with TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        unchanged_files: list[str] = []
        result_dir = (
            Path(__file__).parent.parent / 'example' / 'result'
        )
        for file in result_dir.glob('*.docx'):
            if is_git_status_modified(file):
                #  print(f'{file} is modified in the git status')
                if is_unchanged_file(file, FileType.DOCX, temp_dir):
                    unchanged_files.append(str(file))
        for file in result_dir.glob('*.odt'):
            if is_git_status_modified(file):
                #  print(f'{file} is modified in the git status')
                if is_unchanged_file(file, FileType.ODT, temp_dir):
                    unchanged_files.append(str(file))
        return unchanged_files


def restore_unchanged_files() -> None:
    """Restore unchanged files."""
    unchanged_files = list_unchanged_files()
    for file in sorted(unchanged_files):
        git_str = f'git restore {file}'
        subprocess.run(git_str, shell=True, check=True)
        print(f'git restored {file}')
    print(f'Restored {len(unchanged_files)} unchanged files.')


def main() -> None:
    """Main function."""
    restore_unchanged_files()

if __name__ == "__main__":
    main()
