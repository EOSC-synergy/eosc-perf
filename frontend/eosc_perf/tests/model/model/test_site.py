import unittest

from eosc_perf.tests.model.model.model_test_base import FacadeTestBase


class FacadeSiteTests(FacadeTestBase):
    def test_add_site_valid(self):
        """Test valid call to add_site."""
        self.assertTrue(self.facade.add_site(*self.TESTED_SITE_PARAMS))

        try:
            self.facade.get_site(self.TESTED_SITE_NAME)
        except self.facade.NotFoundError:
            self.fail("added site not found")

    def test_add_site_invalid(self):
        """Test various invalid calls to add_site."""
        # empty name
        with self.assertRaises(ValueError):
            self.facade.add_site("", self.TESTED_SITE_ADDRESS)

        # empty address
        with self.assertRaises(ValueError):
            self.facade.add_site(self.TESTED_SITE_NAME, "")

        self.test_add_site_valid()
        self.assertFalse(self.facade.add_site(*self.TESTED_SITE_PARAMS))

    def test_find_site(self):
        """Test finding added site."""
        self.test_add_site_valid()
        try:
            self.facade.get_site(self.TESTED_SITE_NAME)
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
        self.assertTrue(self.facade.remove_site(self.TESTED_SITE_NAME))
        with self.assertRaises(self.facade.NotFoundError):
            self.facade.get_site(self.TESTED_SITE_NAME)

    def test_remove_site_invalid(self):
        """Test removing a site that doesn't exist."""
        self.assertFalse(self.facade.remove_site(self.TESTED_SITE_NAME))

    def test_add_flavor(self):
        self.test_add_site_valid()
        self.assertTrue(self.facade.add_flavor(self.TESTED_FLAVOR_NAME, "", self.TESTED_SITE_NAME))


if __name__ == '__main__':
    unittest.main()
