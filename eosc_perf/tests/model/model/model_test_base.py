import unittest

from flask import Flask

from eosc_perf.configuration import configuration
from eosc_perf.model.database import configure_database
from eosc_perf.model.facade import DatabaseFacade
from eosc_perf.tests.utility import setup_test_config


class FacadeTestBase(unittest.TestCase):
    """Tests for facade."""
    TESTED_UPLOADER_ID: str = 'test_user'
    TESTED_UPLOADER_EMAIL: str = 'test@example.com'
    TESTED_UPLOADER_NAME: str = 'test user'
    TESTED_BENCHMARK_NAME: str = 'foobar/bazbutt'
    TESTED_SITE_NAME: str = 'iamasitename'
    TESTED_SITE_ADDRESS: str = 'localhost'
    TESTED_SITE_DESCRIPTION: str = 'hello world'
    TESTED_TAG_NAME: str = 'testtag'
    TESTED_FLAVOR_NAME: str = 'test-flavor'

    TESTED_RESULT_PARAMS = [TESTED_UPLOADER_ID, TESTED_SITE_NAME, TESTED_BENCHMARK_NAME, TESTED_FLAVOR_NAME]
    TESTED_UPLOADER_PARAMS = [TESTED_UPLOADER_ID, TESTED_UPLOADER_NAME, TESTED_UPLOADER_EMAIL]
    TESTED_SITE_PARAMS = [TESTED_SITE_NAME, TESTED_SITE_ADDRESS]

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
        self.assertTrue(self.facade.add_uploader(*self.TESTED_UPLOADER_PARAMS))
        self.assertTrue(self.facade.add_benchmark(self.TESTED_BENCHMARK_NAME, self.TESTED_UPLOADER_ID))
        self.assertTrue(self.facade.add_site(*self.TESTED_SITE_PARAMS))
        success, uuid = self.facade.add_flavor(self.TESTED_FLAVOR_NAME, "hello", self.TESTED_SITE_NAME)
        self.assertTrue(success)

        return {
            'flavor_uuid': uuid
        }
