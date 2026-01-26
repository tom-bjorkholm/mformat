#!/usr/bin/env python3
"""Script to generate example/README.md from example source and result files."""  # noqa: E501

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License

import ast
from pathlib import Path
from typing import NamedTuple

from mformat.factory import create_mf, OptArgsDict

# =============================================================================
# Configuration - Edit this section to customize the output
# =============================================================================

# The title for the README
README_TITLE = 'mformat Examples'

# The introductory paragraphs for the README (each string is a paragraph)
INTRO_PARAGRAPHS = [
    'This folder contains simple examples illustrating how to use the '
    'mformat API.',

    'The examples demonstrate various features of the mformat package, '
    'including paragraphs, headings, lists, tables, URLs, and code blocks. '
    'Each example shows how to create output in multiple formats (HTML, '
    'Markdown, Word, and ODT) using the same code.',

    'Notice that the first example file e01_paragraph.py is a complete '
    'example including the command line parsing. This is imported and used '
    'by the other examples. Simpler examples are listed earlier, to help '
    'you get started.',
]

# Base URL for bitbucket repository
BITBUCKET_BASE_URL = (
    'https://bitbucket.org/tom-bjorkholm/mformat/src/master/example'
)

# Categories with their file name patterns (prefix after 'e' and before '_')
# Order matters - first match wins
CATEGORIES: list[tuple[str, list[str]]] = [
    ('Paragraphs', ['01', '02', '03', '04']),
    ('Headings', ['05', '06']),
    ('Bullet Lists', ['07', '08', '09']),
    ('Numbered Lists', ['10', '11', '12']),
    ('Mixed Lists', ['13']),
    ('Tables', ['14', '15', '16', '17']),
    ('URLs', ['20', '21', '22', '23', '24', '25']),
    ('Code Blocks', ['30']),
    ('Passing extra arguments', ['40', '41']),
    ('Complete Example', ['50']),
    ('Extend with own formats', ['60']),
]

# Result file extensions to include (in order)
RESULT_EXTENSIONS = ['.html', '.md', '.docx', '.odt']

# Extension display names for the README
EXTENSION_NAMES = {
    '.html': 'HTML',
    '.md': 'Markdown',
    '.docx': 'Word (docx)',
    '.odt': 'ODT',
}


# =============================================================================
# Implementation
# =============================================================================

class ExampleInfo(NamedTuple):
    """Information about an example file."""

    name: str  # Base name without extension (e.g., 'e01_paragraph')
    source_path: Path  # Path to the source file
    description: str  # Description from function docstring
    result_files: dict[str, Path]  # Extension -> path for existing results


def get_script_directory() -> Path:
    """Return the directory where this script is located."""
    return Path(__file__).parent.resolve()


def get_example_directories(script_dir: Path) -> tuple[Path, Path]:
    """Return the paths to the example source and result directories."""
    example_dir = script_dir / 'example'
    return example_dir / 'src', example_dir / 'result'


def extract_function_docstring(source_path: Path) -> str:
    """Extract the first function's docstring from a Python file."""
    try:
        source_code = source_path.read_text(encoding='utf-8')
        tree = ast.parse(source_code)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node)
                if docstring:
                    return docstring
    except (SyntaxError, FileNotFoundError, UnicodeDecodeError) as e:
        print(f'Warning: Could not parse {source_path}: {e}')
    return 'No description available.'


def discover_examples(src_dir: Path,
                      result_dir: Path) -> list[ExampleInfo]:
    """Discover all example files and their associated result files."""
    examples = []
    # Find all Python files in the source directory
    source_files = sorted(src_dir.glob('e*.py'))
    for source_path in source_files:
        name = source_path.stem  # e.g., 'e01_paragraph'
        # Extract function docstring
        description = extract_function_docstring(source_path)
        # Find existing result files
        result_files = {}
        for ext in RESULT_EXTENSIONS:
            result_path = result_dir / f'{name}{ext}'
            if result_path.exists():
                result_files[ext] = result_path
        examples.append(ExampleInfo(
            name=name,
            source_path=source_path,
            description=description,
            result_files=result_files,
        ))
    return examples


