import unittest

from frontend.tests.model.model.model_test_base import FacadeTestBase


class FacadeTagTests(FacadeTestBase):
    def test_add_tag_valid(self):
        """Test valid call to add_tag."""
        self.assertTrue(self.facade.add_tag(self.TESTED_TAG_NAME))

        try:
            self.facade.get_tag(self.TESTED_TAG_NAME)
        except self.facade.NotFoundError:
            self.fail("added tag not found")

    def test_add_tag_invalid(self):
        """Test various invalid calls to add_tag."""
        with self.assertRaises(ValueError):
            self.facade.add_tag("")

        self.test_add_tag_valid()
        self.assertFalse(self.facade.add_tag(self.TESTED_TAG_NAME))

    def test_find_tag(self):
        """Test finding added tag."""
        self.test_add_tag_valid()
        try:
            self.facade.get_tag(self.TESTED_TAG_NAME)
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


if __name__ == '__main__':
    unittest.main()
