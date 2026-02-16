# Table row by row with bold & italic example

| **City** | **Country** | **Size** |
|----------|-------------|----------|
| Mariehamn | Finland     | Small    |
| *Copenhagen* | *Denmark*   | *Large*  |
| ***Tokyo***  | ***Japan*** | ***Huge*** |

| *Capital* | *Country* | *Continent* |
|-----------|-----------|-------------|
| Oslo      | Norway    | Europe      |
| Tokyo     | Japan     | Asia        |
| **Berlin** | **Germany** | **Europe**  |
| Kairo      | Egypt       | Africa      |
| ***Brussels*** | ***Belgium*** | ***Europe*** |

Note: As the rows are added and written one by one, the library cannot know the
width of columns in future rows, this will make markdown formatted output look a
bit odd when reading the markdown file, however any further formatting from
markdown will hide this and make the table look as expected.
