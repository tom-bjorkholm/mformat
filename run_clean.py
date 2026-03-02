#! /usr/bin/env python3
"""Thin wrapper calling common_build_tools/src/clean.py."""

import sys
from run_wrapper_common import run_target_script


if __name__ == '__main__':
    sys.exit(run_target_script(
        'clean.py',
        sys.argv[1:],
    ))
