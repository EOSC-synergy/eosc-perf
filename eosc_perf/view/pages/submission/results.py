"""This module exposes the factory to generate the result upload page.

Exposed endpoints:
    /submit/result      - Result submission page.
    /ajax/submit/result - AJAX endpoint that takes in new result data.
"""

from pathlib import Path
from typing import Tuple, Any, Dict

from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.controller.io_controller import controller
from eosc_perf.utility.type_aliases import HTML
from eosc_perf.view.page_factory import PageFactory
from eosc_perf.view.pages.helpers import only_authenticated_json, \
    only_authenticated, error_json_message
from model.facade import facade


class UploadJSONFactory(PageFactory):
    """A factory to build upload pages."""

    UPLOAD_LICENSE_PATH: str = "upload_license.txt"

    def __init__(self):
        super().__init__('submission/result.jinja2.html')

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {"license": self.get_license_string()}

    def get_license_string(self) -> str:
        """Helper: Get result upload license as string.

        Returns:
            str: The license text.
        """
        path = Path(Path.cwd(), self.UPLOAD_LICENSE_PATH)
        with open(path, "r") as license_file:
            license_string = license_file.read()
        return license_string.replace('\n', '<br/>')


upload_json_blueprint = Blueprint('upload_json_blueprint', __name__)


@upload_json_blueprint.route('/submit/result', methods=['GET'])
@only_authenticated
def upload_result():
    """HTTP endpoint for the result upload page."""
    factory = UploadJSONFactory()
    return Response(factory.generate_page(args=None), mimetype='text/html')


@upload_json_blueprint.route('/ajax/submit/result', methods=['POST'])
@only_authenticated_json
def upload_result_submit():
    """HTTP endpoint to take in results."""
    # check if the post request has the file part
    if 'resultData' not in request.files:
        return error_json_message('No file in request')
    file = request.files['resultData']

    # if user does not select file, browser might
    # submit an empty part without filename
    if file.filename == '':
        return error_json_message('Missing file')
    try:
        result_json = file.read().decode("utf-8")
    except KeyError:
        return error_json_message("Uploaded file is not UTF-8 encoded.")

    try:
        tags = request.form.getlist("tags")
    except KeyError:
        return error_json_message("Missing tags")

    try:
        site_id = request.form["siteIdentifier"]
    except KeyError:
        return error_json_message("Missing site")
    custom_site = len(site_id) == 0

    try:
        benchmark_name = request.form['benchmark']
    except KeyError:
        return error_json_message("Missing benchmark")

    flavor = "unknown"

    if custom_site:
        try:
            custom_site_name = request.form["customSiteIdentifier"]
        except KeyError:
            return error_json_message("Missing custom site id")

        try:
            custom_site_address = request.form["customSiteAddress"]
        except KeyError:
            return error_json_message("Missing custom site address")

        try:
            custom_site_description = request.form["customSiteDescription"]
        except KeyError:
            return error_json_message("Missing custom site description")

        try:
            custom_site_flavor = request.form["customSiteFlavor"]
        except KeyError:
            return error_json_message("Missing custom site flavor")

        if len(custom_site_name) == 0:
            return error_json_message("Custom site id empty")

        try:
            site = facade.get_site(custom_site_name)
        except facade.NotFoundError:
            if not controller.submit_site(custom_site_name, custom_site_address, description=custom_site_description):
                return error_json_message('Failed to submit new site')
            try:
                site = facade.get_site(custom_site_name)
            except facade.NotFoundError:
                return error_json_message("Site added, but failed to get it (report a bug!)")
            if len(custom_site_flavor) > 0:
                # ignore response, if it fails, there's a flavor with the name we want, which is fine
                controller.submit_flavor(custom_site_flavor, '', custom_site_name)

        if site.get_hidden() is False:
            return error_json_message('There is already a site with name "{}"'.format(custom_site_name))
        else:
            # if site with same name exists but is hidden, add result anyway, as it was probably added by this same user
            pass

        if len(custom_site_flavor) > 0:
            flavor = custom_site_flavor

        site_id = custom_site_name
    else:
        try:
            # 'unknown' is a selectable option, no special case here
            flavor = request.form["siteFlavor"]
        except KeyError:
            return error_json_message("Missing site flavor")

    try:
        success = controller.submit_result(result_json, controller.get_user_id(), benchmark_name, site_id, flavor, tags)
    except (ValueError, TypeError) as error:
        return error_json_message('Failed to submit result: ' + str(error))
    if not success:
        if custom_site:
            controller.remove_site(site_id)
        return error_json_message("Failed to submit result")

    return Response('{}', mimetype='application/json', status=200)


@upload_json_blueprint.route('/ajax/submit/tag', methods=['POST'])
@only_authenticated_json
def upload_tag():
    """HTTP endpoint to take in new tags."""
    tag = request.form['new_tag']
    if tag == "":
        return error_json_message('No name entered for new tag')
    controller.submit_tag(tag)
    return Response('{}', mimetype='application/json', status=200)
