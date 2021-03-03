"""This module contains the factory to generate pages used to search benchmarks."""
from typing import Tuple, Dict, Any

from flask import Response
from flask.blueprints import Blueprint

from eosc_perf.view.page_factory import PageFactory
from eosc_perf.utility.type_aliases import HTML


class BenchmarkSearchFactory(PageFactory):
    """A factory to build benchmark search pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


benchmark_search_blueprint = Blueprint('benchmark-search', __name__)


@benchmark_search_blueprint.route('/', methods=['GET'])
def search_benchmark():
    """HTTP endpoint for the benchmark search page."""
    factory = BenchmarkSearchFactory()
    return Response(factory.generate_page(template='search/benchmarks.jinja2.html'), mimetype='text/html')
