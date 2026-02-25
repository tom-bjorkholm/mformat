#! /usr/local/bin/python3
"""Test the mformat_txt module table functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from test_helpers import (
    check_run_with_context_manager,
    run_with_context_manager,
)
from mformat.plain_text_table import TableAlignment


def test_simple_table(capsys):
    """Test a simple TXT table."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_table(first_row=['Col1', 'Col2'])
        mfd.add_table_row(row=['A', '1'])
        mfd.add_table_row(row=['B', '2'])

    expected = ('+------+------+\n'
                '| Col1 | Col2 |\n'
                '+------+------+\n'
                '|  A   |    1 |\n'
                '+------+------+\n'
                '|  B   |    2 |\n'
                '+------+------+\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_write_complete_table(capsys):
    """Test write_complete_table in TXT output."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.write_complete_table(
            table=[['Name', 'Value'], ['Alpha', '1'], ['Beta', '22']])

    expected = ('+-------+-------+\n'
                '|  Name | Value |\n'
                '+-------+-------+\n'
                '| Alpha |     1 |\n'
                '+-------+-------+\n'
                '|  Beta |    22 |\n'
                '+-------+-------+\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_row_mismatch_runtime_error(capsys):
    """Test add_table_row with wrong number of cells."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_table(first_row=['A', 'B', 'C'])
        mfd.add_table_row(row=['1', '2'])

    with pytest.raises(RuntimeError) as exc:
        _ = run_with_context_manager('txt', '.txt', test_action)
    assert exc.value.args[0] == 'Row has 2 columns, but table has 3 columns'
    check_capsys(capsys)


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_paragraph(text='Intro')
        mfd.new_table(first_row=['A', 'B'])
        mfd.add_table_row(row=['1', '2'])

    expected = ('Intro\n'
                '\n'
                '+---+---+\n'
                '| A | B |\n'
                '+---+---+\n'
                '| 1 | 2 |\n'
                '+---+---+\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_table(first_row=['A', 'B'])
        mfd.add_table_row(row=['1', '2'])
        mfd.new_paragraph(text='Outro')

    expected = ('+---+---+\n'
                '| A | B |\n'
                '+---+---+\n'
                '| 1 | 2 |\n'
                '+---+---+\n'
                '\n'
                'Outro\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   capsys=capsys)


def test_table_max_line_length_affects_wrapping(capsys):
    """Test table_max_line_length is used for table output."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_table(first_row=['First', 'Second'])
        mfd.add_table_row(row=['AA BB CC DD', '11 22 33 44'])

    expected = ('+-------+-------------+\n'
                '| First |    Second   |\n'
                '+-------+-------------+\n'
                '| AA BB | 11 22 33 44 |\n'
                '| CC DD |             |\n'
                '+-------+-------------+\n')
    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   args={'line_length': 42,
                                         'table_max_line_length': 26},
                                   capsys=capsys)


def test_table_alignment_invalid_type_raises_value_error(capsys):
    """Test invalid table_alignment type raises ValueError."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_table(first_row=['First', 'Second'])
        mfd.add_table_row(row=['AA BB CC DD', '11 22 33 44'])

    with pytest.raises(ValueError) as exc:
        _ = run_with_context_manager('txt', '.txt', test_action,
                                     args={'line_length': 42,
                                           'table_alignment': 1})
    assert exc.value.args[0] == \
        'Alignment specification must be TableAlignment or list of '\
        'TableAlignment'
    check_capsys(capsys)


@pytest.mark.parametrize(
    'alignment, expected',
    [
        (TableAlignment.LEFT,
         '+-------------+-------------+\n'
         '| First       | Second      |\n'
         '+-------------+-------------+\n'
         '| AA BB CC DD | 11 22 33 44 |\n'
         '+-------------+-------------+\n'),
        (TableAlignment.RIGHT,
         '+-------------+-------------+\n'
         '|       First |      Second |\n'
         '+-------------+-------------+\n'
         '| AA BB CC DD | 11 22 33 44 |\n'
         '+-------------+-------------+\n'),
        ([TableAlignment.RIGHT, TableAlignment.LEFT],
         '+-------------+-------------+\n'
         '|       First | Second      |\n'
         '+-------------+-------------+\n'
         '| AA BB CC DD | 11 22 33 44 |\n'
         '+-------------+-------------+\n'),
    ]
)
def test_table_alignment_argument(capsys, alignment, expected):
    """Test table_alignment controls TXT table alignment."""
    def test_action(mfd):
        assert type(mfd).__name__ == 'MultiFormatTxt'
        mfd.new_table(first_row=['First', 'Second'])
        mfd.add_table_row(row=['AA BB CC DD', '11 22 33 44'])

    check_run_with_context_manager('txt', '.txt', test_action,
                                   expected_text=expected,
                                   args={'line_length': 42,
                                         'table_alignment': alignment},
                                   capsys=capsys)
