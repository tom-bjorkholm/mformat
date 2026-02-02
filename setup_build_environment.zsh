#!/bin/zsh
#
# Copyright (c) 2024 - 2026 Tom Björkholm
# MIT License
#
if [ ${#} -gt 0 ]; then
    PYTHON=${1}
    if echo ${PYTHON} | grep -v 'python' > /dev/null
    then
        echo ${PYTHON} 'does not look like a python version'
        exit 1
    fi
    if which ${PYTHON} > /dev/null
    then
        echo 'Using PYTHON' ${PYTHON} 
    else
        echo 'Cannot find executable for' ${PYTHON}
        exit 1
    fi
fi
if [[ ! -v PYTHON ]]; then
    PYTHON=`./bestInstalledPython.zsh`
fi
echo 'Using PYTHON' ${PYTHON} 
set -eE
trap 'printf "\e[31m%s: %s\e[m\n" "Exiting due to error code from command" $?' ERR
set -v
if [ ! -z "${VIRTUAL_ENV}" ] ; then
  echo "Cannot set up build environment if already in virtual environment"
  exit 1
fi
if [ -d venv ] ; then
  echo "Virtual environment already present. "
  echo "To delete virtual environment and reinitialize type any character and press <enter>"
  echo "To abort press ctrl-C"
  read a
  rm -rf venv
fi
for pkg in pip setuptools build pylint mypy coverage
do
    ${PYTHON} -m pip install --upgrade ${pkg}
done
${PYTHON} -m pip install twine==6.0.1
${PYTHON} -m venv venv
. ./venv/bin/activate
for pkg in pytest pytest-html flake8 flake8-html pytest-flake8 \
    pytest-skip-slow flake8-docstrings pytest-pylint pytest-cov \
    wheel pypi-simple requests types-requests argcomplete \
    pylint mypy coverage build setuptools wheel lxml \
    python-docx odfdo mammoth odfpy pydoc-markdown pymarkdownlnt \
    restructuredtext-lint html5lib
do
    ${PYTHON} -m pip install --upgrade ${pkg}
done
${PYTHON} -m pip install --upgrade twine==6.0.1
