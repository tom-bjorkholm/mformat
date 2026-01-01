#! /usr/local/bin/python3
"""Helper functions for testing mformat modules."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
from typing import Optional, Any, Callable
from mformat.factory import create_mf


def run_with_context_manager(
        format_name: str,
        file_extension: str,
        test_action: Callable[[Any], None],
        args: Optional[dict[str, Any]] = None,
        url_as_text: bool = False) -> str:
    """Run test with context manager and return file contents.

    Args:
        format_name: The format name (e.g. 'html', 'md')
        file_extension: The file extension (e.g. '.html', '.md')
        test_action: A function that takes mfd and performs actions
        args: Optional arguments to pass to create_mf
        url_as_text: Whether to format URLs as text

    Returns:
        The contents of the file after the test action runs
    """
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test' + file_extension
        kwargs = {'file_name': fname}
        if args is not None:
            kwargs['args'] = args
        if url_as_text:
            kwargs['url_as_text'] = url_as_text
        with create_mf(format_name, **kwargs) as mfd:
            test_action(mfd)
        with open(fname, 'rt', encoding='utf-8') as file:
            return file.read()


def run_protected_method(
        format_name: str,
        file_extension: str,
        method_name: str,
        method_args: Optional[tuple[Any, ...]] = None,
        args: Optional[dict[str, Any]] = None) -> str:
    """Run a protected method and return file contents.

    Args:
        format_name: The format name (e.g. 'html', 'md')
        file_extension: The file extension (e.g. '.html', '.md')
        method_name: The name of the protected method to call
        method_args: Optional tuple of arguments to pass to the method
        args: Optional arguments to pass to create_mf

    Returns:
        The contents of the file after the method runs
    """
    with TemporaryDirectory() as tmp_dir:
        fname = tmp_dir + '/test' + file_extension
        kwargs = {'file_name': fname}
        if args is not None:
            kwargs['args'] = args
        mfd = create_mf(format_name, **kwargs)
        mfd.open()
        method = getattr(mfd, method_name)
        if method_args is not None:
            method(*method_args)
        else:
            method()
        mfd._close()  # pylint: disable=protected-access
        with open(fname, 'rt', encoding='utf-8') as file:
            return file.read()
