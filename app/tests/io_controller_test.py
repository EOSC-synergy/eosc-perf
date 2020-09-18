"""
This module contains unit tests for the IOController class
"""
from time import time
import unittest
from flask import Flask, session
from app.model.database import configure_database
from app.controller.authenticator import configure_authenticator
from app.controller.io_controller import controller
from app.configuration import configuration

class IOControllerTest(unittest.TestCase):

    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()
        self.app.secret_key = '!secret'

        # use memory database, reset entirely every time
        configuration.reload()
        configuration.set('database-path', '')
        configuration.set('debug', True)
        configuration.set('debug-db-reset', True)
        configure_authenticator(self.app)
        configure_database(self.app)

        self.controller = controller

    def tearDown(self):
        """Called after each test."""
        del self.controller
        del self.app

    def test_submit_result(self):
        pass

    def test_get_full_name(self):
        with self.app.test_request_context():
            session['user'] = {'info': {'name': 'John Doe'}}
            self.assertEqual(self.controller.get_full_name(), 'John Doe')
            session.pop('user', None)
        with self.app.test_request_context():
            self.assertEqual(self.controller.get_full_name(), None)

    def test_get_email(self):
        with self.app.test_request_context():
            session['user'] = {'info': {'email': 'email@kit.edu'}}
            self.assertEqual(self.controller.get_email(), 'email@kit.edu')
            session.pop('user', None)
        with self.app.test_request_context():
            self.assertEqual(self.controller.get_email(), None)

    def test_get_user_id(self):
        with self.app.test_request_context():
            session['user'] = {'sub': "id"}
            self.assertEqual(self.controller.get_user_id(), "id")
            session.pop('user', None)
        with self.app.test_request_context():
            self.assertEqual(self.controller.get_user_id(), None)

    def test_is_admin_fail_no_affiliations(self):
        with self.app.test_request_context():
            session['user'] = {'exp': time() + 3600}
            self.assertFalse(self.controller.is_admin())
            session.pop('user', None)

    def test_is_admin_fail_wrong_affiliations(self):
        with self.app.test_request_context():
            session['user'] = {'exp': time() + 3600}
            session['user']['info'] = {}
            session['user']['info']['edu_person_scoped_affiliations'] = ["student@mit.edu"]
            self.assertFalse(self.controller.is_admin())
            session.pop('user', None)

    def test_is_admin_one_afilliation(self):
        with self.app.test_request_context():
            session['user'] = {'exp': time() + 3600}
            admin_afill = configuration.get('debug_admin_affiliations')[:1]
            session['user']['info'] = {}
            session['user']['info']['edu_person_scoped_affiliations'] = admin_afill
            self.assertTrue(self.controller.is_admin())
            session.pop('user', None)

    def test_is_admin_all_afilliations(self):
        admin_affiliations = configuration.get('debug_admin_affiliations')
        admin_affiliations += ["test@test.edu", "hacker@1337.ccc"]
        configuration.set("debug_admin_affiliations", admin_affiliations)
        with self.app.test_request_context():
            session['user'] = {'exp': time() + 3600}
            session['user']['info'] = {}
            session['user']['info']['edu_person_scoped_affiliations'] = admin_affiliations
            self.assertTrue(self.controller.is_admin())
            session.pop('user', None)

    def test_authenticated(self):
        """Tests if IOController returns True when logged
           in during is_authenticated method call"""
        with self.app.test_request_context():
            session['user'] = {'exp': time() + 3600}
            self.assertTrue(self.controller.is_authenticated())
            session.pop('user', None)

    def test_not_authenticated(self):
        """Tests if IOController returns False when not logged
           in during is_authenticated method call"""
        with self.app.test_request_context():
            self.assertFalse(self.controller.is_authenticated())

if __name__ == '__main__':
    unittest.main()
