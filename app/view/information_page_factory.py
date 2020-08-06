"""This module contains the factory to generate information pages.
Provided is:
 - InformationPageFactory
"""

import json

from flask import request, Response, redirect
from flask.blueprints import Blueprint

from .page_factory import PageFactory
from .type_aliases import HTML, JSON


class InformationPageFactory(PageFactory):
    """A factory to build information pages."""

    def __init__(self):
        super().__init__()

    def _generate_content(self, args: JSON) -> HTML:
        pass

    # def set_info(self, info: str):
    #    pass


info_blueprint = Blueprint('information-page-factory', __name__)


@info_blueprint.route('/info')
def info():
    """HTTP endpoint for information page"""
    info = request.args.get('text')
    if info is None:
        return redirect("/error?text=Information%20page%20called%20with%20invalid%20arguments", code=302)
    else:
        factory = InformationPageFactory()
        factory.set_info(info)
        with open('templates/information.html') as file:
            page = factory.generate_page('{}', file.read())
        return Response(page, mimetype='text/html')
