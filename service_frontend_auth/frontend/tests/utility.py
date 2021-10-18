def setup_test_config(configuration):
    configuration.reset()
    configuration.set('database-path', '')
    configuration.set('debug', True)
    configuration.set('debug-db-reset', True)
    configuration.set('oidc_client_id', 'test-app')
    configuration.set('oidc_client_secret_file', '../oidc_secret.txt')
    configuration.set('cookie_key_file', '../cookie_secret.txt')
