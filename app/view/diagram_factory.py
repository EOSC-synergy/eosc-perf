"""This module contains the factory to generate result-comparison diagram
pages.
Provided is:
 - DiagramFactory
"""

import json

from flask import request, Response, redirect
from flask.blueprints import Blueprint

from .page_factory import PageFactory
from .type_aliases import HTML, JSON


class DiagramFactory(PageFactory):
    """A factory to build diagram pages."""

    def __init__(self):
        super().__init__()

    def _generate_content(self, args: JSON) -> HTML:
        pass

    # def set_info(self, info: str):
    #    pass


diagram_blueprint = Blueprint('diagram-factory', __name__)


@diagram_blueprint.route('/make_diagram')
def query_results():
    """HTTP endpoint for diagram generation page"""
    uuids = request.args.getlist('result_uuids')
    if uuids is None:
        return redirect("/error?text=Diagram%20page%20called%20with%20invalid%20arguments", code=302)
    else:
        factory = DiagramFactory()
        factory.set_info("benchmark x page y")
        args = {'uuids': uuids}
        with open('templates/diagram.html') as file:
            page = factory.generate_page(json.dumps(args), file.read())
        return Response(page, mimetype='text/html')
