
import yaml

def load_config():
    """Load the config file from 'config.ini'."""
    defaults = {
        'debug': False,
        'database-path': 'sqlite.db',
        'oidc_client_secret': ''
    }
    with open('config.yaml') as file:
        try:
            config = yaml.safe_load(file.read())
        except:
            print("Could not read config.yaml!")
    
    for key, value in defaults.items():
        if key not in config:
            config[key] = str(value)
    
    return config

configuration = load_config()