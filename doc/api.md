# Table of Contents

* [mformat.mformat\_lists\_impl](#mformat.mformat_lists_impl)
  * [PointListType](#mformat.mformat_lists_impl.PointListType)
  * [LevelFunc](#mformat.mformat_lists_impl.LevelFunc)
  * [PointStackItem](#mformat.mformat_lists_impl.PointStackItem)
  * [ListHandlerMixin](#mformat.mformat_lists_impl.ListHandlerMixin)
    * [\_\_init\_\_](#mformat.mformat_lists_impl.ListHandlerMixin.__init__)
* [mformat.mformat\_state](#mformat.mformat_state)
  * [MultiFormatState](#mformat.mformat_state.MultiFormatState)
  * [Formatting](#mformat.mformat_state.Formatting)
  * [FormattingWithWS](#mformat.mformat_state.FormattingWithWS)
* [mformat.mformat\_textbased](#mformat.mformat_textbased)
  * [split\_whitespace](#mformat.mformat_textbased.split_whitespace)
  * [MultiFormatTextBased](#mformat.mformat_textbased.MultiFormatTextBased)
    * [\_\_init\_\_](#mformat.mformat_textbased.MultiFormatTextBased.__init__)
    * [open](#mformat.mformat_textbased.MultiFormatTextBased.open)
* [mformat.factory](#mformat.factory)
  * [OptArgsDict](#mformat.factory.OptArgsDict)
  * [MultiFormatFactory](#mformat.factory.MultiFormatFactory)
    * [\_\_init\_\_](#mformat.factory.MultiFormatFactory.__init__)
    * [i\_get\_factory](#mformat.factory.MultiFormatFactory.i_get_factory)
    * [register](#mformat.factory.MultiFormatFactory.register)
    * [i\_register](#mformat.factory.MultiFormatFactory.i_register)
    * [create](#mformat.factory.MultiFormatFactory.create)
    * [i\_create](#mformat.factory.MultiFormatFactory.i_create)
    * [filter\_args](#mformat.factory.MultiFormatFactory.filter_args)
    * [i\_filter\_args](#mformat.factory.MultiFormatFactory.i_filter_args)
    * [get\_registered\_formats](#mformat.factory.MultiFormatFactory.get_registered_formats)
    * [i\_get\_registered\_formats](#mformat.factory.MultiFormatFactory.i_get_registered_formats)
    * [get\_usage](#mformat.factory.MultiFormatFactory.get_usage)
    * [i\_get\_usage](#mformat.factory.MultiFormatFactory.i_get_usage)
  * [create\_mf](#mformat.factory.create_mf)
  * [filter\_args\_mf](#mformat.factory.filter_args_mf)
  * [list\_registered\_mf](#mformat.factory.list_registered_mf)
  * [usage\_mf](#mformat.factory.usage_mf)
  * [register\_mf](#mformat.factory.register_mf)
* [mformat.mformat\_md](#mformat.mformat_md)
  * [MultiFormatMd](#mformat.mformat_md.MultiFormatMd)
    * [\_\_init\_\_](#mformat.mformat_md.MultiFormatMd.__init__)
    * [file\_name\_extension](#mformat.mformat_md.MultiFormatMd.file_name_extension)
    * [get\_arg\_desciption](#mformat.mformat_md.MultiFormatMd.get_arg_desciption)
* [mformat.mformat](#mformat.mformat)
  * [FormatterDescriptor](#mformat.mformat.FormatterDescriptor)
  * [TableInformation](#mformat.mformat.TableInformation)
    * [\_\_init\_\_](#mformat.mformat.TableInformation.__init__)
  * [MultiFormat](#mformat.mformat.MultiFormat)
    * [\_\_init\_\_](#mformat.mformat.MultiFormat.__init__)
    * [\_\_enter\_\_](#mformat.mformat.MultiFormat.__enter__)
    * [\_\_exit\_\_](#mformat.mformat.MultiFormat.__exit__)
    * [get\_arg\_desciption](#mformat.mformat.MultiFormat.get_arg_desciption)
    * [file\_name\_extension](#mformat.mformat.MultiFormat.file_name_extension)
    * [open](#mformat.mformat.MultiFormat.open)
    * [close](#mformat.mformat.MultiFormat.close)
    * [new\_heading](#mformat.mformat.MultiFormat.new_heading)
    * [new\_paragraph](#mformat.mformat.MultiFormat.new_paragraph)
    * [new\_block\_quote](#mformat.mformat.MultiFormat.new_block_quote)
    * [add\_text](#mformat.mformat.MultiFormat.add_text)
    * [add\_code\_in\_text](#mformat.mformat.MultiFormat.add_code_in_text)
    * [add\_url](#mformat.mformat.MultiFormat.add_url)
    * [new\_bullet\_item](#mformat.mformat.MultiFormat.new_bullet_item)
    * [new\_numbered\_point\_item](#mformat.mformat.MultiFormat.new_numbered_point_item)
    * [new\_table](#mformat.mformat.MultiFormat.new_table)
    * [add\_table\_row](#mformat.mformat.MultiFormat.add_table_row)
    * [write\_complete\_table](#mformat.mformat.MultiFormat.write_complete_table)
    * [write\_code\_block](#mformat.mformat.MultiFormat.write_code_block)
    * [file\_name\_with\_extension](#mformat.mformat.MultiFormat.file_name_with_extension)
    * [start\_paragraph](#mformat.mformat.MultiFormat.start_paragraph)
    * [start\_heading](#mformat.mformat.MultiFormat.start_heading)
    * [start\_bullet\_item](#mformat.mformat.MultiFormat.start_bullet_item)
    * [start\_numbered\_point\_item](#mformat.mformat.MultiFormat.start_numbered_point_item)
    * [start\_table](#mformat.mformat.MultiFormat.start_table)
* [mformat.mformat\_html](#mformat.mformat_html)
  * [MultiFormatHtml](#mformat.mformat_html.MultiFormatHtml)
    * [\_\_init\_\_](#mformat.mformat_html.MultiFormatHtml.__init__)
    * [file\_name\_extension](#mformat.mformat_html.MultiFormatHtml.file_name_extension)
    * [get\_arg\_desciption](#mformat.mformat_html.MultiFormatHtml.get_arg_desciption)
* [mformat.reg\_pkg\_formats](#mformat.reg_pkg_formats)
  * [register\_formats\_in\_pkg](#mformat.reg_pkg_formats.register_formats_in_pkg)
* [mformat\_ext.mformat\_odt](#mformat_ext.mformat_odt)
  * [OdtStyles](#mformat_ext.mformat_odt.OdtStyles)
  * [MultiFormatOdt](#mformat_ext.mformat_odt.MultiFormatOdt)
    * [\_\_init\_\_](#mformat_ext.mformat_odt.MultiFormatOdt.__init__)
    * [file\_name\_extension](#mformat_ext.mformat_odt.MultiFormatOdt.file_name_extension)
    * [get\_arg\_desciption](#mformat_ext.mformat_odt.MultiFormatOdt.get_arg_desciption)
    * [open](#mformat_ext.mformat_odt.MultiFormatOdt.open)
* [mformat\_ext.mformat\_docx](#mformat_ext.mformat_docx)
  * [MultiFormatDocx](#mformat_ext.mformat_docx.MultiFormatDocx)
    * [\_\_init\_\_](#mformat_ext.mformat_docx.MultiFormatDocx.__init__)
    * [file\_name\_extension](#mformat_ext.mformat_docx.MultiFormatDocx.file_name_extension)
    * [get\_arg\_desciption](#mformat_ext.mformat_docx.MultiFormatDocx.get_arg_desciption)
    * [open](#mformat_ext.mformat_docx.MultiFormatDocx.open)
* [mformat\_ext.reg\_extpkg\_formats](#mformat_ext.reg_extpkg_formats)
  * [register\_formats\_in\_ext\_pkg](#mformat_ext.reg_extpkg_formats.register_formats_in_ext_pkg)

<a id="mformat.mformat_lists_impl"></a>

# mformat.mformat\_lists\_impl

Mixin class providing list handling for MultiFormat.

<a id="mformat.mformat_lists_impl.PointListType"></a>

## PointListType Objects

```python
class PointListType(IntEnum)
```

Enum for the type of point list.

<a id="mformat.mformat_lists_impl.LevelFunc"></a>

## LevelFunc Objects

```python
class LevelFunc(Protocol)
```

Function that takes a level and returns None.

<a id="mformat.mformat_lists_impl.PointStackItem"></a>

## PointStackItem Objects

```python
class PointStackItem(TypedDict)
```

Item in the point list stack.

<a id="mformat.mformat_lists_impl.ListHandlerMixin"></a>

## ListHandlerMixin Objects

```python
class ListHandlerMixin()
```

Mixin providing list handling functionality for MultiFormat.

This mixin provides the implementation of the handling of bullet
and numbered lists. It accesses state variables (point_list_stack,
state, etc.) through self. The derived class must implement the
abstract methods, and MultiFormat must provide the start state
for self.state and the public methods new_bullet_item,
new_numbered_item.

The mixin defines:
- Internal state machine: _start_list_item_impl and helpers
- Abstract methods for derived classes to implement

<a id="mformat.mformat_lists_impl.ListHandlerMixin.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Initialize the ListHandlerMixin.

<a id="mformat.mformat_state"></a>

# mformat.mformat\_state

Enum for the state of the multi file format.

<a id="mformat.mformat_state.MultiFormatState"></a>

## MultiFormatState Objects

```python
class MultiFormatState(IntEnum)
```

Enum for the state of the multi file format.

<a id="mformat.mformat_state.Formatting"></a>

## Formatting Objects

```python
class Formatting(NamedTuple)
```

Formatting information.

<a id="mformat.mformat_state.FormattingWithWS"></a>

## FormattingWithWS Objects

```python
class FormattingWithWS(NamedTuple)
```

Formatting information with whitespace.

<a id="mformat.mformat_textbased"></a>

# mformat.mformat\_textbased

Base class for all text based format classes.

<a id="mformat.mformat_textbased.split_whitespace"></a>

#### split\_whitespace

```python
def split_whitespace(text: str) -> tuple[str, str, str]
```

Split a string into leading, stripped, and trailing whitespace.

<a id="mformat.mformat_textbased.MultiFormatTextBased"></a>

## MultiFormatTextBased Objects

```python
class MultiFormatTextBased(MultiFormat)
```

Base class for all text based format classes.

<a id="mformat.mformat_textbased.MultiFormatTextBased.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: str,
             url_as_text: bool = False,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the TextBasedFormat class.

**Arguments**:

- `file_name` - The name of the file to write to.
- `url_as_text` - Format URLs as text not clickable URLs.
- `file_exists_callback` - A callback function to call if the file
  already exists. Return to allow the file to
  be overwritten. Raise an exception to prevent
  the file from being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)

<a id="mformat.mformat_textbased.MultiFormatTextBased.open"></a>

#### open

```python
def open() -> None
```

Open the file.

Avoid using this method directly.
Use as a context manager instead, using a with statement.

<a id="mformat.factory"></a>

# mformat.factory

Factory class for creating MultiFormat instances.

<a id="mformat.factory.OptArgsDict"></a>

## OptArgsDict Objects

```python
class OptArgsDict(TypedDict)
```

Optional arguments for the MultiFormat constructor.

<a id="mformat.factory.MultiFormatFactory"></a>

## MultiFormatFactory Objects

```python
class MultiFormatFactory()
```

Factory class for creating instances of MultiFormat subclasses.

<a id="mformat.factory.MultiFormatFactory.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Initialize the factory with an empty registry.

<a id="mformat.factory.MultiFormatFactory.i_get_factory"></a>

#### i\_get\_factory

```python
@staticmethod
def i_get_factory() -> 'MultiFormatFactory'
```

Internally get the factory instance.

<a id="mformat.factory.MultiFormatFactory.register"></a>

#### register

```python
@staticmethod
def register(format_class: type[MultiFormat]) -> None
```

Register a MultiFormat subclass with the factory.

**Arguments**:

- `format_class` - The MultiFormat subclass to register.

**Raises**:

- `ValueError` - If the format_class is not a subclass of MultiFormat.
- `KeyError` - If the format_name is already registered.

<a id="mformat.factory.MultiFormatFactory.i_register"></a>

#### i\_register

```python
def i_register(format_class: type[MultiFormat]) -> None
```

Internally register a MultiFormat subclass with the factory.

<a id="mformat.factory.MultiFormatFactory.create"></a>

#### create

```python
@staticmethod
def create(format_name: str,
           file_name: str,
           url_as_text: bool = False,
           args: OptArgs = None) -> MultiFormat
```

Create an instance of a registered MultiFormat subclass.

**Arguments**:

- `format_name` - The name identifier of the format class to create.
- `file_name` - The file path to pass to the MultiFormat constructor.
- `url_as_text` - Format URLs as text not clickable URLs.
- `args` - additional arguments to pass to the MultiFormat constructor.

**Returns**:

  An instance of the requested MultiFormat subclass.
  Intended to be used as context manager, using a with statement.

**Raises**:

- `KeyError` - If the format_name is not registered.

<a id="mformat.factory.MultiFormatFactory.i_create"></a>

#### i\_create

```python
def i_create(format_name: str,
             file_name: str,
             url_as_text: bool = False,
             args: OptArgs = None) -> MultiFormat
```

Internally create an instance of a registered subclass.

<a id="mformat.factory.MultiFormatFactory.filter_args"></a>

#### filter\_args

```python
@staticmethod
def filter_args(args: OptArgs, format_name: str) -> OptArgs
```

Filter the arguments for a registered format.

Filter the arguments to only include the arguments that are valid for
the given format name. This is useful when the args dictionary
includes arguments for several formats, and not all of them are valid
for the given format name. (The risk of using this function is that
a misspelled arguement will be silently ignored, and the programming
error will not be detected.)

**Arguments**:

- `args` - The arguments to filter.
- `format_name` - The name identifier of the format class to filter
  the arguments for.

**Returns**:

  The filtered arguments.

**Raises**:

- `KeyError` - If the format_name is not registered.

<a id="mformat.factory.MultiFormatFactory.i_filter_args"></a>

#### i\_filter\_args

```python
def i_filter_args(args: OptArgs, format_name: str) -> OptArgs
```

Internally filter the arguments for a registered format.

<a id="mformat.factory.MultiFormatFactory.get_registered_formats"></a>

#### get\_registered\_formats

```python
@staticmethod
def get_registered_formats(lower: bool = False,
                           upper: bool = False) -> list[str]
```

Get a list of all registered format names.

Always includes the correct case for the format names in the returned
list. If lower or upper is True, also includes those cases of the
format names in the returned list. (Including lower case and upper
case variants is probably not a good idea when printint the list
for a human user, but it is useful when checking if a format name
is in the allowed list of format names.)

**Arguments**:

- `lower` - If True, also include the format name in lower case.
- `upper` - If True, also include the format name in upper case.

**Returns**:

  A list of registered format name strings.

<a id="mformat.factory.MultiFormatFactory.i_get_registered_formats"></a>

#### i\_get\_registered\_formats

```python
def i_get_registered_formats(lower: bool = False,
                             upper: bool = False) -> list[str]
```

Internally get a list of registered format names.

<a id="mformat.factory.MultiFormatFactory.get_usage"></a>

#### get\_usage

```python
@staticmethod
def get_usage(format_name: str) -> FormatterDescriptor
```

Get the usage information for a registered format.

**Arguments**:

- `format_name` - The name identifier of the format class to get
  the usage information for.

**Returns**:

  The usage information for the requested format.

**Raises**:

- `KeyError` - If the format_name is not registered.

<a id="mformat.factory.MultiFormatFactory.i_get_usage"></a>

#### i\_get\_usage

```python
def i_get_usage(format_name: str) -> FormatterDescriptor
```

Internally get the usage information for a registered format.

<a id="mformat.factory.create_mf"></a>

#### create\_mf

```python
def create_mf(format_name: str,
              file_name: str,
              url_as_text: bool = False,
              args: OptArgs = None) -> MultiFormat
```

Create an instance of a registered MultiFormat subclass.

Intended to be used as context manager, using a with statement.
This is a shortcut for MultiFormatFactory.create().

**Arguments**:

- `format_name` - The name identifier of the format class to create.
- `file_name` - The file path to pass to the MultiFormat constructor.
- `url_as_text` - Format URLs as text not clickable URLs.
- `args` - additional arguments to pass to the MultiFormat constructor.

**Returns**:

  An instance of the requested MultiFormat subclass.

**Raises**:

- `KeyError` - If the format_name is not registered.

<a id="mformat.factory.filter_args_mf"></a>

#### filter\_args\_mf

```python
def filter_args_mf(args: OptArgs, format_name: str) -> OptArgs
```

Filter the arguments for a registered format.

This is a shortcut for MultiFormatFactory.filter_args().
Filter the arguments to only include the arguments that are valid for
the given format name. This is useful when the args dictionary includes
arguments for several formats, and not all of them are valid for the given
format name. (The risk of using this function is that a misspelled
arguement will be silently ignored, and the programming error will not be
detected.)

**Arguments**:

- `args` - The arguments to filter.
- `format_name` - The name identifier of the format class to filter
  the arguments for.

**Returns**:

  The filtered arguments.

**Raises**:

- `KeyError` - If the format_name is not registered.

<a id="mformat.factory.list_registered_mf"></a>

#### list\_registered\_mf

```python
def list_registered_mf(lower: bool = False, upper: bool = False) -> list[str]
```

Get a list of all registered format names.

This is a shortcut for MultiFormatFactory.get_registered_formats().
Always includes the correct case for the format names in the returned
list. If lower or upper is True, also includes those cases of the
format names in the returned list. (Including lower case and upper
case variants is probably not a good idea when printint the list
for a human user, but it is useful when checking if a format name
is in the allowed list of format names.)

**Arguments**:

- `lower` - If True, also include the format name in lower case.
- `upper` - If True, also include the format name in upper case.

**Returns**:

  A list of registered format name strings.

<a id="mformat.factory.usage_mf"></a>

#### usage\_mf

```python
def usage_mf(format_name: str) -> FormatterDescriptor
```

Get the usage information for a registered format.

This is a shortcut for MultiFormatFactory.get_usage().

**Arguments**:

- `format_name` - The name identifier of the format class to get the
  usage information for.

**Returns**:

  The usage information for the requested format.

**Raises**:

- `KeyError` - If the format_name is not registered.

<a id="mformat.factory.register_mf"></a>

#### register\_mf

```python
def register_mf(format_class: type[MultiFormat]) -> None
```

Register a MultiFormat subclass with the factory.

This is a shortcut for MultiFormatFactory.register().

**Arguments**:

- `format_class` - The MultiFormat subclass to register.

**Raises**:

- `ValueError` - If the format_class is not a subclass of MultiFormat.
- `KeyError` - If the format_name is already registered.

<a id="mformat.mformat_md"></a>

# mformat.mformat\_md

Markdown format class.

<a id="mformat.mformat_md.MultiFormatMd"></a>

## MultiFormatMd Objects

```python
class MultiFormatMd(MultiFormatTextBased)
```

Markdown format class.

<a id="mformat.mformat_md.MultiFormatMd.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: str,
             url_as_text: bool = False,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the MdFormat class.

**Arguments**:

- `file_name` - The name of the file to write to.
- `url_as_text` - Format URLs as text not clickable URLs.
- `file_exists_callback` - A callback function to call if the file
  already exists. Return to allow the file to
  be overwritten. Raise an exception to prevent
  the file from being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)

<a id="mformat.mformat_md.MultiFormatMd.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension for the formatter.

<a id="mformat.mformat_md.MultiFormatMd.get_arg_desciption"></a>

#### get\_arg\_desciption

```python
@classmethod
def get_arg_desciption(cls) -> FormatterDescriptor
```

Get the description of the arguments for the formatter.

<a id="mformat.mformat"></a>

# mformat.mformat

Base class for all multi file format classes.

<a id="mformat.mformat.FormatterDescriptor"></a>

## FormatterDescriptor Objects

```python
class FormatterDescriptor(NamedTuple)
```

Descriptor for a formatter.

<a id="mformat.mformat.TableInformation"></a>

## TableInformation Objects

```python
class TableInformation()
```

Information about a table.

<a id="mformat.mformat.TableInformation.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Initialize the TableInformation class.

<a id="mformat.mformat.MultiFormat"></a>

## MultiFormat Objects

```python
class MultiFormat(ListHandlerMixin)
```

Base class for all multi file format classes.

<a id="mformat.mformat.MultiFormat.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: str,
             url_as_text: bool = False,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the MultiFormat class.

**Arguments**:

- `file_name` - The name of the file to write to.
- `url_as_text` - Format URLs as text not clickable URLs.
- `file_exists_callback` - A callback function to call if the file
  already exists. Return to allow the file to
  be overwritten. Raise an exception to
  prevent the file from being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)

<a id="mformat.mformat.MultiFormat.__enter__"></a>

#### \_\_enter\_\_

```python
def __enter__() -> 'MultiFormat'
```

Enter the context manager.

<a id="mformat.mformat.MultiFormat.__exit__"></a>

#### \_\_exit\_\_

```python
def __exit__(exc_type: type[BaseException] | None,
             exc_value: BaseException | None,
             traceback: TracebackType | None) -> bool
```

Exit the context manager.

**Arguments**:

- `exc_type` - The type of the exception.
- `exc_value` - The value of the exception.
- `traceback` - The traceback of the exception.

**Returns**:

  True if the exception was handled, False otherwise.

<a id="mformat.mformat.MultiFormat.get_arg_desciption"></a>

#### get\_arg\_desciption

```python
@classmethod
def get_arg_desciption(cls) -> FormatterDescriptor
```

Get the description of the arguments for the formatter.

Must be overridden by subclasses.

<a id="mformat.mformat.MultiFormat.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension for the formatter.

Must be overridden by subclasses.

<a id="mformat.mformat.MultiFormat.open"></a>

#### open

```python
def open() -> None
```

Open the file.

Avoid using this method directly.
Use MultiFormat as a context manager instead, using a with statement.

<a id="mformat.mformat.MultiFormat.close"></a>

#### close

```python
def close() -> None
```

Close the file.

Avoid using this method directly.
Use MultiFormat as a context manager instead, using a with statement.

<a id="mformat.mformat.MultiFormat.new_heading"></a>

#### new\_heading

```python
def new_heading(level: int,
                text: str,
                smart_ws: bool = True,
                bold: bool = False,
                italic: bool = False) -> None
```

Start a new heading.

**Arguments**:

- `level` - The level of the heading.
- `text` - The text to write in the heading.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  new_heading or add_text).
- `bold` - If True, the text is bold.
  Recommended to leave False for headings as it will be
  formatted as a heading.
- `italic` - If True, the text is italic.
  Recommended to leave False for headings as it will be
  formatted as a heading.

<a id="mformat.mformat.MultiFormat.new_paragraph"></a>

#### new\_paragraph

```python
def new_paragraph(text: str,
                  smart_ws: bool = True,
                  bold: bool = False,
                  italic: bool = False) -> None
```

Start a new paragraph.

**Arguments**:

- `text` - The text to write in the paragraph.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  new_paragraph or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.new_block_quote"></a>

#### new\_block\_quote

```python
def new_block_quote(text: str,
                    smart_ws: bool = True,
                    bold: bool = False,
                    italic: bool = False) -> None
```

Start a new block quote.

Start a new block quote with the given text and formatting.
Additional text can be added into the block quote with add_text,
add_code_in_text, add_url, etc.

Block quotes cannot be nested. If called while already in a block
quote, the current block quote is ended and a new one is started.

**Arguments**:

- `text` - The text to write in the block quote.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  new_block_quote or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.add_text"></a>

#### add\_text

```python
def add_text(text: str,
             smart_ws: bool = True,
             bold: bool = False,
             italic: bool = False) -> None
```

Add text to the current item (paragraph, bullet list item, etc.).

**Arguments**:

- `text` - The text to add to the current item.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  new_paragraph, new_bullet_item, ... or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.add_code_in_text"></a>

#### add\_code\_in\_text

```python
def add_code_in_text(text: str, smart_ws: bool = True) -> None
```

Add single or few words of code in the current text item.

This is used to add a function name, a variable name,
formattten as code into the current text item (paragraph,
bullet list item, etc.). This cannot be used to add lines of code,
use write_code_block for that.

**Arguments**:

- `text` - The text to add to the current item.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  add_code_in_text or add_text).

<a id="mformat.mformat.MultiFormat.add_url"></a>

#### add\_url

```python
def add_url(url: str,
            text: Optional[str] = None,
            smart_ws: bool = True,
            bold: bool = False,
            italic: bool = False) -> None
```

Add a URL to the current item (paragraph, bullet list item, etc.).

**Arguments**:

- `url` - The URL to add to the current item.
- `text` - The text to add to the current item.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  add_url or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.new_bullet_item"></a>

#### new\_bullet\_item

```python
def new_bullet_item(text: str,
                    level: Optional[int] = None,
                    smart_ws: bool = True,
                    bold: bool = False,
                    italic: bool = False) -> None
```

Start a new bullet list item and a new bullet list if needed.

If level is not provided, the item is added to the current list.
If level is not provided and there is no current bullet list, a new
bullet list is started.
If level is provided and it is one greater than the current level, a
new bullet list is started.
If level is provided and it is less than the current level, one or
several lists are ended to get to the level specified.
If level is provided and it is equal to the current level, the item is
added to the current bullet list item.
If level is provided and it is more than one greater than the current
level, an error is raised.
If level is provided and and the list at that level is not a bullet
list, the list at that level is ended and a new bullet list is started.

**Arguments**:

- `text` - The text to write in the bullet list item.
- `level` - The level of the bullet list item.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  new_bullet_item or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.new_numbered_point_item"></a>

#### new\_numbered\_point\_item

```python
def new_numbered_point_item(text: str,
                            level: Optional[int] = None,
                            smart_ws: bool = True,
                            bold: bool = False,
                            italic: bool = False) -> None
```

Start a new numbered point list item and a new list if needed.

If level is not provided, the item is added to the current list.
If level is not provided and there is no current numbered point list,
a new numbered point list is started.
If level is provided and it is one greater than the current level, a
new numbered point list is started.
If level is provided and it is less than the current level, one or
several lists are ended to get to the level specified.
If level is provided and it is equal to the current level, the item is
added to the current numbered point list item.
If level is provided and it is more than one greater than the current
level, an error is raised.
If level is provided and and the list at that level is not a numbered
point list, the list at that level is ended and a new numbered point
list is started.

**Arguments**:

- `text` - The text to write in the numbered point list item.
- `level` - The level of the numbered point list item.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  new_numbered_point_item or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.new_table"></a>

#### new\_table

```python
def new_table(first_row: list[str],
              bold: bool = False,
              italic: bool = False) -> None
```

Start a new table.

**Arguments**:

- `first_row` - The first row of the table.
- `bold` - If True, the text in each cell in first row is bold.
- `italic` - If True, the text in each cell in first row is italic.

<a id="mformat.mformat.MultiFormat.add_table_row"></a>

#### add\_table\_row

```python
def add_table_row(row: list[str],
                  bold: bool = False,
                  italic: bool = False) -> None
```

Add a row to the table.

**Arguments**:

- `row` - The row to add to the table.
- `formatting` - The formatting of the text in each cell in row.

<a id="mformat.mformat.MultiFormat.write_complete_table"></a>

#### write\_complete\_table

```python
def write_complete_table(table: list[list[str]],
                         bold_first_row: bool = False,
                         italic_first_row: bool = False) -> None
```

Add a complete table.

Result is same as calling new_table followed by add_table_row
for each row. Args:
table: The complete table to add.
formatting_first_row: The formatting of the text in each
cell in first row.

<a id="mformat.mformat.MultiFormat.write_code_block"></a>

#### write\_code\_block

```python
def write_code_block(text: str,
                     programming_language: Optional[str] = None) -> None
```

Add a code block.

Write a text block verbatim into the document. Trying to keep all
aspects of the text block, including whitespace, line breaks, etc.
The text block is ended with a line break.
Depending on the actual document format, the text block may be
formatted as a code block or as a verbatim text block.

**Arguments**:

- `text` - The text to add to the code block.
- `programming_language` - The programming language of the code block.
  Depending on the actual document format,
  this may be ignored or used to syntax
  highlight the code block.

<a id="mformat.mformat.MultiFormat.file_name_with_extension"></a>

#### file\_name\_with\_extension

```python
@staticmethod
def file_name_with_extension(file_name: str, extension: str) -> str
```

Get the file name with the extension.

<a id="mformat.mformat.MultiFormat.start_paragraph"></a>

#### start\_paragraph

```python
def start_paragraph(text: str,
                    smart_ws: bool = True,
                    bold: bool = False,
                    italic: bool = False) -> None
```

Start a new paragraph (deprecated).

.. deprecated:: 0.3.0
  Use :meth:`new_paragraph` instead.

<a id="mformat.mformat.MultiFormat.start_heading"></a>

#### start\_heading

```python
def start_heading(level: int,
                  text: str,
                  smart_ws: bool = True,
                  bold: bool = False,
                  italic: bool = False) -> None
```

Start a new heading (deprecated).

.. deprecated:: 0.3.0
  Use :meth:`new_heading` instead.

<a id="mformat.mformat.MultiFormat.start_bullet_item"></a>

#### start\_bullet\_item

```python
def start_bullet_item(text: str,
                      level: Optional[int] = None,
                      smart_ws: bool = True,
                      bold: bool = False,
                      italic: bool = False) -> None
```

Start a bullet item (deprecated).

.. deprecated:: 0.3.0
  Use :meth:`new_bullet_item` instead.

<a id="mformat.mformat.MultiFormat.start_numbered_point_item"></a>

#### start\_numbered\_point\_item

```python
def start_numbered_point_item(text: str,
                              level: Optional[int] = None,
                              smart_ws: bool = True,
                              bold: bool = False,
                              italic: bool = False) -> None
```

Start a numbered point item (deprecated).

.. deprecated:: 0.3.0
  Use :meth:`new_numbered_point_item` instead.

<a id="mformat.mformat.MultiFormat.start_table"></a>

#### start\_table

```python
def start_table(first_row: list[str],
                bold: bool = False,
                italic: bool = False) -> None
```

Start a table (deprecated).

.. deprecated:: 0.3.0
  Use :meth:`new_table` instead.

<a id="mformat.mformat_html"></a>

# mformat.mformat\_html

HTML format class.

<a id="mformat.mformat_html.MultiFormatHtml"></a>

## MultiFormatHtml Objects

```python
class MultiFormatHtml(MultiFormatTextBased)
```

HTML format class.

<a id="mformat.mformat_html.MultiFormatHtml.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: str,
             url_as_text: bool = False,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             title: str = 'HTML file',
             css_file: Optional[str] = None,
             lang: str = 'en')
```

Initialize the HtmlFormat class.

**Arguments**:

- `file_name` - The name of the file to write to.
- `url_as_text` - Format URLs as text not clickable URLs.
- `file_exists_callback` - A callback function to call if the file
  already exists. Return to allow the file to
  be overwritten. Raise an exception to prevent
  the file from being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)
- `title` - The title of the HTML file.
- `css_file` - The name of the CSS file to use.
- `lang` - The language of the HTML file.

<a id="mformat.mformat_html.MultiFormatHtml.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension for the formatter.

<a id="mformat.mformat_html.MultiFormatHtml.get_arg_desciption"></a>

#### get\_arg\_desciption

```python
@classmethod
def get_arg_desciption(cls) -> FormatterDescriptor
```

Get the description of the arguments for the formatter.

<a id="mformat.reg_pkg_formats"></a>

# mformat.reg\_pkg\_formats

Register the formats defined in the package with the factory.

<a id="mformat.reg_pkg_formats.register_formats_in_pkg"></a>

#### register\_formats\_in\_pkg

```python
def register_formats_in_pkg() -> list[type[MultiFormat]]
```

Get formats defined in the package to register with the factory.

<a id="mformat_ext.mformat_odt"></a>

# mformat\_ext.mformat\_odt

Extension of the MultiFormat class for DOCX files.

<a id="mformat_ext.mformat_odt.OdtStyles"></a>

## OdtStyles Objects

```python
class OdtStyles(NamedTuple)
```

Styles for ODT files.

<a id="mformat_ext.mformat_odt.MultiFormatOdt"></a>

## MultiFormatOdt Objects

```python
class MultiFormatOdt(MultiFormat)
```

Extension of the MultiFormat class for ODT files.

<a id="mformat_ext.mformat_odt.MultiFormatOdt.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: str,
             url_as_text: bool = False,
             file_exists_callback: Optional[Callable[[str], None]] = None,
             lang: str = 'en-UK')
```

Initialize the MultiFormatOdt class.

**Arguments**:

- `file_name` - The name of the file to write to.
- `url_as_text` - Format URLs as text not clickable URLs.
- `file_exists_callback` - A callback function to call if the file
  already exists. Return to allow the file to
  be overwritten. Raise an exception to prevent
  the file from being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)
- `lang` - The language of the document.

<a id="mformat_ext.mformat_odt.MultiFormatOdt.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension for the formatter.

<a id="mformat_ext.mformat_odt.MultiFormatOdt.get_arg_desciption"></a>

#### get\_arg\_desciption

```python
@classmethod
def get_arg_desciption(cls) -> FormatterDescriptor
```

Get the description of the arguments for the formatter.

<a id="mformat_ext.mformat_odt.MultiFormatOdt.open"></a>

#### open

```python
def open() -> None
```

Open the file.

Avoid using this method directly.
Use as a context manager instead, using a with statement.

<a id="mformat_ext.mformat_docx"></a>

# mformat\_ext.mformat\_docx

Extension of the MultiFormat class for DOCX files.

<a id="mformat_ext.mformat_docx.MultiFormatDocx"></a>

## MultiFormatDocx Objects

```python
class MultiFormatDocx(MultiFormat)
```

Extension of the MultiFormat class for DOCX files.

<a id="mformat_ext.mformat_docx.MultiFormatDocx.__init__"></a>

#### \_\_init\_\_

```python
def __init__(file_name: str,
             url_as_text: bool = False,
             file_exists_callback: Optional[Callable[[str], None]] = None)
```

Initialize the MultiFormatDocx class.

**Arguments**:

- `file_name` - The name of the file to write to.
- `url_as_text` - Format URLs as text not clickable URLs.
- `file_exists_callback` - A callback function to call if the file
  already exists. Return to allow the file to
  be overwritten. Raise an exception to prevent
  the file from being overwritten.
  (May for instance save existing file as
  backup.)
  (Default is to raise an exception.)

<a id="mformat_ext.mformat_docx.MultiFormatDocx.file_name_extension"></a>

#### file\_name\_extension

```python
@classmethod
def file_name_extension(cls) -> str
```

Get the file name extension for the formatter.

<a id="mformat_ext.mformat_docx.MultiFormatDocx.get_arg_desciption"></a>

#### get\_arg\_desciption

```python
@classmethod
def get_arg_desciption(cls) -> FormatterDescriptor
```

Get the description of the arguments for the formatter.

<a id="mformat_ext.mformat_docx.MultiFormatDocx.open"></a>

#### open

```python
def open() -> None
```

Open the file.

Avoid using this method directly.
Use as a context manager instead, using a with statement.

<a id="mformat_ext.reg_extpkg_formats"></a>

# mformat\_ext.reg\_extpkg\_formats

Register the formats defined in the ext package with the factory.

<a id="mformat_ext.reg_extpkg_formats.register_formats_in_ext_pkg"></a>

#### register\_formats\_in\_ext\_pkg

```python
def register_formats_in_ext_pkg() -> list[type[MultiFormat]]
```

Get formats defined in the ext package to register with the factory.

