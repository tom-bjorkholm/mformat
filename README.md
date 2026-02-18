# mformat

> **👤 Looking to use this in your program**  
> This repository is for developers of the package. If you want to install and use `mformat` or `mformat-ext` including writing programs that use them, please visit the **PyPI project page [https://pypi.org/project/mformat](https://pypi.org/project/mformat) or [https://pypi.org/project/mformat-ext](https://pypi.org/project/mformat-ext)** for installation instructions and user documentation.

## What is it

The mformat package contains a number of classes providing a uniform way for a python program to write to a number of different file formats.

The primary intended use is for text output from a python program, where the programmer would like the user to be able to select the output file formats. Some users may want the text as a Microsoft Word file, others as a LibreOffice Open Document Text file, while still others might want it as Markdown. By using the uniform way of writing provided by mformat the same python code can produce output in a number of different formats.

This is intended to provide an easy and uniform way to produce information in different formats. The emphasis is on getting the same information into the different formats. This will allow you to get a correct (but perhaps rudimentary) document in several formats. If you want to produce the most estetically pleasing document in a particular format, this is not the correct library to use.

### mformat base package

The base package contains support for the output formats that are supported with a minimum of dependencies. The base folder contains the source code and tests of the base package.

### mformat-ext extended package

The extended package contains also support for additional output formats that require additional dependencies. The extend folder contains the source code and tests of the extended package.

### Examples

To make it easy for a programmer new to mformat to start using it there are a number of example programs. The example folder contains the example programs, as well as the output produced by running the example programs. There is currently very few tests of the example programs in the automatic test suite.

## For developers

### Needed environment

#### OS

For running the script and running the test suite you need a mac or a Linux computer. Even if the resulting package can be installed and used on Windows, the scripts for building and testing are only implemented for mac and Linux.

#### Python version

Please see README_pypi.md for information on needed python version. Main development is on newest Python version.

#### Zsh

The scripts are all zsh. zsh is available by default on modern macs. zsh can easily be installed on Linux (on Ubuntu: `sudo apt install zsh`).

### Quick start

1. Clone this repository
2. Run `./setup_build_environment.zsh` to set up the build environment
3. Run `./doBuild.zsh` to build and test the package

### Building application

There are 3 main scripts (and 2 extra convinience scripts) for building the application:

- `setup_build_environment.zsh` Run this script first to get the environment set up for building
- `doBuild.zsh` Run this script to build an installation package (.whl) and to run the tests on it in a venv (virtual environment).
- `clean.zsh` Deletes all files that was produced by the build to start over from a clean state.
- `cleanBuild.zsh` Combines the use of `clean.zsh`, `setup_build_environment.zsh` and `doBuild.zsh` into one script. Pylint discover some duplicate code warnings only on a clean build so this is useful.
- `doPypiBuild.zsh` Builds for PyPI upload and can do the upload too.

The "testing" includes pytest, pylint, flake8 and mypy.

After running `doBuild.zsh` you can open `reports/index.html` to see all test reports.

### The readme files for PyPI

The script `build_helpers/create_pypi_readme.py` creates the 2 readme files for PyPI:
`base/README_pypi.md` and `extend/README_pypi.org`.

## Test summary

- Test result: 1480 passed in 26s
- No Flake8 warnings.
- No mypy errors found.
- 0.3 built and tested using python version: Python 3.12.6
