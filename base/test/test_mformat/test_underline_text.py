#! /usr/local/bin/python3
"""Test the underline_text module."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

import pytest

from mformat.underline_text import UnderlineSpec, underline_text, wrap_text

# --- Tests for wrap_text ---


class TestWrapTextValidation:
    """Test input validation in wrap_text."""

    @pytest.mark.parametrize('text', [
        'hello\nworld',
        '\n',
        'abc\ndef\nghi',
    ])
    def test_newline_raises(self, text) -> None:
        """Test that newlines in text raise ValueError."""
        with pytest.raises(ValueError, match='newlines'):
            wrap_text(text, 80)

    @pytest.mark.parametrize('max_len', [0, -1, -10])
    def test_max_line_length_too_small_raises(self, max_len) -> None:
        """Test that max_line_length < 1 raises ValueError."""
        with pytest.raises(ValueError, match='at least 1'):
            wrap_text('hello', max_len)

    def test_max_line_length_1_accepted(self) -> None:
        """Test that max_line_length=1 is the minimum accepted value."""
        result = wrap_text('h', 1)
        assert result == ['h']


class TestWrapTextEmptyInput:
    """Test wrap_text with empty or whitespace-only input."""

    def test_empty_string(self) -> None:
        """Test that empty string returns empty list."""
        result = wrap_text('', 80)
        assert not result
        assert isinstance(result, list)

    @pytest.mark.parametrize('text', [' ', '  ', '     '])
    def test_whitespace_only(self, text) -> None:
        """Test that whitespace-only strings return empty list."""
        result = wrap_text(text, 80)
        assert not result
        assert isinstance(result, list)


class TestWrapTextNoWrapping:
    """Test wrap_text when text fits on a single line."""

    @pytest.mark.parametrize('text, max_len', [
        ('hello', 80),
        ('hello world', 80),
        ('hello world', 11),
    ])
    def test_short_text_single_row(self, text, max_len) -> None:
        """Test that text fitting within max_line_length is one row."""
        assert wrap_text(text, max_len) == [text]

    def test_leading_trailing_whitespace_stripped(self) -> None:
        """Test that leading/trailing whitespace is stripped."""
        assert wrap_text('  hello world  ', 80) == ['hello world']


class TestWrapTextWrapping:
    """Test wrap_text word-wrapping behavior."""

    def test_basic_wrap(self) -> None:
        """Test wrapping at a word boundary."""
        result = wrap_text('hello world foo', 11)
        assert result == ['hello world', 'foo']

    def test_wrap_into_three_rows(self) -> None:
        """Test wrapping into three rows."""
        result = wrap_text('hello world foo bar baz', 11)
        assert result == ['hello world', 'foo bar baz']

    def test_wrap_many_words(self) -> None:
        """Test wrapping many short words."""
        result = wrap_text('a b c d e f g h i j k l', 11)
        assert result == ['a b c d e f', 'g h i j k l']

    def test_wrap_picks_rightmost_space(self) -> None:
        """Test that wrapping picks the rightmost space before limit."""
        result = wrap_text('aa bb cc dd ee', 11)
        assert result == ['aa bb cc dd', 'ee']

    def test_multiple_spaces_preserved_away_from_wrap(self) -> None:
        """Test that multiple spaces are preserved away from wrap points."""
        result = wrap_text('aa  bb  cc dd ee ff gg', 14)
        assert result == ['aa  bb  cc dd', 'ee ff gg']

    def test_multiple_spaces_collapsed_at_wrap_point(self) -> None:
        """Test that multiple spaces at wrap point are collapsed."""
        result = wrap_text('hello     world', 12)
        assert result == ['hello', 'world']


class TestWrapTextLongWords:
    """Test wrap_text with words longer than max_line_length."""

    def test_single_long_word(self) -> None:
        """Test that a single long word is kept intact on one line."""
        assert wrap_text('superlongword', 11) == ['superlongword']

    def test_long_word_at_end(self) -> None:
        """Test a long word at the end of text is kept intact."""
        result = wrap_text('hi superlongword', 11)
        assert result == ['hi', 'superlongword']

    def test_long_word_at_start(self) -> None:
        """Test a long word at the start followed by short words."""
        result = wrap_text('superlongword hi there', 11)
        assert result == ['superlongword', 'hi there']

    def test_two_long_words(self) -> None:
        """Test two consecutive long words are each on their own line."""
        result = wrap_text('superlongword anotherlongone', 11)
        assert result == ['superlongword', 'anotherlongone']

    def test_long_word_between_short_words(self) -> None:
        """Test a long word sandwiched between short words."""
        result = wrap_text('hi superlongword bye', 11)
        assert result == ['hi', 'superlongword', 'bye']


# --- Tests for underline_text ---


class TestUnderlineTextValidation:
    """Test input validation in underline_text."""

    def test_empty_pattern_raises(self) -> None:
        """Test that an empty pattern raises ValueError."""
        spec = UnderlineSpec(
            pattern='', empty_lines_between=0, empty_lines_after=0
        )
        with pytest.raises(ValueError, match='pattern must not be empty'):
            underline_text('hello', spec, 80)

    def test_newline_in_text_raises(self) -> None:
        """Test that newlines in text raise ValueError."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=0
        )
        with pytest.raises(ValueError, match='newlines'):
            underline_text('hello\nworld', spec, 80)


