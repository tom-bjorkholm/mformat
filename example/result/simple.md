# Main heading of example

With start_paragraph we can start a paragraph. With add_text we can add text to the paragraph.

## Sub heading of example where add_text adds text to the sub heading

Whenever we start a new item type the previous item type is automatically closed. Add text does not automatically close the previous item type, instead it just adds text to that item. ***There is never a need to close an item type.***

## Heading with URL to [the example file](https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src/simple_complete.py)

As you can see, we can add URLs to both headings and paragraphs. It is also possible to add URLs to text, for instance the URL to the example file is added here. [The same example file](https://bitbucket.org/tom-bjorkholm/mformat/src/master/example/src/simple_complete.py)

URLs can (depending on the format) be formatted as clickable URLs or as text. To force URLs to be formatted as text, set url_as_text=True.

You may have noticed that we have not worried about about the whitespace between text. This is because we use a smart whitespace handling.If we disable smart whitespace handling,we need to handle whitespace manually,  which can be cumbersome as shown here.

## Bullet lists and numbered lists

- Item 1

- Item 2

  - Item 2.1

  - Item 2.2

- Item 3

1. Item 1

2. Item 2 with some more text. Naturally more text can be added in the same item using add_text.

3. Item 3

  1. Item 3.1

    - Item 3.1.1

    - Item 3.1.1

4. Item 4

## A simple table

| **Full Name** | **Street and Number** | **City or Town** |
|---------------|-----------------------|------------------|
| *John Doe*    | *123 Main St*         | *Anytown*        |
| Jane Doe      | 456 Main St           | Anytown          |
| Jim Doe       | 789 Main St           | The Village      |

### Another table

| **Name** | **Age** | **Gender** |
|----------|---------|------------|
| John Doe | 30      | Male       |
| Jane Doe | 25      | Female     |
| Jim Doe  | 35      | Male       |

## Finally code blocks

Code blocks are written with write_code_block.

````python
def my_function(x: int) -> int:
    return x + 1

print(my_function(1))
````
