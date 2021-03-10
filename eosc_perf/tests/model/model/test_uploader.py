import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeUploaderTests(FacadeTestBase):
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


if __name__ == '__main__':
    unittest.main()
