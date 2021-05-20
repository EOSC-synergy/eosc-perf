import unittest

from eosc_perf.controller.authenticator import AuthenticateError
from eosc_perf.tests.controller.controller.controller_test_base import IOControllerTestBase


class SubmitTagTests(IOControllerTestBase):
    def test_submit_tag_malformed(self):
        with self.app.test_request_context():
            self.assertRaises(ValueError, self.controller.submit_tag, None)
            self.assertRaises(ValueError, self.controller.submit_tag, "")

    def test_submit_tag_success(self):
        with self.app.test_request_context():
            self.assertTrue(self.controller.submit_tag("tag"))
            self.assertTrue(self.controller.submit_tag("tag2"))

    def test_submit_tag_duplicate(self):
        with self.app.test_request_context():
            self.controller.submit_tag("tag")
            self.assertFalse(self.controller.submit_tag("tag"))


if __name__ == '__main__':
    unittest.main()
