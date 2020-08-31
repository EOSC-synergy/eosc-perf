"""This module contains the factory to generate benchmark submission pages.
Provided is:
 - AddBenchmarkPageFactory
"""

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...controller.io_controller import controller

from .helpers import error_json_redirect, error_redirect

class AddBenchmarkPageFactory(PageFactory):
    """A factory to build information pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

add_benchmark_blueprint = Blueprint('add-benchmark-factory', __name__)

@add_benchmark_blueprint.route('/add_benchmark', methods=['GET'])
def add_benchmark():
    """HTTP endpoint for the benchmark submission page"""

    if not controller.is_authenticated():
        return error_redirect('Not logged in')

    factory = AddBenchmarkPageFactory()

    with open('templates/add_benchmark.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read())
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

    # parse input
    uid = controller.get_user_id()
    if uid is None or len(uid) == 0:
        return error_json_redirect('Could not submit benchmark (not logged in?)')


    # handle redirect in a special way because ajax
    if not controller.submit_benchmark(uid, docker_name, message):
        return error_json_redirect('Failed to submit benchmark')

    return Response('{}', mimetype='application/json', status=200)
