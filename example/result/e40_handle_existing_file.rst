Existing File Example
=====================

Using the file_exists_callback in the OptArgs dictionary and passing this
dictionary to the MultiFormat constructor (directly or using the create_mf
function) allows us to handle an exiting file in any way we want. The default
behaviour if no callback is provided is to refuse to overwrite existing files.