def get_category_for_example(example_name: str) -> str:
    """Determine the category for an example based on its name."""
    # Extract the number part (e.g., '01' from 'e01_paragraph')
    if example_name.startswith('e') and len(example_name) > 2:
        number_part = example_name[1:3]
        for category_name, patterns in CATEGORIES:
            if number_part in patterns:
                return category_name
    return 'Other'


def group_examples_by_category(
        examples: list[ExampleInfo]) -> dict[str, list[ExampleInfo]]:
    """Group examples by their category."""
    grouped: dict[str, list[ExampleInfo]] = {}
    for example in examples:
        category = get_category_for_example(example.name)
        if category not in grouped:
            grouped[category] = []
        grouped[category].append(example)
    return grouped


def generate_bitbucket_url(relative_path: str) -> str:
    """Generate a bitbucket URL for a file."""
    return f'{BITBUCKET_BASE_URL}/{relative_path}'


def get_ordered_categories(
        grouped: dict[str, list[ExampleInfo]]) -> list[str]:
    """Get categories in the configured order, with Other at the end."""
    ordered = [cat for cat, _ in CATEGORIES if cat in grouped]
    if 'Other' in grouped:
        ordered.append('Other')
    return ordered


def allow_overwrite(file_name: str) -> None:
    """Allow overwriting existing files."""
    # Simply return to allow overwriting; the file_name is not used
    _ = file_name


def write_readme(examples: list[ExampleInfo], readme_path: Path) -> None:
    """Write the README.md file using mformat."""
    grouped = group_examples_by_category(examples)
    ordered_categories = get_ordered_categories(grouped)
    args: OptArgsDict = {'file_exists_callback': allow_overwrite}
    with create_mf(format_name='md', file_name=str(readme_path),
                   args=args) as mf:
        # Write title and intro paragraphs
        mf.start_heading(level=1, text=README_TITLE)
        for paragraph in INTRO_PARAGRAPHS:
            mf.start_paragraph(text=paragraph)
        # Write examples grouped by category
        for category in ordered_categories:
            category_examples = grouped[category]
            # Category header (level 1 bullet, bold)
            mf.start_heading(level=2, text=category)
            for example in category_examples:
                # Example description (level 2 bullet)
                mf.start_bullet_item(text=example.description, level=1)
                # Source code link (level 3 bullet)
                source_url = generate_bitbucket_url(f'src/{example.name}.py')
                mf.start_bullet_item(text='Source: ', level=2)
                mf.add_url(text=f'{example.name}.py', url=source_url)
                # Result files (level 3 bullet header, level 4 for each file)
                if not example.result_files:
                    continue
                mf.start_bullet_item(text='Results:', level=2)
                for ext in RESULT_EXTENSIONS:
                    if ext not in example.result_files:
                        continue
                    result_url = generate_bitbucket_url(
                        f'result/{example.name}{ext}')
                    ext_name = EXTENSION_NAMES.get(ext, ext)
                    mf.start_bullet_item(text='', level=3)
                    mf.add_url(text=ext_name, url=result_url)


def main() -> None:
    """Generate example/README.md from example source and result files."""
    script_dir = get_script_directory()
    src_dir, result_dir = get_example_directories(script_dir)
    # Verify directories exist
    if not src_dir.exists():
        print(f'Error: Source directory not found: {src_dir}')
        return
    if not result_dir.exists():
        print(f'Error: Result directory not found: {result_dir}')
        return
    # Discover examples
    examples = discover_examples(src_dir, result_dir)
    if not examples:
        print('Error: No example files found.')
        return
    print(f'Found {len(examples)} example files.')
    # Generate and write README
    readme_path = script_dir / 'example' / 'README.md'
    write_readme(examples, readme_path)
    print(f'Generated: {readme_path}')


if __name__ == '__main__':
    main()
