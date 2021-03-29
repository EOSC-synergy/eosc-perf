import unittest

from eosc_perf.tests.model.data_types.datatype_test_base import DatatypeTestBase


class UploaderTests(DatatypeTestBase):
    def test_uploader(self):
        """Test creating uploader object."""
        uploader = self._make_uploader()
        self.assertEqual(uploader.get_id(), self.UPLOADER_IDENTIFIER)
        self.assertEqual(uploader.get_email(), self.UPLOADER_EMAIL)
        self.assertEqual(uploader.get_name(), self.UPLOADER_NAME)

    def test_uploader_set_email(self):
        """Test setting uploader email."""
        uploader = self._make_uploader()
        new_email: str = self.UPLOADER_EMAIL + '___'
        uploader.set_email(new_email)
        self.assertEqual(uploader.get_email(), new_email)

    def test_uploader_set_name(self):
        """Test setting uploader name."""
        uploader = self._make_uploader()
        new_name: str = self.UPLOADER_NAME + '___'
        uploader.set_name(new_name)
        self.assertEqual(uploader.get_name(), new_name)

    @unittest.skip("missing helpers")
    def test_uploader_get_results(self):
        """Test fetching results through uploader."""
        uploader = self._make_uploader()
        #result = self._make_result(uploader, )

    def test_uploader_get_benchmarks(self):
        """Test fetching benchmarks through uploader."""
        uploader = self._make_uploader()
        self._add_to_database(uploader)
        benchmark = self._make_benchmark(uploader)
        self._add_to_database(benchmark)
        self.assertEqual(len(uploader.get_benchmarks()), 1)

    def test_uploader_repr(self):
        """Test if uploader repr does anything."""
        uploader = self._make_uploader()
        self.assertEquals(type(str(uploader)), str)

if __name__ == '__main__':
    unittest.main()
