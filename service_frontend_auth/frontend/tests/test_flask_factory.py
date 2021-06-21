import unittest

from flask import Flask

from frontend.flask_factory import create_app


class FlaskFactoryTests(unittest.TestCase):
    @unittest.skip("requires fully set up environment with files")
    def test_create_app(self):
        self.assertEqual(Flask, type(create_app()))

    @unittest.skip("requires fully set up environment with files")
    def test_create_app_custom_config(self):
        self.assertEqual(Flask, type(create_app({'debug': True, 'database-path': ''})))


if __name__ == '__main__':
    unittest.main()
