import unittest

from frontend.tests.model.model.model_test_base import FacadeTestBase


class FacadeBenchmarkTests(FacadeTestBase):
    def test_add_benchmark_valid(self):
        """Test valid call to add_benchmark."""
        # add necessary uploader
        self.facade.add_uploader(*self.TESTED_UPLOADER_PARAMS)

        self.assertTrue(
            self.facade.add_benchmark(self.TESTED_BENCHMARK_NAME, self.TESTED_UPLOADER_ID))

        try:
            self.facade.get_benchmark(self.TESTED_BENCHMARK_NAME)
        except self.facade.NotFoundError:
            self.fail("added benchmark not found")

    def test_add_benchmark_invalid(self):
        """Test various invalid calls to add_benchmark."""
        # too short docker_name
        with self.assertRaises(ValueError):
            self.facade.add_benchmark('ab', self.TESTED_UPLOADER_ID)

        # empty uploader
        with self.assertRaises(ValueError):
            self.facade.add_benchmark(self.TESTED_BENCHMARK_NAME, '')

        # unknown uploader
        with self.assertRaises(ValueError):
            self.facade.add_benchmark(self.TESTED_BENCHMARK_NAME, 'hopefully nobody has this id')

        # duplicate
        self.test_add_benchmark_valid()
        self.assertFalse(
            self.facade.add_benchmark(self.TESTED_BENCHMARK_NAME, self.TESTED_UPLOADER_ID))

    def test_find_benchmark(self):
        """Test finding added benchmark."""
        self.test_add_benchmark_valid()
        try:
            self.facade.get_benchmark(self.TESTED_BENCHMARK_NAME)
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
        self.assertGreater(len(self.facade.query_benchmarks([self.TESTED_BENCHMARK_NAME])), 0)

    def test_find_benchmarks_empty(self):
        """Test finding no benchmarks."""
        self.assertEqual(len(self.facade.get_benchmarks()), 0)


if __name__ == '__main__':
    unittest.main()
