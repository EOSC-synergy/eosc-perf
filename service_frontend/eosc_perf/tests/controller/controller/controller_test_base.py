import unittest
from time import time

from flask import Flask

from eosc_perf.configuration import configuration
from eosc_perf.controller.io_controller import IOController
from eosc_perf.model.database import configure_database
from eosc_perf.model.facade import DatabaseFacade
from eosc_perf.tests.utility import setup_test_config


class IOControllerTestBase(unittest.TestCase):
    BENCHMARK_NAME: str = "name/name:tag"
    BENCHMARK_DESCRIPTION: str = "Hello world!"
    FLAVOR_NAME: str = "test-flavor"
    SITE_NAME: str = "test-site"
    SITE_ADDRESS: str = "https://example.com/testsite"
    UPLOADER_ID: str = "hamburger"
    UPLOADER_EMAIL: str = "hamburger@example.com"
    UPLOADER_NAME: str = "Hamburger"

    REAL_BENCHMARK: str = "rosskukulinski/leaking-app"
    REAL_BENCHMARK2: str = "rosskukulinski/leaking-app:latest"

    RESULT_DATA = [UPLOADER_ID, SITE_NAME, BENCHMARK_NAME, FLAVOR_NAME]
    UPLOADER_DATA = [UPLOADER_ID, UPLOADER_NAME, UPLOADER_EMAIL]

    TEST_USER: dict = {
        'exp': time() + 3600,
        'sub': UPLOADER_ID,
        'info': {
            'email': UPLOADER_EMAIL,
            'name': UPLOADER_NAME
        }
    }

    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()
        self.app.secret_key = '!secret'

        # use memory database, reset entirely every time
        setup_test_config(configuration)
        configure_database(self.app)

        self.controller = IOController()
        self.facade = DatabaseFacade()

    def tearDown(self):
        """Called after each test."""
        del self.controller
        del self.facade
        del self.app

    def _add_test_data(self):
        self.facade.add_uploader(self.UPLOADER_ID, self.UPLOADER_NAME, self.UPLOADER_EMAIL)
        self.facade.add_benchmark(self.BENCHMARK_NAME, self.UPLOADER_ID)
        self.facade.add_site(self.SITE_NAME, self.SITE_ADDRESS)
        success, uuid = self.facade.add_flavor(self.FLAVOR_NAME, '', self.SITE_NAME)

        return {
            'flavor_uuid': uuid
        }

    @staticmethod
    def _get_sample_result_data():
        with open("eosc_perf/tests/controller/sample_result.json") as file:
            return file.read()
