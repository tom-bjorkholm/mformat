#! /usr/local/bin/python3
"""Example of using a CSS file and document language with HTML output."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from e01_paragraph import example_main
from mformat.factory import create_mf, OptArgs

# Relative path from result/ to example CSS; works when viewing HTML locally.
# Raw Bitbucket URL:
# https://github.com/tom-bjorkholm/mformat/blob/master/example/css/e41_styles.css  # noqa: E501
CSS_PATH = '../css/e41_styles.css'


def use_css_in_html_example(format_name: str, file_name: str) -> None:
    """Show how to use a CSS file and set document language in HTML."""
    opt_args: OptArgs = None
    if format_name == 'html':
        # css_file and lang are HTML-only; pass via OptArgs to create_mf.
        opt_args = {
            'css_file': CSS_PATH,
            'lang': 'de',
        }
    with create_mf(format_name=format_name, file_name=file_name,
                   args=opt_args) as mf:
        mf.new_heading(level=1, text='CSS und Sprache in HTML')
        mf.new_paragraph(
            text='Dieses Beispiel zeigt, wie Sie eine CSS-Datei und die '
            'Dokumentensprache (lang) mit mformat setzen. Übergeben Sie '
            'OptArgs mit "css_file" und "lang" an create_mf, wenn das '
            'Format HTML ist.'
        )
        mf.new_paragraph(
            text='Die CSS-Datei liegt unter example/css/ und wird per '
            'relativem Pfad eingebunden (für lokale Anzeige). Die Ausgabe '
            'ist auf Deutsch; lang="de" steht im erzeugten <html>-Tag.'
        )


if __name__ == '__main__':
    example_main(example_text='CSS and language in HTML',
                 function=use_css_in_html_example)
