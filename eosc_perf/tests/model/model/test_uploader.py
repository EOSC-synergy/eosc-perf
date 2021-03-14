import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeUploaderTests(FacadeTestBase):
    def test_add_uploader_valid(self):
        """Test valid call to add_uploader."""
        self.assertTrue(self.facade.add_uploader(*self.TESTED_UPLOADER_PARAMS))

        try:
            self.facade.get_uploader(self.TESTED_UPLOADER_ID)
        except self.facade.NotFoundError:
            self.fail("added uploader not found")

    def test_add_uploader_invalid(self):
        """Test various invalid calls to add_uploader."""
        # empty id
        with self.assertRaises(ValueError):
            self.facade.add_uploader("", self.TESTED_UPLOADER_NAME, self.TESTED_UPLOADER_EMAIL)

        # empty user
        with self.assertRaises(ValueError):
            self.facade.add_uploader(self.TESTED_UPLOADER_ID, "", self.TESTED_UPLOADER_EMAIL)

        # empty email
        with self.assertRaises(ValueError):
            self.facade.add_uploader(self.TESTED_UPLOADER_ID, self.TESTED_UPLOADER_NAME, "")

        # duplicate
        self.test_add_uploader_valid()
        self.assertFalse(self.facade.add_uploader(*self.TESTED_UPLOADER_PARAMS))

    def test_find_uploader(self):
        """Test finding added uploader."""
        self.test_add_uploader_valid()
        try:
            self.facade.get_uploader(self.TESTED_UPLOADER_ID)
        except self.facade.NotFoundError:
            self.fail("could not find added uploader")


if __name__ == '__main__':
    unittest.main()
