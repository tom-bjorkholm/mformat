#! /usr/local/bin/python3
"""Factory class for creating MultiFormat instances."""

# Copyright (c) 2025 - 2026 Tom Björkholm
# MIT License
#

from typing import Optional, TypedDict, Callable
from mformat.mformat import MultiFormat, FormatterDescriptor, PathLike
from mformat.reg_pkg_formats import register_formats_in_pkg


_the_factory: Optional['MultiFormatFactory'] = None  # pylint: disable=invalid-name # noqa: E501


class OptArgsDict(TypedDict, total=False):
    """Optional arguments for the MultiFormat constructor."""

    file_exists_callback: Optional[Callable[[str], None]]
    lang: Optional[str]
    title: Optional[str]
    css_file: Optional[str]
    line_length: Optional[int]


type OptArgs = Optional[OptArgsDict]

COMMON_ARGS = ['file_exists_callback']


class MultiFormatFactory:
    """Factory class for creating instances of MultiFormat subclasses."""

    def __init__(self) -> None:
        """Initialize the factory with an empty registry."""
        self._registry: dict[str, type[MultiFormat]] = {}
        self._usage: dict[str, FormatterDescriptor] = {}
        self._lower2correct: dict[str, str] = {}  # Lower case to correct case
        formats: list[type[MultiFormat]] = register_formats_in_pkg()
        for format_class in formats:
            self.i_register(format_class)

    @staticmethod
    def i_get_factory() -> 'MultiFormatFactory':
        """Internally get the factory instance."""
        global _the_factory  # pylint: disable=global-statement # noqa: E501
        if _the_factory is None:
            _the_factory = MultiFormatFactory()
        return _the_factory

    @staticmethod
    def register(format_class: type[MultiFormat]) -> None:
        """Register a MultiFormat subclass with the factory.

        Args:
            format_class: The MultiFormat subclass to register.
        Raises:
            ValueError: If the format_class is not a subclass of MultiFormat.
            KeyError: If the format_name is already registered.
        """
        factory = MultiFormatFactory.i_get_factory()
        factory.i_register(format_class=format_class)

    def i_register(self, format_class: type[MultiFormat]) -> None:
        """Internally register a MultiFormat subclass with the factory."""
        if not issubclass(format_class, MultiFormat):
            err = f'{format_class.__name__} must be a subclass of MultiFormat'
            raise ValueError(err)
        desc: FormatterDescriptor = format_class.get_arg_desciption()
        if desc.name in self._registry:
            raise KeyError(f'Format "{desc.name}" is already registered.')
        if desc.name.lower() in self._lower2correct:
            msg = f'Cannot register format "{desc.name}" as ' + \
                f'"{self._lower2correct[desc.name.lower()]}" ' + \
                'is already registered.'
            raise KeyError(msg)
        self._registry[desc.name] = format_class
        self._usage[desc.name] = desc
        self._lower2correct[desc.name.lower()] = desc.name

    @staticmethod
    def create(format_name: str, file_name: PathLike,
               url_as_text: bool = False,
               args: OptArgs = None) -> MultiFormat:
        """Create an instance of a registered MultiFormat subclass.

        Args:
            format_name: The name identifier of the format class to create.
            file_name: The file path to pass to the MultiFormat constructor.
            url_as_text: Format URLs as text not clickable URLs.
            args: additional arguments to pass to the MultiFormat constructor.
        Returns:
            An instance of the requested MultiFormat subclass.
            Intended to be used as context manager, using a with statement.
        Raises:
            KeyError: If the format_name is not registered.
        """
        factory = MultiFormatFactory.i_get_factory()
        return factory.i_create(format_name=format_name,
                                file_name=file_name,
                                url_as_text=url_as_text,
                                args=args)

    def i_create(self, format_name: str, file_name: PathLike,
                 url_as_text: bool = False,
                 args: OptArgs = None) -> MultiFormat:
        """Internally create an instance of a registered subclass."""
        correct_name: Optional[str] = None
        if format_name in self._registry:
            correct_name = format_name
        elif format_name.lower() in self._lower2correct:
            correct_name = self._lower2correct[format_name.lower()]
        else:
            raise KeyError(
                f'Format "{format_name}" is not registered. ' +
                'Available formats: ' +
                f'{", ".join(sorted(list(self._registry.keys())))}'
            )
        assert correct_name is not None
        format_class = self._registry[correct_name]
        if args is None:
            return format_class(file_name=file_name, url_as_text=url_as_text)
        assert args is not None
        return format_class(file_name=file_name,  # type: ignore[misc]
                            url_as_text=url_as_text, **args)
        # mypy cannot see which MultiFormat subclass is being created, so it
        # cannot know which arguments are valid.

    @staticmethod
    def filter_args(args: OptArgs, format_name: str) -> OptArgs:
        """Filter the arguments for a registered format.

        Filter the arguments to only include the arguments that are valid for
        the given format name. This is useful when the args dictionary
        includes arguments for several formats, and not all of them are valid
        for the given format name. (The risk of using this function is that
        a misspelled arguement will be silently ignored, and the programming
        error will not be detected.)
        Args:
            args: The arguments to filter.
            format_name: The name identifier of the format class to filter
                         the arguments for.
        Returns:
            The filtered arguments.
        Raises:
            KeyError: If the format_name is not registered.
        """
        factory = MultiFormatFactory.i_get_factory()
        return factory.i_filter_args(args=args, format_name=format_name)

    def i_filter_args(self, args: OptArgs, format_name: str) -> OptArgs:
        """Internally filter the arguments for a registered format."""
        format_usage = self.i_get_usage(format_name=format_name)
        if args is None:
            return None
        assert args is not None
        ret: OptArgsDict = {}
        for arg_name in args:
            if arg_name in format_usage.mandatory_args:
                ret[arg_name] = args[arg_name]  # type: ignore[literal-required] # noqa: E501
            elif arg_name in format_usage.optional_args:
                ret[arg_name] = args[arg_name]  # type: ignore[literal-required] # noqa: E501
            elif arg_name in COMMON_ARGS:
                ret[arg_name] = args[arg_name]  # type: ignore[literal-required] # noqa: E501
        return ret

    @staticmethod
    def get_registered_formats(lower: bool = False,
                               upper: bool = False) -> list[str]:
        """Get a list of all registered format names.

        Always includes the correct case for the format names in the returned
        list. If lower or upper is True, also includes those cases of the
        format names in the returned list. (Including lower case and upper
        case variants is probably not a good idea when printint the list
        for a human user, but it is useful when checking if a format name
        is in the allowed list of format names.)
        Args:
            lower: If True, also include the format name in lower case.
            upper: If True, also include the format name in upper case.
        Returns:
            A list of registered format name strings.
        """
        factory = MultiFormatFactory.i_get_factory()
        return factory.i_get_registered_formats(lower=lower, upper=upper)

    def i_get_registered_formats(self, lower: bool = False,
                                 upper: bool = False) -> list[str]:
        """Internally get a list of registered format names."""
        sorted_names = sorted(list(self._registry.keys()))
        ret: list[str] = []
        for name in sorted_names:
            ret.append(name)
            if lower and name != name.lower():
                ret.append(name.lower())
            if upper and name != name.upper():
                ret.append(name.upper())
        return ret

    @staticmethod
    def get_usage(format_name: str) -> FormatterDescriptor:
        """Get the usage information for a registered format.

        Args:
            format_name: The name identifier of the format class to get
                         the usage information for.
        Returns:
            The usage information for the requested format.
        Raises:
            KeyError: If the format_name is not registered.
        """
        factory = MultiFormatFactory.i_get_factory()
        return factory.i_get_usage(format_name=format_name)

    def i_get_usage(self, format_name: str) -> FormatterDescriptor:
        """Internally get the usage information for a registered format."""
        if format_name in self._usage:
            return self._usage[format_name]
        if format_name.lower() not in self._lower2correct:
            raise KeyError(
                f'Format "{format_name}" is not registered. ' +
                'Available formats: ' +
                f'{", ".join(sorted(list(self._registry.keys())))}'
            )
        correct_name = self._lower2correct[format_name.lower()]
        return self._usage[correct_name]


