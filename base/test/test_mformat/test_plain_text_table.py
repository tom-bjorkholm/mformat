#! /usr/local/bin/python3
"""Test the plain_text_table module."""

# Copyright (c) 2026 Tom Björkholm
# MIT License
#

import pytest
from mformat.plain_text_table import (BorderSpec, TableAlignment,
                                      align_cell_value, format_border_row,
                                      format_bottom_border,
                                      format_one_table_row, format_top_border,
                                      get_plain_text_table, get_rst_like_spec,
                                      line_wraps_per_column_width,
                                      select_column_widths)


def _simple_spec() -> BorderSpec:
    """Get a simple border spec with 1-char wide borders.

    All border elements are single characters so that border
    rows and data rows have the same total width.
    """
    return BorderSpec(
        top='=', bottom='=',
        left='|', right='|',
        top_left='+', top_right='+',
        bottom_left='+', bottom_right='+',
        inner_horizontal='-',
        inner_vertical='|',
        top_corner='+',
        bottom_corner='+',
        left_corner='+',
        right_corner='+',
        inner_cell_corner='+',
    )


# --- Tests for BorderSpec ---


class TestBorderSpec:
    """Test BorderSpec named tuple."""

    def test_field_count(self) -> None:
        """Test that BorderSpec has 15 fields."""
        assert len(BorderSpec._fields) == 15

    def test_fields_accessible(self) -> None:
        """Test field access on a BorderSpec instance."""
        spec = get_rst_like_spec()
        assert spec.top == '-'
        assert spec.bottom == '-'
        assert spec.left == '| '
        assert spec.right == ' |'
        assert spec.inner_horizontal == '-'
        assert spec.inner_vertical == ' | '
        assert spec.inner_cell_corner == '-+-'

    def test_is_named_tuple(self) -> None:
        """Test that BorderSpec behaves as a NamedTuple."""
        spec = get_rst_like_spec()
        assert isinstance(spec, tuple)
        assert hasattr(spec, '_fields')


# --- Tests for get_rst_like_spec ---


class TestGetRstLikeSpec:
    """Test get_rst_like_spec function."""

    def test_returns_border_spec(self) -> None:
        """Test return type is BorderSpec."""
        assert isinstance(get_rst_like_spec(), BorderSpec)

    def test_outer_borders(self) -> None:
        """Test outer border patterns."""
        spec = get_rst_like_spec()
        assert spec.top == '-'
        assert spec.bottom == '-'
        assert spec.left == '| '
        assert spec.right == ' |'

    def test_corner_patterns(self) -> None:
        """Test corner patterns."""
        spec = get_rst_like_spec()
        assert spec.top_left == '+-'
        assert spec.top_right == '-+'
        assert spec.bottom_left == '+-'
        assert spec.bottom_right == '-+'
        assert spec.left_corner == '+-'
        assert spec.right_corner == '-+'
        assert spec.top_corner == '-+-'
        assert spec.bottom_corner == '-+-'
        assert spec.inner_cell_corner == '-+-'


# --- Tests for line_wraps_per_column_width ---


