"""This module contains the factory to generate result search pages.

Exposed endpoints:
    /search_results - Result search page
"""

import json
from typing import Tuple, Any, Dict

from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.controller.io_controller import controller
from eosc_perf.model.facade import facade
from eosc_perf.utility.type_aliases import HTML, JSON
from eosc_perf.view.page_factory import PageFactory
from eosc_perf.view.pages.helpers import error_redirect


class SearchResultFactory(PageFactory):
    """ A factory to create search result pages."""

    def __init__(self):
        super().__init__('search/results.jinja2.html')

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        """Generate js code containing information required for the search page.

        Args:
            args (dict): A json containing the benchmark name.
        Returns:
            HTML: JS variables for 'benchmark' and 'admin'.
        """
        return "", {"benchmark": args["benchmark"], 'admin': controller.is_admin()}


result_search_blueprint = Blueprint('result_search', __name__)


@result_search_blueprint.route('/search_results')
def make_search_page():
    """Http endpoint for result search generation."""
    benchmark = request.args.get('benchmark', default="")
    if benchmark != "":
        try:
            facade.get_benchmark(docker_name=benchmark)
        except facade.NotFoundError:
            return error_redirect('Result search requires a valid Benchmark name')
    args = json.dumps({'benchmark': benchmark})
    factory = SearchResultFactory()
    return Response(factory.generate_page(args=args), mimetype='text/html')


@result_search_blueprint.route('/ajax/delete/result')
def delete_result():
    """Http endpoint for result deletion ajax fetch.

    JSON Args:
        uuid - Result UUID
    """
    if not controller.is_admin():
        return Response('You not authenticated for this action.', mimetype='text/html')

    uuid = request.args.get('uuid')

    if not controller.remove_result(uuid=uuid):
        return Response('Result search requires a valid Benchmark name', mimetype='text/html')

    return Response("Successful removed result.", mimetype='text/html')
