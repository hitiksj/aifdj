"""Defines the specification to implement a plugin."""

import pluggy
from abc import abstractmethod
from sqlfluff.core.plugin import plugin_base_name
from typing import List, Type
from sqlfluff.core.rules import BaseRule

hookspec = pluggy.HookspecMarker(plugin_base_name)


class PluginSpec:
    """Defines the method signatures for plugin implementations."""

    @hookspec
    @abstractmethod
    def get_rules(self) -> List[Type[BaseRule]]:
        """Get plugin rules."""

    @hookspec
    @abstractmethod
    def load_default_config(self) -> dict:
        """Loads the default configuration for the plugin."""

    @hookspec
    @abstractmethod
    def get_configs_info(self) -> dict:
        """Get rule config validations and descriptions."""
