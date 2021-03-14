import json
import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeResultTests(FacadeTestBase):
    def test_add_result_valid(self):
        """Test valid call to add_result."""
        content_json = '{ "tag": 3.1415926535 }'
        data = self._add_result_data()
        self.facade.add_tag(self.TESTED_TAG_NAME)
        self.assertTrue(self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, self.TESTED_SITE_NAME,
                                               self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                               [self.TESTED_TAG_NAME]))

    def test_add_result_invalid(self):
        """Test invalid calls to add_result."""

        data = self._add_result_data()
        content_json = '{ "tag": 3.1415926535 }'

        # invalid uploader
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, "", self.TESTED_SITE_NAME,
                                   self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, "???", self.TESTED_SITE_NAME,
                                   self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, 1, self.TESTED_SITE_NAME,
                                   self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        # invalid site
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, "",
                                   self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, "???",
                                   self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, 1,
                                   self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        # invalid benchmark
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, self.TESTED_SITE_NAME,
                                   "", data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, self.TESTED_SITE_NAME,
                                   "the moon is made of cheese", data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, self.TESTED_SITE_NAME,
                                   1, data['flavor_uuid'],
                                   [self.TESTED_TAG_NAME])

        # invalid tags
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, self.TESTED_SITE_NAME,
                                   self.TESTED_BENCHMARK_NAME, data['flavor_uuid'],
                                   ["oeuf"])

        # unknown flavor
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, self.TESTED_UPLOADER_ID, self.TESTED_SITE_NAME,
                                   self.TESTED_BENCHMARK_NAME, "nil",
                                   [self.TESTED_TAG_NAME])

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
                "value": self.TESTED_BENCHMARK_NAME
            },
            {
                "type": "uploader",
                "value": self.TESTED_UPLOADER_EMAIL
            },
            {
                "type": "site",
                "value": self.TESTED_SITE_NAME
            },
            {
                "type": "tag",
                "value": self.TESTED_TAG_NAME
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
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "json",
                "mode": "less_or_equals",
                "key": "tag",
                "value": 1.41421356237
            }
        ]}))), 0)
        self.assertEqual(len(self.facade.query_results(json.dumps({"filters": [
            {
                "type": "json",
                "mode": "greater_or_equals",
                "key": "tag",
                "value": 6.28318530718
            }
        ]}))), 0)


if __name__ == '__main__':
    unittest.main()
