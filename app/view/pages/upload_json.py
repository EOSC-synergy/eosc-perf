"""This module contains the factory to generate the result upload page.
Provided is:
 - UploadJSONFactory
"""

import json

from flask import request, Response, redirect
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from ...controller.io_controller import controller
from ...configuration import configuration
from ...model.database import db
from ...model.data_types import ResultIterator

from .helpers import error_json_redirect, error_redirect

class UploadJSONFactory(PageFactory):
    """A factory to build upload pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

upload_json_blueprint = Blueprint('upload_json_blueprint', __name__)

@upload_json_blueprint.route('/upload', methods=['GET'])
def report_result():
    """HTTP endpoint for the result upload page"""

    if not controller.authenticate():
        return error_redirect('Not logged in')

    factory = UploadJSONFactory()

    with open('templates/upload.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read())
    return Response(page, mimetype='text/html')

@upload_json_blueprint.route('/upload_submit', methods=['POST'])
def report_result_submit():
    pass