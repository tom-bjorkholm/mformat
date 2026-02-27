#! /usr/local/bin/python3
"""Test the mformat_rst module table functionality."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from check_capsys import check_capsys
from rst_test_helpers import check_rst_output, run_rst_output
from mformat.mformat_state import Formatting
from mformat.plain_text_table import TableAlignment


def test_simple_table(capsys):
    """Test a simple reST table."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_table', {'first_row': ['Col1', 'Col2']}),
            ('add_table_row', {'row': ['A', '1']}),
            ('add_table_row', {'row': ['B', '2']}),
        ],
        expected_text='+------+------+\n'
                      '| Col1 | Col2 |\n'
                      '+------+------+\n'
                      '| A    | 1    |\n'
                      '+------+------+\n'
                      '| B    | 2    |\n'
                      '+------+------+\n')


def test_write_complete_table(capsys):
    """Test write_complete_table in reST output."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('write_complete_table',
             {'table': [['Name', 'Value'], ['Alpha', '1'], ['Beta', '22']]}),
        ],
        expected_text='+-------+-------+\n'
                      '| Name  | Value |\n'
                      '+-------+-------+\n'
                      '| Alpha | 1     |\n'
                      '+-------+-------+\n'
                      '| Beta  | 22    |\n'
                      '+-------+-------+\n')


def test_table_row_mismatch_runtime_error(capsys):
    """Test add_table_row with wrong number of cells."""
    with pytest.raises(RuntimeError) as exc:
        run_rst_output(
            method_calls=[
                ('new_table', {'first_row': ['A', 'B', 'C']}),
                ('add_table_row', {'row': ['1', '2']}),
            ])
    assert exc.value.args[0] == 'Row has 2 columns, but table has 3 columns'
    check_capsys(capsys)


def test_table_row_mismatch_value_error(capsys):
    """Test _write_table_row reports row number in error message."""
    with pytest.raises(ValueError) as exc:
        run_rst_output(
            method_calls=[
                ('new_table', {'first_row': ['Name', 'Age', 'City']}),
                ('_write_table_row', {
                    'row': ['Alice', '30'],
                    'formatting': Formatting(bold=False, italic=False),
                    'row_number': 2}),
                ('add_table_row', {'row': ['Bob', '25', 'LA']}),
            ])
    assert exc.value.args[0] == 'Row 2 has 2 columns, but table has 3 columns.'
    check_capsys(capsys)


def test_paragraph_then_table(capsys):
    """Test paragraph followed by table."""
    expected_lines = [
        'Intro',
        '',
        '+---+---+',
        '| A | B |',
        '+---+---+',
        '| 1 | 2 |',
        '+---+---+',
    ]
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_paragraph', {'text': 'Intro'}),
            ('new_table', {'first_row': ['A', 'B']}),
            ('add_table_row', {'row': ['1', '2']}),
        ],
        expected_text='\n'.join(expected_lines) + '\n')


def test_table_then_paragraph(capsys):
    """Test table followed by paragraph."""
    expected = [
        '+---+---+',
        '| A | B |',
        '+---+---+',
        '| 1 | 2 |',
        '+---+---+',
        '',
        'Outro',
    ]
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_table', {'first_row': ['A', 'B']}),
            ('add_table_row', {'row': ['1', '2']}),
            ('new_paragraph', {'text': 'Outro'}),
        ],
        expected_text='\n'.join(expected) + '\n')


def test_table_max_line_length_affects_wrapping(capsys):
    """Test table_max_line_length is used for table output."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_table', {'first_row': ['First', 'Second']}),
            ('add_table_row', {'row': ['AA BB CC DD', '11 22 33 44']}),
        ],
        expected_text='+-------+-------------+\n'
                      '| First | Second      |\n'
                      '+-------+-------------+\n'
                      '| AA BB | 11 22 33 44 |\n'
                      '| CC DD |             |\n'
                      '+-------+-------------+\n',
        args={'line_length': 42, 'table_max_line_length': 26})


def test_table_alignment_invalid_type_raises_value_error(capsys):
    """Test invalid table_alignment type raises ValueError."""
    with pytest.raises(ValueError) as exc:
        run_rst_output(
            method_calls=[
                ('new_table', {'first_row': ['First', 'Second']}),
                ('add_table_row', {'row': ['AA BB CC DD', '11 22 33 44']}),
            ],
            args={'line_length': 42, 'table_alignment': 1})
    assert exc.value.args[0] == \
        'Alignment specification must be TableAlignment or list of ' \
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
    """Test table_alignment controls reST table alignment."""
    check_rst_output(
        capsys=capsys,
        method_calls=[
            ('new_table', {'first_row': ['First', 'Second']}),
            ('add_table_row', {'row': ['AA BB CC DD', '11 22 33 44']}),
        ],
        expected_text=expected,
        args={'line_length': 42, 'table_alignment': alignment})
