"""Tests for facade behaviour."""
import unittest
import json
from flask import Flask
from ..configuration import configuration
from ..model.database import configure_database
from ..model.facade import DatabaseFacade

class FacadeTest(unittest.TestCase):
    """Tests for facade."""
    tested_uploader_id: str = 'test_user'
    tested_benchmark_name: str = 'foobar/bazbutt'
    tested_site_name: str = 'iamasitename'
    tested_tag_name: str = 'testtag'

    def setUp(self):
        """Called before each test."""
        # set up flask app necessary for flask_sqlalchemy
        self.app = Flask("Test")
        self.app.config['DEBUG'] = True
        self.app.app_context().push()

        # use memory database, reset entirely every time
        configuration.reset()
        configure_database(self.app)

        # facade
        self.facade = DatabaseFacade()

    def tearDown(self):
        """Called after each test."""
        del self.facade
        del self.app

    def test_add_uploader_valid(self):
        """Test valid call to add_uploader."""
        meta = {
            'id': self.tested_uploader_id,
            'name': 'user',
            'email': 'test@example.com'
        }
        self.assertTrue(self.facade.add_uploader(json.dumps(meta)))

        try:
            self.facade.get_uploader(self.tested_uploader_id)
        except self.facade.NotFoundError:
            self.fail("added uploader not found")

    def test_add_uploader_invalid(self):
        """Test various invalid calls to add_uploader."""
        # invalid json
        with self.assertRaises(json.JSONDecodeError):
            self.facade.add_uploader('{invalid json}')

        # empty id
        meta = {
            'id': '',
            'user': 'name',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # missing id
        meta = {
            'user': 'name',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # empty user
        meta = {
            'id': 'random',
            'user': '',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # missing user
        meta = {
            'id': 'random',
            'email': 'test@example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # empty email
        meta = {
            'id': 'random',
            'user': 'name',
            'email': ''
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # missing email
        meta = {
            'id': 'random',
            'user': 'name',
        }
        with self.assertRaises(ValueError):
            self.facade.add_uploader(json.dumps(meta))

        # duplicate
        meta = {
            'id': self.tested_uploader_id,
            'name': 'user',
            'email': 'test@example.com'
        }
        self.test_add_uploader_valid()
        self.assertFalse(self.facade.add_uploader(json.dumps(meta)))

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
        
        self.assertGreater(len(self.facade.get_benchmarks()), 0)

    def test_add_site_valid(self):
        """Test valid call to add_site."""
        meta = {
            'short_name': self.tested_site_name,
            'address': 'example.com'
        }
        self.assertTrue(self.facade.add_site(json.dumps(meta)))

        try:
            self.facade.get_site(self.tested_site_name)
        except self.facade.NotFoundError:
            self.fail("added site not found")

    def test_add_site_invalid(self):
        """Test various invalid calls to add_site."""

        # invalid json
        with self.assertRaises(json.JSONDecodeError):
            self.facade.add_site('{invalid json}')

        # missing name
        meta = {
            'address': 'example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        # empty name
        meta = {
            'short_name': '',
            'address': 'example.com'
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        # missing address
        meta = {
            'short_name': self.tested_site_name
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        # empty address
        meta = {
            'short_name': self.tested_site_name,
            'address': ''
        }
        with self.assertRaises(ValueError):
            self.facade.add_site(json.dumps(meta))

        meta = {
            'short_name': self.tested_site_name,
            'address': 'example.com'
        }
        self.test_add_site_valid()
        self.assertFalse(self.facade.add_site(json.dumps(meta)))

    def test_find_site(self):
        """Test finding added site."""
        self.test_add_site_valid()
        try:
            self.facade.get_site(self.tested_site_name)
        except self.facade.NotFoundError:
            self.fail("could not find added site")
        
        self.assertGreater(len(self.facade.get_sites()), 0)

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

        self.assertGreater(len(self.facade.get_tags()), 0)

    def _add_result_data(self):
        usermeta = {
            'id': self.tested_uploader_id,
            'name': 'user',
            'email': 'test@example.com'
        }
        sitemeta = {
            'short_name': self.tested_site_name,
            'address': 'example.com'
        }

        self.assertTrue(self.facade.add_uploader(json.dumps(usermeta)))
        self.assertTrue(self.facade.add_benchmark(self.tested_benchmark_name, self.tested_uploader_id))
        self.assertTrue(self.facade.add_site(json.dumps(sitemeta)))

    def test_add_result_valid(self):
        """Test valid call to add_result."""
        content_json = "{ 'tag': 'value' }"
        meta = {
            'uploader': self.tested_uploader_id,
            'site': self.tested_site_name,
            'benchmark': self.tested_benchmark_name,
            'tags': [self.tested_tag_name]
        }
        self._add_result_data()
        self.test_add_tag_valid()
        self.assertTrue(self.facade.add_result(content_json, json.dumps(meta)))

        # no duplicate test for results because they are not guaranteed unique

    def test_add_result_invalid(self):
        """Test invalid calls to add_result."""
        # missing uploader
        content_json = "{ 'tag': 'value' }"
        meta = {
            'site': self.tested_site_name,
            'benchmark': self.tested_benchmark_name,
            'tags': [self.tested_tag_name]
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

        # invalid uploader
        meta = {
            'uploader': 'foobar',
            'site': self.tested_site_name,
            'benchmark': self.tested_benchmark_name,
            'tags': [self.tested_tag_name]
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

        # missing site
        meta = {
            'uploader': self.tested_uploader_id,
            'benchmark': self.tested_benchmark_name,
            'tags': [self.tested_tag_name]
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

        # invalid site
        meta = {
            'uploader': self.tested_uploader_id,
            'site': 'hello world',
            'benchmark': self.tested_benchmark_name,
            'tags': [self.tested_tag_name]
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

        # missing benchmark
        meta = {
            'uploader': self.tested_uploader_id,
            'site': self.tested_site_name,
            'tags': [self.tested_tag_name]
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

        # invalid benchmark
        meta = {
            'uploader': self.tested_uploader_id,
            'site': self.tested_site_name,
            'benchmark': 'the moon is made of cheese',
            'tags': [self.tested_tag_name]
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

        # missing tags is not an error

        # invalid tags
        meta = {
            'uploader': self.tested_uploader_id,
            'site': self.tested_site_name,
            'benchmark': self.tested_benchmark_name,
            'tags': 'not a list'
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

        meta = {
            'uploader': self.tested_uploader_id,
            'site': self.tested_site_name,
            'benchmark': self.tested_benchmark_name,
            'tags': [['not a list of strings']]
        }
        with self.assertRaises(ValueError):
            self.facade.add_result(content_json, json.dumps(meta))

    def test_find_result(self):
        """Test if added results can be found."""
        self.test_add_result_valid()
        self.assertGreater(len(self.facade.query_results('{ "filters": [] }')), 0)

    def test_add_report_valid(self):
        """Test valid calls to add_report."""

        self.test_add_result_valid()

        # site
        meta = {
            'uploader': self.tested_uploader_id,
            'type': 'site',
            'value': self.tested_site_name
        }
        self.assertTrue(self.facade.add_report(json.dumps(meta)))

        # benchmark
        meta = {
            'uploader': self.tested_uploader_id,
            'type': 'benchmark',
            'value': self.tested_benchmark_name
        }
        self.assertTrue(self.facade.add_report(json.dumps(meta)))

        # result
        # no simple available way to reference test result
        #meta = {
        #    'uploader': self.tested_uploader_id,
        #    'type': 'result',
        #    'value': ?
        #}
        #self.assertTrue(self.facade.add_report(json.dumps(meta)))

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

    def test_find_report(self):
        """Test if added reports can be found."""
        self.test_add_report_valid()
        self.assertGreater(len(self.facade.get_reports()), 0)

if __name__ == '__main__':
    unittest.main()
