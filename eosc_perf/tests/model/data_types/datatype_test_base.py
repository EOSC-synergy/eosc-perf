import unittest

from flask import Flask

from eosc_perf.configuration import configuration
from eosc_perf.model.data_types import Uploader, Result, Site, Benchmark, SiteFlavor
from eosc_perf.model.database import configure_database
from eosc_perf.model.facade import facade


class DatatypeTestBase(unittest.TestCase):
    UPLOADER_IDENTIFIER: str = "IDENTIFIER"
    UPLOADER_EMAIL: str = "EMAIL"
    UPLOADER_NAME: str = "NAME"

    RESULT_JSON: str = "{}"

    BENCHMARK_DOCKER_NAME: str = "thechristophe/example-bench"
    BENCHMARK_DESCRIPTION: str = "Hello world!"
    BENCHMARK_TEMPLATE: str = "{}"

    def setUp(self):
        """Called before each test."""
        app = Flask("test")
        # set path to nowhere to use in-memory
        configuration.set('database-path', '')
        configure_database(app)

    def tearDown(self):
        """Called after each test."""

    def _make_uploader(self) -> Uploader:
        return Uploader(identifier=self.UPLOADER_IDENTIFIER, email=self.UPLOADER_EMAIL, name=self.UPLOADER_NAME)

    def _make_result(self, uploader: Uploader, site: Site, benchmark: Benchmark, flavor: SiteFlavor) -> Result:
        return Result(self.RESULT_JSON, uploader, site, benchmark, flavor)

    def _make_benchmark(self, uploader: Uploader) -> Benchmark:
        return Benchmark(self.BENCHMARK_DOCKER_NAME, uploader, self.BENCHMARK_DESCRIPTION, self.BENCHMARK_TEMPLATE)

    @staticmethod
    def _add_to_database(obj):
        # reuse from facade
        facade._add_to_database(obj)
