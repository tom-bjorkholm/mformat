#! /usr/local/bin/python3
"""Example of how to handle an existing file."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import os
import sys
from e01_paragraph import example_main
from mformat.factory import create_mf, OptArgs


def example_file_exists(file_name: str) -> None:
    """Show a callback function to handle an existing file."""
    # This function will be given to the MultiFormat constructor as the
    # file_exists_callback argument as show in funciton existing_file_example.
    # This function will be called only when the file already exists.
    # This function shall determine how to handle the existing file.
    print(f'File {file_name} already exists.', file=sys.stderr)
    # Here we simply check an environment variable to have a simple example.
    if os.getenv('MFORMAT_FILE_EXISTS') == 'overwrite':
        print(f'Overwriting file {file_name}.', file=sys.stderr)
        # Returning tells the MultiFormat class to proceed to write the file.
    elif os.getenv('MFORMAT_FILE_EXISTS') == 'backup':
        os.rename(file_name, file_name + '.backup')
        print(f'Backed up file {file_name} to {file_name}.backup.',
              file=sys.stderr)
        # Returning tells the MultiFormat class to proceed to write the file.
    else:
        print(f'Not overwriting file {file_name}.', file=sys.stderr)
        txt = 'Set the environment variable MFORMAT_FILE_EXISTS to ' +\
            '"overwrite" or "backup" to change the behaviour.'
        print(txt, file=sys.stderr)
        # Raising an exception tells the MultiFormat class to stop
        # and not write the file.
        raise FileExistsError(f'File {file_name} already exists.')


def existing_file_example(format_name: str, file_name: str) -> None:
    """Show how to handle an existing file."""
    # We pass the file_exists_callback argument to the MultiFormat constructor
    # using the OptArgs dictionary.
    opt_args: OptArgs = {
        'file_exists_callback': example_file_exists,
    }
    # We use the opt_args dictionary to pass the file_exists_callback argument
    # to the MultiFormat constructor throuch the factory create_mf function,
    # using the optional args argument.
    # We do create_mf in a with statement as described in example
    # e01_paragraph.
    with create_mf(format_name=format_name, file_name=file_name,
                   args=opt_args) as mf:
        mf.start_heading(level=1, text='Existing File Example')
        txt = 'Using the file_exists_callback in the OptArgs dictionary ' +\
            'and passing this dictionary to the MultiFormat constructor ' +\
            '(directly or using the create_mf function) ' +\
            'allows us to handle an exiting file in any way we want. ' +\
            'The default behaviour if no callback is provided is to ' +\
            'refuse to overwrite existing files.'
        mf.start_paragraph(text=txt)


if __name__ == '__main__':
    example_main(example_text='Existing File',
                 function=existing_file_example)
