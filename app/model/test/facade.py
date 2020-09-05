import unittest
from flask import Flask
from ..database import configure_database
from ..facade import DatabaseFacade
from ...configuration import configuration, load_defaults

configuration = load_defaults()

class FacadeTest(unittest.TestCase):
    """Tests for facade."""
    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()

        # use memory database, reset entirely every time
        configuration['database-path'] = ''
        configuration['debug'] = True
        configuration['debug-db-reset'] = True
        configure_database(self.app, configuration)

        # facade
        self.facade = DatabaseFacade()
    
    def tearDown(self):
        """Called after each test."""
        del self.facade
        del self.app

    def test_add_site(self):
        self.assertTrue(self.facade.add_site('{"short_name": "test", "address": "example.com"}'))
    
    def test_add_invalid_site(self):
        with self.assertRaises(ValueError):
            self.facade.add_site('{"short_name": "", "address": ""}')

if __name__ == '__main__':
    unittest.main()