def create_mf(format_name: str, file_name: PathLike,
              url_as_text: bool = False,
              args: OptArgs = None) -> MultiFormat:
    """Create an instance of a registered MultiFormat subclass.

    Intended to be used as context manager, using a with statement.
    This is a shortcut for MultiFormatFactory.create().
    Args:
        format_name: The name identifier of the format class to create.
        file_name: The file path to pass to the MultiFormat constructor.
        url_as_text: Format URLs as text not clickable URLs.
        args: additional arguments to pass to the MultiFormat constructor.
    Returns:
        An instance of the requested MultiFormat subclass.
    Raises:
        KeyError: If the format_name is not registered.
    """
    return MultiFormatFactory.create(format_name=format_name,
                                     file_name=file_name,
                                     url_as_text=url_as_text,
                                     args=args)


def filter_args_mf(args: OptArgs, format_name: str) -> OptArgs:
    """Filter the arguments for a registered format.

    This is a shortcut for MultiFormatFactory.filter_args().
    Filter the arguments to only include the arguments that are valid for
    the given format name. This is useful when the args dictionary includes
    arguments for several formats, and not all of them are valid for the given
    format name. (The risk of using this function is that a misspelled
    arguement will be silently ignored, and the programming error will not be
    detected.)
    Args:
        args: The arguments to filter.
        format_name: The name identifier of the format class to filter
                     the arguments for.
    Returns:
        The filtered arguments.
    Raises:
        KeyError: If the format_name is not registered.
    """
    return MultiFormatFactory.filter_args(args=args, format_name=format_name)


def list_registered_mf(lower: bool = False,
                       upper: bool = False) -> list[str]:
    """Get a list of all registered format names.

    This is a shortcut for MultiFormatFactory.get_registered_formats().
    Always includes the correct case for the format names in the returned
    list. If lower or upper is True, also includes those cases of the
    format names in the returned list. (Including lower case and upper
    case variants is probably not a good idea when printint the list
    for a human user, but it is useful when checking if a format name
    is in the allowed list of format names.)
    Args:
        lower: If True, also include the format name in lower case.
        upper: If True, also include the format name in upper case.
    Returns:
        A list of registered format name strings.
    """
    return MultiFormatFactory.get_registered_formats(lower=lower,
                                                     upper=upper)


def usage_mf(format_name: str) -> FormatterDescriptor:
    """Get the usage information for a registered format.

    This is a shortcut for MultiFormatFactory.get_usage().
    Args:
        format_name: The name identifier of the format class to get the
                     usage information for.
    Returns:
        The usage information for the requested format.
    Raises:
        KeyError: If the format_name is not registered.
    """
    return MultiFormatFactory.get_usage(format_name=format_name)


def register_mf(format_class: type[MultiFormat]) -> None:
    """Register a MultiFormat subclass with the factory.

    This is a shortcut for MultiFormatFactory.register().
    Args:
        format_class: The MultiFormat subclass to register.
    Raises:
        ValueError: If the format_class is not a subclass of MultiFormat.
        KeyError: If the format_name is already registered.
    """
    MultiFormatFactory.register(format_class=format_class)
