"""This module contains the factory to generate information pages.
Provided is:
 - InformationPageFactory
"""

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from .helpers import error_redirect

class InformationPageFactory(PageFactory):
    """A factory to build information pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass


info_blueprint = Blueprint('information-page-factory', __name__)


@info_blueprint.route('/info')
def info_page():
    """HTTP endpoint for information page"""
    info = request.args.get('text')
    if info is None:
        return error_redirect('Information page called with invalid arguments')

    factory = InformationPageFactory()
    factory.set_info(info)
    with open('templates/information.html') as file:
        page = factory.generate_page('{}', file.read())
    return Response(page, mimetype='text/html')
