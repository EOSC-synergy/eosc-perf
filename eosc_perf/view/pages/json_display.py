"""This module contains the factory to generate a Page displaying a result."""
import json
from typing import Any, Tuple, Dict

from flask import request, Response, Markup
from flask.blueprints import Blueprint

from ..page_factory import PageFactory
from eosc_perf.utility.type_aliases import HTML

from ...model.facade import facade
from .helpers import error_redirect


class DisplayJsonFactory(PageFactory):
    """A factory to build information pages."""

    def _generate_content(self, uuid: Any) -> Tuple[HTML, Dict]:
        """Generate page body code.

        This contains the result json for the template.
        Args:
            uuid (str): uuid of the result to get displayed.
        Returns:
            HTML: The JSON in a readable format.
        """
        result = facade.get_result(uuid)
        # return a pretty-printed version.
        result_json = json.loads(result.get_json())
        # pretty-print with HTML newlines
        string = json.dumps(result_json, indent=2).replace('\n', '<br/>')
        return Markup(string), {}

    def result_exists(self, uuid: str) -> bool:
        """Helper to determine whether a result exists.

        Args:
            uuid (str): The result uuid to check.
        Returns:
            bool: If the result is in the database.
        """
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

    page = factory.generate_page(
        template='display_json.html',
        args=uuid,
        uuid=uuid)

    return Response(page, mimetype='text/html')
