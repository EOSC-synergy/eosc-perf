import unittest
from time import time

from dotenv import load_dotenv
from flask import Flask, session
from frontend.configuration import configuration
from frontend.controller.authenticator import read_file_content, Authenticator, MockAuthenticator
from frontend.controller.io_controller import IOController
from frontend.tests.utility import setup_test_config

mock_authenticator = MockAuthenticator()


class AuthenticatorTests(unittest.TestCase):
    TEST_USER: dict = {
        'exp': time() + 3600,
        'sub': mock_authenticator.get_user_id(),
        'info': {
            'email': mock_authenticator.get_email(),
            'name': mock_authenticator.get_full_name()
        }
    }

    def setUp(self) -> None:
        self.flask = Flask('test')
        self.flask.config['DEBUG'] = True
        self.flask.app_context().push()
        self.flask.secret_key = '!secret'

        setup_test_config(configuration)
        self.controller = IOController()
        self.controller.load_authenticator(self.flask)

    def tearDown(self) -> None:
        pass

    def test_nonexistent_file_read(self):
        self.assertIsNone(read_file_content('ce_fichier_nexiste_pas.txt'))

    @unittest.skip("requires set-up paths")
    def test_configuration(self):
        load_dotenv('valid.env')
        configuration.reload()
        Authenticator(self.flask)

        configuration.reload()
        configuration.set('oidc_client_secret_file', 'SET_ME')
        self.assertRaises(ValueError, Authenticator, self.flask)

        configuration.reload()
        configuration.set('secret_key_file', 'SET_ME')
        self.assertRaises(ValueError, Authenticator, self.flask)

        configuration.reload()
        configuration.set('oidc_client_id', 'SET_ME')
        self.assertRaises(ValueError, Authenticator, self.flask)

        configuration.reload()
        configuration.set('oidc_redirect_hostname', 'SET_ME')
        self.assertRaises(ValueError, Authenticator, self.flask)

        configuration.reload()
        configuration.set('debug', 'False')
        self.assertIsNone(Authenticator, self.flask)

    def test_get_email(self):
        with self.flask.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_email(), self.TEST_USER["info"]["email"])
            self._logout()
        with self.flask.test_request_context():
            self.assertIsNone(self.controller.get_email())

    def test_get_full_name(self):
        with self.flask.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_full_name(), self.TEST_USER["info"]["name"])
            self._logout()
        with self.flask.test_request_context():
            self.assertIsNone(self.controller.get_full_name())

    def test_get_user_id(self):
        with self.flask.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_user_id(), self.TEST_USER["sub"])
            self._logout()
        with self.flask.test_request_context():
            self.assertIsNone(self.controller.get_user_id())

    def test_authenticate_not_authenticated(self):
        with self.flask.test_request_context():
            self.assertIsNotNone(self.controller.authenticate())

    def test_authenticate_already_authenticated(self):
        with self.flask.test_request_context():
            self._login_standard_user()
            self.assertIsNone(self.controller.authenticate())

    def test_is_admin_fail_no_affiliations(self):
        with self.flask.test_request_context():
            self._login_standard_user()
            self.assertFalse(self.controller.is_admin())

    def test_is_admin_fail_wrong_affiliations(self):
        with self.flask.test_request_context():
            self._login_standard_user()
            session['user']['info']['edu_person_scoped_affiliations'] = ["student@mit.edu"]
            self.assertFalse(self.controller.is_admin())

    def test_is_admin_one_entitlement(self):
        with self.flask.test_request_context():
            self._login_admin()
            self.assertTrue(self.controller.is_admin())

    def test_authenticated(self):
        """Tests if IOController returns True when logged
           in during is_authenticated method call"""
        with self.flask.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.is_authenticated())

    def test_not_authenticated(self):
        """Tests if IOController returns False when not logged
           in during is_authenticated method call"""
        with self.flask.test_request_context():
            self.assertFalse(self.controller.is_authenticated())

    @unittest.skip("requires properly configured .env")
    def test_authentication_redirect(self):
        self.controller.authenticator.redirect_to_authentication()

    def _login_standard_user(self):
        session['user'] = self.TEST_USER
        session['user']['info'].pop('eduperson_entitlement', None)

    def _login_admin(self):
        self._login_standard_user()
        admin_entitlement = configuration.get('debug_admin_entitlements')[:1]
        admin_entitlement[0] += '#aai.egi.eu'
        session['user']['info']['eduperson_entitlement'] = admin_entitlement

    @staticmethod
    def _logout():
        session.pop('user', None)


if __name__ == '__main__':
    unittest.main()