class TestLineWrapsPerColumnWidth:
    """Test line_wraps_per_column_width function."""

    def test_single_short_value(self) -> None:
        """Test single value that never needs wrapping."""
        result = line_wraps_per_column_width(['foo'])
        assert result == {3: 0}

    def test_single_value_two_words(self) -> None:
        """Test single value that can be wrapped once."""
        result = line_wraps_per_column_width(
            ['hello world'])
        assert result == {11: 0, 5: 1}

    def test_deduplication_keeps_smallest_width(self) -> None:
        """Test only smallest width per wrap count kept."""
        result = line_wraps_per_column_width(
            ['foo bar baz'])
        assert result == {11: 0, 7: 1, 3: 2}

    def test_multiple_values_accumulate_wraps(self) -> None:
        """Test wraps accumulated across multiple values."""
        result = line_wraps_per_column_width(
            ['hello world', 'foo bar baz'])
        assert result == {11: 0, 7: 2, 5: 3}

    def test_identical_short_values(self) -> None:
        """Test identical short values produce single entry."""
        result = line_wraps_per_column_width(['ab', 'cd'])
        assert result == {2: 0}

    def test_minimum_width_equals_longest_word(self) -> None:
        """Test minimum width is the longest word length."""
        result = line_wraps_per_column_width(
            ['hello world'])
        assert min(result.keys()) == 5

    def test_maximum_width_equals_longest_value(self) -> None:
        """Test maximum width is the longest value length."""
        result = line_wraps_per_column_width(
            ['hello world', 'hi'])
        assert max(result.keys()) == 11

    def test_wrap_counts_strictly_increase(self) -> None:
        """Test wrap counts increase as width decreases."""
        result = line_wraps_per_column_width(
            ['foo bar baz'])
        widths = sorted(result.keys(), reverse=True)
        for i in range(1, len(widths)):
            assert result[widths[i]] > \
                result[widths[i - 1]]

    def test_max_width_always_has_zero_wraps(self) -> None:
        """Test the largest width always has 0 wraps."""
        result = line_wraps_per_column_width(
            ['hello world', 'foo bar baz'])
        max_width = max(result.keys())
        assert result[max_width] == 0


# --- Tests for select_column_widths validation ---


class TestSelectColumnWidthsValidation:
    """Test input validation in select_column_widths."""

    @pytest.mark.parametrize('data', [[], 'bad', 42])
    def test_invalid_data_raises(self, data) -> None:
        """Test invalid data types raise ValueError."""
        with pytest.raises(ValueError,
                           match='not a list'):
            select_column_widths(
                data, _simple_spec(), 80)

    @pytest.mark.parametrize('data', [[[]], [['a'], []]])
    def test_empty_row_raises(self, data) -> None:
        """Test empty rows raise ValueError."""
        with pytest.raises(ValueError,
                           match='not a list'):
            select_column_widths(
                data, _simple_spec(), 80)

    def test_different_column_counts_raises(self) -> None:
        """Test mismatched column counts raise ValueError."""
        with pytest.raises(ValueError,
                           match='different number'):
            select_column_widths(
                [['a', 'b'], ['c']],
                _simple_spec(), 80)

    def test_non_string_cell_raises(self) -> None:
        """Test non-string cells raise ValueError."""
        with pytest.raises(ValueError,
                           match='not a list'):
            select_column_widths(
                [[1, 2]], _simple_spec(), 80)  # type: ignore[list-item]

    @pytest.mark.parametrize('max_len', [0, 1, 5, 9, -1])
    def test_max_line_length_below_10_raises(
            self, max_len) -> None:
        """Test max_line_length < 10 raises ValueError."""
        with pytest.raises(ValueError,
                           match='less than 10'):
            select_column_widths(
                [['a']], _simple_spec(), max_len)

    def test_max_line_length_10_accepted(self) -> None:
        """Test max_line_length=10 is accepted."""
        result = select_column_widths(
            [['a']], _simple_spec(), 10)
        assert result == [1]

    def test_too_short_for_borders_raises(self) -> None:
        """Test RuntimeError when too short for borders."""
        spec = _simple_spec()._replace(
            inner_vertical='|||||||||')
        with pytest.raises(RuntimeError,
                           match='too short'):
            select_column_widths(
                [['a', 'b']], spec, 10)

    def test_too_short_for_data_raises(self) -> None:
        """Test RuntimeError when data cannot fit."""
        with pytest.raises(RuntimeError,
                           match='too short'):
            select_column_widths(
                [['verylongword']],
                _simple_spec(), 10)


# --- Tests for select_column_widths no-wrap ---


