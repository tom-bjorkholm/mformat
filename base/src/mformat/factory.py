#! /usr/local/bin/python3
"""Factory class for creating MultiFormat instances."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from typing import Optional
from mformat.mformat import MultiFormat, FormatterDescriptor


the_factory: Optional[MultiFormatFactory] = None  # pylint: disable=invalid-name # noqa: E501


class MultiFormatFactory:
    """Factory class for creating instances of MultiFormat subclasses."""

    def __init__(self) -> None:
        """Initialize the factory with an empty registry."""
        self._registry: dict[str, type[MultiFormat]] = {}
        self._usage: dict[str, FormatterDescriptor] = {}

    @staticmethod
    def i_get_factory() -> MultiFormatFactory:
        """Get the factory instance."""
        global the_factory  # pylint: disable=global-statement # noqa: E501
        if the_factory is None:
            the_factory = MultiFormatFactory()
        return the_factory

    @staticmethod
    def register(format_class: type[MultiFormat]) -> None:
        """Register a MultiFormat subclass with the factory."""
        if not issubclass(format_class, MultiFormat):
            err = f'{format_class.__name__} must be a subclass of MultiFormat'
            raise ValueError(err)
        factory = MultiFormatFactory.i_get_factory()
        factory.i_register(format_class=format_class)

    def i_register(self, format_class: type[MultiFormat]) -> None:
        """Register a MultiFormat subclass with the factory."""
        desc: FormatterDescriptor = format_class.get_arg_desciption()
        self._registry[desc.name] = format_class
        self._usage[desc.name] = desc

    @staticmethod
    def create(format_name: str, file_name: str,
               url_as_text: bool = False,
               args: Optional[dict[str, str]] = None) -> MultiFormat:
        """Create an instance of a registered MultiFormat subclass.

        Args:
            format_name: The name identifier of the format class to create.
            file_name: The file path to pass to the MultiFormat constructor.
            url_as_text: Format URLs as text not clickable URLs.
            args: additional arguments to pass to the MultiFormat constructor.

        Returns:
            An instance of the requested MultiFormat subclass.

        Raises:
            ValueError: If the format_name is not registered.
        """
        factory = MultiFormatFactory.i_get_factory()
        return factory.i_create(format_name=format_name,
                                file_name=file_name,
                                url_as_text=url_as_text,
                                args=args)

    def i_create(self, format_name: str, file_name: str,
                 url_as_text: bool = False,
                 args: Optional[dict[str, str]] = None) -> MultiFormat:
        """Create an instance of a registered MultiFormat subclass."""
        if format_name not in self._registry:
            raise ValueError(
                f'Format "{format_name}" is not registered. '
                f'Available formats: {list(self._registry.keys())}'
            )
        format_class = self._registry[format_name]
        if args is None:
            return format_class(file_name=file_name, url_as_text=url_as_text)
        assert args is not None
        return format_class(file_name=file_name, url_as_text=url_as_text,
                            **args)

    @staticmethod
    def get_registered_formats() -> list[str]:
        """Get a list of all registered format names.

        Returns:
            A list of registered format name strings.
        """
        factory = MultiFormatFactory.i_get_factory()
        return factory.i_get_registered_formats()

    def i_get_registered_formats(self) -> list[str]:
        """Get a list of registered format names."""
        return list(self._registry.keys())

    @staticmethod
    def get_usage(format_name: str) -> FormatterDescriptor:
        """Get the usage information for a registered format."""
        factory = MultiFormatFactory.i_get_factory()
        return factory.i_get_usage(format_name=format_name)

    def i_get_usage(self, format_name: str) -> FormatterDescriptor:
        """Get the usage information for a registered format."""
        return self._usage[format_name]
