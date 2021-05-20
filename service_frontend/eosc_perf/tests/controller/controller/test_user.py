import unittest

from flask import session

from eosc_perf.model.facade import DatabaseFacade
from eosc_perf.tests.controller.controller.controller_test_base import IOControllerTestBase


class ControllerUserTests(IOControllerTestBase):
    def test_authenticate_not_authenticated(self):
        with self.app.test_request_context():
            self.assertIsNotNone(self.controller.authenticate())

    def test_authenticate_already_authenticated(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertIsNone(self.controller.authenticate())

    def test_add_current_user_if_missing(self):
        with self.app.test_request_context():
            self.assertRaises(DatabaseFacade.NotFoundError, self.facade.get_uploader, self.TEST_USER['sub'])
            self._login_standard_user()
            self.controller._add_current_user_if_missing()
            self.assertTrue(self.facade.get_uploader(self.TEST_USER['sub']))
            self.controller._add_current_user_if_missing()
            self.assertTrue(self.facade.get_uploader(self.TEST_USER['sub']))

    def test_get_email(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.email, self.TEST_USER["info"]["email"])
            self._logout()
        with self.app.test_request_context():
            self.assertIsNone(self.controller.email)

    def test_get_full_name(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_full_name(), self.TEST_USER["info"]["name"])
            self._logout()
        with self.app.test_request_context():
            self.assertIsNone(self.controller.get_full_name())

    def test_get_user_id(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertEqual(self.controller.get_user_id(), self.TEST_USER["sub"])
            self._logout()
        with self.app.test_request_context():
            self.assertIsNone(self.controller.get_user_id())

    def test_is_admin_fail_no_affiliations(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertFalse(self.controller.is_admin())

    def test_is_admin_fail_wrong_affiliations(self):
        with self.app.test_request_context():
            self._login_standard_user()
            session['user']['info']['edu_person_scoped_affiliations'] = ["student@mit.edu"]
            self.assertFalse(self.controller.is_admin())

    def test_is_admin_one_entitlement(self):
        with self.app.test_request_context():
            self._login_admin()
            self.assertTrue(self.controller.is_admin())

    def test_authenticated(self):
        """Tests if IOController returns True when logged
           in during is_authenticated method call"""
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertTrue(self.controller.is_authenticated())

    def test_not_authenticated(self):
        """Tests if IOController returns False when not logged
           in during is_authenticated method call"""
        with self.app.test_request_context():
            self.assertFalse(self.controller.is_authenticated())


if __name__ == '__main__':
    unittest.main()
