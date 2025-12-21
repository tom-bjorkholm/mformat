#! /usr/local/bin/python3
"""Factory class for creating MultiFormat instances."""

# Copyright (c) 2025 Tom Björkholm
# MIT License
#

from mformat.mformat import MultiFormat, Iov


class MultiFormatFactory:
    """Factory class for creating instances of MultiFormat subclasses."""

    def __init__(self) -> None:
        """Initialize the factory with an empty registry."""
        self._registry: dict[str, type[MultiFormat]] = {}

    def register(
        self, format_name: str, format_class: type[MultiFormat]
    ) -> None:
        """
        Register a MultiFormat subclass with the factory.

        Args:
            format_name: The name identifier for the format class.
            format_class: The class to register (must be a subclass of
                         MultiFormat).
        """
        if not issubclass(format_class, MultiFormat):
            raise ValueError(
                f'{format_class.__name__} must be a subclass of '
                f'MultiFormat'
            )
        self._registry[format_name] = format_class

    def create(self, format_name: str, file: Iov) -> MultiFormat:
        """Create an instance of a registered MultiFormat subclass.

        Args:
            format_name: The name identifier of the format class to create.
            file_path: The file path to pass to the MultiFormat constructor.

        Returns:
            An instance of the requested MultiFormat subclass.

        Raises:
            ValueError: If the format_name is not registered.
        """
        if format_name not in self._registry:
            raise ValueError(
                f'Format "{format_name}" is not registered. '
                f'Available formats: {list(self._registry.keys())}'
            )
        format_class = self._registry[format_name]
        return format_class(file)

    def get_registered_formats(self) -> list[str]:
        """Get a list of all registered format names.

        Returns:
            A list of registered format name strings.
        """
        return list(self._registry.keys())
