# Table of Contents

* [mformat.mformat\_lists\_impl](#mformat.mformat_lists_impl)
  * [PointListType](#mformat.mformat_lists_impl.PointListType)
  * [LevelFunc](#mformat.mformat_lists_impl.LevelFunc)
  * [PointStackItem](#mformat.mformat_lists_impl.PointStackItem)
  * [ListHandlerMixin](#mformat.mformat_lists_impl.ListHandlerMixin)
    * [\_\_init\_\_](#mformat.mformat_lists_impl.ListHandlerMixin.__init__)
    * [\_start\_list\_item\_impl](#mformat.mformat_lists_impl.ListHandlerMixin._start_list_item_impl)
    * [\_validate\_list\_level](#mformat.mformat_lists_impl.ListHandlerMixin._validate_list_level)
    * [\_adjust\_to\_list\_level](#mformat.mformat_lists_impl.ListHandlerMixin._adjust_to_list_level)
    * [\_end\_item\_before\_nesting](#mformat.mformat_lists_impl.ListHandlerMixin._end_item_before_nesting)
    * [\_push\_and\_start\_list](#mformat.mformat_lists_impl.ListHandlerMixin._push_and_start_list)
    * [\_start\_item\_in\_list](#mformat.mformat_lists_impl.ListHandlerMixin._start_item_in_list)
    * [\_full\_number\_of\_list\_item](#mformat.mformat_lists_impl.ListHandlerMixin._full_number_of_list_item)
    * [\_decrease\_list\_depth](#mformat.mformat_lists_impl.ListHandlerMixin._decrease_list_depth)
    * [\_end\_wrong\_list\_type\_at\_lev](#mformat.mformat_lists_impl.ListHandlerMixin._end_wrong_list_type_at_lev)
    * [\_increase\_list\_depth](#mformat.mformat_lists_impl.ListHandlerMixin._increase_list_depth)
    * [\_get\_states\_of\_pltype](#mformat.mformat_lists_impl.ListHandlerMixin._get_states_of_pltype)
    * [\_get\_point\_list\_type\_name](#mformat.mformat_lists_impl.ListHandlerMixin._get_point_list_type_name)
    * [\_is\_in\_list\_state](#mformat.mformat_lists_impl.ListHandlerMixin._is_in_list_state)
    * [\_is\_in\_list\_item\_state](#mformat.mformat_lists_impl.ListHandlerMixin._is_in_list_item_state)
    * [\_dispatch\_start\_list](#mformat.mformat_lists_impl.ListHandlerMixin._dispatch_start_list)
    * [\_dispatch\_end\_list](#mformat.mformat_lists_impl.ListHandlerMixin._dispatch_end_list)
    * [\_dispatch\_start\_item](#mformat.mformat_lists_impl.ListHandlerMixin._dispatch_start_item)
    * [\_dispatch\_end\_item](#mformat.mformat_lists_impl.ListHandlerMixin._dispatch_end_item)
    * [\_state\_from\_point\_list](#mformat.mformat_lists_impl.ListHandlerMixin._state_from_point_list)
    * [\_end\_list\_state](#mformat.mformat_lists_impl.ListHandlerMixin._end_list_state)
    * [\_end\_state](#mformat.mformat_lists_impl.ListHandlerMixin._end_state)
    * [\_to\_write](#mformat.mformat_lists_impl.ListHandlerMixin._to_write)
    * [\_write\_text](#mformat.mformat_lists_impl.ListHandlerMixin._write_text)
    * [\_start\_bullet\_list](#mformat.mformat_lists_impl.ListHandlerMixin._start_bullet_list)
    * [\_end\_bullet\_list](#mformat.mformat_lists_impl.ListHandlerMixin._end_bullet_list)
    * [\_start\_bullet\_item](#mformat.mformat_lists_impl.ListHandlerMixin._start_bullet_item)
    * [\_end\_bullet\_item](#mformat.mformat_lists_impl.ListHandlerMixin._end_bullet_item)
    * [\_start\_numbered\_list](#mformat.mformat_lists_impl.ListHandlerMixin._start_numbered_list)
    * [\_end\_numbered\_list](#mformat.mformat_lists_impl.ListHandlerMixin._end_numbered_list)
    * [\_start\_numbered\_item](#mformat.mformat_lists_impl.ListHandlerMixin._start_numbered_item)
    * [\_end\_numbered\_item](#mformat.mformat_lists_impl.ListHandlerMixin._end_numbered_item)
* [mformat.mformat\_state](#mformat.mformat_state)
  * [MultiFormatState](#mformat.mformat_state.MultiFormatState)
  * [Formatting](#mformat.mformat_state.Formatting)
  * [FormattingWithWS](#mformat.mformat_state.FormattingWithWS)
* [mformat.mformat\_textbased](#mformat.mformat_textbased)
  * [MultiFormatTextBased](#mformat.mformat_textbased.MultiFormatTextBased)
    * [\_\_init\_\_](#mformat.mformat_textbased.MultiFormatTextBased.__init__)
    * [open](#mformat.mformat_textbased.MultiFormatTextBased.open)
    * [\_close](#mformat.mformat_textbased.MultiFormatTextBased._close)
    * [\_get\_last\_chars\_written](#mformat.mformat_textbased.MultiFormatTextBased._get_last_chars_written)
* [mformat.factory](#mformat.factory)
  * [\_the\_factory](#mformat.factory._the_factory)
  * [OptArgsDict](#mformat.factory.OptArgsDict)
  * [MultiFormatFactory](#mformat.factory.MultiFormatFactory)
    * [\_\_init\_\_](#mformat.factory.MultiFormatFactory.__init__)
    * [i\_get\_factory](#mformat.factory.MultiFormatFactory.i_get_factory)
    * [register](#mformat.factory.MultiFormatFactory.register)
    * [i\_register](#mformat.factory.MultiFormatFactory.i_register)
    * [create](#mformat.factory.MultiFormatFactory.create)
    * [i\_create](#mformat.factory.MultiFormatFactory.i_create)
    * [get\_registered\_formats](#mformat.factory.MultiFormatFactory.get_registered_formats)
    * [i\_get\_registered\_formats](#mformat.factory.MultiFormatFactory.i_get_registered_formats)
    * [get\_usage](#mformat.factory.MultiFormatFactory.get_usage)
    * [i\_get\_usage](#mformat.factory.MultiFormatFactory.i_get_usage)
  * [create\_mf](#mformat.factory.create_mf)
  * [list\_registered\_mf](#mformat.factory.list_registered_mf)
  * [usage\_mf](#mformat.factory.usage_mf)
  * [register\_mf](#mformat.factory.register_mf)
* [mformat.mformat\_md](#mformat.mformat_md)
  * [split\_whitespace](#mformat.mformat_md.split_whitespace)
  * [MultiFormatMd](#mformat.mformat_md.MultiFormatMd)
    * [\_\_init\_\_](#mformat.mformat_md.MultiFormatMd.__init__)
    * [file\_name\_extension](#mformat.mformat_md.MultiFormatMd.file_name_extension)
    * [get\_arg\_desciption](#mformat.mformat_md.MultiFormatMd.get_arg_desciption)
    * [\_write\_file\_prefix](#mformat.mformat_md.MultiFormatMd._write_file_prefix)
    * [\_write\_file\_suffix](#mformat.mformat_md.MultiFormatMd._write_file_suffix)
    * [\_start\_paragraph](#mformat.mformat_md.MultiFormatMd._start_paragraph)
    * [\_end\_paragraph](#mformat.mformat_md.MultiFormatMd._end_paragraph)
    * [\_empty\_line\_before](#mformat.mformat_md.MultiFormatMd._empty_line_before)
    * [\_start\_heading](#mformat.mformat_md.MultiFormatMd._start_heading)
    * [\_end\_heading](#mformat.mformat_md.MultiFormatMd._end_heading)
    * [\_format\_text](#mformat.mformat_md.MultiFormatMd._format_text)
    * [\_write\_text](#mformat.mformat_md.MultiFormatMd._write_text)
    * [\_write\_url](#mformat.mformat_md.MultiFormatMd._write_url)
    * [\_start\_bullet\_list](#mformat.mformat_md.MultiFormatMd._start_bullet_list)
    * [\_end\_bullet\_list](#mformat.mformat_md.MultiFormatMd._end_bullet_list)
    * [\_indent](#mformat.mformat_md.MultiFormatMd._indent)
    * [\_start\_bullet\_item](#mformat.mformat_md.MultiFormatMd._start_bullet_item)
    * [\_end\_bullet\_item](#mformat.mformat_md.MultiFormatMd._end_bullet_item)
    * [\_start\_numbered\_list](#mformat.mformat_md.MultiFormatMd._start_numbered_list)
    * [\_end\_numbered\_list](#mformat.mformat_md.MultiFormatMd._end_numbered_list)
    * [\_start\_numbered\_item](#mformat.mformat_md.MultiFormatMd._start_numbered_item)
    * [\_end\_numbered\_item](#mformat.mformat_md.MultiFormatMd._end_numbered_item)
    * [\_start\_code\_block](#mformat.mformat_md.MultiFormatMd._start_code_block)
    * [\_end\_code\_block](#mformat.mformat_md.MultiFormatMd._end_code_block)
    * [\_write\_code\_block](#mformat.mformat_md.MultiFormatMd._write_code_block)
    * [\_start\_table](#mformat.mformat_md.MultiFormatMd._start_table)
    * [\_end\_table](#mformat.mformat_md.MultiFormatMd._end_table)
    * [\_write\_table\_first\_row](#mformat.mformat_md.MultiFormatMd._write_table_first_row)
    * [\_write\_table\_row](#mformat.mformat_md.MultiFormatMd._write_table_row)
    * [\_encode\_text](#mformat.mformat_md.MultiFormatMd._encode_text)
    * [\_escape\_char](#mformat.mformat_md.MultiFormatMd._escape_char)
    * [\_escape\_line\_context\_char](#mformat.mformat_md.MultiFormatMd._escape_line_context_char)
    * [\_escape\_greater\_than](#mformat.mformat_md.MultiFormatMd._escape_greater_than)
    * [\_escape\_list\_marker](#mformat.mformat_md.MultiFormatMd._escape_list_marker)
    * [\_escape\_emphasis](#mformat.mformat_md.MultiFormatMd._escape_emphasis)
    * [\_escape\_equals](#mformat.mformat_md.MultiFormatMd._escape_equals)
    * [\_is\_emphasis\_position](#mformat.mformat_md.MultiFormatMd._is_emphasis_position)
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
    * [start\_heading](#mformat.mformat.MultiFormat.start_heading)
    * [start\_paragraph](#mformat.mformat.MultiFormat.start_paragraph)
    * [add\_text](#mformat.mformat.MultiFormat.add_text)
    * [add\_url](#mformat.mformat.MultiFormat.add_url)
    * [start\_bullet\_item](#mformat.mformat.MultiFormat.start_bullet_item)
    * [start\_numbered\_point\_item](#mformat.mformat.MultiFormat.start_numbered_point_item)
    * [start\_table](#mformat.mformat.MultiFormat.start_table)
    * [add\_table\_row](#mformat.mformat.MultiFormat.add_table_row)
    * [write\_complete\_table](#mformat.mformat.MultiFormat.write_complete_table)
    * [write\_code\_block](#mformat.mformat.MultiFormat.write_code_block)
    * [\_close](#mformat.mformat.MultiFormat._close)
    * [\_write\_file\_prefix](#mformat.mformat.MultiFormat._write_file_prefix)
    * [\_write\_file\_suffix](#mformat.mformat.MultiFormat._write_file_suffix)
    * [\_end\_state](#mformat.mformat.MultiFormat._end_state)
    * [\_start\_paragraph](#mformat.mformat.MultiFormat._start_paragraph)
    * [\_end\_paragraph](#mformat.mformat.MultiFormat._end_paragraph)
    * [\_start\_heading](#mformat.mformat.MultiFormat._start_heading)
    * [\_end\_heading](#mformat.mformat.MultiFormat._end_heading)
    * [\_write\_text](#mformat.mformat.MultiFormat._write_text)
    * [\_write\_url](#mformat.mformat.MultiFormat._write_url)
    * [file\_name\_with\_extension](#mformat.mformat.MultiFormat.file_name_with_extension)
    * [\_must\_be\_overridden](#mformat.mformat.MultiFormat._must_be_overridden)
    * [\_file\_exists\_check](#mformat.mformat.MultiFormat._file_exists_check)
    * [\_to\_write\_optional](#mformat.mformat.MultiFormat._to_write_optional)
    * [\_to\_write](#mformat.mformat.MultiFormat._to_write)
    * [\_start\_bullet\_list](#mformat.mformat.MultiFormat._start_bullet_list)
    * [\_end\_bullet\_list](#mformat.mformat.MultiFormat._end_bullet_list)
    * [\_start\_bullet\_item](#mformat.mformat.MultiFormat._start_bullet_item)
    * [\_end\_bullet\_item](#mformat.mformat.MultiFormat._end_bullet_item)
    * [\_start\_numbered\_list](#mformat.mformat.MultiFormat._start_numbered_list)
    * [\_end\_numbered\_list](#mformat.mformat.MultiFormat._end_numbered_list)
    * [\_start\_numbered\_item](#mformat.mformat.MultiFormat._start_numbered_item)
    * [\_end\_numbered\_item](#mformat.mformat.MultiFormat._end_numbered_item)
    * [\_update\_table\_column\_widths](#mformat.mformat.MultiFormat._update_table_column_widths)
    * [\_start\_table](#mformat.mformat.MultiFormat._start_table)
    * [\_end\_table](#mformat.mformat.MultiFormat._end_table)
    * [\_write\_table\_first\_row](#mformat.mformat.MultiFormat._write_table_first_row)
    * [\_write\_table\_row](#mformat.mformat.MultiFormat._write_table_row)
    * [\_start\_code\_block](#mformat.mformat.MultiFormat._start_code_block)
    * [\_end\_code\_block](#mformat.mformat.MultiFormat._end_code_block)
    * [\_write\_code\_block](#mformat.mformat.MultiFormat._write_code_block)
    * [\_encode\_text](#mformat.mformat.MultiFormat._encode_text)
    * [\_encode\_table\_row](#mformat.mformat.MultiFormat._encode_table_row)
* [mformat.mformat\_html](#mformat.mformat_html)
  * [MultiFormatHtml](#mformat.mformat_html.MultiFormatHtml)
    * [\_\_init\_\_](#mformat.mformat_html.MultiFormatHtml.__init__)
    * [file\_name\_extension](#mformat.mformat_html.MultiFormatHtml.file_name_extension)
    * [get\_arg\_desciption](#mformat.mformat_html.MultiFormatHtml.get_arg_desciption)
    * [\_write\_file\_prefix](#mformat.mformat_html.MultiFormatHtml._write_file_prefix)
    * [\_write\_file\_suffix](#mformat.mformat_html.MultiFormatHtml._write_file_suffix)
    * [\_start\_paragraph](#mformat.mformat_html.MultiFormatHtml._start_paragraph)
    * [\_end\_paragraph](#mformat.mformat_html.MultiFormatHtml._end_paragraph)
    * [\_start\_heading](#mformat.mformat_html.MultiFormatHtml._start_heading)
    * [\_end\_heading](#mformat.mformat_html.MultiFormatHtml._end_heading)
    * [\_write\_text](#mformat.mformat_html.MultiFormatHtml._write_text)
    * [\_write\_url](#mformat.mformat_html.MultiFormatHtml._write_url)
    * [\_start\_bullet\_list](#mformat.mformat_html.MultiFormatHtml._start_bullet_list)
    * [\_end\_bullet\_list](#mformat.mformat_html.MultiFormatHtml._end_bullet_list)
    * [\_start\_bullet\_item](#mformat.mformat_html.MultiFormatHtml._start_bullet_item)
    * [\_end\_bullet\_item](#mformat.mformat_html.MultiFormatHtml._end_bullet_item)
    * [\_start\_numbered\_list](#mformat.mformat_html.MultiFormatHtml._start_numbered_list)
    * [\_end\_numbered\_list](#mformat.mformat_html.MultiFormatHtml._end_numbered_list)
    * [\_start\_numbered\_item](#mformat.mformat_html.MultiFormatHtml._start_numbered_item)
    * [\_end\_numbered\_item](#mformat.mformat_html.MultiFormatHtml._end_numbered_item)
    * [\_start\_table](#mformat.mformat_html.MultiFormatHtml._start_table)
    * [\_end\_table](#mformat.mformat_html.MultiFormatHtml._end_table)
    * [\_write\_table\_first\_row](#mformat.mformat_html.MultiFormatHtml._write_table_first_row)
    * [\_write\_table\_row](#mformat.mformat_html.MultiFormatHtml._write_table_row)
    * [\_start\_code\_block](#mformat.mformat_html.MultiFormatHtml._start_code_block)
    * [\_end\_code\_block](#mformat.mformat_html.MultiFormatHtml._end_code_block)
    * [\_write\_code\_block](#mformat.mformat_html.MultiFormatHtml._write_code_block)
    * [\_encode\_text](#mformat.mformat_html.MultiFormatHtml._encode_text)
* [mformat.reg\_pkg\_formats](#mformat.reg_pkg_formats)
  * [register\_formats\_in\_pkg](#mformat.reg_pkg_formats.register_formats_in_pkg)
* [mformat\_ext.mformat\_odt](#mformat_ext.mformat_odt)
  * [OdtStyles](#mformat_ext.mformat_odt.OdtStyles)
  * [MultiFormatOdt](#mformat_ext.mformat_odt.MultiFormatOdt)
    * [\_\_init\_\_](#mformat_ext.mformat_odt.MultiFormatOdt.__init__)
    * [\_insert\_odt\_styles](#mformat_ext.mformat_odt.MultiFormatOdt._insert_odt_styles)
    * [\_create\_list\_level\_properties](#mformat_ext.mformat_odt.MultiFormatOdt._create_list_level_properties)
    * [\_create\_numbered\_list\_style](#mformat_ext.mformat_odt.MultiFormatOdt._create_numbered_list_style)
    * [\_create\_bullet\_list\_style](#mformat_ext.mformat_odt.MultiFormatOdt._create_bullet_list_style)
    * [\_create\_code\_paragraph\_style](#mformat_ext.mformat_odt.MultiFormatOdt._create_code_paragraph_style)
    * [\_create\_link\_style](#mformat_ext.mformat_odt.MultiFormatOdt._create_link_style)
    * [\_create\_odt\_styles](#mformat_ext.mformat_odt.MultiFormatOdt._create_odt_styles)
    * [\_style\_name\_from\_formatting](#mformat_ext.mformat_odt.MultiFormatOdt._style_name_from_formatting)
    * [\_link\_style\_name\_from\_formatting](#mformat_ext.mformat_odt.MultiFormatOdt._link_style_name_from_formatting)
    * [file\_name\_extension](#mformat_ext.mformat_odt.MultiFormatOdt.file_name_extension)
    * [get\_arg\_desciption](#mformat_ext.mformat_odt.MultiFormatOdt.get_arg_desciption)
    * [open](#mformat_ext.mformat_odt.MultiFormatOdt.open)
    * [\_close](#mformat_ext.mformat_odt.MultiFormatOdt._close)
    * [\_write\_file\_prefix](#mformat_ext.mformat_odt.MultiFormatOdt._write_file_prefix)
    * [\_write\_file\_suffix](#mformat_ext.mformat_odt.MultiFormatOdt._write_file_suffix)
    * [\_start\_paragraph](#mformat_ext.mformat_odt.MultiFormatOdt._start_paragraph)
    * [\_end\_paragraph](#mformat_ext.mformat_odt.MultiFormatOdt._end_paragraph)
    * [\_start\_heading](#mformat_ext.mformat_odt.MultiFormatOdt._start_heading)
    * [\_end\_heading](#mformat_ext.mformat_odt.MultiFormatOdt._end_heading)
    * [\_formatted\_write](#mformat_ext.mformat_odt.MultiFormatOdt._formatted_write)
    * [\_write\_text](#mformat_ext.mformat_odt.MultiFormatOdt._write_text)
    * [\_impl\_write\_url](#mformat_ext.mformat_odt.MultiFormatOdt._impl_write_url)
    * [\_write\_url](#mformat_ext.mformat_odt.MultiFormatOdt._write_url)
    * [\_start\_bullet\_list](#mformat_ext.mformat_odt.MultiFormatOdt._start_bullet_list)
    * [\_end\_bullet\_list](#mformat_ext.mformat_odt.MultiFormatOdt._end_bullet_list)
    * [\_start\_bullet\_item](#mformat_ext.mformat_odt.MultiFormatOdt._start_bullet_item)
    * [\_end\_bullet\_item](#mformat_ext.mformat_odt.MultiFormatOdt._end_bullet_item)
    * [\_start\_numbered\_list](#mformat_ext.mformat_odt.MultiFormatOdt._start_numbered_list)
    * [\_end\_numbered\_list](#mformat_ext.mformat_odt.MultiFormatOdt._end_numbered_list)
    * [\_start\_numbered\_item](#mformat_ext.mformat_odt.MultiFormatOdt._start_numbered_item)
    * [\_end\_numbered\_item](#mformat_ext.mformat_odt.MultiFormatOdt._end_numbered_item)
    * [\_start\_table](#mformat_ext.mformat_odt.MultiFormatOdt._start_table)
    * [\_end\_table](#mformat_ext.mformat_odt.MultiFormatOdt._end_table)
    * [\_write\_table\_first\_row](#mformat_ext.mformat_odt.MultiFormatOdt._write_table_first_row)
    * [\_write\_table\_row](#mformat_ext.mformat_odt.MultiFormatOdt._write_table_row)
    * [\_start\_code\_block](#mformat_ext.mformat_odt.MultiFormatOdt._start_code_block)
    * [\_end\_code\_block](#mformat_ext.mformat_odt.MultiFormatOdt._end_code_block)
    * [\_write\_code\_block](#mformat_ext.mformat_odt.MultiFormatOdt._write_code_block)
    * [\_encode\_text](#mformat_ext.mformat_odt.MultiFormatOdt._encode_text)
* [mformat\_ext.mformat\_docx](#mformat_ext.mformat_docx)
  * [MultiFormatDocx](#mformat_ext.mformat_docx.MultiFormatDocx)
    * [\_\_init\_\_](#mformat_ext.mformat_docx.MultiFormatDocx.__init__)
    * [file\_name\_extension](#mformat_ext.mformat_docx.MultiFormatDocx.file_name_extension)
    * [get\_arg\_desciption](#mformat_ext.mformat_docx.MultiFormatDocx.get_arg_desciption)
    * [open](#mformat_ext.mformat_docx.MultiFormatDocx.open)
    * [\_close](#mformat_ext.mformat_docx.MultiFormatDocx._close)
    * [\_write\_file\_prefix](#mformat_ext.mformat_docx.MultiFormatDocx._write_file_prefix)
    * [\_write\_file\_suffix](#mformat_ext.mformat_docx.MultiFormatDocx._write_file_suffix)
    * [\_start\_paragraph](#mformat_ext.mformat_docx.MultiFormatDocx._start_paragraph)
    * [\_end\_paragraph](#mformat_ext.mformat_docx.MultiFormatDocx._end_paragraph)
    * [\_start\_heading](#mformat_ext.mformat_docx.MultiFormatDocx._start_heading)
    * [\_end\_heading](#mformat_ext.mformat_docx.MultiFormatDocx._end_heading)
    * [\_write\_text](#mformat_ext.mformat_docx.MultiFormatDocx._write_text)
    * [\_write\_url](#mformat_ext.mformat_docx.MultiFormatDocx._write_url)
    * [\_add\_hyperlink](#mformat_ext.mformat_docx.MultiFormatDocx._add_hyperlink)
    * [\_start\_bullet\_list](#mformat_ext.mformat_docx.MultiFormatDocx._start_bullet_list)
    * [\_end\_bullet\_list](#mformat_ext.mformat_docx.MultiFormatDocx._end_bullet_list)
    * [\_start\_bullet\_item](#mformat_ext.mformat_docx.MultiFormatDocx._start_bullet_item)
    * [\_end\_bullet\_item](#mformat_ext.mformat_docx.MultiFormatDocx._end_bullet_item)
    * [\_start\_numbered\_list](#mformat_ext.mformat_docx.MultiFormatDocx._start_numbered_list)
    * [\_end\_numbered\_list](#mformat_ext.mformat_docx.MultiFormatDocx._end_numbered_list)
    * [\_start\_numbered\_item](#mformat_ext.mformat_docx.MultiFormatDocx._start_numbered_item)
    * [\_add\_tab\_stop](#mformat_ext.mformat_docx.MultiFormatDocx._add_tab_stop)
    * [\_end\_numbered\_item](#mformat_ext.mformat_docx.MultiFormatDocx._end_numbered_item)
    * [\_start\_table](#mformat_ext.mformat_docx.MultiFormatDocx._start_table)
    * [\_end\_table](#mformat_ext.mformat_docx.MultiFormatDocx._end_table)
    * [\_write\_table\_first\_row](#mformat_ext.mformat_docx.MultiFormatDocx._write_table_first_row)
    * [\_write\_table\_row](#mformat_ext.mformat_docx.MultiFormatDocx._write_table_row)
    * [\_start\_code\_block](#mformat_ext.mformat_docx.MultiFormatDocx._start_code_block)
    * [\_end\_code\_block](#mformat_ext.mformat_docx.MultiFormatDocx._end_code_block)
    * [\_write\_code\_block](#mformat_ext.mformat_docx.MultiFormatDocx._write_code_block)
    * [\_encode\_text](#mformat_ext.mformat_docx.MultiFormatDocx._encode_text)
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
for self.state and the public methods start_bullet_item,
start_numbered_item.

The mixin defines:
- Internal state machine: _start_list_item_impl and helpers
- Abstract methods for derived classes to implement

<a id="mformat.mformat_lists_impl.ListHandlerMixin.__init__"></a>

#### \_\_init\_\_

```python
def __init__() -> None
```

Initialize the ListHandlerMixin.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._start_list_item_impl"></a>

#### \_start\_list\_item\_impl

```python
def _start_list_item_impl(text: str, level: Optional[int],
                          formatting: FormattingWithWS,
                          point_list_type: PointListType) -> None
```

Start a list item of any type.

Handle the full state machine for list items with a clear,
linear flow:
1. Calculate the effective target level
2. Validate the level
3. Exit any non-list state
4. Adjust to the target level and type
5. Start the new item
6. Write the text

**Arguments**:

- `text` - The text to write in the list item.
- `level` - The level of the list item (None = current or 1).
- `formatting` - The formatting of the text.
- `point_list_type` - The type of point list (bullet or numbered).

<a id="mformat.mformat_lists_impl.ListHandlerMixin._validate_list_level"></a>

#### \_validate\_list\_level

```python
def _validate_list_level(target_level: int,
                         point_list_type: PointListType) -> None
```

Validate that the target level is reachable.

**Arguments**:

- `target_level` - The level to validate.
- `point_list_type` - The type of list (for error message).

**Raises**:

- `RuntimeError` - If the target level skips a level.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._adjust_to_list_level"></a>

#### \_adjust\_to\_list\_level

```python
def _adjust_to_list_level(target_level: int,
                          point_list_type: PointListType) -> None
```

Adjust the list stack to the target level with the right type.

This method handles three operations in sequence:
1. Decrease depth: End lists until at or below target level
2. Switch type: End list at target level if type doesn't match
3. Increase depth: Start new list at target level if needed

**Arguments**:

- `target_level` - The level to reach.
- `point_list_type` - The type of list needed at target level.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_item_before_nesting"></a>

#### \_end\_item\_before\_nesting

```python
def _end_item_before_nesting() -> None
```

End the current item before starting a nested list.

Transitions from item state to list state. Does nothing if not
currently in an item state or if no list exists.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._push_and_start_list"></a>

#### \_push\_and\_start\_list

```python
def _push_and_start_list(point_list_type: PointListType) -> None
```

Push a new list onto the stack and start it.

**Arguments**:

- `point_list_type` - The type of list to start.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._start_item_in_list"></a>

#### \_start\_item\_in\_list

```python
def _start_item_in_list(point_list_type: PointListType) -> None
```

Start a new item in the current list.

Ends the current item if in item state, then starts a new one.

**Arguments**:

- `point_list_type` - The type of list item to start.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._full_number_of_list_item"></a>

#### \_full\_number\_of\_list\_item

```python
def _full_number_of_list_item(num: int) -> str
```

Get the full number of the current item.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._decrease_list_depth"></a>

#### \_decrease\_list\_depth

```python
def _decrease_list_depth(target_level: int) -> None
```

Decrease depth: End lists until at or below target level.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_wrong_list_type_at_lev"></a>

#### \_end\_wrong\_list\_type\_at\_lev

```python
def _end_wrong_list_type_at_lev(target_level: int,
                                point_list_type: PointListType) -> None
```

End list at target level if type doesn't match.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._increase_list_depth"></a>

#### \_increase\_list\_depth

```python
def _increase_list_depth(target_level: int,
                         point_list_type: PointListType) -> None
```

Increase depth: Start new list at target level if needed.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._get_states_of_pltype"></a>

#### \_get\_states\_of\_pltype

```python
@staticmethod
def _get_states_of_pltype(
    point_list_type: PointListType
) -> tuple[MultiFormatState, MultiFormatState]
```

Get the list and item states for a point list type.

**Arguments**:

- `point_list_type` - The type of point list.

**Returns**:

  A tuple of (list_state, item_state).

<a id="mformat.mformat_lists_impl.ListHandlerMixin._get_point_list_type_name"></a>

#### \_get\_point\_list\_type\_name

```python
@staticmethod
def _get_point_list_type_name(point_list_type: PointListType) -> str
```

Get the name of a point list type for error messages.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._is_in_list_state"></a>

#### \_is\_in\_list\_state

```python
def _is_in_list_state() -> bool
```

Check if currently in any list state (list or item).

<a id="mformat.mformat_lists_impl.ListHandlerMixin._is_in_list_item_state"></a>

#### \_is\_in\_list\_item\_state

```python
def _is_in_list_item_state() -> bool
```

Check if currently in any list item state.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._dispatch_start_list"></a>

#### \_dispatch\_start\_list

```python
def _dispatch_start_list(level: int, point_list_type: PointListType) -> None
```

Call the appropriate _start_*_list method.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._dispatch_end_list"></a>

#### \_dispatch\_end\_list

```python
def _dispatch_end_list(level: int, point_list_type: PointListType) -> None
```

Call the appropriate _end_*_list method.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._dispatch_start_item"></a>

#### \_dispatch\_start\_item

```python
def _dispatch_start_item(level: int, point_list_type: PointListType) -> None
```

Call the appropriate _start_*_item method.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._dispatch_end_item"></a>

#### \_dispatch\_end\_item

```python
def _dispatch_end_item(level: int, point_list_type: PointListType) -> None
```

Call the appropriate _end_*_item method.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._state_from_point_list"></a>

#### \_state\_from\_point\_list

```python
def _state_from_point_list() -> None
```

Set the state from the point list stack.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_list_state"></a>

#### \_end\_list\_state

```python
def _end_list_state() -> None
```

End a list state.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

End the current state.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._to_write"></a>

#### \_to\_write

```python
def _to_write(text: str, smart_ws: bool, in_add: bool) -> str
```

Get the text to write.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._write_text"></a>

#### \_write\_text

```python
def _write_text(text: str, state: MultiFormatState,
                formatting: Formatting) -> None
```

Write the text.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._start_bullet_list"></a>

#### \_start\_bullet\_list

```python
def _start_bullet_list(level: int) -> None
```

Start a bullet list. Must be overridden by subclasses.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_bullet_list"></a>

#### \_end\_bullet\_list

```python
def _end_bullet_list(level: int) -> None
```

End a bullet list. Must be overridden by subclasses.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._start_bullet_item"></a>

#### \_start\_bullet\_item

```python
def _start_bullet_item(level: int) -> None
```

Start a bullet item. Must be overridden by subclasses.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_bullet_item"></a>

#### \_end\_bullet\_item

```python
def _end_bullet_item(level: int) -> None
```

End a bullet item. Must be overridden by subclasses.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._start_numbered_list"></a>

#### \_start\_numbered\_list

```python
def _start_numbered_list(level: int) -> None
```

Start a numbered list. Must be overridden by subclasses.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_numbered_list"></a>

#### \_end\_numbered\_list

```python
def _end_numbered_list(level: int) -> None
```

End a numbered list. Must be overridden by subclasses.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._start_numbered_item"></a>

#### \_start\_numbered\_item

```python
def _start_numbered_item(level: int, num: int, full_number: str) -> None
```

Start a numbered item. Must be overridden by subclasses.

<a id="mformat.mformat_lists_impl.ListHandlerMixin._end_numbered_item"></a>

#### \_end\_numbered\_item

```python
def _end_numbered_item(level: int, num: int) -> None
```

End a numbered item. Must be overridden by subclasses.

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

<a id="mformat.mformat_textbased.MultiFormatTextBased._close"></a>

#### \_close

```python
def _close() -> None
```

Close the file.

Avoid using this method directly.
Use as a context manager instead, using a with statement.

<a id="mformat.mformat_textbased.MultiFormatTextBased._get_last_chars_written"></a>

#### \_get\_last\_chars\_written

```python
def _get_last_chars_written(num_chars: int) -> str
```

Get the last characters written to the file.

Keep the file pointer at the same position, i.e. at the end of the
file, so that we can continue writing after the last characters.
Returns the last characters written to the file.

<a id="mformat.factory"></a>

# mformat.factory

Factory class for creating MultiFormat instances.

<a id="mformat.factory._the_factory"></a>

#### \_the\_factory

pylint: disable=invalid-name # noqa: E501

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
def i_get_factory() -> MultiFormatFactory
```

Internally get the factory instance.

<a id="mformat.factory.MultiFormatFactory.register"></a>

#### register

```python
@staticmethod
def register(format_class: type[MultiFormat]) -> None
```

Register a MultiFormat subclass with the factory.

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

- `ValueError` - If the format_name is not registered.

<a id="mformat.factory.MultiFormatFactory.i_create"></a>

#### i\_create

```python
def i_create(format_name: str,
             file_name: str,
             url_as_text: bool = False,
             args: OptArgs = None) -> MultiFormat
```

Internally create an instance of a registered subclass.

<a id="mformat.factory.MultiFormatFactory.get_registered_formats"></a>

#### get\_registered\_formats

```python
@staticmethod
def get_registered_formats() -> list[str]
```

Get a list of all registered format names.

**Returns**:

  A list of registered format name strings.

<a id="mformat.factory.MultiFormatFactory.i_get_registered_formats"></a>

#### i\_get\_registered\_formats

```python
def i_get_registered_formats() -> list[str]
```

Internally get a list of registered format names.

<a id="mformat.factory.MultiFormatFactory.get_usage"></a>

#### get\_usage

```python
@staticmethod
def get_usage(format_name: str) -> FormatterDescriptor
```

Get the usage information for a registered format.

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

- `ValueError` - If the format_name is not registered.

<a id="mformat.factory.list_registered_mf"></a>

#### list\_registered\_mf

```python
def list_registered_mf() -> list[str]
```

Get a list of all registered format names.

This is a shortcut for MultiFormatFactory.get_registered_formats().

**Returns**:

  A list of registered format name strings.

<a id="mformat.factory.usage_mf"></a>

#### usage\_mf

```python
def usage_mf(format_name: str) -> FormatterDescriptor
```

Get the usage information for a registered format.

This is a shortcut for MultiFormatFactory.get_usage().

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

<a id="mformat.mformat_md"></a>

# mformat.mformat\_md

Markdown format class.

<a id="mformat.mformat_md.split_whitespace"></a>

#### split\_whitespace

```python
def split_whitespace(text: str) -> tuple[str, str, str]
```

Split a string into leading, stripped, and trailing whitespace.

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

<a id="mformat.mformat_md.MultiFormatMd._write_file_prefix"></a>

#### \_write\_file\_prefix

```python
def _write_file_prefix() -> None
```

Write the file prefix.

<a id="mformat.mformat_md.MultiFormatMd._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the file suffix.

<a id="mformat.mformat_md.MultiFormatMd._start_paragraph"></a>

#### \_start\_paragraph

```python
def _start_paragraph() -> None
```

Start a paragraph.

<a id="mformat.mformat_md.MultiFormatMd._end_paragraph"></a>

#### \_end\_paragraph

```python
def _end_paragraph() -> None
```

End a paragraph.

<a id="mformat.mformat_md.MultiFormatMd._empty_line_before"></a>

#### \_empty\_line\_before

```python
def _empty_line_before() -> None
```

Make sure there is an empty line before next item.

<a id="mformat.mformat_md.MultiFormatMd._start_heading"></a>

#### \_start\_heading

```python
def _start_heading(level: int) -> None
```

Start a heading.

<a id="mformat.mformat_md.MultiFormatMd._end_heading"></a>

#### \_end\_heading

```python
def _end_heading(level: int) -> None
```

End a heading.

<a id="mformat.mformat_md.MultiFormatMd._format_text"></a>

#### \_format\_text

```python
@staticmethod
def _format_text(text: str, formatting: Formatting) -> str
```

Format text with bold and italic.

<a id="mformat.mformat_md.MultiFormatMd._write_text"></a>

#### \_write\_text

```python
def _write_text(text: str, state: MultiFormatState,
                formatting: Formatting) -> None
```

Write text into current item (paragraph, bullet list item, etc.).

**Arguments**:

- `text` - The text to write into the current item.
- `state` - The state of the current item.
- `formatting` - The formatting of the text.

<a id="mformat.mformat_md.MultiFormatMd._write_url"></a>

#### \_write\_url

```python
def _write_url(url: str, text: Optional[str], state: MultiFormatState,
               formatting: Formatting) -> None
```

Write a URL into current item (paragraph, bullet list item...).

<a id="mformat.mformat_md.MultiFormatMd._start_bullet_list"></a>

#### \_start\_bullet\_list

```python
def _start_bullet_list(level: int) -> None
```

Start a bullet list.

<a id="mformat.mformat_md.MultiFormatMd._end_bullet_list"></a>

#### \_end\_bullet\_list

```python
def _end_bullet_list(level: int) -> None
```

End a bullet list.

<a id="mformat.mformat_md.MultiFormatMd._indent"></a>

#### \_indent

```python
def _indent(level: int) -> str
```

Get the indentation for a level.

<a id="mformat.mformat_md.MultiFormatMd._start_bullet_item"></a>

#### \_start\_bullet\_item

```python
def _start_bullet_item(level: int) -> None
```

Start a bullet item.

<a id="mformat.mformat_md.MultiFormatMd._end_bullet_item"></a>

#### \_end\_bullet\_item

```python
def _end_bullet_item(level: int) -> None
```

End a bullet item.

<a id="mformat.mformat_md.MultiFormatMd._start_numbered_list"></a>

#### \_start\_numbered\_list

```python
def _start_numbered_list(level: int) -> None
```

Start a numbered list.

<a id="mformat.mformat_md.MultiFormatMd._end_numbered_list"></a>

#### \_end\_numbered\_list

```python
def _end_numbered_list(level: int) -> None
```

End a numbered list.

<a id="mformat.mformat_md.MultiFormatMd._start_numbered_item"></a>

#### \_start\_numbered\_item

```python
def _start_numbered_item(level: int, num: int, full_number: str) -> None
```

Start a numbered item.

<a id="mformat.mformat_md.MultiFormatMd._end_numbered_item"></a>

#### \_end\_numbered\_item

```python
def _end_numbered_item(level: int, num: int) -> None
```

End a numbered item.

<a id="mformat.mformat_md.MultiFormatMd._start_code_block"></a>

#### \_start\_code\_block

```python
def _start_code_block(programming_language: Optional[str]) -> None
```

Start a code block.

<a id="mformat.mformat_md.MultiFormatMd._end_code_block"></a>

#### \_end\_code\_block

```python
def _end_code_block(programming_language: Optional[str]) -> None
```

End a code block.

<a id="mformat.mformat_md.MultiFormatMd._write_code_block"></a>

#### \_write\_code\_block

```python
def _write_code_block(text: str, programming_language: Optional[str]) -> None
```

Write a code block.

<a id="mformat.mformat_md.MultiFormatMd._start_table"></a>

#### \_start\_table

```python
def _start_table(num_columns: int) -> None
```

Start a table.

<a id="mformat.mformat_md.MultiFormatMd._end_table"></a>

#### \_end\_table

```python
def _end_table(num_columns: int, num_rows: int) -> None
```

End a table.

<a id="mformat.mformat_md.MultiFormatMd._write_table_first_row"></a>

#### \_write\_table\_first\_row

```python
def _write_table_first_row(first_row: list[str],
                           formatting: Formatting) -> None
```

Write the first row of a table.

<a id="mformat.mformat_md.MultiFormatMd._write_table_row"></a>

#### \_write\_table\_row

```python
def _write_table_row(row: list[str], formatting: Formatting,
                     row_number: int) -> None
```

Write a row of a table.

<a id="mformat.mformat_md.MultiFormatMd._encode_text"></a>

#### \_encode\_text

```python
def _encode_text(text: str) -> str
```

Encode text (escape special characters) for Markdown.

Uses context-aware escaping based on Markdown syntax rules.
Characters are only escaped when they could be interpreted as
Markdown syntax in their specific context.

<a id="mformat.mformat_md.MultiFormatMd._escape_char"></a>

#### \_escape\_char

```python
def _escape_char(char: str, prev_char: str, next_char: str) -> str
```

Escape a single character based on context.

**Arguments**:

- `char` - The character to potentially escape.
- `prev_char` - The previous character ('' if at start).
- `next_char` - The next character ('' if at end).
  

**Returns**:

  The character, escaped if necessary.

<a id="mformat.mformat_md.MultiFormatMd._escape_line_context_char"></a>

#### \_escape\_line\_context\_char

```python
def _escape_line_context_char(char: str, prev_char: str, next_char: str,
                              at_line_start: bool) -> str
```

Escape characters that depend on line position context.

**Arguments**:

- `char` - The character to potentially escape.
- `prev_char` - The previous character ('' if at start).
- `next_char` - The next character ('' if at end).
- `at_line_start` - True if at the start of a line.
  

**Returns**:

  The character, escaped if necessary.

<a id="mformat.mformat_md.MultiFormatMd._escape_greater_than"></a>

#### \_escape\_greater\_than

```python
def _escape_greater_than(prev_char: str, at_line_start: bool) -> str
```

Escape > for blockquotes and HTML.

<a id="mformat.mformat_md.MultiFormatMd._escape_list_marker"></a>

#### \_escape\_list\_marker

```python
def _escape_list_marker(char: str, next_char: str, at_line_start: bool) -> str
```

Escape - or + for list markers and horizontal rules.

<a id="mformat.mformat_md.MultiFormatMd._escape_emphasis"></a>

#### \_escape\_emphasis

```python
def _escape_emphasis(char: str, prev_char: str, next_char: str,
                     at_line_start: bool) -> str
```

Escape * or _ for emphasis markers.

<a id="mformat.mformat_md.MultiFormatMd._escape_equals"></a>

#### \_escape\_equals

```python
def _escape_equals(next_char: str, at_line_start: bool) -> str
```

Escape = for setext heading underlines.

<a id="mformat.mformat_md.MultiFormatMd._is_emphasis_position"></a>

#### \_is\_emphasis\_position

```python
def _is_emphasis_position(prev_char: str, next_char: str) -> bool
```

Check if position could be an emphasis delimiter.

Based on CommonMark flanking rules - emphasis delimiters are
recognized at word boundaries (adjacent to whitespace, punctuation,
or string boundaries).

**Arguments**:

- `prev_char` - Character before the potential delimiter ('' if none).
- `next_char` - Character after the potential delimiter ('' if none).
  

**Returns**:

  True if the position could be an emphasis delimiter.

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

<a id="mformat.mformat.MultiFormat.start_heading"></a>

#### start\_heading

```python
def start_heading(level: int,
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
  start_heading or add_text).
- `bold` - If True, the text is bold.
  Recommended to leave False for headings as it will be
  formatted as a heading.
- `italic` - If True, the text is italic.
  Recommended to leave False for headings as it will be
  formatted as a heading.

<a id="mformat.mformat.MultiFormat.start_paragraph"></a>

#### start\_paragraph

```python
def start_paragraph(text: str,
                    smart_ws: bool = True,
                    bold: bool = False,
                    italic: bool = False) -> None
```

Start a new paragraph.

**Arguments**:

- `text` - The text to write in the paragraph.
- `smart_ws` - If True, leading and trailing whitespace are collapsed
  and a single space is inserted between texts (from
  start_paragraph or add_text).
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
  start_paragraph, start_bullet, ... or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

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

<a id="mformat.mformat.MultiFormat.start_bullet_item"></a>

#### start\_bullet\_item

```python
def start_bullet_item(text: str,
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
  start_bullet_item or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.start_numbered_point_item"></a>

#### start\_numbered\_point\_item

```python
def start_numbered_point_item(text: str,
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
  start_numbered_point_item or add_text).
- `bold` - If True, the text is bold.
- `italic` - If True, the text is italic.

<a id="mformat.mformat.MultiFormat.start_table"></a>

#### start\_table

```python
def start_table(first_row: list[str],
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

Result is same as calling start_table followed by add_table_row
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

<a id="mformat.mformat.MultiFormat._close"></a>

#### \_close

```python
def _close() -> None
```

Close the file.

Must be overridden by subclasses.

<a id="mformat.mformat.MultiFormat._write_file_prefix"></a>

#### \_write\_file\_prefix

```python
def _write_file_prefix() -> None
```

Write the file prefix.

<a id="mformat.mformat.MultiFormat._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the file suffix.

<a id="mformat.mformat.MultiFormat._end_state"></a>

#### \_end\_state

```python
def _end_state() -> None
```

End the current state.

<a id="mformat.mformat.MultiFormat._start_paragraph"></a>

#### \_start\_paragraph

```python
def _start_paragraph() -> None
```

Start a paragraph.

<a id="mformat.mformat.MultiFormat._end_paragraph"></a>

#### \_end\_paragraph

```python
def _end_paragraph() -> None
```

End a paragraph.

<a id="mformat.mformat.MultiFormat._start_heading"></a>

#### \_start\_heading

```python
def _start_heading(level: int) -> None
```

Start a heading.

<a id="mformat.mformat.MultiFormat._end_heading"></a>

#### \_end\_heading

```python
def _end_heading(level: int) -> None
```

End a heading.

<a id="mformat.mformat.MultiFormat._write_text"></a>

#### \_write\_text

```python
def _write_text(text: str, state: MultiFormatState,
                formatting: Formatting) -> None
```

Write text into current item (paragraph, bullet list item...).

<a id="mformat.mformat.MultiFormat._write_url"></a>

#### \_write\_url

```python
def _write_url(url: str, text: Optional[str], state: MultiFormatState,
               formatting: Formatting) -> None
```

Write a URL into current item (paragraph, bullet list item...).

<a id="mformat.mformat.MultiFormat.file_name_with_extension"></a>

#### file\_name\_with\_extension

```python
@staticmethod
def file_name_with_extension(file_name: str, extension: str) -> str
```

Get the file name with the extension.

<a id="mformat.mformat.MultiFormat._must_be_overridden"></a>

#### \_must\_be\_overridden

```python
@classmethod
def _must_be_overridden(cls, func_name: str) -> str
```

Error message if the function is not overridden by a subclass.

<a id="mformat.mformat.MultiFormat._file_exists_check"></a>

#### \_file\_exists\_check

```python
def _file_exists_check() -> None
```

Check if the file exists and handle it accordingly.

<a id="mformat.mformat.MultiFormat._to_write_optional"></a>

#### \_to\_write\_optional

```python
def _to_write_optional(text: Optional[str], smart_ws: bool,
                       in_add: bool) -> Optional[str]
```

Get the text to write.

<a id="mformat.mformat.MultiFormat._to_write"></a>

#### \_to\_write

```python
def _to_write(text: str, smart_ws: bool, in_add: bool) -> str
```

Get the text to write.

<a id="mformat.mformat.MultiFormat._start_bullet_list"></a>

#### \_start\_bullet\_list

```python
def _start_bullet_list(level: int) -> None
```

Start a bullet list.

<a id="mformat.mformat.MultiFormat._end_bullet_list"></a>

#### \_end\_bullet\_list

```python
def _end_bullet_list(level: int) -> None
```

End a bullet list.

<a id="mformat.mformat.MultiFormat._start_bullet_item"></a>

#### \_start\_bullet\_item

```python
def _start_bullet_item(level: int) -> None
```

Start a bullet item.

<a id="mformat.mformat.MultiFormat._end_bullet_item"></a>

#### \_end\_bullet\_item

```python
def _end_bullet_item(level: int) -> None
```

End a bullet item.

<a id="mformat.mformat.MultiFormat._start_numbered_list"></a>

#### \_start\_numbered\_list

```python
def _start_numbered_list(level: int) -> None
```

Start a numbered list.

<a id="mformat.mformat.MultiFormat._end_numbered_list"></a>

#### \_end\_numbered\_list

```python
def _end_numbered_list(level: int) -> None
```

End a numbered list.

<a id="mformat.mformat.MultiFormat._start_numbered_item"></a>

#### \_start\_numbered\_item

```python
def _start_numbered_item(level: int, num: int, full_number: str) -> None
```

Start a numbered item.

**Arguments**:

- `level` - The level of the item.
- `num` - The number of the item at this level.
- `full_number` - The full number of the item including all levels.

<a id="mformat.mformat.MultiFormat._end_numbered_item"></a>

#### \_end\_numbered\_item

```python
def _end_numbered_item(level: int, num: int) -> None
```

End a numbered item.

<a id="mformat.mformat.MultiFormat._update_table_column_widths"></a>

#### \_update\_table\_column\_widths

```python
def _update_table_column_widths(row: list[str]) -> None
```

Update the column widths of the table.

<a id="mformat.mformat.MultiFormat._start_table"></a>

#### \_start\_table

```python
def _start_table(num_columns: int) -> None
```

Start a table.

<a id="mformat.mformat.MultiFormat._end_table"></a>

#### \_end\_table

```python
def _end_table(num_columns: int, num_rows: int) -> None
```

End a table.

<a id="mformat.mformat.MultiFormat._write_table_first_row"></a>

#### \_write\_table\_first\_row

```python
def _write_table_first_row(first_row: list[str],
                           formatting: Formatting) -> None
```

Write the first row of the table.

<a id="mformat.mformat.MultiFormat._write_table_row"></a>

#### \_write\_table\_row

```python
def _write_table_row(row: list[str], formatting: Formatting,
                     row_number: int) -> None
```

Write a row of the table.

<a id="mformat.mformat.MultiFormat._start_code_block"></a>

#### \_start\_code\_block

```python
def _start_code_block(programming_language: Optional[str]) -> None
```

Start a code block.

<a id="mformat.mformat.MultiFormat._end_code_block"></a>

#### \_end\_code\_block

```python
def _end_code_block(programming_language: Optional[str]) -> None
```

End a code block.

<a id="mformat.mformat.MultiFormat._write_code_block"></a>

#### \_write\_code\_block

```python
def _write_code_block(text: str, programming_language: Optional[str]) -> None
```

Write a code block.

<a id="mformat.mformat.MultiFormat._encode_text"></a>

#### \_encode\_text

```python
def _encode_text(text: str) -> str
```

Encode text (escape special characters).

Derived classes must implement this method.
Whenever special characters need to be encoded, this method
should be defined in the derived class. The base class always
calls this method with the text to encode.
Notice that the derived class implementation have access to
the self.state variable, in case the encoding depends on the
current state.

**Arguments**:

- `text` - The text to encode.

**Returns**:

  The encoded text.

<a id="mformat.mformat.MultiFormat._encode_table_row"></a>

#### \_encode\_table\_row

```python
def _encode_table_row(row: list[str]) -> list[str]
```

Encode a table row.

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

<a id="mformat.mformat_html.MultiFormatHtml._write_file_prefix"></a>

#### \_write\_file\_prefix

```python
def _write_file_prefix() -> None
```

Write the file prefix.

<a id="mformat.mformat_html.MultiFormatHtml._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the file suffix.

<a id="mformat.mformat_html.MultiFormatHtml._start_paragraph"></a>

#### \_start\_paragraph

```python
def _start_paragraph() -> None
```

Start a paragraph.

<a id="mformat.mformat_html.MultiFormatHtml._end_paragraph"></a>

#### \_end\_paragraph

```python
def _end_paragraph() -> None
```

End a paragraph.

<a id="mformat.mformat_html.MultiFormatHtml._start_heading"></a>

#### \_start\_heading

```python
def _start_heading(level: int) -> None
```

Start a heading.

<a id="mformat.mformat_html.MultiFormatHtml._end_heading"></a>

#### \_end\_heading

```python
def _end_heading(level: int) -> None
```

End a heading.

<a id="mformat.mformat_html.MultiFormatHtml._write_text"></a>

#### \_write\_text

```python
def _write_text(text: str, state: MultiFormatState,
                formatting: Formatting) -> None
```

Write text into current item (paragraph, bullet list item, etc.).

**Arguments**:

- `text` - The text to write into the current item.
- `state` - The state of the current item.
- `formatting` - The formatting of the text.

<a id="mformat.mformat_html.MultiFormatHtml._write_url"></a>

#### \_write\_url

```python
def _write_url(url: str, text: Optional[str], state: MultiFormatState,
               formatting: Formatting) -> None
```

Write a URL into current item (paragraph, bullet list item...).

<a id="mformat.mformat_html.MultiFormatHtml._start_bullet_list"></a>

#### \_start\_bullet\_list

```python
def _start_bullet_list(level: int) -> None
```

Start a bullet list.

<a id="mformat.mformat_html.MultiFormatHtml._end_bullet_list"></a>

#### \_end\_bullet\_list

```python
def _end_bullet_list(level: int) -> None
```

End a bullet list.

<a id="mformat.mformat_html.MultiFormatHtml._start_bullet_item"></a>

#### \_start\_bullet\_item

```python
def _start_bullet_item(level: int) -> None
```

Start a bullet item.

<a id="mformat.mformat_html.MultiFormatHtml._end_bullet_item"></a>

#### \_end\_bullet\_item

```python
def _end_bullet_item(level: int) -> None
```

End a bullet item.

<a id="mformat.mformat_html.MultiFormatHtml._start_numbered_list"></a>

#### \_start\_numbered\_list

```python
def _start_numbered_list(level: int) -> None
```

Start a numbered list.

<a id="mformat.mformat_html.MultiFormatHtml._end_numbered_list"></a>

#### \_end\_numbered\_list

```python
def _end_numbered_list(level: int) -> None
```

End a numbered list.

<a id="mformat.mformat_html.MultiFormatHtml._start_numbered_item"></a>

#### \_start\_numbered\_item

```python
def _start_numbered_item(level: int, num: int, full_number: str) -> None
```

Start a numbered item.

<a id="mformat.mformat_html.MultiFormatHtml._end_numbered_item"></a>

#### \_end\_numbered\_item

```python
def _end_numbered_item(level: int, num: int) -> None
```

End a numbered item.

<a id="mformat.mformat_html.MultiFormatHtml._start_table"></a>

#### \_start\_table

```python
def _start_table(num_columns: int) -> None
```

Start a table.

<a id="mformat.mformat_html.MultiFormatHtml._end_table"></a>

#### \_end\_table

```python
def _end_table(num_columns: int, num_rows: int) -> None
```

End a table.

<a id="mformat.mformat_html.MultiFormatHtml._write_table_first_row"></a>

#### \_write\_table\_first\_row

```python
def _write_table_first_row(first_row: list[str],
                           formatting: Formatting) -> None
```

Write the first row of a table.

<a id="mformat.mformat_html.MultiFormatHtml._write_table_row"></a>

#### \_write\_table\_row

```python
def _write_table_row(row: list[str], formatting: Formatting,
                     row_number: int) -> None
```

Write a row of a table.

<a id="mformat.mformat_html.MultiFormatHtml._start_code_block"></a>

#### \_start\_code\_block

```python
def _start_code_block(programming_language: Optional[str]) -> None
```

Start a code block.

<a id="mformat.mformat_html.MultiFormatHtml._end_code_block"></a>

#### \_end\_code\_block

```python
def _end_code_block(programming_language: Optional[str]) -> None
```

End a code block.

<a id="mformat.mformat_html.MultiFormatHtml._write_code_block"></a>

#### \_write\_code\_block

```python
def _write_code_block(text: str, programming_language: Optional[str]) -> None
```

Write a code block.

<a id="mformat.mformat_html.MultiFormatHtml._encode_text"></a>

#### \_encode\_text

```python
def _encode_text(text: str) -> str
```

Encode text (escape special characters).

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

<a id="mformat_ext.mformat_odt.MultiFormatOdt._insert_odt_styles"></a>

#### \_insert\_odt\_styles

```python
def _insert_odt_styles() -> None
```

Insert the ODT styles into the document.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._create_list_level_properties"></a>

#### \_create\_list\_level\_properties

```python
@staticmethod
def _create_list_level_properties(level_num: int) -> Element
```

Create list-level-properties element for indentation.

**Arguments**:

- `level_num` - The list level number (1-9).
  

**Returns**:

  An Element representing style:list-level-properties.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._create_numbered_list_style"></a>

#### \_create\_numbered\_list\_style

```python
@staticmethod
def _create_numbered_list_style() -> Element
```

Create a numbered list style for ODF documents.

**Returns**:

  An Element representing a text:list-style for numbered lists.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._create_bullet_list_style"></a>

#### \_create\_bullet\_list\_style

```python
@staticmethod
def _create_bullet_list_style() -> Element
```

Create a bullet list style for ODF documents.

**Returns**:

  An Element representing a text:list-style for bullet lists.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._create_code_paragraph_style"></a>

#### \_create\_code\_paragraph\_style

```python
@staticmethod
def _create_code_paragraph_style() -> Style
```

Create a code paragraph style with monospace font.

**Returns**:

  A Style object for code blocks with monospace font.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._create_link_style"></a>

#### \_create\_link\_style

```python
@staticmethod
def _create_link_style(name: str,
                       bold: bool = False,
                       italic: bool = False) -> Style
```

Create a link style with blue color and underline.

**Arguments**:

- `name` - The name of the style.
- `bold` - Whether the link text should be bold.
- `italic` - Whether the link text should be italic.
  

**Returns**:

  A Style object for links with the specified formatting.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._create_odt_styles"></a>

#### \_create\_odt\_styles

```python
def _create_odt_styles() -> OdtStyles
```

Create the ODT styles needed for documents.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._style_name_from_formatting"></a>

#### \_style\_name\_from\_formatting

```python
@staticmethod
def _style_name_from_formatting(formatting: Formatting) -> str
```

Get the style name from the formatting.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._link_style_name_from_formatting"></a>

#### \_link\_style\_name\_from\_formatting

```python
@staticmethod
def _link_style_name_from_formatting(formatting: Formatting) -> str
```

Get the link style name from the formatting.

Link styles include blue color and underline to be visible as links.

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

<a id="mformat_ext.mformat_odt.MultiFormatOdt._close"></a>

#### \_close

```python
def _close() -> None
```

Close the file.

Avoid using this method directly.
Use as a context manager instead, using a with statement.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._write_file_prefix"></a>

#### \_write\_file\_prefix

```python
def _write_file_prefix() -> None
```

Write the file prefix.

For ODT files, this is a no-op since the document
structure is handled by odfdo.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the file suffix.

For ODT files, this is a no-op since the document
structure is handled by odfdo.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_paragraph"></a>

#### \_start\_paragraph

```python
def _start_paragraph() -> None
```

Start a paragraph.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_paragraph"></a>

#### \_end\_paragraph

```python
def _end_paragraph() -> None
```

End a paragraph.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_heading"></a>

#### \_start\_heading

```python
def _start_heading(level: int) -> None
```

Start a heading.

**Arguments**:

- `level` - The level of the heading (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_heading"></a>

#### \_end\_heading

```python
def _end_heading(level: int) -> None
```

End a heading.

**Arguments**:

- `level` - The level of the heading (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._formatted_write"></a>

#### \_formatted\_write

```python
def _formatted_write(paragraph: Paragraph, formatting: Formatting,
                     text: str) -> None
```

Apply formatting to a paragraph or list item.

In ODF/XML, paragraph.text holds text before any child elements,
and each element's tail holds text after that element. To maintain
correct text order when mixing formatted and unformatted text, we:
- Use Span elements for formatted text (appended as children)
- For unformatted text: add to paragraph.text if no children exist,
  otherwise add to the tail of the last child element.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._write_text"></a>

#### \_write\_text

```python
def _write_text(text: str, state: MultiFormatState,
                formatting: Formatting) -> None
```

Write text into current item (paragraph, bullet list item, etc.).

**Arguments**:

- `text` - The text to write into the current item.
- `state` - The state of the current item.
- `formatting` - The formatting of the text.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._impl_write_url"></a>

#### \_impl\_write\_url

```python
def _impl_write_url(paragraph: Paragraph, url: str, text: Optional[str],
                    formatting: Formatting) -> None
```

Implement the writing of a URL into a paragraph or list item.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._write_url"></a>

#### \_write\_url

```python
def _write_url(url: str, text: Optional[str], state: MultiFormatState,
               formatting: Formatting) -> None
```

Write a URL into current item (paragraph, bullet list item, etc.).

**Arguments**:

- `url` - The URL to write into the current item.
- `text` - The text to display for the URL.
- `state` - The state of the current item.
- `formatting` - The formatting of the text.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_bullet_list"></a>

#### \_start\_bullet\_list

```python
def _start_bullet_list(level: int) -> None
```

Start a bullet list.

**Arguments**:

- `level` - The level of the bullet list (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_bullet_list"></a>

#### \_end\_bullet\_list

```python
def _end_bullet_list(level: int) -> None
```

End a bullet list.

**Arguments**:

- `level` - The level of the bullet list (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_bullet_item"></a>

#### \_start\_bullet\_item

```python
def _start_bullet_item(level: int) -> None
```

Start a bullet item.

**Arguments**:

- `level` - The level of the bullet item (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_bullet_item"></a>

#### \_end\_bullet\_item

```python
def _end_bullet_item(level: int) -> None
```

End a bullet item.

**Arguments**:

- `level` - The level of the bullet item (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_numbered_list"></a>

#### \_start\_numbered\_list

```python
def _start_numbered_list(level: int) -> None
```

Start a numbered list.

**Arguments**:

- `level` - The level of the numbered list (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_numbered_list"></a>

#### \_end\_numbered\_list

```python
def _end_numbered_list(level: int) -> None
```

End a numbered list.

**Arguments**:

- `level` - The level of the numbered list (1-9).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_numbered_item"></a>

#### \_start\_numbered\_item

```python
def _start_numbered_item(level: int, num: int, full_number: str) -> None
```

Start a numbered item.

**Arguments**:

- `level` - The level of the numbered item (1-9).
- `num` - The number of the item.
- `full_number` - The full number of the item including all levels.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_numbered_item"></a>

#### \_end\_numbered\_item

```python
def _end_numbered_item(level: int, num: int) -> None
```

End a numbered item.

**Arguments**:

- `level` - The level of the numbered item (1-9).
- `num` - The number of the item.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_table"></a>

#### \_start\_table

```python
def _start_table(num_columns: int) -> None
```

Start a table.

**Arguments**:

- `num_columns` - The number of columns in the table.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_table"></a>

#### \_end\_table

```python
def _end_table(num_columns: int, num_rows: int) -> None
```

End a table.

**Arguments**:

- `num_columns` - The number of columns in the table.
- `num_rows` - The number of rows in the table.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._write_table_first_row"></a>

#### \_write\_table\_first\_row

```python
def _write_table_first_row(first_row: list[str],
                           formatting: Formatting) -> None
```

Write the first row of a table.

**Arguments**:

- `first_row` - The first row of the table.
- `formatting` - The formatting of the text in each cell.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._write_table_row"></a>

#### \_write\_table\_row

```python
def _write_table_row(row: list[str], formatting: Formatting,
                     row_number: int) -> None
```

Write a row of a table.

**Arguments**:

- `row` - The row to add to the table.
- `formatting` - The formatting of the text in each cell.
- `row_number` - The row number (0-based).

<a id="mformat_ext.mformat_odt.MultiFormatOdt._start_code_block"></a>

#### \_start\_code\_block

```python
def _start_code_block(programming_language: Optional[str]) -> None
```

Start a code block.

**Arguments**:

- `programming_language` - The programming language of the code block.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._end_code_block"></a>

#### \_end\_code\_block

```python
def _end_code_block(programming_language: Optional[str]) -> None
```

End a code block.

**Arguments**:

- `programming_language` - The programming language of the code block.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._write_code_block"></a>

#### \_write\_code\_block

```python
def _write_code_block(text: str, programming_language: Optional[str]) -> None
```

Write a code block.

**Arguments**:

- `text` - The text to add to the code block.
- `programming_language` - The programming language of the code block.

<a id="mformat_ext.mformat_odt.MultiFormatOdt._encode_text"></a>

#### \_encode\_text

```python
def _encode_text(text: str) -> str
```

Encode text (escape special characters).

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

<a id="mformat_ext.mformat_docx.MultiFormatDocx._close"></a>

#### \_close

```python
def _close() -> None
```

Close the file.

Avoid using this method directly.
Use as a context manager instead, using a with statement.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._write_file_prefix"></a>

#### \_write\_file\_prefix

```python
def _write_file_prefix() -> None
```

Write the file prefix.

For DOCX files, this is a no-op since the document
structure is handled by python-docx.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._write_file_suffix"></a>

#### \_write\_file\_suffix

```python
def _write_file_suffix() -> None
```

Write the file suffix.

For DOCX files, this is a no-op since the document
structure is handled by python-docx.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_paragraph"></a>

#### \_start\_paragraph

```python
def _start_paragraph() -> None
```

Start a paragraph.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_paragraph"></a>

#### \_end\_paragraph

```python
def _end_paragraph() -> None
```

End a paragraph.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_heading"></a>

#### \_start\_heading

```python
def _start_heading(level: int) -> None
```

Start a heading.

**Arguments**:

- `level` - The level of the heading (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_heading"></a>

#### \_end\_heading

```python
def _end_heading(level: int) -> None
```

End a heading.

**Arguments**:

- `level` - The level of the heading (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._write_text"></a>

#### \_write\_text

```python
def _write_text(text: str, state: MultiFormatState,
                formatting: Formatting) -> None
```

Write text into current item (paragraph, bullet list item, etc.).

**Arguments**:

- `text` - The text to write into the current item.
- `state` - The state of the current item.
- `formatting` - The formatting of the text.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._write_url"></a>

#### \_write\_url

```python
def _write_url(url: str, text: Optional[str], state: MultiFormatState,
               formatting: Formatting) -> None
```

Write a URL into current item (paragraph, bullet list item, etc.).

**Arguments**:

- `url` - The URL to write into the current item.
- `text` - The text to display for the URL.
- `state` - The state of the current item.
- `formatting` - The formatting of the text.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._add_hyperlink"></a>

#### \_add\_hyperlink

```python
def _add_hyperlink(paragraph: Paragraph, url: str, text: str,
                   formatting: Formatting) -> None
```

Add a clickable hyperlink to a paragraph.

**Arguments**:

- `paragraph` - The paragraph to add the hyperlink to.
- `url` - The URL for the hyperlink.
- `text` - The display text for the hyperlink.
- `formatting` - The formatting (bold/italic) for the text.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_bullet_list"></a>

#### \_start\_bullet\_list

```python
def _start_bullet_list(level: int) -> None
```

Start a bullet list.

**Arguments**:

- `level` - The level of the bullet list (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_bullet_list"></a>

#### \_end\_bullet\_list

```python
def _end_bullet_list(level: int) -> None
```

End a bullet list.

**Arguments**:

- `level` - The level of the bullet list (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_bullet_item"></a>

#### \_start\_bullet\_item

```python
def _start_bullet_item(level: int) -> None
```

Start a bullet item.

**Arguments**:

- `level` - The level of the bullet item (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_bullet_item"></a>

#### \_end\_bullet\_item

```python
def _end_bullet_item(level: int) -> None
```

End a bullet item.

**Arguments**:

- `level` - The level of the bullet item (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_numbered_list"></a>

#### \_start\_numbered\_list

```python
def _start_numbered_list(level: int) -> None
```

Start a numbered list.

**Arguments**:

- `level` - The level of the numbered list (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_numbered_list"></a>

#### \_end\_numbered\_list

```python
def _end_numbered_list(level: int) -> None
```

End a numbered list.

**Arguments**:

- `level` - The level of the numbered list (1-9).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_numbered_item"></a>

#### \_start\_numbered\_item

```python
def _start_numbered_item(level: int, num: int, full_number: str) -> None
```

Start a numbered item.

**Arguments**:

- `level` - The level of the numbered item (1-9).
- `num` - The number of the item.
- `full_number` - The full number of the item including all levels.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._add_tab_stop"></a>

#### \_add\_tab\_stop

```python
@staticmethod
def _add_tab_stop(paragraph: Paragraph, position_twips: int) -> None
```

Add a left-aligned tab stop to a paragraph.

**Arguments**:

- `paragraph` - The paragraph to add the tab stop to.
- `position_twips` - The position of the tab stop in twips.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_numbered_item"></a>

#### \_end\_numbered\_item

```python
def _end_numbered_item(level: int, num: int) -> None
```

End a numbered item.

**Arguments**:

- `level` - The level of the numbered item (1-9).
- `num` - The number of the item.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_table"></a>

#### \_start\_table

```python
def _start_table(num_columns: int) -> None
```

Start a table.

**Arguments**:

- `num_columns` - The number of columns in the table.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_table"></a>

#### \_end\_table

```python
def _end_table(num_columns: int, num_rows: int) -> None
```

End a table.

**Arguments**:

- `num_columns` - The number of columns in the table.
- `num_rows` - The number of rows in the table.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._write_table_first_row"></a>

#### \_write\_table\_first\_row

```python
def _write_table_first_row(first_row: list[str],
                           formatting: Formatting) -> None
```

Write the first row of a table.

**Arguments**:

- `first_row` - The first row of the table.
- `formatting` - The formatting of the text in each cell.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._write_table_row"></a>

#### \_write\_table\_row

```python
def _write_table_row(row: list[str], formatting: Formatting,
                     row_number: int) -> None
```

Write a row of a table.

**Arguments**:

- `row` - The row to add to the table.
- `formatting` - The formatting of the text in each cell.
- `row_number` - The row number (0-based).

<a id="mformat_ext.mformat_docx.MultiFormatDocx._start_code_block"></a>

#### \_start\_code\_block

```python
def _start_code_block(programming_language: Optional[str]) -> None
```

Start a code block.

**Arguments**:

- `programming_language` - The programming language of the code block.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._end_code_block"></a>

#### \_end\_code\_block

```python
def _end_code_block(programming_language: Optional[str]) -> None
```

End a code block.

**Arguments**:

- `programming_language` - The programming language of the code block.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._write_code_block"></a>

#### \_write\_code\_block

```python
def _write_code_block(text: str, programming_language: Optional[str]) -> None
```

Write a code block.

**Arguments**:

- `text` - The text to add to the code block.
- `programming_language` - The programming language of the code block.

<a id="mformat_ext.mformat_docx.MultiFormatDocx._encode_text"></a>

#### \_encode\_text

```python
def _encode_text(text: str) -> str
```

Encode text (escape special characters).

<a id="mformat_ext.reg_extpkg_formats"></a>

# mformat\_ext.reg\_extpkg\_formats

Register the formats defined in the ext package with the factory.

<a id="mformat_ext.reg_extpkg_formats.register_formats_in_ext_pkg"></a>

#### register\_formats\_in\_ext\_pkg

```python
def register_formats_in_ext_pkg() -> list[type[MultiFormat]]
```

Get formats defined in the ext package to register with the factory.

