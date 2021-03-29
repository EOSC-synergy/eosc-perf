"""This module contains the factory to generate the site editor page available to administrators.

Exposed endpoints:
    /site_editor - HTML page for the user
    /ajax/update/site - AJAX endpoint to update a given site
"""
from typing import Tuple, Dict, Any

from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.utility.type_aliases import HTML
from eosc_perf.model.facade import facade
from .helpers import error_json_redirect, only_admin, only_admin_json
from ..page_factory import PageFactory


class EditSitePageFactory(PageFactory):
    """A factory to build site edit pages."""

    def __init__(self):
        super().__init__('site_editor.jinja2.html')

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


site_editor_blueprint = Blueprint('edit-site-factory', __name__)


@site_editor_blueprint.route('/site_editor', methods=['GET'])
@only_admin
def site_editor():
    """HTTP endpoint for the site editor."""
    factory = EditSitePageFactory()
    page = factory.generate_page()
    return Response(page, mimetype='text/html')


@site_editor_blueprint.route('/ajax/update/site', methods=['POST'])
@only_admin_json
def ajax_update_site():
    """HTTP endpoint to take in updated site information.

    JSON Args:
        identifier  - Site identifier
        description - Human-readable description text
        full_name   - Human-readable full name
        address     - Homepage/website of this given site
    """
    site_name = request.form.get("identifier")
    site = facade.get_site(site_name)
    if site is None:
        return error_json_redirect("Unknown site")

    description = request.form.get("description")
    if description is not None:
        site.set_description(description)
    full_name = request.form.get("full_name", default=site_name)
    if full_name is not None:
        site.set_name(full_name)
    address = request.form.get("address")
    if address is not None:
        site.set_address(address)

    return Response('{}', mimetype='application/json', status=200)
