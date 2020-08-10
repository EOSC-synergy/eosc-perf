"""This module contains the factory to generate pages used to search 
benchmarks.
Provided is:
 - BenchmarkSearchFactory
"""

from flask import Response, redirect
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON


class BenchmarkSearchFactory(PageFactory):
    """A factory to build benchmark search pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def genereate_page_content(self) -> HTML:
        # Stub
        return "Search"

benchmark_search_blueprint = Blueprint('benchmark-search', __name__)

@benchmark_search_blueprint.route('/benchmark_search', methods=['GET'])
def search_benchmark():
    """HTTP endpoint for the benchmark search page"""
    factory = BenchmarkSearchFactory()

    with open('templates/benchmark_search.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read())
    return Response(page, mimetype='text/html')

@benchmark_search_blueprint.route('/benchmark_search_submit', methods=['POST'])
def search_benchmark_submit():
    """HTTP endpoint to take in benchmark searches"""
    return redirect('/')