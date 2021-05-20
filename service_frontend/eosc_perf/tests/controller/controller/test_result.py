import json
import unittest

from eosc_perf.controller.authenticator import AuthenticateError
from eosc_perf.tests.controller.controller.controller_test_base import IOControllerTestBase


class ControllerResultTests(IOControllerTestBase):
    def test_submit_result_malformed_json(self):
        data = self._add_test_data()
        with self.app.test_request_context():
            self.assertRaises(ValueError, self.controller.submit_result, "---", self.TEST_USER["sub"],
                              self.BENCHMARK_NAME, self.SITE_NAME, data['flavor_uuid'], [])

    def test_submit_result_success(self):
        data = self._add_test_data()
        with self.app.test_request_context():
            self.controller.submit_result(self._get_sample_result_data(), self.TEST_USER["sub"], self.BENCHMARK_NAME,
                                          self.SITE_NAME, data['flavor_uuid'], [])

    def test_remove_result_not_found(self):
        data = self._add_test_data()
        with self.app.test_request_context():
            self.controller.submit_result(self._get_sample_result_data(), self.TEST_USER["sub"], self.BENCHMARK_NAME,
                                          self.SITE_NAME, data['flavor_uuid'], [])
            self.assertFalse(self.controller.remove_result("wrong_uuid"))

    def test_remove_result(self):
        data = self._add_test_data()
        with self.app.test_request_context():
            self.controller.submit_result(self._get_sample_result_data(), self.TEST_USER["sub"], self.BENCHMARK_NAME,
                                          self.SITE_NAME, data['flavor_uuid'], [])
            filters = {'filters': [
                {'type': 'uploader', 'value': self.TEST_USER["info"]["email"]},
            ]}
            results = self.facade.query_results(json.dumps(filters))
            self.assertEqual(len(results), 1)
            self.assertTrue(self.controller.remove_result(results[0].uuid))
            # make sure that result is now hidden
            results = self.facade.query_results(json.dumps(filters))
            self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