class TestSelectColumnWidthsNoWrap:
    """Test select_column_widths when no wrapping needed."""

    def test_single_column(self) -> None:
        """Test single column with short value."""
        result = select_column_widths(
            [['AB']], _simple_spec(), 80)
        assert result == [2]

    def test_two_columns(self) -> None:
        """Test two columns with short values."""
        result = select_column_widths(
            [['AB', 'CD']], _simple_spec(), 80)
        assert result == [2, 2]

    def test_multiple_rows_picks_widest(self) -> None:
        """Test that widest value per column is used."""
        result = select_column_widths(
            [['A', 'BC'], ['DEF', 'G']],
            _simple_spec(), 80)
        assert result == [3, 2]

    def test_exact_fit_no_wrap(self) -> None:
        """Test values that exactly fill available space."""
        spec = _simple_spec()
        result = select_column_widths(
            [['ABCD', 'EFG']], spec, 10)
        assert result == [4, 3]


# --- Tests for select_column_widths with wrap ---


class TestSelectColumnWidthsWithWrap:
    """Test select_column_widths when wrapping needed."""

    def test_single_column_wraps(self) -> None:
        """Test wrapping with a single column."""
        spec = _simple_spec()
        result = select_column_widths(
            [['hello world']], spec, 12)
        assert result == [5]

    def test_two_columns_one_wraps(self) -> None:
        """Test wrapping one column to fit."""
        spec = _simple_spec()
        result = select_column_widths(
            [['hello world', 'AB']], spec, 15)
        assert result == [5, 2]

    def test_optimal_minimizes_total_wraps(self) -> None:
        """Test DP picks combination with fewest wraps."""
        spec = _simple_spec()
        data = [['hello world', 'foo bar baz']]
        result = select_column_widths(data, spec, 21)
        cols = list(zip(*data))
        total_wraps = sum(
            line_wraps_per_column_width(col)[w]
            for col, w in zip(cols, result))
        assert total_wraps == 1
        assert sum(result) <= 18

    def test_tight_fit_only_option(self) -> None:
        """Test when only minimum widths fit."""
        spec = _simple_spec()
        result = select_column_widths(
            [['hello world', 'foo bar baz']],
            spec, 11)
        assert result == [5, 3]

    def test_wrapping_with_multiple_rows(self) -> None:
        """Test wrapping considers all rows in column."""
        spec = _simple_spec()
        data = [['hello world', 'AB'],
                ['short', 'CD']]
        result = select_column_widths(data, spec, 10)
        assert result == [5, 2]


# --- Tests for TableAlignment ---


class TestTableAlignment:
    """Test TableAlignment enum."""

    def test_all_values_exist(self) -> None:
        """Test that all alignment values exist."""
        assert TableAlignment.RIGHT
        assert TableAlignment.LEFT
        assert TableAlignment.LEFT_BUT_DIGITS_RIGHT
        assert TableAlignment.CENTER
        assert TableAlignment.CENTER_BUT_DIGITS_RIGHT

    def test_values_are_distinct(self) -> None:
        """Test that alignment values are distinct."""
        values = [a.value for a in TableAlignment]
        assert len(values) == len(set(values))


# --- Tests for align_cell_value ---


