"""This module contains the factory to generate the site editor page available to administrators.

Exposed endpoints:
    /site_editor - HTML page for the user
    /ajax/update/site - AJAX endpoint to update a given site
"""
from typing import Tuple, Dict, Any

from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.utility.type_aliases import HTML
from model.facade import facade
from .helpers import error_json_redirect, only_admin, only_admin_json
from ..page_factory import PageFactory
from ...controller.io_controller import controller


class EditSitePageFactory(PageFactory):
    """A factory to build site edit pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


site_editor_blueprint = Blueprint('edit-site-factory', __name__)


@site_editor_blueprint.route('/site_editor', methods=['GET'])
@only_admin
def site_editor():
    """HTTP endpoint for the site editor."""
    factory = EditSitePageFactory()
    page = factory.generate_page(template='site_editor.jinja2.html')
    return Response(page, mimetype='text/html')


@site_editor_blueprint.route('/ajax/update/site', methods=['POST'])
@only_admin_json
def ajax_update_site():
    """HTTP endpoint to take in updated site information.

    Required fields:
        identifier  - Site identifier
        description - Human-readable description text
        full_name   - Human-readable full name
        address     - Homepage/website of this given site
    """
    site_name = request.form["identifier"]
    try:
        site = facade.get_site(site_name)
    except facade.NotFoundError:
        return error_json_redirect("Unknown site")

    if "description" not in request.form:
        return error_json_redirect("[Missing description field, file a bug]")
    if "full_name" not in request.form:
        return error_json_redirect("[Missing full_name field, file a bug]")
    if "address" not in request.form:
        return error_json_redirect("[Missing address field, file a bug]")

    description = request.form["description"]
    full_name = request.form["full_name"] if len(request.form["full_name"]) > 0 else site_name
    address = request.form["address"]

    # update fields from here
    site.set_description(description)
    site.set_name(full_name)
    site.set_address(address)

    return Response('{}', mimetype='application/json', status=200)
