# This is the first heading, it is at level 1

## This is the second heading, it is at level 2

### This is the third heading, it is at level 3

We can add text to headings with add_text(), just as we can add text to
paragraphs. New headings can be added at any level. The argument smart_ws is
used to control how whitespace is handled in headings just as in paragraphs.

new_heading() also obeys the arguments bold and italic, just as in paragraphs.
However, they make less sense for headings. Explicitly setting bold or italic on
a heading may not produce the expected readability, as the heading has
formatting from the heading definition that is specific to the output format.

## The fourth heading is again at level 2
