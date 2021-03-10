import json
import unittest

from eosc_perf.controller.authenticator import AuthenticateError
from eosc_perf.tests.controller.controller.controller_test_base import IOControllerTestBase


class ControllerResultTests(IOControllerTestBase):
    def test_submit_result_unauthenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.submit_result, "", "")

    def test_submit_result_malformed_json(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_result, "---", "")

    def test_submit_result_success(self):
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
            self.assertTrue(self.controller.submit_result(self._get_sample_result_data(), metadata))

    def test_remove_result_not_authenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.remove_result, "name")

    def test_remove_result_not_admin(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(AuthenticateError, self.controller.remove_result, "name")

    def test_remove_result_not_found(self):
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
            self.assertFalse(self.controller.remove_result("wrong_uuid"))

    def test_remove_result(self):
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
            filters = {'filters': [
                {'type': 'uploader', 'value': self.TEST_USER["info"]["email"]},
            ]}
            results = self.facade.query_results(json.dumps(filters))
            self.assertEqual(len(results), 1)
            self.assertTrue(self.controller.remove_result(results[0].get_uuid()))
            # make sure that result is now hidden
            results = self.facade.query_results(json.dumps(filters))
            self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
