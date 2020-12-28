"""This module contains the factory to generate site editing pages."""
import logging
from typing import Tuple, Dict, Any

from flask import request, Response
from flask.blueprints import Blueprint

from ...model.database import db
from ..page_factory import PageFactory
from eosc_perf.utility.type_aliases import HTML
from ...controller.authenticator import AuthenticateError

from ...controller.io_controller import controller

from .helpers import error_json_redirect, error_redirect, only_admin, only_admin_json


class EditSitePageFactory(PageFactory):
    """A factory to build site edit pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


site_editor_blueprint = Blueprint('edit-site-factory', __name__)


@site_editor_blueprint.route('/site_editor', methods=['GET'])
@only_admin
def edit_site():
    """HTTP endpoint for the benchmark submission page."""
    factory = EditSitePageFactory()
    page = factory.generate_page(template='site_editor.html')
    return Response(page, mimetype='text/html')


@site_editor_blueprint.route('/update-site', methods=['POST'])
@only_admin_json
def edit_site_submit():
    """HTTP endpoint to take in the reports."""
    site_name = request.form["short_name"]
    site = controller.get_site(site_name)
    if site is None:
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
