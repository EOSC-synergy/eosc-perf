"""
This module contains unit tests for the IOController class
"""
from time import time
import unittest
from flask import Flask, session
from ...model.database import configure_database
from ..io_controller import controller
from ...configuration import configuration

class FacadeTest(unittest.TestCase):

    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()
        self.app.secret_key = '!secret'

        # use memory database, reset entirely every time
        configuration.reset()
        configure_database(self.app)

        # facade
        self.controller = controller

    def tearDown(self):
        """Called after each test."""
        del self.controller
        del self.app

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