class TestAlignCellValue:
    """Test align_cell_value function."""

    @pytest.mark.parametrize('value, width, expected', [
        ('foo', 5, 'foo  '),
        ('A', 4, 'A   '),
        ('test', 4, 'test'),
    ])
    def test_left(self, value, width, expected) -> None:
        """Test LEFT alignment pads on the right."""
        result = align_cell_value(
            value, TableAlignment.LEFT, width)
        assert result == expected

    @pytest.mark.parametrize('value, width, expected', [
        ('foo', 5, '  foo'),
        ('A', 4, '   A'),
        ('test', 4, 'test'),
    ])
    def test_right(self, value, width, expected) -> None:
        """Test RIGHT alignment pads on the left."""
        result = align_cell_value(
            value, TableAlignment.RIGHT, width)
        assert result == expected

    @pytest.mark.parametrize('value, width, expected', [
        ('foo', 5, ' foo '),
        ('A', 4, ' A  '),
        ('test', 4, 'test'),
    ])
    def test_center(self, value, width, expected) -> None:
        """Test CENTER alignment centers the value."""
        result = align_cell_value(
            value, TableAlignment.CENTER, width)
        assert result == expected

    @pytest.mark.parametrize('value, width, expected', [
        ('foo', 5, 'foo  '),
        ('123', 5, '  123'),
        ('12.5', 6, '  12.5'),
        ('1,000', 7, '  1,000'),
    ])
    def test_left_but_digits_right(self, value, width,
                                   expected) -> None:
        """Test LEFT_BUT_DIGITS_RIGHT alignment."""
        align = TableAlignment.LEFT_BUT_DIGITS_RIGHT
        result = align_cell_value(value, align, width)
        assert result == expected

    @pytest.mark.parametrize('value, width, expected', [
        ('foo', 5, ' foo '),
        ('123', 5, '  123'),
        ('12.5', 6, '  12.5'),
    ])
    def test_center_but_digits_right(self, value, width,
                                     expected) -> None:
        """Test CENTER_BUT_DIGITS_RIGHT alignment."""
        align = TableAlignment.CENTER_BUT_DIGITS_RIGHT
        result = align_cell_value(value, align, width)
        assert result == expected

    def test_empty_value_same_for_all_alignments(self) -> None:
        """Test empty string produces same output for all."""
        for align in TableAlignment:
            result = align_cell_value('', align, 3)
            assert result == '   '
            assert len(result) == 3


# --- Tests for format_one_table_row ---


class TestFormatOneTableRow:
    """Test format_one_table_row function."""

    def test_single_column(self) -> None:
        """Test formatting a single-column row."""
        spec = _simple_spec()
        result = format_one_table_row(
            ['AB'], [4], spec, [TableAlignment.LEFT])
        assert result == '|AB  |'

    def test_two_columns(self) -> None:
        """Test formatting a two-column row."""
        spec = _simple_spec()
        result = format_one_table_row(
            ['AB', 'CD'], [4, 3], spec,
            [TableAlignment.LEFT, TableAlignment.LEFT])
        assert result == '|AB  |CD |'

    def test_right_alignment(self) -> None:
        """Test formatting with right alignment."""
        spec = _simple_spec()
        result = format_one_table_row(
            ['AB'], [4], spec,
            [TableAlignment.RIGHT])
        assert result == '|  AB|'

    def test_exact_width(self) -> None:
        """Test when value exactly fills column width."""
        spec = _simple_spec()
        result = format_one_table_row(
            ['ABCD'], [4], spec, [TableAlignment.LEFT])
        assert result == '|ABCD|'


# --- Tests for format_border_row ---


class TestFormatBorderRow:
    """Test format_border_row function."""

    def test_single_column(self) -> None:
        """Test a single-column border row."""
        result = format_border_row(
            '+', '+', '-', '+', [4])
        assert result == '+----+'

    def test_two_columns(self) -> None:
        """Test a two-column border row."""
        result = format_border_row(
            '+', '+', '-', '+', [4, 3])
        assert result == '+----+---+'

    def test_multi_char_horizontal_pattern(self) -> None:
        """Test with multi-character horizontal pattern."""
        result = format_border_row(
            '+', '+', '=-', '+', [4])
        assert result == '+=-=-+'

    def test_multi_char_horizontal_truncation(self) -> None:
        """Test horizontal pattern truncated to width."""
        result = format_border_row(
            '+', '+', '=-', '+', [3])
        assert result == '+=-=+'


# --- Tests for format_top_border ---


class TestFormatTopBorder:
    """Test format_top_border function."""

    def test_simple_spec(self) -> None:
        """Test top border with simple spec."""
        spec = _simple_spec()
        result = format_top_border(spec, [4, 3])
        assert result == '+====+===+'

    def test_rst_spec_single_column(self) -> None:
        """Test top border with RST spec."""
        spec = get_rst_like_spec()
        result = format_top_border(spec, [4])
        assert result == '+------+'


# --- Tests for format_bottom_border ---


class TestFormatBottomBorder:
    """Test format_bottom_border function."""

    def test_simple_spec(self) -> None:
        """Test bottom border with simple spec."""
        spec = _simple_spec()
        result = format_bottom_border(spec, [4, 3])
        assert result == '+====+===+'

    def test_rst_spec_single_column(self) -> None:
        """Test bottom border with RST spec."""
        spec = get_rst_like_spec()
        result = format_bottom_border(spec, [4])
        assert result == '+------+'


