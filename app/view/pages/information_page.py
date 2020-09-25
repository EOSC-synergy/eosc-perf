"""This module contains the factory to generate information pages.
Provided is:
 - InformationPageFactory
 - Http endpoint code guidelines
 - Http endpoint upload instructions
"""
import json
import os
from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON
from ...controller.json_result_validator import DEFAULT_TEMPLATE_PATH

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


@info_blueprint.route('/instructions')
def privacy_page():
    """HTTP endpoint for the upload instructions page."""
    factory = InformationPageFactory()
    with open('templates/upload_instruction.html') as file:
        page = factory.generate_page('{}', file.read())
    return Response(page, mimetype='text/html')


@info_blueprint.route('/code_guidelines')
def code_guidelines():
    """HTTP endpoint for code guidelines page"""
    factory = InformationPageFactory()
    info = json.loads("{}")
    with open('controller/'+DEFAULT_TEMPLATE_PATH) as min_template:
        info = json.loads(min_template.read())
    info = json.dumps(info, indent=4, sort_keys=True)
    factory.set_info(info)
    with open('templates/code_guidelines.html') as file:
        page = factory.generate_page('{}', file.read())
    return Response(page, mimetype='text/html')
