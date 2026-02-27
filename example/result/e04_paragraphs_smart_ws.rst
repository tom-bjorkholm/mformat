With new_paragraph we can start a paragraph. Thanks to smart whitespace
handling, we do not need to add whitespace between text fragments from
different calls to add_text or new_paragraph calls. If we have extra
whitespace, it will be consolidated into a single space.

With new_paragraph we can start another paragraph. With smart_ws=False the
whitespace between text fragments will be preserved.So we can have no whitespae
or multiple spaces between text fragments if we want to. We can at any time
switch on smart whitespace handling by ommitting the smart_ws=False argument,
or by explicitly setting smart_ws=True.

**(As this example does not have a heading the generated markdown file will not
have a heading. If markdownlint is used on the generated markdown file it will
report an error for the missing heading.)**
