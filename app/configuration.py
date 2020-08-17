"""Configuration structure for config files to the application."""
import os
import yaml

def load_config():
    """Load the config file from 'config.ini'."""
    defaults = {
        'debug': False,
        'database-path': 'sqlite.db',
        'admin_affiliations': ['example@kit.edu'],
        'debug_admin_affiliations': ['example2@kit.edu'],
        'oidc_client_secret': '',
        'oidc_redirect_hostname': 'localhost',
        'upload_license_filename': 'upload_license.txt'
    }
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
