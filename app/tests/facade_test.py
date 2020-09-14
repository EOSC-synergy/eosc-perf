"""Tests for facade behaviour."""
import unittest
import json
from flask import Flask
from ..model.database import configure_database
from ..model.facade import DatabaseFacade
from ..configuration import configuration, load_defaults

configuration = load_defaults()

class FacadeTest(unittest.TestCase):
    """Tests for facade."""
    tested_uploader_id: str = 'test_user'
    tested_benchmark_name: str = 'foobar/bazbutt'
    tested_site_name: str = 'iamasitename'

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

    def test_add_uploader_valid(self):
        """Test valid call to add_uploader."""
        meta = {
            'id': self.tested_uploader_id,
            'name': 'user',
            'email': 'test@example.com'
        }
        self.assertTrue(self.facade.add_uploader(json.dumps(meta)))

    def test_add_uploader_invalid(self):
        """Test various invalid calls to add_uploader."""
        # invalid json
        with self.assertRaises(json.JSONDecodeError):
            self.facade.add_uploader('{invalid json}')

        # empty id
        meta = {
            'id': '',
            'user': 'name',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # missing id
        meta = {
            'user': 'name',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # empty user
        meta = {
            'id': 'random',
            'user': '',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # missing user
        meta = {
            'id': 'random',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # empty email
        meta = {
            'id': 'random',
            'user': 'name',
            'email': ''
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # missing email
        meta = {
            'id': 'random',
            'user': 'name',
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # duplicate
        meta = {
            'id': self.tested_uploader_id,
            'name': 'user',
            'email': 'test@example.com'
        }
        self.test_add_uploader_valid()
        self.assertFalse(self.facade.add_uploader(json.dumps(meta)))

    def test_add_benchmark_valid(self):
        """Test valid call to add_benchmark."""
        # add necessary uploader
        self.test_add_uploader_valid()

        self.assertTrue(self.facade.add_benchmark(self.tested_benchmark_name, self.tested_uploader_id))

    def test_add_benchmark_invalid(self):
        """Test various invalid calls to add_benchmark."""
        # too short docker_name
        with self.assertRaises(ValueError):
            self.facade.add_benchmark('ab', self.tested_uploader_id)

        # empty uploader
        with self.assertRaises(ValueError):
            self.facade.add_benchmark(self.tested_benchmark_name, '')

        # unknown uploader
        with self.assertRaises(ValueError):
            self.facade.add_benchmark(self.tested_benchmark_name, 'hopefully nobody has this id')

        # duplicate
        self.test_add_benchmark_valid()
        self.assertFalse(self.facade.add_benchmark(self.tested_benchmark_name, self.tested_uploader_id))

    def test_add_site_valid(self):
        """Test valid call to add_site."""
        meta = {
            'short_name': self.tested_site_name,
            'address': 'example.com'
        }
        self.assertTrue(self.facade.add_site(json.dumps(meta)))

    def test_add_site_invalid(self):
        """Test various invalid calls to add_site."""

        # invalid json
        with self.assertRaises(json.JSONDecodeError):
            self.facade.add_site('{invalid json}')

        # missing name
        meta = {
            'address': 'example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        # empty name
        meta = {
            'short_name': '',
            'address': 'example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        # missing address
        meta = {
            'short_name': self.tested_site_name
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        # empty address
        meta = {
            'short_name': self.tested_site_name,
            'address': ''
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        meta = {
            'short_name': self.tested_site_name,
            'address': 'example.com'
        }
        self.test_add_site_valid()
        self.assertFalse(self.facade.add_site(json.dumps(meta)))


if __name__ == '__main__':
    unittest.main()
