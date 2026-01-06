#! /usr/local/bin/python3
# pylint: disable=protected-access
"""Test the _encode_text method of MultiFormatMd."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from tempfile import TemporaryDirectory
import pytest
from check_capsys import check_capsys
from mformat.mformat_md import MultiFormatMd
from mformat.mformat import MultiFormatState


class TestEncodeTextEmpty:
    """Tests for empty text handling."""

    def test_empty_string(self, capsys):
        """Test that empty string returns empty string."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                assert mfd._encode_text('') == ''
        check_capsys(capsys)

    def test_none_like_empty(self, capsys):
        """Test that falsy empty string returns as-is."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                result = mfd._encode_text('')
                assert result == ''
        check_capsys(capsys)


class TestEncodeTextCodeBlock:
    """Tests for code block state escaping."""

    def test_code_block_triple_backticks(self, capsys):
        """Test that triple backticks are escaped in code blocks."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                # Set CODE_BLOCK state to test the branch
                mfd.state = MultiFormatState.CODE_BLOCK
                result = mfd._encode_text('code with ``` backticks')
                assert result == 'code with \\`\\`\\` backticks'
        check_capsys(capsys)

    def test_code_block_other_chars_not_escaped(self, capsys):
        """Test that other special chars are NOT escaped in code blocks."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                # Set CODE_BLOCK state to test the branch
                mfd.state = MultiFormatState.CODE_BLOCK
                result = mfd._encode_text('*bold* [link] #heading')
                assert result == '*bold* [link] #heading'
        check_capsys(capsys)

    def test_code_block_multiple_triple_backticks(self, capsys):
        """Test multiple occurrences of triple backticks."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                # Set CODE_BLOCK state to test the branch
                mfd.state = MultiFormatState.CODE_BLOCK
                result = mfd._encode_text('``` and ```')
                assert result == '\\`\\`\\` and \\`\\`\\`'
        check_capsys(capsys)


