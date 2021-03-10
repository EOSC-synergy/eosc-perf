import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeBenchmarkTests(FacadeTestBase):
    def test_add_benchmark_valid(self):
        """Test valid call to add_benchmark."""
        # add necessary uploader
        self.facade.add_uploader(*self.tested_uploader_params)

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


if __name__ == '__main__':
    unittest.main()
