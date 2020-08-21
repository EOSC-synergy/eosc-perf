"""This module contains the factory to generate the result upload page.
Provided is:
 - UploadJSONFactory
"""

import json
from pathlib import Path

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON
from ...configuration import configuration

from ...controller.io_controller import controller

from .helpers import error_json_redirect, error_redirect

class UploadJSONFactory(PageFactory):
    """A factory to build upload pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    @staticmethod
    def get_license_string() -> str:
        """Helper: Get result upload license as string:"""
        filename = configuration["upload_license_filename"]
        path = str(Path(__file__).parent) + "/../../../" + filename
        with open(path, "r") as license_file:
            license_string = license_file.read()
        return license_string

upload_json_blueprint = Blueprint('upload_json_blueprint', __name__)

@upload_json_blueprint.route('/upload', methods=['GET'])
def upload_result():
    """HTTP endpoint for the result upload page"""

    if not controller.is_authenticated():
        return error_redirect('Not logged in')

    factory = UploadJSONFactory()

    with open('templates/upload.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
            license=factory.get_license_string().replace('\n', '<br>'))
    return Response(page, mimetype='text/html')

@upload_json_blueprint.route('/upload_submit', methods=['POST'])
def upload_result_submit():
    """HTTP endpoint to take in results"""
    if not controller.is_authenticated():
        return error_json_redirect('Not logged in')
    # check if the post request has the file part
    if 'file' not in request.files:
        return error_redirect('No file in request')
    file = request.files['file']
    # if user does not select file, browser might
    # submit an empty part without filename
    if file.filename == '':
        return error_json_redirect('No file in request')

    tags = request.form.getlist("tags")
    if "--No Tag--" in tags:
        tags.remove("--No Tag--")

    site_name = ""
    custom_site = (request.form["custom_site"] == 'true')
    if not custom_site:
        site_name = request.form['site']
    else:
        site_name = request.form["new_site_name"]
        existing_site = controller.get_site(site_name)
        if existing_site is None:
            if site_name == "":
                return error_json_redirect("No name for custom site entered.")
            if request.form["new_site_address"] == "":
                return error_json_redirect("No address for custom site entered.")
            if not controller.submit_site(site_name, request.form["new_site_address"], description=request.form["new_site_description"]):
                return error_json_redirect('Failed to submit new site.')
        else:
            print(existing_site.get_hidden())
            if existing_site.get_hidden() is False:
                msg = 'There is already a site with name "{}"'.format(site_name)
                return error_json_redirect(msg)
            else:
                # if site with same name exists but is hidden, add result anyway
                pass

    metadata = {
        'uploader': controller.get_user_id(),
        'site': site_name,
        'benchmark': request.form['benchmark'],
        'tags': tags
    }
    try:
        result_json = file.read().decode("utf-8")
    except ValueError:
        return error_json_redirect("Uploaded file is not UTF-8 encoded.")

    try:
        success = controller.submit_result(result_json, json.dumps(metadata))
    except (ValueError, TypeError) as error:
        return error_json_redirect('Failed to submit result: ' + str(error))
    if not success:
        return error_json_redirect('Failed to submit result.')

    return Response('{}', mimetype='application/json', status=200)

@upload_json_blueprint.route('/upload_tag', methods=['POST'])
def upload_tag():
    """HTTP endpoint to take in new tags"""
    tag = request.form['new_tag']
    if tag == "":
        return error_json_redirect('No name entered for new tag')
    if tag == "--No Tag--":
        return error_json_redirect('New tag cannot ba called "--No Tag--", as that is a placeholder name')
    controller.submit_tag(tag)
    return Response('{}', mimetype='application/json', status=200)
