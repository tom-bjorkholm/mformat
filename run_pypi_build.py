#! /usr/bin/env python3
"""Thin wrapper calling common_build_tools/src/do_pypi_build.py."""

import sys
from run_wrapper_common import run_target_script


if __name__ == '__main__':
    sys.exit(run_target_script(
        'do_pypi_build.py',
        sys.argv[1:],
    ))
