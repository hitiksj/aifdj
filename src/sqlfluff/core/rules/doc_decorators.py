"""A collection of decorators to modify rule docstrings for Sphinx."""

from src.sqlfluff.core.rules.config_info import STANDARD_CONFIG_INFO_DICT
from src.sqlfluff.core.rules.base import rules_logger  # noqa


def document_fix_compatible(cls):
    """Mark the rule as fixable in the documentation."""
    cls.__doc__ = cls.__doc__.replace("\n", "\n\n``sqlfluff fix`` compatible.\n", 1)
    return cls


def document_configuration(cls, ruleset="std"):
    """Add a 'Configuration' section to a Rule docstring.

    Utilize the the metadata in config_info to dynamically
    document the configuration options for a given rule.

    This is a little hacky, but it allows us to propagate configuration
    options in the docs, from a single source of truth.
    """
    if ruleset == "std":
        config_info = STANDARD_CONFIG_INFO_DICT
    else:
        raise (
            NotImplementedError(
                "Add another config info dict for the new ruleset here!"
            )
        )

    config_doc = "\n    | **Configuration**"
    try:
        for keyword in cls.config_keywords:
            try:
                info_dict = config_info[keyword]
            except KeyError:
                raise KeyError(
                    "Config value {!r} for rule {} is not configured in `config_info`.".format(
                        keyword, cls.__name__
                    )
                )
            config_doc += "\n    |     `{0}`: {1}. Must be one of {2}.".format(
                keyword, info_dict["definition"], info_dict["validation"]
            )
            config_doc += "\n    |"
    except AttributeError:
        rules_logger.info("No config_keywords defined for {0}".format(cls.__name__))
        return cls
    # Add final blank line
    config_doc += "\n"
    # Add the configuration section immediately after the class description
    # docstring by inserting after the first line break, or first period,
    # if there is no line break.
    end_of_class_description = "." if "\n" not in cls.__doc__ else "\n"

    cls.__doc__ = cls.__doc__.replace(end_of_class_description, "\n" + config_doc, 1)
    return cls
