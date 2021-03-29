"""This module contains the factory to generate pages used to search benchmarks.

Exposed endpoints:
- / - Benchmark search page. This acts as the home page.
"""
from typing import Tuple, Dict, Any

from flask import Response
from flask.blueprints import Blueprint

from eosc_perf.utility.type_aliases import HTML
from eosc_perf.view.page_factory import PageFactory


class BenchmarkSearchFactory(PageFactory):
    """A factory to build benchmark search pages."""

    def __init__(self):
        super().__init__('search/benchmarks.jinja2.html')

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


benchmark_search_blueprint = Blueprint('benchmark-search', __name__)


@benchmark_search_blueprint.route('/', methods=['GET'])
def search_benchmark():
    """HTTP endpoint for the benchmark search page."""
    factory = BenchmarkSearchFactory()
    return Response(factory.generate_page(), mimetype='text/html')
