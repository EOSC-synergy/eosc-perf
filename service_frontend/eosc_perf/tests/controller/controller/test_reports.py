import json
import unittest

from eosc_perf.controller.authenticator import AuthenticateError
from eosc_perf.model.data_types import Report
from eosc_perf.model.facade import DatabaseFacade
from eosc_perf.tests.controller.controller.controller_test_base import IOControllerTestBase


class ControllerReportTests(IOControllerTestBase):
    def test_report_not_authenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.report, "", 0, "", "")

    def test_report_non_existent_object(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(ValueError, self.controller.report, Report.SITE, "name", "msg", self.TEST_USER["sub"], )

    def test_report(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_standard_user()
            self.controller.submit_site("name", "127.0.0.1")
            self.assertTrue(self.controller.report(Report.SITE, "name", "msg", self.TEST_USER["sub"]))

    def test_get_report_not_authenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.get_report, "uuid")

    def test_get_report_not_admin(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(AuthenticateError, self.controller.get_report, "uuid")

    def test_get_report_non_existent(self):
        with self.app.test_request_context():
            self._login_admin()
            self.assertRaises(DatabaseFacade.NotFoundError, self.controller.get_report, "uuid")

    def test_get_report(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_admin()
            self.controller.submit_site("name", "127.0.0.1")
            report = self.controller.get_reports()[0]
            uuid = report.uuid
            self.assertEqual(uuid, self.controller.get_report(uuid).uuid)

    def test_get_reports_not_authenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.get_reports)

    def test_get_reports_not_admin(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(AuthenticateError, self.controller.get_reports)

    def test_get_reports_empty(self):
        with self.app.test_request_context():
            self._login_admin()
            self.assertEqual(len(self.controller.get_reports(True)), 0)

    def test_get_reports(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_admin()
            self.controller.submit_site("name", "127.0.0.1")
            self.controller.report(Report.SITE, "name", "msg", self.TEST_USER["sub"], )
            self.controller.report(Report.SITE, "name", "msg2", self.TEST_USER["sub"], )
            # 3 reports: 2 submitted manually, 1 automatically generated for submitted site
            self.assertEqual(len(self.controller.get_reports(True)), 3)

    def test_process_report_not_authenticated(self):
        with self.app.test_request_context():
            self.assertRaises(AuthenticateError, self.controller.process_report, True, "id")

    def test_process_report_not_admin(self):
        with self.app.test_request_context():
            self._login_standard_user()
            self.assertRaises(AuthenticateError, self.controller.process_report, True, "id")

    def test_process_report_report_not_exists(self):
        with self.app.test_request_context():
            self._login_admin()
            self.assertEqual(self.controller.process_report(True, "id"), False)

    def test_process_report_site(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_admin()
            self.controller.submit_site("name", "127.0.0.1")
            report = self.controller.get_reports()[0]
            uuid = report.uuid
            self.assertEqual(self.controller.process_report(True, uuid), True)

    def test_process_report_benchmark(self):
        self.facade.add_uploader(*self.UPLOADER_DATA)
        with self.app.test_request_context():
            self._login_admin()
            self.controller.submit_benchmark("rosskukulinski/leaking-app", "submit comment.")
            report = self.controller.get_reports()[0]
            uuid = report.uuid
            self.assertEqual(self.controller.process_report(True, uuid), True)

    def test_process_report_result(self):
        data = self._add_test_data()
        with self.app.test_request_context():
            self._login_admin()
            self.controller.submit_result(self._get_sample_result_data(), self.TEST_USER["sub"], self.BENCHMARK_NAME,
                                          self.SITE_NAME, data['flavor_uuid'], [])
            filters = {'filters': [
                {
                    'type': 'uploader',
                    'value': self.TEST_USER["info"]["email"]},
            ]}
            result = self.facade.query_results(json.dumps(filters))[0]
            self.controller.report(Report.RESULT, result.uuid, "msg", self.TEST_USER["sub"], )
            reports = self.controller.get_reports()
            result_report = None
            for report in reports:
                if report.get_report_type() == Report.RESULT:
                    result_report = report
            uuid = result_report.get_uuid()
            self.assertTrue(self.controller.process_report(True, uuid), True)


if __name__ == '__main__':
    unittest.main()
