"""Configuration structure for config files to the application."""
import os
import yaml

class ConfigHandler:
    """Helper for config state."""
    def __init__(self):
        self.config = {}
        self.reset()

    def _get_defaults(self):
        """Get default configuration values."""
        defaults = {
            'debug': False,
            'debug-db-reset': True,
            'debug-db-dummy-items': True,
            'database-path': '',
            'admin_affiliations': ['example@kit.edu'],
            'secret_key': '!secret',
            'debug_admin_affiliations': ['example2@kit.edu'],
            'oidc_client_secret': '',
            'oidc_redirect_hostname': 'localhost',
            'upload_license_filename': 'upload_license.txt',
            'infrastructure_href': 'https://example.com'
        }

        return defaults

    def _load_config(self, load_file: bool = False):
        """Load the config file from 'config.ini'."""
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

    def set(self, tag, value):
        """Set a value."""
        self.config[tag] = value

    def get(self, tag):
        """Get a value."""
        if not tag in self.config:
            raise ValueError("unknown config value requested")
        return self.config[tag]

    def reset(self):
        """Reset all values to defaults."""
        self.config = self._load_config(False)

    def reload(self):
        """Reset and reload values from file."""
        self.config = self._load_config(True)

configuration: ConfigHandler = ConfigHandler()
