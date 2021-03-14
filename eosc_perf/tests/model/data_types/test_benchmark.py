import unittest

from eosc_perf.model.data_types import ResultIterator
from eosc_perf.tests.model.data_types.datatype_test_base import DatatypeTestBase


class BenchmarkTests(DatatypeTestBase):
    def test_benchmark(self):
        """Test if we can create a benchmark."""
        uploader = self._make_uploader()
        benchmark = self._make_benchmark(uploader)
        with self.app.test_request_context():  # required for get_hidden defaulting to false
            self._add_to_database(benchmark)
            self.assertEqual(self.BENCHMARK_DOCKER_NAME, benchmark.get_docker_name())
            self.assertEqual(uploader, benchmark.get_uploader())
            print(benchmark.get_hidden())
            self.assertEqual(True, benchmark.get_hidden())  # true by default
            # requires flask_sqlalchemy session
            # self.assertEqual(ResultIterator, type(benchmark.get_results()))

    def test_benchmark_set_description(self):
        """Test if we can set the benchmark description."""
        uploader = self._make_uploader()
        benchmark = self._make_benchmark(uploader)
        description: str = "Hello world :)"
        benchmark.set_description(description)
        self.assertEqual(description, benchmark.get_description())

    def test_benchmark_set_template(self):
        """Test if we can set the benchmark template."""
        uploader = self._make_uploader()
        benchmark = self._make_benchmark(uploader)
        # validity is not checked in Benchmark class itself!
        template: str = "{{}}"
        benchmark.set_template(template)
        self.assertTrue(benchmark.has_template())
        self.assertEquals(template, benchmark.get_template())

    def test_notable_keys(self):
        """Test if the notable keys determining function works properly."""
        uploader = self._make_uploader()
        benchmark = self._make_benchmark(uploader)

        # no template, no keys
        self.assertEqual([], benchmark.determine_notable_keys())

        template = '{"important": false}'
        benchmark.set_template(template)
        self.assertEqual([], benchmark.determine_notable_keys())
        template = '{"!important": false}'
        benchmark.set_template(template)
        self.assertCountEqual(["important"], benchmark.determine_notable_keys())

    def test_benchmark_repr(self):
        """Test if benchmark repr does anything."""
        uploader = self._make_uploader()
        benchmark = self._make_benchmark(uploader)
        self.assertEquals(str, type(str(benchmark)))


if __name__ == '__main__':
    unittest.main()
