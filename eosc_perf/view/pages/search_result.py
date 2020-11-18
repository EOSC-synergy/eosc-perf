"""This module contains the factory to generate result search pages."""
import json
from typing import Tuple, Any, Dict

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON
from ...controller.io_controller import controller
from ...model.facade import facade

from .helpers import error_redirect


class SearchResultFactory(PageFactory):
    """ A factory to create search result pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        """Generate js code containing information required for the search page.
        Args:
            args (JSON): A json containing a 'benchmark' and 'admin' value.
        Returns:
            HTML: JS variables for 'benchmark' and 'admin'.
        """
        arguments = json.loads(args)
        try:
            result = "admin = {}; benchmark = '{}';".format(
                'true' if arguments['admin'] else 'false',
                arguments['benchmark'])
        except KeyError as error:
            print(error)
            result = ""
        return result, {}


result_search_blueprint = Blueprint('result_search', __name__)


@result_search_blueprint.route('/result_search')
def make_search_page():
    """Http endpoint for result search generation."""
    benchmark = request.args.get('benchmark')
    if benchmark is None:
        benchmark = ""
    else:
        try:
            facade.get_benchmark(docker_name=benchmark)
        except facade.NotFoundError:
            return error_redirect('Result search reqires a valid Benchmark name')
    args = json.dumps({'benchmark': benchmark, 'admin': controller.is_admin()})
    factory = SearchResultFactory()
    page = factory.generate_page(template='result_search.html', args=args)
    return Response(page, mimetype='text/html')


@result_search_blueprint.route('/delete_result')
def delete_result():
    """Http endpoint for result deletion ajax fetch."""
    if not controller.is_admin():
        return Response('You not authenticated for this action.', mimetype='text/html')

    uuid = request.args.get('uuid')

    if not controller.remove_result(uuid=uuid):
        return Response('Result search reqires a valid Benchmark name', mimetype='text/html')

    return Response("Successfull removed result.", mimetype='text/html')
