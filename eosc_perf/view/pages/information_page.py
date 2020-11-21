"""This module contains the factory to generate information pages."""
import json
from typing import Tuple, Any, Dict

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from eosc_perf.utility.type_aliases import HTML
from ...controller.json_result_validator import DEFAULT_TEMPLATE_PATH

from .helpers import error_redirect


class InformationPageFactory(PageFactory):
    """A factory to build information pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return args, {}


info_blueprint = Blueprint('information-page-factory', __name__)


@info_blueprint.route('/info')
def info_page():
    """HTTP endpoint for information page."""
    info = request.args.get('text')
    if info is None:
        return error_redirect('Information page called with invalid arguments')

    factory = InformationPageFactory()
    page = factory.generate_page(template='information.html', args=info)
    return Response(page, mimetype='text/html')


@info_blueprint.route('/instructions')
def privacy_page():
    """HTTP endpoint for the upload instructions page."""
    factory = InformationPageFactory()
    page = factory.generate_page(template='upload_instruction.html')
    return Response(page, mimetype='text/html')


@info_blueprint.route('/code_guidelines')
def code_guidelines():
    """HTTP endpoint for code guidelines page."""
    factory = InformationPageFactory()
    with open('controller/' + DEFAULT_TEMPLATE_PATH) as min_template:
        info = json.loads(min_template.read())
    info_str = json.dumps(info, indent=4, sort_keys=True)
    page = factory.generate_page(template='code_guidelines.html', args=info_str)
    return Response(page, mimetype='text/html')


@info_blueprint.route('/error')
def error():
    """HTTP endpoint for information page."""
    info = request.args.get('text')
    if info is None:
        info = "Unknown error"

    factory = InformationPageFactory()
    page = factory.generate_page(template='error.html', args=info)
    return Response(page, mimetype='text/html')