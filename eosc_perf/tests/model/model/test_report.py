import json
import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeReportTests(FacadeTestBase):
    def _add_result(self):
        content_json = '{ "tag": 3.1415926535 }'
        data = self._add_result_data()
        self.facade.add_tag(self.tested_tag_name)
        self.facade.add_result(content_json, self.tested_uploader_id, self.tested_site_name, self.tested_benchmark_name,
                               data['flavor_uuid'], [self.tested_tag_name])

    def test_add_report_valid(self):
        """Test valid calls to add_report."""

        self._add_result()

        # site
        meta = {
            'uploader': self.tested_uploader_id,
            'type': 'site',
            'value': self.tested_site_name,
            'message': 'hello world'
        }
        self.assertTrue(self.facade.add_report(json.dumps(meta)))

        # benchmark
        meta = {
            'uploader': self.tested_uploader_id,
            'type': 'benchmark',
            'value': self.tested_benchmark_name
        }
        self.assertTrue(self.facade.add_report(json.dumps(meta)))

        #
        # result
        # no simple available way to reference test result
        # meta = {
        #    'uploader': self.tested_uploader_id,
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
            'value': self.tested_site_name
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # no type
        meta = {
            'uploader': self.tested_uploader_id,
            'value': 'something'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # no value
        meta = {
            'uploader': self.tested_uploader_id,
            'type': 'test'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # invalid site
        meta = {
            'uploader': self.tested_uploader_id,
            'type': 'site',
            'value': '!!!invalid'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # invalid benchmark
        meta = {
            'uploader': self.tested_uploader_id,
            'type': 'benchmark',
            'value': '!!!invalid'
        }
        with self.assertRaises(ValueError):
            self.facade.add_report(json.dumps(meta))

        # invalid uploader
        meta = {
            'uploader': 'not an uploader',
            'type': 'site',
            'value': self.tested_site_name
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
