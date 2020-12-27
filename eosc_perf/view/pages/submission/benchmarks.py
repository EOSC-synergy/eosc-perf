"""This module contains the factory to generate benchmark submission pages."""
from typing import Tuple, Dict, Any

from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.view.page_factory import PageFactory
from eosc_perf.utility.type_aliases import HTML
from eosc_perf.controller.authenticator import AuthenticateError

from eosc_perf.controller.io_controller import controller

from eosc_perf.view.pages.helpers import error_json_redirect, error_redirect


class AddBenchmarkPageFactory(PageFactory):
    """A factory to build benchmark submission pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


add_benchmark_blueprint = Blueprint('add-benchmark-factory', __name__)


@add_benchmark_blueprint.route('/add_benchmark', methods=['GET'])
def add_benchmark():
    """HTTP endpoint for the benchmark submission page."""

    if not controller.is_authenticated():
        return error_redirect('Not logged in')

    factory = AddBenchmarkPageFactory()

    page = factory.generate_page(template='submission/benchmark.html')
    return Response(page, mimetype='text/html')


@add_benchmark_blueprint.route('/add_benchmark_submit', methods=['POST'])
def add_benchmark_submit():
    """HTTP endpoint to take in new benchmarks."""
    docker_name = request.form['docker_name'] if 'docker_name' in request.form else None
    message = request.form['message'] if 'message' in request.form else "No description given."
    template = request.form['template'] if 'template' in request.form and len(request.form['template']) > 2 else None

    # validate input
    if docker_name is None:
        return error_json_redirect('⚠ Incomplete report form submitted (missing Docker name)')

    # handle redirect in a special way because ajax
    try:
        if not controller.submit_benchmark(docker_name, message, template):
            return error_json_redirect('Failed to submit benchmark')
    except (RuntimeError, ValueError, AuthenticateError) as exception:
        return error_json_redirect('⚠ ' + str(exception))

    return Response('{}', mimetype='application/json', status=200)
