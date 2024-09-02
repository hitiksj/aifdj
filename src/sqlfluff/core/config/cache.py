"""Low level routines for config file loading and caching."""

import os.path
import sys
from typing import Optional

from sqlfluff.core.config.ini import load_ini_string
from sqlfluff.core.config.removed import validate_config_dict_for_removed
from sqlfluff.core.config.toml import load_toml_file_config
from sqlfluff.core.config.types import ConfigMappingType
from sqlfluff.core.errors import SQLFluffUserError
from sqlfluff.core.helpers.string import (
    split_comma_separated_string,
)

if sys.version_info >= (3, 9):
    from functools import cache
else:  # pragma: no cover
    from functools import lru_cache

    # With maxsize set to `None`, the lru_cache approximates what the later
    # introduced `cache` does. We don't need to worry too much about overflow
    # as config files are usually small, and sqlfluff is not often a long
    # lived process.
    cache = lru_cache(maxsize=None)


COMMA_SEPARATED_PATH_KEYS = ("load_macros_from_path", "loader_search_path")
RESOLVE_PATH_SUFFIXES = ("_path", "_dir")
ALLOWABLE_LAYOUT_CONFIG_KEYS = (
    "spacing_before",
    "spacing_after",
    "spacing_within",
    "line_position",
    "align_within",
    "align_scope",
)


def _load_raw_file_as_dict(filepath: str) -> ConfigMappingType:
    """Loads the raw dict object from file without interpolation."""
    _, file_extension = os.path.splitext(filepath)
    filename = os.path.basename(filepath)
    if filename == "pyproject.toml":
        return load_toml_file_config(filepath)
    # If it's not a pyproject file, assume that it's an ini file.
    with open(filepath, mode="r") as file:
        return load_ini_string(file.read())


def _resolve_path(filepath: str, val: str) -> str:
    """Try to resolve a path found in a config value."""
    # Make the referenced path.
    ref_path = os.path.join(os.path.dirname(filepath), val)
    # Check if it exists, and if it does, replace the value with the path.
    return ref_path if os.path.exists(ref_path) else val


def _resolve_paths_in_config(
    config: ConfigMappingType, filepath: str, logging_reference: Optional[str] = None
):
    """Attempt to resolve any paths found in the config file.

    NOTE: This method is recursive to crawl the whole config object,
    and also mutates the underlying config object rather than returning it.
    """
    log_filename: str = logging_reference or filepath
    for key, val in config.items():
        # If it's a dict, recurse.
        if isinstance(val, dict):
            _resolve_paths_in_config(val, filepath, logging_reference=logging_reference)
        # If it's a potential multi-path, split, resolve and join
        if key.lower() in COMMA_SEPARATED_PATH_KEYS:
            assert isinstance(
                val, str
            ), f"Value for {key} in {log_filename} must be a string not {type(val)}."
            paths = split_comma_separated_string(val)
            val = ",".join(_resolve_path(filepath, path) for path in paths)
        # It it's a single path key, resolve it.
        elif key.lower().endswith(RESOLVE_PATH_SUFFIXES):
            assert isinstance(
                val, str
            ), f"Value for {key} in {log_filename} must be a string not {type(val)}."
            val = _resolve_path(filepath, val)


def _validate_layout_config(config: ConfigMappingType, logging_reference: str) -> None:
    """Validate the layout config section of the config.

    We check for valid key values and for the depth of the
    structure.

    NOTE: For now we don't check that the "type" is a valid one
    to reference, or that the values are valid. For the values,
    these are likely to be rejected by the layout routines at
    runtime. The last risk area is validating that the type is
    a valid one, but that should be handled by the same as the above.
    """
    layout_section = config.get("layout", {})
    if not layout_section:
        return None

    preamble = f"Config file {logging_reference!r} set an invalid `layout` option. "
    reference = (
        "See https://docs.sqlfluff.com/en/stable/perma/layout.html"
        "#configuring-layout for more details."
    )

    if not isinstance(layout_section, dict):
        raise SQLFluffUserError(
            preamble
            + f"Found value {layout_section!r} instead of a valid layout section. "
            + reference
        )

    # The sections within layout can only be "type" (currently).
    non_type_keys = set(layout_section.keys()) - set(("type",))
    type_section = layout_section.get("type", {})
    if non_type_keys or not type_section or not isinstance(type_section, dict):
        raise SQLFluffUserError(
            preamble
            + "Only sections of the form `sqlfluff:layout:type:...` are valid. "
            + reference
        )

    for layout_type, layout_section in type_section.items():
        if not isinstance(layout_section, dict):
            raise SQLFluffUserError(
                preamble
                + f"Layout config for {layout_type!r} is invalid. Expected a section. "
                + reference
            )

        invalid_keys = set(layout_section.keys()) - set(ALLOWABLE_LAYOUT_CONFIG_KEYS)
        if invalid_keys:
            raise SQLFluffUserError(
                preamble
                + f"Layout config for type {layout_type!r} is invalid. "
                + f"Found the following invalid keys: {invalid_keys}. "
                + reference
            )

        for key in ALLOWABLE_LAYOUT_CONFIG_KEYS:
            if key in layout_section:
                if isinstance(layout_section[key], dict):
                    raise SQLFluffUserError(
                        preamble
                        + f"Layout config for type {layout_type!r} is invalid. "
                        + "Found the an unexpected section rather than "
                        + f"value for {key}. "
                        + reference
                    )


def validate_config_dict(config: ConfigMappingType, logging_reference: str) -> None:
    """Validate a config dict.

    Currently we validate:
    - Removed and deprecated values.
    - Layout configuration structure.

    Using this method ensures that any later validation will also be applied.

    NOTE: Some of these method may mutate the config object where they are
    able to correct issues.
    """
    # Validate the config for any removed values
    validate_config_dict_for_removed(config, logging_reference)
    # Validate layout section
    _validate_layout_config(config, logging_reference)


@cache
def load_config_file_as_dict(filepath: str) -> ConfigMappingType:
    """Load the given config file into a dict and validate.

    This method is cached to mitigate being called multiple times.

    This doesn't manage the combination of config files within a nested
    structure, that happens further up the stack.
    """
    raw_config = _load_raw_file_as_dict(filepath)

    # The raw loaded files have some path interpolation which is necessary.
    _resolve_paths_in_config(raw_config, filepath)
    # Validate
    validate_config_dict(raw_config, filepath)

    # Return dict object (which will be cached)
    return raw_config


@cache
def load_config_string_as_dict(
    config_string: str, working_path: str, logging_reference: str
) -> ConfigMappingType:
    """Load the given config string and validate.

    This method is cached to mitigate being called multiple times.

    This doesn't manage the combination of config files within a nested
    structure, that happens further up the stack. The working path is
    necessary to resolve any paths in the config file.
    """
    raw_config = load_ini_string(config_string)

    # The raw loaded files have some path interpolation which is necessary.
    _resolve_paths_in_config(
        raw_config, working_path, logging_reference=logging_reference
    )
    # Validate
    validate_config_dict(raw_config, logging_reference)

    # Return dict object (which will be cached)
    return raw_config