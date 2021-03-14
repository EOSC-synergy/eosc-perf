import os
import unittest

from flask import Flask

from dotenv import load_dotenv

from eosc_perf.configuration import configuration
from eosc_perf.controller.authenticator import Authenticator, configure_authenticator, read_file_content, authenticator


class AuthenticatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.flask = Flask('test')

    def tearDown(self) -> None:
        pass

    def test_nonexistent_file_read(self):
        self.assertIsNone(read_file_content('ce_fichier_nexiste_pas.txt'))

    @unittest.skip("requires set-up paths")
    def test_configuration(self):
        load_dotenv('valid.env')
        configuration.reload()
        self.assertIsNone(configure_authenticator(self.flask))

        configuration.reload()
        configuration.set('oidc_client_secret_file', 'SET_ME')
        self.assertRaises(ValueError, configure_authenticator, self.flask)

        configuration.reload()
        configuration.set('secret_key_file', 'SET_ME')
        self.assertRaises(ValueError, configure_authenticator, self.flask)

        configuration.reload()
        configuration.set('oidc_client_id', 'SET_ME')
        self.assertRaises(ValueError, configure_authenticator, self.flask)

        configuration.reload()
        configuration.set('oidc_redirect_hostname', 'SET_ME')
        self.assertRaises(ValueError, configure_authenticator, self.flask)

        configuration.reload()
        configuration.set('debug', 'False')
        self.assertIsNone(configure_authenticator, self.flask)

    @unittest.skip("requires properly configured .env")
    def test_authentication_redirect(self):
        authenticator.authenticate_user()


if __name__ == '__main__':
    unittest.main()
