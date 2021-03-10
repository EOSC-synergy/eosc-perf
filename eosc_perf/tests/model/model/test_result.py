import json
import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeResultTests(FacadeTestBase):
    def test_add_result_valid(self):
        """Test valid call to add_result."""
        content_json = '{ "tag": 3.1415926535 }'
        data = self._add_result_data()
        self.facade.add_tag(self.tested_tag_name)
        self.assertTrue(self.facade.add_result(content_json, self.tested_uploader_id, self.tested_site_name,
                                               self.tested_benchmark_name, data['flavor_uuid'],
                                               [self.tested_tag_name]))

    def test_add_result_invalid(self):
        """Test invalid calls to add_result."""

        data = self._add_result_data()
        content_json = '{ "tag": 3.1415926535 }'

        # invalid uploader
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, "", self.tested_site_name,
                                   self.tested_benchmark_name, data['flavor_uuid'],
                                   [self.tested_tag_name])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, "???", self.tested_site_name,
                                   self.tested_benchmark_name, data['flavor_uuid'],
                                   [self.tested_tag_name])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, 1, self.tested_site_name,
                                   self.tested_benchmark_name, data['flavor_uuid'],
                                   [self.tested_tag_name])

        # invalid site
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, "",
                                   self.tested_benchmark_name, data['flavor_uuid'],
                                   [self.tested_tag_name])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, "???",
                                   self.tested_benchmark_name, data['flavor_uuid'],
                                   [self.tested_tag_name])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, 1,
                                   self.tested_benchmark_name, data['flavor_uuid'],
                                   [self.tested_tag_name])

        # invalid benchmark
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, self.tested_site_name,
                                   "", data['flavor_uuid'],
                                   [self.tested_tag_name])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, self.tested_site_name,
                                   "the moon is made of cheese", data['flavor_uuid'],
                                   [self.tested_tag_name])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, self.tested_site_name,
                                   1, data['flavor_uuid'],
                                   [self.tested_tag_name])

        # invalid tags
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, self.tested_site_name,
                                   self.tested_benchmark_name, data['flavor_uuid'],
                                   ["oeuf"])

        # unknown flavor
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.tested_uploader_id, self.tested_site_name,
                                   self.tested_benchmark_name, "nil",
                                   [self.tested_tag_name])

    def test_find_results(self):
        """Test if added results can be found."""
        self.test_add_result_valid()
        self.assertGreater(len(self.facade.query_results('{ "filters": [] }')), 0)

    def test_find_results_empty(self):
        """Test finding no results."""
        self.assertEqual(len(self.facade.query_results('{ "filters": [] }')), 0)

    def test_find_results_with_filters(self):
        """Test if added results can be found using filters."""
        self.test_add_result_valid()
        self.assertGreater(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "benchmark",
                "value": self.tested_benchmark_name
            },
            {
                "type": "uploader",
                "value": self.tested_uploader_email
            },
            {
                "type": "site",
                "value": self.tested_site_name
            },
            {
                "type": "tag",
                "value": self.tested_tag_name
            },
            {
                "type": "json",
                "mode": "equals",
                "key": "tag",
                "value": 3.1415926535
            },
            {
                "type": "json",
                "mode": "greater_than",
                "key": "tag",
                "value": 2.7182818284
            },
            {
                "type": "json",
                "mode": "lesser_than",
                "key": "tag",
                "value": 6.28318530718
            }
        ]}))), 0)

    def test_find_results_wrong_filters(self):
        """Test with filters finding no results."""
        self.test_add_result_valid()
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "benchmark",
                "value": "mrbrightside/leave-cage:latest"
            }
        ]}))), 0)
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "uploader",
                "value": "dorian.grey@fictional-domain.tld"
            }
        ]}))), 0)
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "site",
                "value": "wonderland"
            }
        ]}))), 0)
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "tag",
                "value": "important"
            }
        ]}))), 0)
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "json",
                "mode": "equals",
                "key": "tag",
                "value": 2.7182818284
            }
        ]}))), 0)
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "json",
                "mode": "greater_than",
                "key": "tag",
                "value": 6.28318530718
            }
        ]}))), 0)
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "json",
                "mode": "lesser_than",
                "key": "tag",
                "value": 1.41421356237
            }
        ]}))), 0)


if __name__ == '__main__':
    unittest.main()
