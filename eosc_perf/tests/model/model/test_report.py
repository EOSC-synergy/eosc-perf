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
        meta = {
            'uploader': self.TESTED_UPLOADER_ID,
            'type': 'site',
            'value': self.TESTED_SITE_NAME,
            'message': 'hello world'
        }
        self.assertTrue(self.facade.add_report(json.dumps(meta)))

        # benchmark
        meta = {
            'uploader': self.TESTED_UPLOADER_ID,
            'type': 'benchmark',
            'value': self.TESTED_BENCHMARK_NAME
        }
        self.assertTrue(self.facade.add_report(json.dumps(meta)))

        #
        # result
        # no simple available way to reference test result
        # meta = {
        #    'uploader': self.TESTED_UPLOADER_ID,
        #    'type': 'result',
        #    'value': ?
        # }
        # self.assertTrue(self.facade.add_report(json.dumps(meta)))

    def test_add_report_invalid(self):
        """Test various invalid calls to add_report."""
        self._add_result_data()

        # no uploader
        meta = {
            'type': 'site',
            'value': self.TESTED_SITE_NAME
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # no type
        meta = {
            'uploader': self.TESTED_UPLOADER_ID,
            'value': 'something'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # no value
        meta = {
            'uploader': self.TESTED_UPLOADER_ID,
            'type': 'test'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # invalid site
        meta = {
            'uploader': self.TESTED_UPLOADER_ID,
            'type': 'site',
            'value': '!!!invalid'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # invalid benchmark
        meta = {
            'uploader': self.TESTED_UPLOADER_ID,
            'type': 'benchmark',
            'value': '!!!invalid'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # invalid uploader
        meta = {
            'uploader': 'not an uploader',
            'type': 'site',
            'value': self.TESTED_SITE_NAME
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # invalid result
        meta = {
            'uploader': 'not an uploader',
            'type': 'result',
            'value': 'ceci n\'est pas une UUID'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

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
