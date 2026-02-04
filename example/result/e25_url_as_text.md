# URL in paragraph example

This is a paragraph with a URL: The examples are here.
https://bitbucket.org/tom-bjorkholm/mformat/src/master/example

The URL was added as a link using add_url(text, url)

By not specifying the text, the URL is shows as text:
https://bitbucket.org/tom-bjorkholm/mformat/src/master/example

A paragraph can of course have multiple URLs. The source code of the examples
are here. https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src and
The produced output files are here.
https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/result

The URLs are shown as text instead of clickable links. This might be useful when
you want to copy the URLs to the clipboard and paste them into another
application. This is done by passing the url_as_text argument to the create_mf
factory function.
