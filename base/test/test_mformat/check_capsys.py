#! /usr/local/bin/python3
"""Check the values of the captured stdout and stderr."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional
import pytest


def check_capsys(capsys: pytest.CaptureFixture[str],
                 err_msgs: Optional[list[str]] = None,
                 out_msgs: Optional[list[str]] = None):
    """Check the values of the captured stdout and stderr."""
    out, err = capsys.readouterr()
    if err_msgs is None:
        assert '' == err
    else:
        for msg in err_msgs:
            assert msg in err
    if out_msgs is None:
        assert '' == out
    else:
        for msg in out_msgs:
            assert msg in out
