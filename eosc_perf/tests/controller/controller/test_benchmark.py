import unittest

from eosc_perf.controller.authenticator import AuthenticateError
from eosc_perf.tests.controller.controller.controller_test_base import IOControllerTestBase


class ControllerBenchmarkTests(IOControllerTestBase):
    def test_submit_benchmark_unauthenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.submit_benchmark, "", "")

    def test_submit_benchmark_malformed_docker_name(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(RuntimeError, self.controller.submit_benchmark, ":", "")
            self.assertRaises(RuntimeError, self.controller.submit_benchmark, None, "")

    def test_submit_benchmark_success(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.submit_benchmark(self.REAL_BENCHMARK, self.BENCHMARK_DESCRIPTION))
            self.assertTrue(self.controller.submit_benchmark(self.REAL_BENCHMARK2, self.BENCHMARK_DESCRIPTION))

    def test_submit_benchmark_invalid_template(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.submit_benchmark, self.REAL_BENCHMARK,
                              self.BENCHMARK_DESCRIPTION, "{{{")

    def test_submit_benchmark_duplicate(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_benchmark(self.REAL_BENCHMARK, self.BENCHMARK_DESCRIPTION)
            self.assertRaises(RuntimeError, self.controller.submit_benchmark, self.REAL_BENCHMARK,
                              self.BENCHMARK_DESCRIPTION)

    def test_valid_docker_hub_name_fails(self):
        # malformed
        self.assertFalse(self.controller._valid_docker_hub_name(None))
        self.assertFalse(self.controller._valid_docker_hub_name(""))
        self.assertFalse(self.controller._valid_docker_hub_name("Gibberishcfzugiop"))
        # official images are not supported
        self.assertFalse(self.controller._valid_docker_hub_name("mysql"))
        # private image
        self.assertFalse(self.controller._valid_docker_hub_name("thechristophe/example-private"))
        # typos, non existent image, wrong tags etc
        self.assertFalse(self.controller._valid_docker_hub_name("mysql!"))
        self.assertFalse(self.controller._valid_docker_hub_name("mysql:8.0.123"))
        self.assertFalse(self.controller._valid_docker_hub_name("mysql:"))
        self.assertFalse(self.controller._valid_docker_hub_name("rosskukulinsk/leaking-app:latest"))
        self.assertFalse(self.controller._valid_docker_hub_name("rosskukulinski/leakingapp:latest"))
        self.assertFalse(self.controller._valid_docker_hub_name("rosskukulinski/leaking-app:lates"))
        self.assertFalse(self.controller._valid_docker_hub_name("/leaking-app:latest"))
        self.assertFalse(self.controller._valid_docker_hub_name("/:latest"))
        self.assertFalse(self.controller._valid_docker_hub_name("/:"))
        self.assertFalse(self.controller._valid_docker_hub_name(":"))

    def test_valid_docker_hub_name(self):
        self.assertTrue(self.controller._valid_docker_hub_name(self.REAL_BENCHMARK))
        self.assertTrue(self.controller._valid_docker_hub_name(self.REAL_BENCHMARK2))


if __name__ == '__main__':
    unittest.main()
