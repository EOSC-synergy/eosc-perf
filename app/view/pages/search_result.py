"""This module contains the factory to generate result search pages
Provided is:
- SearchResultFactory
"""
import json
from flask import request, Response, redirect
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON
from ...controller.io_controller import controller
from ...model.facade import facade
from ...configuration import configuration


class SearchResultFactory(PageFactory):
    """ A factory to create search result pages."""

    def _generate_content(self, args: JSON) -> HTML:
        """Generate js code containing information reqired for searchpage.
        Args:
            args (JSON): A json containing a 'benchmark' and 'admin' value
        Returns:
            HTML: The finished content."""
        arguments = json.loads(args)
        try:
            result = "admin = {}; benchmark = '{}';".format(
                'true' if arguments['admin'] else 'false',
                arguments['benchmark'])
        except KeyError as error:
            print(error)
            result = ""
        return result


result_search_blueprint = Blueprint('result_search', __name__)


@result_search_blueprint.route('/result_search')
def make_search_page():
    """Http endpoint for resultsearch genration."""
    benchmark = request.args.get('benchmark')
    if benchmark is None:
        benchmark = ""
    else:
        try:
            facade.get_benchmark(benchmark)
        except facade.NotFoundError:
            return redirect(
                '/error?'+url_encode(
                    {'text': 'Result search reqires a valid Benchmark name'}), code=302)
    args = json.dumps({'benchmark': benchmark, 'admin': controller.is_admin()})
    factory = SearchResultFactory()
    print(factory._generate_content(args))
    with open('templates/result_search.html') as file:
        page = factory.generate_page(args=args, template=file.read())
    return Response(page, mimetype='text/html')
