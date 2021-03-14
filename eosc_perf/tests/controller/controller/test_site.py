import json
import unittest

from eosc_perf.controller.authenticator import AuthenticateError
from eosc_perf.model.facade import facade
from .controller_test_base import IOControllerTestBase


class ControllerSiteTests(IOControllerTestBase):
    def test_submit_site_unauthenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.submit_site, "name", "address")

    def test_submit_site_invalid_identifier(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_site, None, "address")
            self.assertRaises(ValueError, self.controller.submit_site, "", "address")

    def test_submit_site_invalid_address(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_site, "name", None)
            self.assertRaises(ValueError, self.controller.submit_site, "name", "")

    def test_submit_site_success(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.submit_site(self.SITE_NAME, self.SITE_ADDRESS, "long name", "description"))

    def test_submit_site_duplicate_name(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_site("name", address="127.0.0.1")
            self.assertFalse(self.controller.submit_site("name", address="127.0.0.2"))

    def test_get_site_not_found(self):
        with self.app.test_request_context():
            self.assertIsNone(self.controller.get_site("name"))

    def test_get_site(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_site("name", "127.0.0.1")
            self.assertEqual(self.controller.get_site("name").get_name(), "name")

    def test_remove_site_not_authenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.remove_site, "name")

    def test_remove_site_not_existing(self):
        with self.app.test_request_context():
            self._login_admin()
            self.assertFalse(self.controller.remove_site("not existing"))

    def test_remove_site_with_results(self):
        data = self._add_test_data()
        with self.app.test_request_context():
            self._login_admin()
            metadata = json.dumps({
                'uploader': self.TEST_USER["sub"],
                'benchmark': self.BENCHMARK_NAME,
                'site': self.SITE_NAME,
                'site_flavor': data['flavor_uuid'],
                'tags': []
            })
            self.controller.submit_result(self._get_sample_result_data(), metadata)
            self.assertRaises(RuntimeError, self.controller.remove_site, self.SITE_NAME)

    def test_remove_site(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_admin()
            self.assertTrue(self.controller.submit_site("name", "127.0.0.1"))
            self.assertTrue(self.controller.remove_site("name"))
            # make sure that site is removed
            self.assertFalse(self.controller.remove_site("name"))

    def test_site_result_amount(self):
        self.assertEqual(self.controller._site_result_amount("name"), 0)
        data = self._add_test_data()
        with self.app.test_request_context():
            self._login_standard_user()
            metadata = json.dumps({
                'uploader': self.TEST_USER["sub"],
                'benchmark': self.BENCHMARK_NAME,
                'site': self.SITE_NAME,
                'site_flavor': data['flavor_uuid'],
                'tags': []
            })
            self.controller.submit_result(self._get_sample_result_data(), metadata)
            self.assertEqual(self.controller._site_result_amount(self.SITE_NAME), 1)

    def test_submit_flavor(self):
        self.test_submit_site_success()
        with self.app.test_request_context():
            self._login_standard_user()
            uuid = self.controller.submit_flavor(self.FLAVOR_NAME, "description", self.SITE_NAME)
            self.assertIsNotNone(uuid)
            return uuid

    def test_update_flavor_success(self):
        # test_submit_flavor comes with site
        flavor_uuid = self.test_submit_flavor()
        with self.app.test_request_context():
            self._login_admin()
            self.controller.update_flavor(flavor_uuid, self.FLAVOR_NAME + '_renamed', "description")

    def test_update_flavor_unknown(self):
        with self.app.test_request_context():
            self._login_admin()
            self.assertFalse(self.controller.update_flavor('invalid_uuid', self.FLAVOR_NAME + '_renamed', "description"))


if __name__ == '__main__':
    unittest.main()
