"""This module contains the factory to generate a Page displaying a result.
Provided is:
 - DisplayJsonFactory
"""
import json

from flask import request, Response
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from .helpers import error_redirect


class DisplayJsonFactory(PageFactory):
    """A factory to build information pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def generate_page_content(self, uuid: str) -> HTML:
        """Generate page body code.

        This contains the result json for the template.
        Args:
        uuid (str): uuid of the result to get displayed.
        Returns:
        HTML: The JSON in a readable format."""
        result = facade.get_result(uuid)
        # return a pretty-printed version.
        result_json = json.loads(result.get_json())
        string = json.dumps(result_json, indent=4, sort_keys=True)
        return string

    def result_exists(self, uuid: str) -> bool:
        """Helper to determine whether a result exists.
        Args:
            uuid (str): The result uuid to check.
        Returns:
            bool: If the result is in the database."""
        try:
            facade.get_result(uuid)
            return True
        except facade.NotFoundError:
            return False


display_json_blueprint = Blueprint('display-json', __name__)


@display_json_blueprint.route('/result')
def display_json_page():
    """HTTP endpoint for display result json page."""
    uuid = request.args.get('uuid')

    if uuid is None:
        return error_redirect('Result not found in Database.')

    factory = DisplayJsonFactory()
    if not factory.result_exists(uuid):
        return error_redirect('Result not found in Database.')

    with open('templates/display_json.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
            page_content=factory.generate_page_content(uuid),
            uuid=uuid)

    return Response(page, mimetype='text/html')
