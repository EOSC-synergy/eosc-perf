import json
import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeReportTests(FacadeTestBase):
    def _add_result(self):
        content_json = '{ "tag": 3.1415926535 }'
        data = self._add_result_data()
        self.facade.add_tag(self.TESTED_TAG_NAME)
        self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, self.TESTED_SITE_NAME, self.TESTED_BENCHMARK_NAME,
                               data['flavor_uuid'], [self.TESTED_TAG_NAME])

    def test_add_report_valid(self):
        """Test valid calls to add_report."""

        self._add_result()

        # site
        self.assertTrue(
            self.facade.add_report('site', self.TESTED_SITE_NAME, self.TESTED_UPLOADER_ID, 'hello world')[0])

        # benchmark
        self.assertTrue(self.facade.add_report('benchmark', self.TESTED_BENCHMARK_NAME, self.TESTED_UPLOADER_ID)[0])

    def test_add_report_invalid(self):
        """Test various invalid calls to add_report."""
        self._add_result_data()

        # invalid site
        with self.assertRaises(ValueError):
            self.facade.add_report('site', '!!!invalid!!!', self.TESTED_UPLOADER_ID)

        # invalid benchmark
        with self.assertRaises(ValueError):
            self.facade.add_report('benchmark', '!!!invalid!!!', self.TESTED_UPLOADER_ID)

        # invalid uploader
        with self.assertRaises(ValueError):
            self.facade.add_report('site', self.TESTED_SITE_NAME, 'inexistent uploader')

        # invalid result
        with self.assertRaises(ValueError):
            self.facade.add_report('result', 'not an uuid lol', self.TESTED_UPLOADER_ID)

    def test_find_reports(self):
        """Test if added reports can be found."""
        self.test_add_report_valid()
        self.assertGreater(len(self.facade.get_reports()), 0)

    def test_find_reports_unanswered(self):
        """Test finding only unanswered reports."""
        self.test_add_report_valid()
        self.assertGreater(len(self.facade.get_reports(only_unanswered=True)), 0)

    def test_find_reports_empty(self):
        """Test finding no reports."""
        self.assertEqual(len(self.facade.get_reports()), 0)


if __name__ == '__main__':
    unittest.main()
