"""This module contains the factory to generate error pages.
Provided is:
 - ErrorPageFactory
"""

import json

from flask import request, Response
from flask.blueprints import Blueprint

from .page_factory import PageFactory
from .information_page_factory import InformationPageFactory
from .type_aliases import HTML, JSON


class ErrorPageFactory(InformationPageFactory):
    """A factory to build information pages."""

    def __init__(self):
        super().__init__()

    def _generate_content(self, args: JSON) -> HTML:
        pass

    # def set_info(self, info: str):
    #    pass


error_blueprint = Blueprint('error-page-factory', __name__)


@error_blueprint.route('/error')
def error():
    """HTTP endpoint for information page"""
    info = request.args.get('text')
    if info is None:
        # TODO: error page
        info = "Unknown error"
        
    factory = ErrorPageFactory()
    factory.set_info(info)
    with open('templates/error.html') as file:
        page = factory.generate_page('{}', file.read())
    return Response(page, mimetype='text/html')