class TestUnderlineTextEmptyInput:
    """Test underline_text with empty or whitespace-only text."""

    def test_empty_text(self) -> None:
        """Test that empty text returns empty list."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=1
        )
        result = underline_text('', spec, 80)
        assert not result
        assert isinstance(result, list)

    @pytest.mark.parametrize('text', [' ', '   '])
    def test_whitespace_only_text(self, text) -> None:
        """Test that whitespace-only text returns empty list."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=1
        )
        result = underline_text(text, spec, 80)
        assert not result
        assert isinstance(result, list)


class TestUnderlineTextSingleLine:
    """Test underline_text with text that fits on a single line."""

    def test_single_char_pattern(self) -> None:
        """Test underlining with a single character pattern."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text('Hello', spec, 80)
        assert result == ['Hello', '-----']

    def test_single_char_pattern_with_lines_after(self) -> None:
        """Test underlining with empty lines after."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=2
        )
        result = underline_text('Hello', spec, 80)
        assert result == ['Hello', '-----', '', '']

    def test_multi_char_pattern(self) -> None:
        """Test underlining with a multi-character pattern."""
        spec = UnderlineSpec(
            pattern='=-', empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text('Hello', spec, 80)
        assert result == ['Hello', '=-=-=']

    def test_pattern_longer_than_text(self) -> None:
        """Test underlining when pattern is longer than text."""
        spec = UnderlineSpec(
            pattern='=-=', empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text('Hi', spec, 80)
        assert result == ['Hi', '=-']

    def test_underline_matches_text_length(self) -> None:
        """Test that underline length exactly matches text length."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=0
        )
        text = 'Test text'
        result = underline_text(text, spec, 80)
        assert len(result[1]) == len(text)

    @pytest.mark.parametrize('text, pattern, expected_underline', [
        ('Hello', '-', '-----'),
        ('Hello', '=-', '=-=-='),
        ('Hello', '=-=', '=-==-'),
        ('Hi', '=-=', '=-'),
        ('ABCDEF', '=-', '=-=-=-'),
        ('ABCDEF', '=-=', '=-==-='),
        ('A', '-', '-'),
    ])
    def test_pattern_repetition(self, text, pattern,
                                expected_underline) -> None:
        """Test various pattern repetition scenarios."""
        spec = UnderlineSpec(
            pattern=pattern,
            empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text(text, spec, 80)
        assert result == [text, expected_underline]

    @pytest.mark.parametrize('between, after', [
        (0, 0), (0, 1), (0, 2),
        (1, 0), (1, 1), (2, 2),
    ])
    def test_single_line_between_has_no_effect(self, between, after) -> None:
        """Test that empty_lines_between is irrelevant for one line."""
        spec = UnderlineSpec(
            pattern='-',
            empty_lines_between=between,
            empty_lines_after=after,
        )
        result = underline_text('Hello', spec, 80)
        expected = ['Hello', '-----'] + [''] * after
        assert result == expected


class TestUnderlineTextMultiLine:
    """Test underline_text with text that wraps to multiple lines."""

    def test_two_lines_no_empty_between(self) -> None:
        """Test two wrapped lines with no empty lines between."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == [
            'hello world', '-----------',
            'foo', '---',
        ]

    def test_two_lines_no_pattern(self) -> None:
        """Test two wrapped lines with no pattern."""
        spec = UnderlineSpec(
            pattern=None, empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == ['hello world', 'foo']

    def test_two_lines_no_pattern_1_between(self) -> None:
        """Test two wrapped lines with no pattern and 1 empty line between."""
        spec = UnderlineSpec(
            pattern=None, empty_lines_between=1, empty_lines_after=0
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == ['hello world', '', 'foo']

    def test_two_lines_with_empty_between(self) -> None:
        """Test two wrapped lines with empty lines between."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=1, empty_lines_after=0
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == [
            'hello world', '-----------',
            '',
            'foo', '---',
        ]

    def test_two_lines_with_multiple_empty_between(self) -> None:
        """Test two wrapped lines with multiple empty lines between."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=2, empty_lines_after=0
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == [
            'hello world', '-----------',
            '', '',
            'foo', '---',
        ]

    def test_two_lines_with_empty_after(self) -> None:
        """Test two wrapped lines with empty lines after."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=1
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == [
            'hello world', '-----------',
            'foo', '---',
            '',
        ]

    def test_between_and_after(self) -> None:
        """Test with both empty lines between and after."""
        spec = UnderlineSpec(
            pattern='=', empty_lines_between=1, empty_lines_after=2
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == [
            'hello world', '===========',
            '',
            'foo', '===',
            '', '',
        ]

    def test_three_lines(self) -> None:
        """Test wrapping into three underlined lines."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=1, empty_lines_after=1
        )
        text = 'aaa bbb ccc ddd eee fff'
        result = underline_text(text, spec, 11)
        assert result == [
            'aaa bbb ccc', '-----------',
            '',
            'ddd eee fff', '-----------',
            '',
        ]

    def test_empty_between_only_between_rows_not_after_last(self) -> None:
        """Test that empty_lines_between is not added after last row."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=3, empty_lines_after=0
        )
        result = underline_text('hello world foo', spec, 11)
        assert result == [
            'hello world', '-----------',
            '', '', '',
            'foo', '---',
        ]

    @pytest.mark.parametrize('between, after', [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 0), (3, 1), (3, 2), (3, 3),
    ])
    def test_two_lines_empty_line_combinations(self, between, after) -> None:
        """Test all combinations of empty lines between and after."""
        spec = UnderlineSpec(
            pattern='-',
            empty_lines_between=between,
            empty_lines_after=after,
        )
        result = underline_text('hello world foo', spec, 11)
        expected = (
            ['hello world', '-----------']
            + [''] * between
            + ['foo', '---']
            + [''] * after
        )
        assert result == expected

    @pytest.mark.parametrize('between, after', [
        (0, 0), (0, 1), (1, 0), (1, 1),
        (2, 0), (2, 2), (3, 3),
    ])
    def test_three_lines_empty_line_combinations(self, between,
                                                 after) -> None:
        """Test empty line combinations with three wrapped lines."""
        spec = UnderlineSpec(
            pattern='-',
            empty_lines_between=between,
            empty_lines_after=after,
        )
        text = 'aaa bbb ccc ddd eee fff ggg hhh iii'
        result = underline_text(text, spec, 11)
        expected = (
            ['aaa bbb ccc', '-----------']
            + [''] * between
            + ['ddd eee fff', '-----------']
            + [''] * between
            + ['ggg hhh iii', '-----------']
            + [''] * after
        )
        assert result == expected


class TestUnderlineTextLongWords:
    """Test underline_text with words longer than max_line_length."""

    def test_single_long_word_underlined(self) -> None:
        """Test that a long word gets a full-length underline."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text('superlongword', spec, 11)
        assert result == ['superlongword', '-------------']

    def test_long_word_underline_matches_word_length(self) -> None:
        """Test that the underline matches the long word's length."""
        spec = UnderlineSpec(
            pattern='-', empty_lines_between=0, empty_lines_after=0
        )
        result = underline_text('superlongword', spec, 11)
        assert len(result[0]) == len('superlongword')
        assert len(result[1]) == len('superlongword')


class TestUnderlineSpec:
    """Test UnderlineSpec named tuple."""

    def test_fields(self) -> None:
        """Test that UnderlineSpec has the expected fields."""
        spec = UnderlineSpec(
            pattern='-',
            empty_lines_between=1,
            empty_lines_after=2
        )
        assert spec.pattern == '-'
        assert spec.empty_lines_between == 1
        assert spec.empty_lines_after == 2

    def test_is_tuple(self) -> None:
        """Test that UnderlineSpec behaves as a tuple."""
        spec = UnderlineSpec(
            pattern='=', empty_lines_between=0, empty_lines_after=1
        )
        assert spec[0] == '='
        assert spec[1] == 0
        assert spec[2] == 1
