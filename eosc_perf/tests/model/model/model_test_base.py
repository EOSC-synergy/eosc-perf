import unittest

from flask import Flask

from eosc_perf.configuration import configuration
from eosc_perf.model.database import configure_database
from eosc_perf.model.facade import DatabaseFacade
from eosc_perf.tests.utility import setup_test_config


class FacadeTestBase(unittest.TestCase):
    """Tests for facade."""
    tested_uploader_id: str = 'test_user'
    tested_uploader_email: str = 'test@example.com'
    tested_uploader_name: str = 'test user'
    tested_benchmark_name: str = 'foobar/bazbutt'
    tested_site_name: str = 'iamasitename'
    tested_site_address: str = 'localhost'
    tested_site_description: str = 'hello world'
    tested_tag_name: str = 'testtag'
    tested_flavor_name: str = 'test-flavor'

    tested_result_params = [tested_uploader_id, tested_site_name, tested_benchmark_name, tested_flavor_name]
    tested_uploader_params = [tested_uploader_id, tested_uploader_name, tested_uploader_email]
    tested_site_params = [tested_site_name, tested_site_address]

    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()

        # use memory database, reset entirely every time
        setup_test_config(configuration)
        configure_database(self.app)

        # facade
        self.facade = DatabaseFacade()

    def tearDown(self):
        """Called after each test."""
        del self.facade
        del self.app

    def _add_result_data(self):
        self.assertTrue(self.facade.add_uploader(*self.tested_uploader_params))
        self.assertTrue(self.facade.add_benchmark(self.tested_benchmark_name, self.tested_uploader_id))
        self.assertTrue(self.facade.add_site(*self.tested_site_params))
        success, uuid = self.facade.add_flavor(self.tested_flavor_name, "hello", self.tested_site_name)
        self.assertTrue(success)

        return {
            'flavor_uuid': uuid
        }
