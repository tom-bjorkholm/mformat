#! /usr/local/bin/python3
"""Example of using a CSS file and document language with HTML output."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf, OptArgs

# Raw Bitbucket URL for the example CSS file (used in <link href="...">).
CSS_RAW_URL = (
    'https://bitbucket.org/tom-bjorkholm/mformat/raw/master/example/css/'
    'e41_styles.css'
)


def use_css_in_html_example(format_name: str, file_name: str) -> None:
    """Show how to use a CSS file and set document language in HTML."""
    opt_args: OptArgs = None
    if format_name == 'html':
        # css_file and lang are HTML-only; pass via OptArgs to create_mf.
        opt_args = {
            'css_file': CSS_RAW_URL,
            'lang': 'de',
        }
    with create_mf(format_name=format_name, file_name=file_name,
                   args=opt_args) as mf:
        mf.start_heading(level=1, text='CSS und Sprache in HTML')
        mf.start_paragraph(
            text='Dieses Beispiel zeigt, wie Sie eine CSS-Datei und die '
            'Dokumentensprache (lang) mit mformat setzen. Übergeben Sie '
            'OptArgs mit "css_file" und "lang" an create_mf, wenn das '
            'Format HTML ist.'
        )
        mf.start_paragraph(
            text='Die CSS-Datei liegt unter example/css/ und wird per '
            'Raw-URL von Bitbucket eingebunden. Die Ausgabe ist auf '
            'Deutsch; lang="de" steht im erzeugten <html>-Tag.'
        )


if __name__ == '__main__':
    example_main(example_text='CSS and language in HTML',
                 function=use_css_in_html_example)
