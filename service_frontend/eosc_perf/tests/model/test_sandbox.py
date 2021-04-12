import unittest

from eosc_perf.configuration import configuration
from eosc_perf.model.sandbox import add_demo


class SandboxTests(unittest.TestCase):
    def setUp(self) -> None:
        configuration.reset()
        configuration.set('database-path', '')

    def tearDown(self) -> None:
        pass

    def test_add_demo(self):
        self.assertIsNone(add_demo())


if __name__ == '__main__':
    unittest.main()
