"""Configuration structure for config files to the application."""
import os
from typing import Any

import yaml


class ConfigHandler:
    """Helper for config state."""

    config: dict = {}

    def __init__(self):
        """Set up a new configuration."""
        self.reset()

    def _get_defaults(self) -> dict:
        """Get default configuration values.

        Returns:
            dict: A dictionary containing default configuration values.
        """
        defaults = {
            'debug': False,
            'debug-db-reset': True,
            'debug-db-dummy-items': True,
            'database-path': '',
            'admin_entitlements': [],
            'debug_admin_entitlements': ['urn:mace:egi.eu:group:mteam.data.kit.edu:role=member'],
            'secret_key': '!secret',
            'oidc_client_secret': '',
            'oidc_redirect_hostname': 'localhost',
            'oidc_client_id': 'SET_ME',
            'upload_license_filename': 'upload_license.txt',
            'infrastructure_href': 'https://example.com'
        }

        return defaults

    def _load_config(self, load_file: bool = False) -> dict:
        """Load the config file from 'config.ini'.

        Args:
            load_file (bool): True if the configuration should be read from `config.ini`.
        Returns:
            dict: A dictionary containing all loaded configuration values.
        """
        defaults = self._get_defaults()
        if load_file and os.path.exists('config.yaml'):
            with open('config.yaml') as file:
                config = yaml.safe_load(file.read())
            if config is None:
                print("Could not read config.yaml!")

            for key, value in defaults.items():
                if key not in config:
                    config[key] = str(value)
            return config

        return defaults

    def set(self, tag: str, value: Any):
        """Set a value.

        Args:
            tag (str): The configuration value to change.
            value (Any): The new value to set it to.
        """
        self.config[tag] = value

    def get(self, tag: str) -> Any:
        """Get a value.

        Args:
            tag (str): The configuration value to get.
        Returns:
            Any: The value of the requested configuration value.
        """
        if tag not in self.config:
            raise ValueError("unknown config value requested")
        return self.config[tag]

    def reset(self):
        """Reset all values to defaults."""
        self.config = self._load_config(False)

    def reload(self):
        """Reset and reload values from file."""
        self.config = self._load_config(True)


configuration: ConfigHandler = ConfigHandler()
