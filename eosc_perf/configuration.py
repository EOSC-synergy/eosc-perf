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


class ConfigHandler:
    """ConfigHandler provides getters and setters for configuration values.

    On application start, all configuration values are loaded from defaults.
    To load environment variables from the environment, call reload().
    """

    config: dict = {}

    DEFAULTS: dict = {
        'secret_key_file': 'SET_ME',
        'oidc_client_secret_file': 'SET_ME',
        'oidc_client_id': 'SET_ME',
        'oidc_redirect_hostname': 'localhost',
        'admin_entitlements': ['urn:mace:egi.eu:group:mteam.data.kit.edu:role=member'],
        'infrastructure_href': 'https://example.com',
        'database-path': '',  # diverge from example to use in-memory database
        'debug': False,
        'debug-db-reset': False,
        'debug-db-demo-items': False,
        'debug-logged-in-is-admin': False,
        'debug_admin_entitlements': ['urn:mace:egi.eu:group:mteam.data.kit.edu:role=member'],
        'support_email': 'perf-support@lists.kit.edu'
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
                'secret_key_file': _get_var('EOSC_PERF_COOKIE_CRYPT_KEY_PATH'),
                'oidc_client_secret_file': _get_var('EOSC_PERF_OIDC_CLIENT_SECRET_PATH'),
                'oidc_client_id': _get_var('EOSC_PERF_OIDC_CLIENT_ID'),
                'oidc_redirect_hostname': _get_var('DOMAIN'),
                'admin_entitlements': _get_var('EOSC_PERF_ADMIN_ENTITLEMENTS', list),
                'infrastructure_href': _get_var('EOSC_PERF_INFRASTRUCTURE_HREF'),
                'database-path': _get_var('EOSC_PERF_DB_PATH'),
                'debug': _get_var('EOSC_PERF_DEBUG', bool),
                'debug-db-reset': _get_var('EOSC_PERF_DEBUG_DB_RESET', bool),
                'debug-db-demo-items': _get_var('EOSC_PERF_DEBUG_DB_DEMO_ITEMS', bool),
                'debug-logged-in-is-admin': _get_var('EOSC_PERF_DEBUG_LOGGED_IN_IS_ADMIN', bool),
                'debug_admin_entitlements': _get_var('EOSC_PERF_DEBUG_ADMIN_ENTITLEMENTS', list),
                'support_email': _get_var('EOSC_PERF_SUPPORT_EMAIL')
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