# --- Tests for get_plain_text_table validation ---


class TestGetPlainTextTableValidation:
    """Test input validation in get_plain_text_table."""

    def test_invalid_alignment_type_raises(self) -> None:
        """Test non-list/non-enum alignment type raises ValueError."""
        with pytest.raises(ValueError,
                           match='must be TableAlignment'):
            get_plain_text_table(
                [['AB']], _simple_spec(), 80,
                1)  # type: ignore[arg-type]

    def test_invalid_alignment_element_raises(self) -> None:
        """Test invalid item in alignment list raises ValueError."""
        with pytest.raises(ValueError,
                           match='contains invalid'):
            get_plain_text_table(
                [['AB']], _simple_spec(), 80,
                [TableAlignment.LEFT, 'bad'])  # type: ignore[list-item]

    def test_wrong_alignment_count_raises(self) -> None:
        """Test wrong number of alignment elements."""
        with pytest.raises(ValueError,
                           match='wrong number'):
            get_plain_text_table(
                [['AB', 'CD']], _simple_spec(), 80,
                [TableAlignment.LEFT])

    def test_too_many_alignment_elements_raises(self) -> None:
        """Test too many alignment elements raises."""
        with pytest.raises(ValueError,
                           match='wrong number'):
            get_plain_text_table(
                [['AB']], _simple_spec(), 80,
                [TableAlignment.LEFT,
                 TableAlignment.RIGHT])


# --- Tests for get_plain_text_table no-wrap ---


class TestGetPlainTextTableNoWrap:
    """Test get_plain_text_table without wrapping."""

    def test_single_cell(self) -> None:
        """Test a 1x1 table."""
        result = get_plain_text_table(
            [['AB']], _simple_spec(), 80,
            TableAlignment.LEFT)
        assert result == [
            '+==+',
            '|AB|',
            '+==+',
        ]

    def test_two_by_two(self) -> None:
        """Test a 2x2 table with inner borders."""
        result = get_plain_text_table(
            [['AB', 'CD'], ['EF', 'GH']],
            _simple_spec(), 80, TableAlignment.LEFT)
        assert result == [
            '+==+==+',
            '|AB|CD|',
            '+--+--+',
            '|EF|GH|',
            '+==+==+',
        ]

    def test_single_alignment_broadcast(self) -> None:
        """Test single alignment applied to all columns."""
        result = get_plain_text_table(
            [['A', '1'], ['BC', '23']],
            _simple_spec(), 80, TableAlignment.LEFT)
        assert result == [
            '+==+==+',
            '|A |1 |',
            '+--+--+',
            '|BC|23|',
            '+==+==+',
        ]

    def test_mixed_alignment(self) -> None:
        """Test different alignment per column."""
        result = get_plain_text_table(
            [['A', '1'], ['BC', '23']],
            _simple_spec(), 80,
            [TableAlignment.LEFT, TableAlignment.RIGHT])
        assert result == [
            '+==+==+',
            '|A | 1|',
            '+--+--+',
            '|BC|23|',
            '+==+==+',
        ]

    def test_empty_cells(self) -> None:
        """Test table with empty cell values."""
        result = get_plain_text_table(
            [['hello', ''], ['', 'world']],
            _simple_spec(), 80, TableAlignment.LEFT)
        assert result == [
            '+=====+=====+',
            '|hello|     |',
            '+-----+-----+',
            '|     |world|',
            '+=====+=====+',
        ]

    def test_three_rows(self) -> None:
        """Test a 3-row table has correct inner borders."""
        result = get_plain_text_table(
            [['A'], ['B'], ['C']],
            _simple_spec(), 80, TableAlignment.LEFT)
        assert result == [
            '+=+',
            '|A|',
            '+-+',
            '|B|',
            '+-+',
            '|C|',
            '+=+',
        ]

    def test_all_lines_same_width(self) -> None:
        """Test all output lines have the same width."""
        result = get_plain_text_table(
            [['AB', 'CDE'], ['FG', 'H']],
            _simple_spec(), 80, TableAlignment.LEFT)
        widths = {len(line) for line in result}
        assert len(widths) == 1


