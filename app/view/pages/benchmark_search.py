"""This module contains the factory to generate pages used to search 
benchmarks.
Provided is:
 - BenchmarkSearchFactory
"""

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from flask.blueprints import Blueprint


class BenchmarkSearchFactory(PageFactory):
    """A factory to build benchmark search pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def genereate_page_content(self) -> HTML:
        # Stub
        return "Search"

        