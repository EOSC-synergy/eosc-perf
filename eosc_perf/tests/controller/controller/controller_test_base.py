import unittest
from time import time

from flask import Flask, session

from eosc_perf.controller.authenticator import configure_authenticator
from eosc_perf.controller.io_controller import controller
from eosc_perf.model.database import configure_database
from eosc_perf.model.facade import DatabaseFacade
from eosc_perf.tests.utility import setup_test_config
from eosc_perf.configuration import configuration


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
        #print('"', configuration.get('oidc_client_secret'), '"')
        configure_authenticator(self.app)
        configure_database(self.app)

        self.controller = controller
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

    def _login_standard_user(self):
        session['user'] = self.TEST_USER
        session['user']['info'].pop('eduperson_entitlement', None)

    def _login_admin(self):
        self._login_standard_user()
        admin_entitlement = configuration.get('debug_admin_entitlements')[:1]
        admin_entitlement[0] += '#aai.egi.eu'
        session['user']['info']['eduperson_entitlement'] = admin_entitlement

    @staticmethod
    def _get_sample_result_data():
        with open("eosc_perf/tests/controller/sample_result.json") as file:
            return file.read()

    @staticmethod
    def _logout():
        session.pop('user', None)
