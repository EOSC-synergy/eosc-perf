"""This module contains the factory to generate the result upload page.
Provided is:
 - UploadJSONFactory
"""

import json

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...controller.io_controller import controller

from .helpers import error_json_redirect, error_redirect, info_redirect

class UploadJSONFactory(PageFactory):
    """A factory to build upload pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

upload_json_blueprint = Blueprint('upload_json_blueprint', __name__)

@upload_json_blueprint.route('/upload', methods=['GET'])
def report_result():
    """HTTP endpoint for the result upload page"""

    if not controller.is_authenticated():
        return error_redirect('Not logged in')

    factory = UploadJSONFactory()

    with open('templates/upload.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read())
    return Response(page, mimetype='text/html')

@upload_json_blueprint.route('/upload_submit', methods=['POST'])
def report_result_submit():
    """HTTP endpoint to take in results"""
    if not controller.is_authenticated():
        return error_redirect('Not logged in')
    # check if the post request has the file part
    if 'file' not in request.files:
        return error_redirect('No file in request')
    file = request.files['file']
    # if user does not select file, browser might
    # submit an empty part without filename
    if file.filename == '':
        return error_redirect('No file in request')

    tags = request.form.getlist("tags")
    try:
        # trying to remove placeholder for no tags
        tags.remove("--No Tag--")
    except ValueError:
        pass

    metadata = {
        'uploader': controller.get_user_id(),
        'site': request.form['site'],
        'benchmark': request.form['benchmark'],
        'tags': tags}

    try:
        result_json = file.read().decode("utf-8")
    except ValueError:
        return error_redirect("Uploaded file is not UTF-8 encoded.")

    try:
        success = controller.submit_result(result_json, json.dumps(metadata))
    except (ValueError, TypeError) as e:
        return error_redirect('Failed to submit report: ' + str(e))
    if not success:
        return error_redirect('Failed to submit report.')
    return info_redirect("Submission succesful")
