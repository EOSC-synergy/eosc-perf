"""This module contains the factory to generate result report review pages.

Exposed endpoints:
    /review/result      - Result review page for administrators.
    /ajax/review/result - AJAX endpoint for the verdict.
"""

import json
from typing import Tuple, Any, Dict

from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.controller.io_controller import controller
from eosc_perf.model.data_types import Report, ResultReport
from eosc_perf.model.facade import facade
from eosc_perf.utility.type_aliases import HTML
from eosc_perf.view.page_factory import PageFactory
from eosc_perf.view.pages.helpers import error_redirect, only_admin, only_admin_json
from eosc_perf.view.pages.review.helper import process_report_review


class ViewReportPageFactory(PageFactory):
    """A factory to build result report view pages."""

    def __init__(self):
        super().__init__('review/result.jinja2.html')

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}

    @staticmethod
    def report_exists(uuid: str) -> bool:
        """Helper to determine whether a result exists.

        Args:
            uuid (str): The result to check existence for.
        Returns:
            bool: True if the result exists.
        """
        try:
            facade.get_report(uuid)
            return True
        except facade.NotFoundError:
            return False


view_report_blueprint = Blueprint('view-report', __name__)


@view_report_blueprint.route('/review/result', methods=['GET'])
@only_admin
def view_report():
    """HTTP endpoint for the view report page."""
    uuid = request.args.get('uuid')
    if uuid is None:
        return error_redirect('View report page opened with no uuid')

    factory = ViewReportPageFactory()
    if not factory.report_exists(uuid):
        return error_redirect('Report given to view page does not exist')

    report: ResultReport = controller.get_report(uuid)

    if report.get_report_type() != Report.RESULT:
        return error_redirect('View report page opened with wrong report type')

    message = report.get_message()
    reporter = report.get_reporter()
    reporter_name = reporter.get_name()
    reporter_mail = reporter.get_email()
    date = report.get_date()

    result = report.get_result()
    uploader = result.get_uploader()
    uploader_name = uploader.get_name()
    uploader_mail = uploader.get_email()

    site = result.get_site().get_name()
    benchmark = result.get_benchmark().get_docker_name()

    tags = [t.get_name() for t in result.get_tags()]
    tag_str = ', '.join(tags)
    json_data = json.dumps(json.loads(result.get_json()), indent=4)

    page = factory.generate_page(
        reporter_name=reporter_name,
        reporter_mail=reporter_mail,
        report_message=message,
        site=site,
        benchmark=benchmark,
        uploader_name=uploader_name,
        uploader_mail=uploader_mail,
        tags=tag_str,
        JSON=json_data,
        date=date,
        uuid=uuid)
    return Response(page, mimetype='text/html')


@view_report_blueprint.route('/ajax/review/result', methods=['POST'])
@only_admin_json
def view_report_submit():
    """HTTP endpoint to take in the reports.

    JSON Args: see process_report_review()
    """
    return process_report_review(request)
