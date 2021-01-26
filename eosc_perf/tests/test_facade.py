"""Tests for facade behaviour."""
import unittest
import json
from flask import Flask
from eosc_perf.configuration import configuration
from eosc_perf.model.database import configure_database
from eosc_perf.model.facade import DatabaseFacade
from eosc_perf.tests.utility import setup_test_config


class FacadeTest(unittest.TestCase):
    """Tests for facade."""
    tested_uploader_id: str = 'test_user'
    tested_uploader_email: str = 'test@example.com'
    tested_uploader_name: str = 'test user'
    tested_benchmark_name: str = 'foobar/bazbutt'
    tested_site_name: str = 'iamasitename'
    tested_site_address: str = 'localhost'
    tested_site_description: str = 'hello world'
    tested_tag_name: str = 'testtag'
    tested_flavor_name: str = 'test-flavor'

    tested_result_params = [tested_uploader_id, tested_site_name, tested_benchmark_name, tested_flavor_name]
    tested_uploader_params = [tested_uploader_id, tested_uploader_name, tested_uploader_email]
    tested_site_params = [tested_site_name, tested_site_address]

    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()

        # use memory database, reset entirely every time
        setup_test_config(configuration)
        configure_database(self.app)

        # facade
        self.facade = DatabaseFacade()

    def tearDown(self):
        """Called after each test."""
        del self.facade
        del self.app

    def test_add_uploader_valid(self):
        """Test valid call to add_uploader."""
        self.assertTrue(self.facade.add_uploader(*self.tested_uploader_params))

        try:
            self.facade.get_uploader(self.tested_uploader_id)
        except self.facade.NotFoundError:
            self.fail("added uploader not found")

    def test_add_uploader_invalid(self):
        """Test various invalid calls to add_uploader."""
        # empty id
        with self.assertRaises(ValueError):
            self.facade.add_uploader("", self.tested_uploader_name, self.tested_uploader_email)

        # empty user
        with self.assertRaises(ValueError):
            self.facade.add_uploader(self.tested_uploader_id, "", self.tested_uploader_email)

        # empty email
        with self.assertRaises(ValueError):
            self.facade.add_uploader(self.tested_uploader_id, self.tested_uploader_name, "")

        # duplicate
        self.test_add_uploader_valid()
        self.assertFalse(self.facade.add_uploader(*self.tested_uploader_params))

    def test_find_uploader(self):
        """Test finding added uploader."""
        self.test_add_uploader_valid()
        try:
            self.facade.get_uploader(self.tested_uploader_id)
        except self.facade.NotFoundError:
            self.fail("could not find added uploader")

    def test_add_benchmark_valid(self):
        """Test valid call to add_benchmark."""
        # add necessary uploader
        self.test_add_uploader_valid()

        self.assertTrue(
            self.facade.add_benchmark(self.tested_benchmark_name, self.tested_uploader_id))

        try:
            self.facade.get_benchmark(self.tested_benchmark_name)
        except self.facade.NotFoundError:
            self.fail("added benchmark not found")

    def test_add_benchmark_invalid(self):
        """Test various invalid calls to add_benchmark."""
        # too short docker_name
        with self.assertRaises(ValueError):
            self.facade.add_benchmark('ab', self.tested_uploader_id)

        # empty uploader
        with self.assertRaises(ValueError):
            self.facade.add_benchmark(self.tested_benchmark_name, '')

        # unknown uploader
        with self.assertRaises(ValueError):
            self.facade.add_benchmark(self.tested_benchmark_name, 'hopefully nobody has this id')

        # duplicate
        self.test_add_benchmark_valid()
        self.assertFalse(
            self.facade.add_benchmark(self.tested_benchmark_name, self.tested_uploader_id))

    def test_find_benchmark(self):
        """Test finding added benchmark."""
        self.test_add_benchmark_valid()
        try:
            self.facade.get_benchmark(self.tested_benchmark_name)
        except self.facade.NotFoundError:
            self.fail("could not find added benchmark")

    def test_find_benchmark_invalid(self):
        """Test finding nonexistent benchmark."""
        with self.assertRaises(self.facade.NotFoundError):
            self.facade.get_benchmark("this benchmark does not exist")

    def test_find_benchmarks(self):
        """Test finding benchmarks."""
        self.test_add_benchmark_valid()
        self.assertGreater(len(self.facade.get_benchmarks()), 0)

    def test_query_benchmarks(self):
        """Test querying benchmarks."""
        self.test_add_benchmark_valid()
        self.assertGreater(len(self.facade.query_benchmarks([])), 0)

    def test_query_benchmarks_by_name(self):
        """Test querying benchmarks by name."""
        self.test_add_benchmark_valid()
        self.assertGreater(len(self.facade.query_benchmarks([self.tested_benchmark_name])), 0)

    def test_find_benchmarks_empty(self):
        """Test finding no benchmarks."""
        self.assertEqual(len(self.facade.get_benchmarks()), 0)

    def test_add_site_valid(self):
        """Test valid call to add_site."""
        self.assertTrue(self.facade.add_site(*self.tested_site_params))

        try:
            self.facade.get_site(self.tested_site_name)
        except self.facade.NotFoundError:
            self.fail("added site not found")

    def test_add_site_invalid(self):
        """Test various invalid calls to add_site."""
        # empty name
        with self.assertRaises(ValueError):
            self.facade.add_site("", self.tested_site_address)

        # empty address
        with self.assertRaises(ValueError):
            self.facade.add_site(self.tested_site_name, "")

        self.test_add_site_valid()
        self.assertFalse(self.facade.add_site(*self.tested_site_params))

    def test_find_site(self):
        """Test finding added site."""
        self.test_add_site_valid()
        try:
            self.facade.get_site(self.tested_site_name)
        except self.facade.NotFoundError:
            self.fail("could not find added site")

    def test_find_site_invalid(self):
        """Test finding nonexistent site."""
        with self.assertRaises(self.facade.NotFoundError):
            self.facade.get_site("this site does not exist")

    def test_find_sites(self):
        """Test finding sites."""
        self.test_add_site_valid()
        self.assertGreater(len(self.facade.get_sites()), 0)

    def test_find_sites_empty(self):
        """Test finding no sites."""
        self.assertEqual(len(self.facade.get_sites()), 0)

    def test_remove_site(self):
        """Test removing a site."""
        self.test_add_site_valid()
        self.assertTrue(self.facade.remove_site(self.tested_site_name))
        with self.assertRaises(self.facade.NotFoundError):
            self.facade.get_site(self.tested_site_name)

    def test_remove_site_invalid(self):
        """Test removing a site that doesn't exist."""
        self.assertFalse(self.facade.remove_site(self.tested_site_name))

    def test_add_flavor(self):
        self.test_add_site_valid()
        self.assertTrue(self.facade.add_flavor(self.tested_flavor_name, "", self.tested_site_name))

    def test_add_tag_valid(self):
        """Test valid call to add_tag."""
        self.assertTrue(self.facade.add_tag(self.tested_tag_name))

        try:
            self.facade.get_tag(self.tested_tag_name)
        except self.facade.NotFoundError:
            self.fail("added tag not found")

    def test_add_tag_invalid(self):
        """Test various invalid calls to add_tag."""
        with self.assertRaises(ValueError):
            self.facade.add_tag("")

        self.test_add_tag_valid()
        self.assertFalse(self.facade.add_tag(self.tested_tag_name))

    def test_find_tag(self):
        """Test finding added tag."""
        self.test_add_tag_valid()
        try:
            self.facade.get_tag(self.tested_tag_name)
        except self.facade.NotFoundError:
            self.fail("could not find added tag")

    def test_find_tag_invalid(self):
        """Test finding nonexistent tag."""
        with self.assertRaises(self.facade.NotFoundError):
            self.facade.get_tag("this tag does not exist")

    def test_find_tags(self):
        """Test finding all tags."""
        self.test_add_tag_valid()
        self.assertGreater(len(self.facade.get_tags()), 0)

    def test_find_tags_empty(self):
        """Test finding no tags."""
        self.assertEqual(len(self.facade.get_tags()), 0)

    def _add_result_data(self):
        self.assertTrue(self.facade.add_uploader(*self.tested_uploader_params))
        self.assertTrue(self.facade.add_benchmark(self.tested_benchmark_name, self.tested_uploader_id))
        self.assertTrue(self.facade.add_site(*self.tested_site_params))
        success, uuid = self.facade.add_flavor(self.tested_flavor_name, "hello", self.tested_site_name)
        self.assertTrue(success)

        return {
            'flavor_uuid': uuid
        }

    def test_add_result_valid(self):
        """Test valid call to add_result."""
        content_json = '{ "tag": 3.1415926535 }'
        data = self._add_result_data()
        self.test_add_tag_valid()
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

    def test_add_report_valid(self):
        """Test valid calls to add_report."""

        self.test_add_result_valid()

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
