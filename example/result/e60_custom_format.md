# Custom Format Example

This example demonstrates how to create and use a custom format in the mformat
framework. The same code can be used to write to different formats, just by
changing the format name.

## Features

- Easy to extend the framework

- Supports all standard document elements

- Format-agnostic API

1. First step: Create a format class

2. Second step: Implement required methods

3. Third step: Register the format

| **Element** | **Method**          |
|-------------|---------------------|
| Paragraph   | start_paragraph()   |
| Heading     | start_heading()     |
| List        | start_bullet_item() |


````python
def example():
    print("Hello, World!")
````

This text is **bold** and this is *italic* .

Visit [our website](https://example.com)
