"""Configuration structure for config files to the application."""
import os
import yaml

def load_defaults():
    """Get default configuration values."""
    defaults = {
        'debug': False,
        'debug-db-reset': False,
        'debug-db-dummy-items': True,
        'database-path': '',
        'admin_affiliations': ['example@kit.edu'],
        'debug_admin_affiliations': ['example2@kit.edu'],
        'oidc_client_secret': '',
        'oidc_redirect_hostname': 'localhost',
        'upload_license_filename': 'upload_license.txt',
        'infrastructure_href': 'https://example.com'
    }

    return defaults

def load_config():
    """Load the config file from 'config.ini'."""
    defaults = load_defaults()
    if os.path.exists('config.yaml'):
        with open('config.yaml') as file:
            config = yaml.safe_load(file.read())
        if config is None:
            print("Could not read config.yaml!")

        for key, value in defaults.items():
            if key not in config:
                config[key] = str(value)
        return config

    return defaults


configuration = load_config()
