"""This module contains the factory to generate benchmark submission pages."""
from typing import Tuple, Dict, Any

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...controller.io_controller import controller

from .helpers import error_json_redirect, error_redirect

class AddBenchmarkPageFactory(PageFactory):
    """A factory to build information pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}

add_benchmark_blueprint = Blueprint('add-benchmark-factory', __name__)

@add_benchmark_blueprint.route('/add_benchmark', methods=['GET'])
def add_benchmark():
    """HTTP endpoint for the benchmark submission page"""

    if not controller.is_authenticated():
        return error_redirect('Not logged in')

    factory = AddBenchmarkPageFactory()

    page = factory.generate_page(template='add_benchmark.html')
    return Response(page, mimetype='text/html')

@add_benchmark_blueprint.route('/add_benchmark_submit', methods=['POST'])
def add_benchmark_submit():
    """HTTP endpoint to take in the reports"""

    if not controller.is_authenticated():
        return error_json_redirect('Not logged in')

    docker_name = request.form['docker_name']
    message = request.form['message']
    # validate input
    if docker_name is None:
        return error_json_redirect('Incomplete report form submitted (missing Docker name)')

    # handle redirect in a special way because ajax
    try:
        if not controller.submit_benchmark(docker_name, message):
            return error_json_redirect('Failed to submit benchmark')
    except (RuntimeError, ValueError) as exception:
        return error_json_redirect(str(exception))

    return Response('{}', mimetype='application/json', status=200)
