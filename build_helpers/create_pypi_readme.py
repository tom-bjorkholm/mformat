#! /usr/local/bin/python3
"""Create the base/README_pypi.md and extend/README_pypi.md files."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from enum import IntEnum
from typing import NamedTuple, TypedDict
from pathlib import Path
import sys
from mformat.factory import create_mf, OptArgsDict
from mformat.mformat import MultiFormat


class ReadmeType(IntEnum):
    """Type of README file."""

    BASE = 0
    EXTEND = 1


class Paths(NamedTuple):
    """Paths to the destination README_pypi.md file and version files."""

    readme: Path
    setup: Path
    pyproject: Path


class PathsForBoth(TypedDict):
    """Paths for both base and extend."""

    base: Paths
    extend: Paths


def get_paths() -> PathsForBoth:
    """Return the paths for both base and extend."""
    script_dir = Path(__file__).parent.resolve()
    base_dir = script_dir / '..' / 'base'
    extend_dir = script_dir / '..' / 'extend'
    base_paths = Paths(readme=base_dir / 'README_pypi.md',
                       setup=base_dir / 'setup.py',
                       pyproject=base_dir / 'pyproject.toml')
    extend_paths = Paths(readme=extend_dir / 'README_pypi.md',
                         setup=extend_dir / 'setup.py',
                         pyproject=extend_dir / 'pyproject.toml')
    return {
        'base': base_paths,
        'extend': extend_paths
    }


def file_exists_callback(file_name: str) -> None:
    """Allow the file to be overwritten."""
    _ = file_name


TITLE_BASE = 'mformat'
TITLE_EXTEND = 'mformat-ext'
INTRO_P1 = 'The mformat package contains a number of classes providing a ' \
            'uniform way for a python program to write to a number of ' \
           'different file formats.'
INTRO_P2 = 'The primary intended use is for text output from a python ' \
           'program, where the programmer would like the user to be able ' \
           'to select the output file formats. Some users may want the text ' \
           'as a Microsoft Word file, others as a LibreOffice Open ' \
           'Document Text file, while still others might want it as ' \
           'Markdown. By using the uniform way of writing provided by ' \
           'mformat the same python code can produce output in a number ' \
           'of different formats.'
INTRO_P3 = 'This is intended to provide an easy and uniform way to produce ' \
           'information in different formats. The emphasis is on getting ' \
           'the same information into the different formats. This will ' \
           'allow you to get a correct (but perhaps rudimentary) document ' \
           'in several formats. If you want to produce the most ' \
           'esthetically pleasing document in a particular format, this is ' \
           'not the correct library to use.'
H2_INSTALLING_B_BASE = 'Installing mformat (base package, this package)'
H2_INSTALLING_B_EXTEND = 'Installing mformat (base package)'
BASE_P1 = 'The base package contains support for the output formats that ' \
          'are supported with a minimum of dependencies. Use this if you ' \
          'for some reason want to avoid extra dependencies.'
BASE_P2_1 = 'If you want to use it, install it using pip from '
BASE_URL = 'https://pypi.org/project/mformat'
BASE_P2_2 = '. There is no need to download anything from Bitbucket to ' \
            'write Python programs that use the library.'
H3_INSTALLING_B_LINUX = 'Installing base mformat on mac and Linux'
COMMAND_INSTALLING_B_LINUX = 'pip3 install --upgrade mformat'
H3_INSTALLING_B_WINDOWS = 'Installing base mformat on Microsoft Windows'
COMMAND_INSTALLING_B_WINDOWS = 'pip install --upgrade mformat'
H2_INSTALLING_E_BASE = 'Installing mformat-ext (extended package)'
H2_INSTALLING_E_EXTEND = 'Installing mformat-ext (extended package, ' \
                         'this package)'
EXTEND_P1 = 'The extended package contains support also for output ' \
            'formats that require some additional dependencies. Use this ' \
            'if you want the full selection of output formats.'
EXTEND_P2_1 = 'If you want to use it, install it using pip from '
EXTEND_URL = 'https://pypi.org/project/mformat-ext'
EXTEND_P2_2 = '. There is no need to download anything from Bitbucket to ' \
            'write Python programs that use the library.'
H3_INSTALLING_E_LINUX = 'Installing extended mformat on mac and Linux'
COMMAND_INSTALLING_E_LINUX = 'pip3 install --upgrade mformat-ext'
H3_INSTALLING_E_WINDOWS = 'Installing extended mformat on Microsoft Windows'
COMMAND_INSTALLING_E_WINDOWS = 'pip install --upgrade mformat-ext'
H2_WHAT_IT_DOES = 'What it does'
P1_WHAT_IT_DOES = 'The main features supported in a uniform way for all ' \
    'supported output file formats are:'
B_WHAT_IT_DOES = [
    'Factory function that takes file format and output file name as '
    'arguments',
    'It opens and closes a file in the selected format, with protection '
    'against accidentically overwriting an existing file',
    'The recommended way to use it is as a context manager in a '
    'with-clause, opening and closing the file',
    'Headings (several levels)',
    'Paragraphs',
    'Nested bullet point lists',
    'Nested numbered point lists',
    'Mixed nested numbered point and bullet point lists',
    'Tables',
    'URLs in paragraphs, headings, numbered point list items and in '
    'bullet point list items'
]
H2_DESIGN_OF_USE = 'Design of program that uses mformat'
P1_DESIGN_OF_USE_1 = 'It is recommended that the ouput function(s) of ' \
    'the a Python program using mformat should have a with-clause ' \
    'getting the formatting object from the factory (easiest with '
P1_DESIGN_OF_USE_C = 'with create_mf(file_format=fmt, ' \
    'file_name=output_file_name) as'
P1_DESIGN_OF_USE_2 = ').'
P2_DESIGN_OF_USE = 'In the context of the with-clause the programmer just ' \
    'calls a minimum of member functions:'
B_DESIGN_OF_USE = [
    ['start_paragraph',
     'to start a new paragraph with some provided text content.'],
    ['start_heading',
     'to start a new heading with some provided text content.'],
    ['start_bullet_item',
     'to start a new bullet point list item with some provided text '
     'content, and if needed to start the bullet point list with the '
     'bullet point item.'],
    ['start_numbered_point_item',
     'to start a new numbered point list item with some provided text '
     'content, and if needed to start the numbered point list with the '
     'number point list item.'],
    ['add_text',
     'to add more text to an already started paragraph, heading, '
     'bullet point list item or numbered point list item.'],
    ['add_url',
     'to add a URL (link) to an already started paragraph, heading, '
     'bullet point list item or numbered point list item.'],
    ['add_code_in_text',
     'to add some short text (function name, variable name, etc.) ' \
     'as code to an already started paragraph, heading, bullet point ' \
     'list item or numbered point list item.'],
    ['start_table', 'to start a new table with the provided first row.'],
    ['add_table_row', 'to add another row to an already started table.'],
    ['write_complete_table', 'to write a table all at once.'],
    ['write_code_block', 'to write some preformatted text as a code block'],
]
P3_DESIGN_OF_USE = 'There are no member functions to end or close any ' \
    'document item. Each document item is automatically closed as another ' \
    'docuemnt item is started (or when closing the file at the end of the ' \
    'context manager scope). start_bullet_item and ' \
    'start_numbered_point_item take an optional level argument, ' \
    'that is used to change to another nesting level.'
H2_EXAMPLES = 'Example programs'
P1_EXAMPLES_1 = 'A number of minimal but complete example programs are ' \
    'provided to help the programmer new to mformat. See '
URL_EXAMPLES = \
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/README.md'
URL_EXAMPLES_TEXT = 'list of examples'
P1_EXAMPLES_2 = '.'
H2_API_DOCUMENTATION = 'API documentation'
P1_API_DOCUMENTATION_1 = 'PI documentation automatically extracted from ' \
    'the Python code and docstrings are available '
API_URL_PUBLIC = \
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/doc/api.md'
API_URL_PUBLIC_TEXT = 'here for the public API'
P1_API_DOCUMENTATION_2 = 'for programmers using the API and '
API_URL_PROTECTED = \
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/doc/' \
    'protected_api.md'
API_URL_PROTECTED_TEXT = 'here for the protected API'
P1_API_DOCUMENTATION_3 = 'for programmers that want to extend the API by ' \
    'adding their own derived class that provide some other output format.'
P2_API_DOCUMENTATION_1 = 'Even though some may like reading API ' \
    'documentation, the '
URL_EXAMPLES_TEXT2 = 'example programs'
P2_API_DOCUMENTATION_2 = 'probably provide a better introduction.'
H2_VERSION_HISTORY = 'Version history'
VERSION_HISTORY = [
     ['Version', 'Date', 'Python version', 'Description'],
     ['0.2.2', '31 Jan 2026', '3.12 or newer', 'Dependency corrected'],
     ['0.2.1', '30 Jan 2026', '3.12 or newer', 'Minor documentation fix'],
     ['0.2', '30 Jan 2026', '3.12 or newer', 'First released version']
]
H2_FORMATS = 'Output file formats'
P1_FORMATS = 'The following table provides information about in which '\
    'version support for a format was introduced.'
FORMATS = [
    ['Format', 'Full name of format', 'Which package', 'Starting at version'],
    ['docx', 'Microsoft Word', 'mformat-ext', '0.2'],
    ['html', 'HTML Web page', 'mformat', '0.2'],
    ['md', 'Markdown', 'mformat', '0.2'],
    ['odt', 'Open Document Text', 'mformat-ext', '0.2']
]
DISPATCHER: dict[str, dict[ReadmeType, str]] = {
    'title': {
        ReadmeType.BASE: TITLE_BASE,
        ReadmeType.EXTEND: TITLE_EXTEND
    },
    'installing_base': {
        ReadmeType.BASE: H2_INSTALLING_B_BASE,
        ReadmeType.EXTEND: H2_INSTALLING_B_EXTEND
    },
    'installing_extend': {
        ReadmeType.BASE: H2_INSTALLING_E_BASE,
        ReadmeType.EXTEND: H2_INSTALLING_E_EXTEND
    }
}


def _write_installing(mft: MultiFormat, readme_type: ReadmeType) -> None:
    """Write the installing section."""
    mft.start_heading(level=2,
                      text=DISPATCHER['installing_base'][readme_type])
    mft.start_paragraph(text=BASE_P1)
    mft.start_paragraph(text=BASE_P2_1)
    mft.add_url(url=BASE_URL)
    mft.add_text(text=BASE_P2_2)
    mft.start_heading(level=3, text=H3_INSTALLING_B_LINUX)
    mft.write_code_block(text=COMMAND_INSTALLING_B_LINUX,
                         programming_language='sh')
    mft.start_heading(level=3, text=H3_INSTALLING_B_WINDOWS)
    mft.write_code_block(text=COMMAND_INSTALLING_B_WINDOWS,
                         programming_language='sh')
    mft.start_heading(level=2,
                      text=DISPATCHER['installing_extend'][readme_type])
    mft.start_paragraph(text=EXTEND_P1)
    mft.start_paragraph(text=EXTEND_P2_1)
    mft.add_url(url=EXTEND_URL)
    mft.add_text(text=EXTEND_P2_2)
    mft.start_heading(level=3, text=H3_INSTALLING_E_LINUX)
    mft.write_code_block(text=COMMAND_INSTALLING_E_LINUX,
                         programming_language='sh')
    mft.start_heading(level=3, text=H3_INSTALLING_E_WINDOWS)
    mft.write_code_block(text=COMMAND_INSTALLING_E_WINDOWS,
                         programming_language='sh')


def create_pypi_readme(readme_type: ReadmeType, path: Path) -> None:
    """Create the README_pypi.md file."""
    args: OptArgsDict = {
        'file_exists_callback': file_exists_callback
    }
    with create_mf(format_name='md', file_name=str(path), args=args) as mft:
        mft.start_heading(level=1, text=DISPATCHER['title'][readme_type])
        mft.start_paragraph(text=INTRO_P1)
        mft.start_paragraph(text=INTRO_P2)
        mft.start_paragraph(text=INTRO_P3)
        _write_installing(mft, readme_type)
        mft.start_heading(level=2, text=H2_WHAT_IT_DOES)
        mft.start_paragraph(text=P1_WHAT_IT_DOES)
        for item in B_WHAT_IT_DOES:
            mft.start_bullet_item(text=item)
        mft.start_heading(level=2, text=H2_DESIGN_OF_USE)
        mft.start_paragraph(text=P1_DESIGN_OF_USE_1)
        mft.add_code_in_text(text=P1_DESIGN_OF_USE_C)
        mft.add_text(text=P1_DESIGN_OF_USE_2)
        mft.start_paragraph(text=P2_DESIGN_OF_USE)
        for items in B_DESIGN_OF_USE:
            mft.start_bullet_item(text='')
            mft.add_code_in_text(text=items[0])
            mft.add_text(text=items[1])
        mft.start_paragraph(text=P3_DESIGN_OF_USE)
        mft.start_heading(level=2, text=H2_EXAMPLES)
        mft.start_paragraph(text=P1_EXAMPLES_1)
        mft.add_url(url=URL_EXAMPLES, text=URL_EXAMPLES_TEXT)
        mft.add_text(text=P1_EXAMPLES_2)
        mft.start_heading(level=2, text=H2_API_DOCUMENTATION)
        mft.start_paragraph(text=P1_API_DOCUMENTATION_1)
        mft.add_url(url=API_URL_PUBLIC, text=API_URL_PUBLIC_TEXT)
        mft.add_text(text=P1_API_DOCUMENTATION_2)
        mft.add_url(url=API_URL_PROTECTED, text=API_URL_PROTECTED_TEXT)
        mft.add_text(text=P1_API_DOCUMENTATION_3)
        mft.start_paragraph(text=P2_API_DOCUMENTATION_1)
        mft.add_url(url=URL_EXAMPLES, text=URL_EXAMPLES_TEXT2)
        mft.add_text(text=P2_API_DOCUMENTATION_2)
        mft.start_heading(level=2, text=H2_VERSION_HISTORY)
        mft.write_complete_table(table=VERSION_HISTORY)
        mft.start_heading(level=2, text=H2_FORMATS)
        mft.start_paragraph(text=P1_FORMATS)
        mft.write_complete_table(table=FORMATS)
        mft.start_heading(level=2, text='Test summary')
    print(f'Created {str(path)} file for {readme_type.name}',
          file=sys.stderr)


def get_version_in_file(path: Path) -> str:
    """Get the version from the pyproject.toml or setup.py file."""
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            lline = line.strip()
            if lline.startswith('version =') or lline.startswith('version='):
                word2 = lline.split('=')[1]
                word3 = word2.strip(' \t\n\r"\',')
                return word3
    return ''


def version_in_readme() -> str:
    """Get the biggest version number in README we create now."""
    version = '0.0.0'
    for line in VERSION_HISTORY[1:]:
        if line[0] > version:
            version = line[0]
    return version


def check_version(paths: PathsForBoth) -> None:
    """Check that the version information is consistent between the files."""
    versions: list[str] = []
    for key, path in paths.items():
        assert key in ['base', 'extend']
        assert isinstance(path, Paths)
        versions.append(get_version_in_file(path.pyproject))
        versions.append(get_version_in_file(path.setup))
    if len(versions) != 4:
        print(f'Expected 4 versions, got {len(versions)}',
              file=sys.stderr)
        sys.exit(1)
    for i in versions[1:]:
        if i != versions[0]:
            print(f'Versions are not consistent: {versions[0]} and {i}',
                  file=sys.stderr)
            sys.exit(1)
    ver_in_readme = version_in_readme()
    if ver_in_readme > versions[0]:
        print(f'Version in README {ver_in_readme} is not consistent with '
              f'versions in files {versions[0]}',
              file=sys.stderr)
        sys.exit(1)
    ver_list_readme: list[str] = ver_in_readme.split('.')
    ver_list_files: list[str] = versions[0].split('.')
    for j in [0, 1]:
        if ver_list_readme[j] != ver_list_files[j]:
            print(f'Version in README {ver_in_readme} is not consistent with '
                  f'versions in files {versions[0]}',
                  file=sys.stderr)
            sys.exit(1)


def main() -> None:
    """Create the README_pypi.md files for the base and extend packages."""
    both_paths: PathsForBoth = get_paths()
    check_version(both_paths)
    create_pypi_readme(ReadmeType.BASE, both_paths['base'].readme)
    create_pypi_readme(ReadmeType.EXTEND, both_paths['extend'].readme)


if __name__ == "__main__":
    main()
