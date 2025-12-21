#! /usr/local/bin/python3
"""Setup file specifying build of .whl."""

from setuptools import setup

setup(
  name='mformat',
  version='0.0.1',
  description='Multi file format class',
  author='Tom Björkholm',
  author_email='klausuler_linnet0q@icloud.com',
  python_requires='>=3.12',
  packages=['mformat'],
  package_dir={'mformat': 'src/mformat'},
  package_data={'mformat': ['src/py.typed']},
  install_requires=[  # pylint: disable=duplicate-code
    'pypi-simple >= 1.8.0',
    'packaging >= 25.0',
    'argcomplete >= 3.6.3',
    'requests >= 2.32.3',
    'types-requests >= 2.32.4.20250913',
    'pip >= 25.3',
    'setuptools >= 80.9.0',
    'build >= 1.3.0',
    'wheel>=0.45.1'
  ]
)
