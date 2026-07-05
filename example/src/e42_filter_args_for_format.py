#! /usr/local/bin/python3
"""Example of using a CSS file and document language with HTML output."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf, OptArgs, filter_args_mf
from mformat.paper_size import PaperSize

# Relative path from result/ to example CSS; works when viewing HTML locally.
# Raw Bitbucket URL:
# https://github.com/tom-bjorkholm/mformat/blob/master/example/css/e41_styles.css  # noqa: E501
CSS_PATH = '../css/e41_styles.css'


def filter_args_for_format_example(format_name: str, file_name: str) -> None:
    """Show filtering of arguments to match the format used."""
    # In example e41_use_css_in_html.py we pass the arguments directly to
    # the create_mf function, and then we needed different arguments for
    # HTML and other formats.
    # Here we use the filter_args_mf function to filter the arguments to
    # match the format used. Only the arguments that are valid for the
    # format used are included in the returned OptArgs dictionary.
    # Aside from the arguments we saw in e41_use_css_in_html.py we also
    # pass the paper_size argument to the create_mf function that is valid
    # for the Rich Text Format (RTF), DOCX and ODT formats.
    # The risk of using filter_args_mf function is that a misspelled
    # arguement will be silently filtered out, and the programming error will
    # not be detected.
    all_opt_args: OptArgs = {
        'css_file': CSS_PATH,
        'lang': 'de',
        'paper_size': PaperSize.A5,
    }
    opt_args = filter_args_mf(args=all_opt_args, format_name=format_name)
    with create_mf(format_name=format_name, file_name=file_name,
                   args=opt_args) as mf:
        mf.new_heading(level=1,
                       text='CSS in HTML gefiltert für andere Formate')
        mf.new_paragraph(
            text='Dieses Beispiel zeigt, wie Sie eine CSS-Datei für HTML '
            'gefiltert haben, so dass sie nicht für andere Formate verfügbar '
            'ist.'
        )
        mf.new_paragraph(
            text='Die CSS-Datei liegt unter example/css/ und wird per '
            'relativem Pfad eingebunden (für lokale Anzeige). Die Ausgabe '
            'ist auf Deutsch; in HTML wird lang="de" im erzeugten <html>-Tag '
            'gesetzt. Für ODT wird sprache auch als "de" gesetzt. Für andere '
            'Formate wird die Sprache ignoriert.'
        )


if __name__ == '__main__':
    example_main(example_text='Filtering arguments for format',
                 function=filter_args_for_format_example)