class TestEncodeTextAlwaysEscaped:
    """Tests for characters that are always escaped."""

    @pytest.mark.parametrize('char,escaped', [
        ('\\', '\\\\'),
        ('`', '\\`'),
        ('[', '\\['),
        (']', '\\]'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('<', '\\<'),
        ('|', '\\|'),
    ])
    def test_always_escaped_single(self, capsys, char, escaped):
        """Test that single always-escape characters are escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text(char)
                assert result == escaped
        check_capsys(capsys)

    @pytest.mark.parametrize('text,expected', [
        ('text with \\backslash', 'text with \\\\backslash'),
        ('inline `code` here', 'inline \\`code\\` here'),
        ('[link](url)', '\\[link\\]\\(url)'),
        ('{attr}', '\\{attr\\}'),
        ('<html>', '\\<html>'),
        ('col1|col2', 'col1\\|col2'),
    ])
    def test_always_escaped_in_context(self, capsys, text, expected):
        """Test always-escape characters in realistic contexts."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text(text)
                assert result == expected
        check_capsys(capsys)

    def test_multiple_always_escaped(self, capsys):
        """Test text with multiple always-escaped characters."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('\\`[]{}|<')
                assert result == '\\\\\\`\\[\\]\\{\\}\\|\\<'
        check_capsys(capsys)


class TestEncodeTextParenthesis:
    """Tests for parenthesis escaping (context: after ])."""

    def test_paren_after_bracket_escaped(self, capsys):
        """Test that ( after ] is escaped (link syntax)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('](url)')
                assert '\\]\\(' in result
        check_capsys(capsys)

    def test_paren_not_after_bracket_not_escaped(self, capsys):
        """Test that ( not after ] is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('function(arg)')
                assert result == 'function(arg)'
        check_capsys(capsys)

    def test_paren_at_start(self, capsys):
        """Test that ( at start is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('(parenthesized)')
                assert result == '(parenthesized)'
        check_capsys(capsys)

    def test_closing_paren_not_escaped(self, capsys):
        """Test that ) is never escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('text) more')
                assert result == 'text) more'
        check_capsys(capsys)


class TestEncodeTextExclamation:
    """Tests for exclamation mark escaping (context: before [)."""

    def test_exclamation_before_bracket_escaped(self, capsys):
        """Test that ! before [ is escaped (image syntax)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('![alt](img.png)')
                assert result.startswith('\\!\\[')
        check_capsys(capsys)

    def test_exclamation_not_before_bracket_not_escaped(self, capsys):
        """Test that ! not before [ is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('Hello! World')
                assert result == 'Hello! World'
        check_capsys(capsys)

    def test_exclamation_at_end(self, capsys):
        """Test that ! at end is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('Exciting!')
                assert result == 'Exciting!'
        check_capsys(capsys)

    def test_exclamation_before_other_char(self, capsys):
        """Test that ! before non-[ is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('!important')
                assert result == '!important'
        check_capsys(capsys)


class TestEncodeTextTilde:
    """Tests for tilde escaping (context: adjacent to ~)."""

    def test_double_tilde_escaped(self, capsys):
        """Test that ~~ (strikethrough) is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('~~strikethrough~~')
                assert result == '\\~\\~strikethrough\\~\\~'
        check_capsys(capsys)

    def test_single_tilde_not_escaped(self, capsys):
        """Test that single ~ is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('approximately ~100')
                assert result == 'approximately ~100'
        check_capsys(capsys)

    def test_tilde_separated_not_escaped(self, capsys):
        """Test that separated tildes are NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('~a~ b ~c~')
                assert '\\~\\~' not in result
        check_capsys(capsys)

    def test_triple_tilde(self, capsys):
        """Test that ~~~ is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('~~~')
                assert result == '\\~\\~\\~'
        check_capsys(capsys)


class TestEncodeTextGreaterThan:
    """Tests for > escaping (context: line start or after <)."""

    def test_greater_than_at_line_start_escaped(self, capsys):
        """Test that > at line start is escaped (blockquote)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('> quoted')
                assert result == '\\> quoted'
        check_capsys(capsys)

    def test_greater_than_after_newline_escaped(self, capsys):
        """Test that > after newline is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('line1\n> quoted')
                assert result == 'line1\n\\> quoted'
        check_capsys(capsys)

    def test_greater_than_mid_line_not_escaped(self, capsys):
        """Test that > mid-line is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('a > b')
                assert result == 'a > b'
        check_capsys(capsys)

    def test_greater_than_after_less_than_escaped(self, capsys):
        """Test that > after < is escaped (HTML tag)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                # Note: > is only escaped at line start or directly after <
                # In 'a<b>c', the > is after 'b', not after '<'
                result = mfd._encode_text('a<b>c')
                assert result == 'a\\<b>c'
        check_capsys(capsys)

    def test_greater_than_directly_after_less_than(self, capsys):
        """Test that > directly after < is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                # Empty tag: > is directly after <
                result = mfd._encode_text('a<>b')
                assert result == 'a\\<\\>b'
        check_capsys(capsys)

    def test_comparison_operators(self, capsys):
        """Test comparison operators in code-like text."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('x > 5 and y > 3')
                assert result == 'x > 5 and y > 3'
        check_capsys(capsys)


class TestEncodeTextHash:
    """Tests for # escaping (context: line start)."""

    def test_hash_at_line_start_escaped(self, capsys):
        """Test that # at line start is escaped (heading)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('# heading')
                assert result == '\\# heading'
        check_capsys(capsys)

    def test_hash_after_newline_escaped(self, capsys):
        """Test that # after newline is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('text\n## heading')
                assert result == 'text\n\\## heading'
        check_capsys(capsys)

    def test_hash_mid_line_not_escaped(self, capsys):
        """Test that # mid-line is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('C# programming')
                assert result == 'C# programming'
        check_capsys(capsys)

    def test_hashtag_mid_line(self, capsys):
        """Test hashtag mid-line is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('trending #topic')
                assert result == 'trending #topic'
        check_capsys(capsys)

    def test_multiple_hashes_at_start(self, capsys):
        """Test multiple # at line start."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('### heading')
                assert result.startswith('\\#')
        check_capsys(capsys)


class TestEncodeTextListMarkers:
    """Tests for - and + escaping (context: line start + space/same char)."""

    @pytest.mark.parametrize('text,expected', [
        ('- item', '\\- item'),
        ('+ item', '\\+ item'),
        ('-\t item', '\\-\t item'),
        ('+\t item', '\\+\t item'),
    ])
    def test_list_marker_at_start_with_space(self, capsys, text, expected):
        """Test list markers at line start with space/tab."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text(text)
                assert result == expected
        check_capsys(capsys)

    def test_dash_at_start_alone(self, capsys):
        """Test single dash at start (end of text) is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('-')
                assert result == '\\-'
        check_capsys(capsys)

    def test_horizontal_rule_dashes(self, capsys):
        """Test --- at line start - only first dash is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                # Only the first dash at line start is escaped
                result = mfd._encode_text('---')
                assert result == '\\---'
        check_capsys(capsys)

    def test_dash_mid_line_not_escaped(self, capsys):
        """Test dash mid-line is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('a-b-c')
                assert result == 'a-b-c'
        check_capsys(capsys)

    def test_dash_mid_line_with_spaces(self, capsys):
        """Test dash mid-line with spaces NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('a - b')
                assert result == 'a - b'
        check_capsys(capsys)

    def test_plus_mid_line_not_escaped(self, capsys):
        """Test plus mid-line is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('a+b')
                assert result == 'a+b'
        check_capsys(capsys)

    def test_list_after_newline(self, capsys):
        """Test list marker after newline is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('line\n- item')
                assert result == 'line\n\\- item'
        check_capsys(capsys)

    def test_dash_at_start_no_space(self, capsys):
        """Test dash at start without space is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('-text')
                assert result == '-text'
        check_capsys(capsys)


class TestEncodeTextEmphasis:
    """Tests for * and _ escaping (emphasis at word boundaries)."""

    @pytest.mark.parametrize('text,expected', [
        ('*bold*', '\\*bold\\*'),
        ('_italic_', '\\_italic\\_'),
        ('**strong**', '\\*\\*strong\\*\\*'),
        ('__emphasis__', '\\_\\_emphasis\\_\\_'),
    ])
    def test_emphasis_markers_at_boundaries(self, capsys, text, expected):
        """Test emphasis markers at word boundaries."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text(text)
                assert result == expected
        check_capsys(capsys)

    def test_asterisk_between_alphanumerics_not_escaped(self, capsys):
        """Test * between alphanumerics is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('a*b*c')
                assert result == 'a*b*c'
        check_capsys(capsys)

    def test_underscore_between_alphanumerics_not_escaped(self, capsys):
        """Test _ between alphanumerics is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('snake_case_name')
                assert result == 'snake_case_name'
        check_capsys(capsys)

    def test_asterisk_at_line_start_with_space(self, capsys):
        """Test * at line start with space is escaped (list)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('* item')
                assert result == '\\* item'
        check_capsys(capsys)

    def test_asterisk_horizontal_rule(self, capsys):
        """Test *** at line start is escaped (horizontal rule)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('***')
                assert result == '\\*\\*\\*'
        check_capsys(capsys)

    def test_underscore_horizontal_rule(self, capsys):
        """Test ___ at line start is escaped (all underscores at boundary)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                # All underscores are at word boundaries
                result = mfd._encode_text('___')
                assert result == '\\_\\_\\_'
        check_capsys(capsys)

    def test_asterisk_after_punctuation(self, capsys):
        """Test * after punctuation is escaped (word boundary)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('word.*bold*')
                assert '\\*bold\\*' in result
        check_capsys(capsys)

    def test_asterisk_before_punctuation(self, capsys):
        """Test * before punctuation is escaped (word boundary)."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('*bold*.')
                assert result.startswith('\\*bold\\*')
        check_capsys(capsys)


class TestEncodeTextEquals:
    """Tests for = escaping (setext heading underline)."""

    def test_equals_at_line_start_followed_by_equals(self, capsys):
        """Test = at line start followed by = is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('===')
                assert result.startswith('\\=')
        check_capsys(capsys)

    def test_equals_at_line_start_alone(self, capsys):
        """Test single = at line start (end of text) is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('=')
                assert result == '\\='
        check_capsys(capsys)

    def test_equals_mid_line_not_escaped(self, capsys):
        """Test = mid-line is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('a=b')
                assert result == 'a=b'
        check_capsys(capsys)

    def test_equals_in_equation(self, capsys):
        """Test = in equation is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('x = y + z')
                assert result == 'x = y + z'
        check_capsys(capsys)

    def test_equals_after_newline(self, capsys):
        """Test = after newline followed by = is escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('heading\n===')
                assert 'heading\n\\=' in result
        check_capsys(capsys)

    def test_equals_at_start_not_followed_by_equals(self, capsys):
        """Test = at start not followed by = is NOT escaped."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('=value')
                assert result == '=value'
        check_capsys(capsys)


class TestEncodeTextRegularText:  # pylint: disable=too-few-public-methods
    """Tests for regular text that should not be escaped."""

    @pytest.mark.parametrize('text', [
        'Hello World',
        'Simple text with spaces',
        '12345',
        'MixedCase123',
        'dots.and.commas,here',
        'question? and answer',
        'semicolon; colon:',
        '"quoted" and \'apostrophe\'',
        'path/to/file',
        'email@example.com',
    ])
    def test_regular_text_unchanged(self, capsys, text):
        """Test that regular text passes through unchanged."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text(text)
                assert result == text
        check_capsys(capsys)


class TestEncodeTextComplexCases:
    """Tests for complex real-world scenarios."""

    def test_markdown_link_syntax(self, capsys):
        """Test escaping of markdown link syntax."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('[link text](http://example.com)')
                assert '\\[' in result
                assert '\\]' in result
                assert '\\(' in result
        check_capsys(capsys)

    def test_markdown_image_syntax(self, capsys):
        """Test escaping of markdown image syntax."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('![alt text](image.png)')
                assert '\\!' in result
                assert '\\[' in result
        check_capsys(capsys)

    def test_html_tag(self, capsys):
        """Test escaping of HTML-like tags."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                # Only < is always escaped; > is only escaped at line start
                # or directly after <
                result = mfd._encode_text('<div>content</div>')
                assert '\\<' in result
                # > after 'v' and 'v' is not escaped
                assert result == '\\<div>content\\</div>'
        check_capsys(capsys)

    def test_inline_code_backticks(self, capsys):
        """Test escaping of inline code backticks."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('use `code` here')
                assert '\\`code\\`' in result
        check_capsys(capsys)

    def test_table_pipe_syntax(self, capsys):
        """Test escaping of table pipe syntax."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('| col1 | col2 |')
                assert '\\|' in result
        check_capsys(capsys)

    def test_multiple_lines_with_special_chars(self, capsys):
        """Test multiline text with various special characters."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                text = '# heading\n- list\n> quote\n*emphasis*'
                result = mfd._encode_text(text)
                assert result.startswith('\\#')
                assert '\n\\-' in result
                assert '\n\\>' in result
                assert '\\*emphasis\\*' in result
        check_capsys(capsys)

    def test_programming_example(self, capsys):
        """Test text that looks like programming code."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('if (x > 5 && y < 10)')
                assert '\\<' in result
                assert '(' in result and '\\(' not in result
        check_capsys(capsys)

    def test_variable_names_with_underscores(self, capsys):
        """Test variable names with underscores."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('my_variable_name')
                assert result == 'my_variable_name'
        check_capsys(capsys)

    def test_math_expressions(self, capsys):
        """Test mathematical expressions."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('a*b + c*d = e')
                assert result == 'a*b + c*d = e'
        check_capsys(capsys)

    def test_file_path_with_special_chars(self, capsys):
        """Test file path that might contain special chars."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('/path/to/my_file.txt')
                assert result == '/path/to/my_file.txt'
        check_capsys(capsys)

    def test_url_with_special_chars(self, capsys):
        """Test URL-like text."""
        with TemporaryDirectory() as tmp_dir:
            fname = tmp_dir + '/test.md'
            with MultiFormatMd(file_name=fname) as mfd:
                mfd.start_paragraph(text='x')
                result = mfd._encode_text('https://example.com/path?a=1&b=2')
                assert result == 'https://example.com/path?a=1&b=2'
        check_capsys(capsys)
