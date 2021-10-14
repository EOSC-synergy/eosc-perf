"""This module provides the configuration loading system ConfigHandler.
"""
import json
import os
from json import JSONDecodeError
from typing import Any, Optional

from dotenv import load_dotenv


def _get_var(env_name: str, env_type: type = str) -> Optional[Any]:
    """Fetch a value from the environment.

    Args:
        env_name (str): The name of the environment variable to get.
        env_type (type): The type to interpret the variable as.
            Available types: str, int, bool, list (parsed as json array)
    Returns:
        Optional[Any]: The desired value, or None if it is empty or there was an error in parsing.
    """
    if env_name not in os.environ:
        return None
    if env_type == int:
        try:
            return int(os.environ[env_name])
        except TypeError:
            return None
    if env_type == list:
        try:
            return json.loads(os.environ[env_name])
        except JSONDecodeError:
            return None
    if env_type == bool:
        if os.environ[env_name].lower() in ['1', 'true']:
            return True
        return False
    return os.environ[env_name]


def _get_var_or(env_name: str, alternative: Any, env_type: type = str) -> Any:
    value = _get_var(env_name, env_type)
    if value is None:
        return alternative
    return value


class ConfigHandler:
    """ConfigHandler provides getters and setters for configuration values.

    On application start, all configuration values are loaded from defaults.
    To load environment variables from the environment, call reload().
    """

    config: dict = {}

    DEFAULTS: dict = {
        'cookie_key_file': 'SET_ME',
        'oidc_client_secret_file': 'SET_ME',
        'oidc_client_id': 'SET_ME',
        'oidc_redirect_hostname': 'localhost',
        'admin_entitlement': 'urn:mace:egi.eu:group:mteam.data.kit.edu:role=member',
        'debug': False,
        'debug_admin_entitlement': 'urn:mace:egi.eu:group:mteam.data.kit.edu:role=member',
    }

    def __init__(self):
        """Set up a new configuration."""
        self.reset()
        if os.path.exists('.env'):
            load_dotenv('.env')

    def _load_config(self, load_env: bool = False) -> dict:
        """Load the config, optionally from the environment.

        Args:
            load_env (bool): True if the configuration should be read the environment.
        Returns:
            dict: A dictionary containing all loaded configuration values.
        """
        config = self.DEFAULTS

        if load_env:
            env_values: dict = {
                'cookie_key_file': _get_var('COOKIE_KEY_FILE'),
                'oidc_client_secret_file': _get_var('OIDC_CLIENT_SECRET_FILE'),
                'oidc_client_id': _get_var('OIDC_CLIENT_ID'),
                'oidc_redirect_hostname': _get_var('DOMAIN'),
                'admin_entitlement': _get_var('ADMIN_ENTITLEMENTS'),
                'debug': _get_var('EOSC_PERF_DEBUG', bool),
                'debug_admin_entitlement': _get_var('EOSC_PERF_DEBUG_ADMIN_ENTITLEMENTS'),
            }

            for key, value in self.DEFAULTS.items():
                env_value = env_values[key]
                if env_value is None:
                    env_value = value
                config[key] = env_value

        return config

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
        """Reset and reload values from file.

        This method is not run by default so that tests do not accidentally load paths to real data they could
        overwrite, such as a sqlite database file.
        """
        self.config = self._load_config(True)


configuration: ConfigHandler = ConfigHandler()