# --- Tests for get_plain_text_table with wrapping ---


class TestGetPlainTextTableWrapping:
    """Test get_plain_text_table with multi-line cells."""

    def test_one_column_wraps(self) -> None:
        """Test wrapping in a single-column table."""
        result = get_plain_text_table(
            [['hello world']], _simple_spec(), 12,
            TableAlignment.LEFT)
        assert result == [
            '+=====+',
            '|hello|',
            '|world|',
            '+=====+',
        ]

    def test_one_cell_wraps_other_padded(self) -> None:
        """Test one cell wraps while other is padded."""
        result = get_plain_text_table(
            [['hello world', 'AB']],
            _simple_spec(), 10, TableAlignment.LEFT)
        assert result == [
            '+=====+==+',
            '|hello|AB|',
            '|world|  |',
            '+=====+==+',
        ]

    def test_both_columns_wrap(self) -> None:
        """Test both columns wrap with different heights."""
        result = get_plain_text_table(
            [['hello world', 'foo bar baz']],
            _simple_spec(), 11, TableAlignment.LEFT)
        assert result == [
            '+=====+===+',
            '|hello|foo|',
            '|world|bar|',
            '|     |baz|',
            '+=====+===+',
        ]

    def test_wrapping_with_inner_border(self) -> None:
        """Test wrapping with inner borders between rows."""
        result = get_plain_text_table(
            [['hello world', 'AB'], ['hi', 'CD']],
            _simple_spec(), 10, TableAlignment.LEFT)
        assert result == [
            '+=====+==+',
            '|hello|AB|',
            '|world|  |',
            '+-----+--+',
            '|hi   |CD|',
            '+=====+==+',
        ]

    def test_wrapped_lines_within_max_length(self) -> None:
        """Test all output lines fit within max_line_length."""
        max_len = 15
        result = get_plain_text_table(
            [['hello world', 'foo bar baz']],
            _simple_spec(), max_len,
            TableAlignment.LEFT)
        for line in result:
            assert len(line) <= max_len


# --- Tests for get_plain_text_table with RST spec ---


class TestGetPlainTextTableRst:
    """Test get_plain_text_table with RST border spec."""

    def test_rst_inner_border_uses_correct_patterns(self) -> None:
        """Test inner borders use left/right corners."""
        spec = get_rst_like_spec()
        result = get_plain_text_table(
            [['AB', 'CD'], ['EF', 'GH']],
            spec, 80, TableAlignment.LEFT)
        inner_border = result[2]
        assert '+' in inner_border
        assert ' ' not in inner_border

    def test_rst_single_cell(self) -> None:
        """Test RST format for a single cell."""
        spec = get_rst_like_spec()
        result = get_plain_text_table(
            [['AB']], spec, 80, TableAlignment.LEFT)
        assert result[0] == '+----+'
        assert result[1] == '| AB |'
        assert result[2] == '+----+'

    def test_rst_border_rows_consistent_width(self) -> None:
        """Test all RST border rows have same width."""
        spec = get_rst_like_spec()
        result = get_plain_text_table(
            [['AB', 'CD'], ['EF', 'GH']],
            spec, 80, TableAlignment.LEFT)
        border_lines = [result[0], result[2], result[4]]
        widths = {len(line) for line in border_lines}
        assert len(widths) == 1

    def test_rst_data_rows_consistent_width(self) -> None:
        """Test all RST data rows have same width."""
        spec = get_rst_like_spec()
        result = get_plain_text_table(
            [['AB', 'CD'], ['EF', 'GH']],
            spec, 80, TableAlignment.LEFT)
        data_lines = [result[1], result[3]]
        widths = {len(line) for line in data_lines}
        assert len(widths) == 1
