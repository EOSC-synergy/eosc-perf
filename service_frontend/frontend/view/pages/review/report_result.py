"""This module contains the factory to generate information pages.
"""

import json
from typing import Tuple, Any, Dict

from flask import request, Response
from flask.blueprints import Blueprint

from frontend.controller.io_controller import controller
from frontend.model.facade import facade
from frontend.utility.type_aliases import HTML
from frontend.view.page_factory import PageFactory
from frontend.view.pages.helpers import error_json_redirect, error_redirect, only_authenticated_json, \
    only_authenticated

from ....model.data_types import Report


class ResultReportPageFactory(PageFactory):
    """A factory to build information pages."""

    def __init__(self):
        super().__init__('review/report_result.jinja2.html')

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}

    @staticmethod
    def generate_page_content(uuid: str) -> HTML:
        """Generate page body code.

        This contains the result json for the template.

        Args:
            uuid (str): The UUID of the result to report.
        Returns:
            HTML: HTML content with the result JSON.
        """
        result = facade.get_result(uuid)

        # return a pretty-printed version
        result_json = json.loads(result.get_json())
        string = json.dumps(result_json, indent=4, sort_keys=True)
        return string

    @staticmethod
    def result_exists(uuid: str) -> bool:
        """Helper to determine whether a result exists.

        Args:
            uuid (str): The UUID of the result to look for.
        Returns:
            bool: True if the result exists.
        """
        try:
            facade.get_result(uuid)
            return True
        except facade.NotFoundError:
            return False


result_report_blueprint = Blueprint('result-report-factory', __name__)


@result_report_blueprint.route('/report/result', methods=['GET'])
@only_authenticated
def report_result():
    """HTTP endpoint for the result report submission page."""
    uuid = request.args.get('uuid')
    if uuid is None:
        return error_redirect('Report result page called with no result')

    factory = ResultReportPageFactory()
    if not factory.result_exists(uuid):
        return error_redirect('Result does not exist')

    page = factory.generate_page(
        page_content=factory.generate_page_content(uuid),
        uuid=uuid)
    return Response(page, mimetype='text/html')


@result_report_blueprint.route('/ajax/report/result', methods=['POST'])
@only_authenticated_json
def report_result_submit():
    """HTTP endpoint to take in the reports.

    JSON Args:
        uuid    - UUID of result reported.
        message - Report reason.
    """
    uuid = request.form.get('uuid')
    if uuid is None:
        return error_json_redirect('Missing UUID')

    message = request.form.get('message')
    if message is None:
        return error_json_redirect('Missing report message')

    # parse input
    uid = controller.get_user_id()
    if uid is None or len(uid) == 0:
        return error_json_redirect('Could not submit report (not logged in?)')

    # handle redirect in a special way because ajax
    if not controller.report(Report.RESULT, uuid, message, uid):
        return error_json_redirect('Failed to submit report')

    return Response('{}', mimetype='application/json', status=200)
