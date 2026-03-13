#! venv/bin/python3
"""Script to restore equivalent PDF files from the result folder.

The version control system git will detect changes in PDF files every time
they are regenerated, even though the actual content can be unchanged. When
this script is run it compares the content of the current (not committed)
version of each PDF file in example/result with the content of the latest
committed version of that file. If the content is unchanged the script will
use 'git restore' to restore the already committed version of the file.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

from dataclasses import dataclass
from pathlib import Path
from collections.abc import Callable
from typing import Any
from git_restore_equiv_common import (
    exit_for_missing_venv_dependency,
    get_committed_file,
    is_git_status_modified,
    list_equivalent_files,
    restore_sorted_files,
)
try:
    import pymupdf
except ImportError as exc:
    exit_for_missing_venv_dependency(exc)

_IGNORED_METADATA_KEYS = {'creationDate', 'modDate'}
_ROUND_DIGITS = 3


@dataclass(frozen=True)
class PdfSpan:
    """Normalized PDF text span."""

    text: str
    font: str
    size: float
    color: int
    bbox: tuple[float, float, float, float]


@dataclass(frozen=True)
class PdfLink:
    """Normalized PDF link annotation."""

    kind: int
    target_page: int
    uri: str
    bbox: tuple[float, float, float, float]


@dataclass(frozen=True)
class PdfPage:
    """Normalized PDF page."""

    size: tuple[float, float]
    text: str
    spans: tuple[PdfSpan, ...]
    links: tuple[PdfLink, ...]


@dataclass(frozen=True)
class PdfDocument:
    """Normalized PDF document."""

    metadata: tuple[tuple[str, str], ...]
    toc: tuple[tuple[int, str, int], ...]
    pages: tuple[PdfPage, ...]


def _round_float(value: float) -> float:
    """Round one float to a stable precision for PDF comparisons."""
    return round(value, _ROUND_DIGITS)


def _normalize_bbox(value: Any) -> tuple[float, float, float, float]:
    """Normalize one PDF bbox-like object."""
    if value is None:
        return (0.0, 0.0, 0.0, 0.0)
    x0 = _round_float(float(value[0]))
    y0 = _round_float(float(value[1]))
    x1 = _round_float(float(value[2]))
    y1 = _round_float(float(value[3]))
    return (x0, y0, x1, y1)


def _normalize_metadata(pdf_document: Any) -> tuple[tuple[str, str], ...]:
    """Normalize document metadata and ignore volatile timestamp fields."""
    metadata_obj = getattr(pdf_document, 'metadata')
    if not isinstance(metadata_obj, dict):
        raise AssertionError('Expected PDF metadata dict')
    normalized: list[tuple[str, str]] = []
    for key, value in sorted(metadata_obj.items()):
        if key in _IGNORED_METADATA_KEYS:
            continue
        normalized_value = '<none>' if value is None else str(value)
        normalized.append((key, normalized_value))
    return tuple(normalized)


def _normalize_toc(pdf_document: Any) -> tuple[tuple[int, str, int], ...]:
    """Normalize the PDF table of contents."""
    toc_obj = pdf_document.get_toc()
    if not isinstance(toc_obj, list):
        raise AssertionError('Expected PDF TOC list')
    toc: list[tuple[int, str, int]] = []
    for entry in toc_obj:
        if not isinstance(entry, list):
            raise AssertionError('Expected PDF TOC entry list')
        if len(entry) < 3:
            raise AssertionError('Expected PDF TOC entry with 3 values')
        level = entry[0]
        title = entry[1]
        page_number = entry[2]
        if not isinstance(level, int):
            raise AssertionError('Expected PDF TOC level int')
        if not isinstance(title, str):
            raise AssertionError('Expected PDF TOC title str')
        if not isinstance(page_number, int):
            raise AssertionError('Expected PDF TOC page int')
        toc.append((level, title, page_number))
    return tuple(toc)


def _iter_span_dicts(page: Any) -> list[dict[str, object]]:
    """Return validated span dictionaries for one PDF page."""
    text_dict = page.get_text('dict')
    if not isinstance(text_dict, dict):
        raise AssertionError('Expected PDF text dict')
    span_dicts: list[dict[str, object]] = []
    blocks = text_dict.get('blocks')
    if not isinstance(blocks, list):
        raise AssertionError('Expected PDF blocks list')
    for block in blocks:
        if not isinstance(block, dict):
            raise AssertionError('Expected PDF block dict')
        lines = block.get('lines', [])
        if not isinstance(lines, list):
            raise AssertionError('Expected PDF lines list')
        for line in lines:
            if not isinstance(line, dict):
                raise AssertionError('Expected PDF line dict')
            span_list = line.get('spans', [])
            if not isinstance(span_list, list):
                raise AssertionError('Expected PDF spans list')
            for span in span_list:
                if not isinstance(span, dict):
                    raise AssertionError('Expected PDF span dict')
                span_dicts.append(span)
    return span_dicts


def _normalize_span(span: dict[str, object]) -> PdfSpan:
    """Normalize one visible PDF span."""
    text = span.get('text')
    font = span.get('font')
    size = span.get('size')
    color = span.get('color', 0)
    bbox = span.get('bbox')
    if not isinstance(text, str):
        raise AssertionError('Expected PDF span text str')
    if not isinstance(font, str):
        raise AssertionError('Expected PDF span font str')
    if not isinstance(size, (int, float)):
        raise AssertionError('Expected PDF span size number')
    if not isinstance(color, int):
        raise AssertionError('Expected PDF span color int')
    return PdfSpan(
        text=text,
        font=font,
        size=_round_float(float(size)),
        color=color,
        bbox=_normalize_bbox(bbox),
    )


def _normalize_spans(page: Any) -> tuple[PdfSpan, ...]:
    """Normalize visible PDF spans on one page."""
    return tuple(_normalize_span(span) for span in _iter_span_dicts(page))


def _normalize_links(page: Any) -> tuple[PdfLink, ...]:
    """Normalize link annotations on one page."""
    links_obj = page.get_links()
    if not isinstance(links_obj, list):
        raise AssertionError('Expected PDF links list')
    links: list[PdfLink] = []
    for link in links_obj:
        if not isinstance(link, dict):
            raise AssertionError('Expected PDF link dict')
        kind = link.get('kind', 0)
        target_page = link.get('page', -1)
        uri = link.get('uri', '')
        if not isinstance(kind, int):
            raise AssertionError('Expected PDF link kind int')
        if not isinstance(target_page, int):
            raise AssertionError('Expected PDF link page int')
        if not isinstance(uri, str):
            raise AssertionError('Expected PDF link URI str')
        links.append(PdfLink(
            kind=kind,
            target_page=target_page,
            uri=uri,
            bbox=_normalize_bbox(link.get('from')),
        ))
    return tuple(links)


def _normalize_pages(pdf_document: Any) -> tuple[PdfPage, ...]:
    """Normalize all pages of one PDF document."""
    page_count = pdf_document.page_count
    if not isinstance(page_count, int):
        raise AssertionError('Expected PDF page count int')
    pages: list[PdfPage] = []
    for page_num in range(page_count):
        page = pdf_document[page_num]
        page_text = page.get_text()
        if not isinstance(page_text, str):
            raise AssertionError('Expected PDF page text str')
        pages.append(PdfPage(
            size=(
                _round_float(float(page.rect.width)),
                _round_float(float(page.rect.height)),
            ),
            text=page_text,
            spans=_normalize_spans(page),
            links=_normalize_links(page),
        ))
    return tuple(pages)


def extract_pdf_document(file_name: Path) -> PdfDocument:
    """Extract one normalized PDF document representation."""
    # PyMuPDF currently exposes this entry point without useful type info.
    pdf_document = pymupdf.open(file_name)  # type: ignore[no-untyped-call]
    with pdf_document:
        return PdfDocument(
            metadata=_normalize_metadata(pdf_document),
            toc=_normalize_toc(pdf_document),
            pages=_normalize_pages(pdf_document),
        )


def are_pdf_files_equivalent(file1: Path, file2: Path) -> bool:
    """Check if two PDF files are equivalent."""
    return extract_pdf_document(file1) == extract_pdf_document(file2)


PATTERN_DISPATCH: dict[str, Callable[[Path, Path], bool]] = {
    '*.pdf': are_pdf_files_equivalent
}


def list_unchanged_files() -> list[str]:
    """Find unchanged files in example/result/*.pdf."""
    return list_equivalent_files(
        module_file=__file__,
        pattern_dispatch=PATTERN_DISPATCH,
        status_func=is_git_status_modified,
        committed_file_func=get_committed_file
    )


def restore_unchanged_files() -> None:
    """Restore unchanged PDF files."""
    unchanged_files = list_unchanged_files()
    restore_sorted_files(unchanged_files)


def main() -> None:
    """Restore unchanged PDF files."""
    restore_unchanged_files()


if __name__ == '__main__':
    main()
