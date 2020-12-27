"""This module contains the factory to generate report review pages."""

import json
from typing import Tuple, Any, Dict

from flask import request, Response, redirect
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode

from eosc_perf.view.page_factory import PageFactory
from eosc_perf.utility.type_aliases import HTML

from eosc_perf.model.facade import facade
from eosc_perf.model.data_types import Report, ResultReport
from eosc_perf.controller.io_controller import controller

from eosc_perf.view.pages.helpers import error_json_redirect, error_redirect, info_redirect


class ViewReportPageFactory(PageFactory):
    """A factory to build result report view pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        pass

    def report_exists(self, uuid: str) -> bool:
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


@view_report_blueprint.route('/view_report_fetch_first', methods=['GET'])
def test_view_report():
    """Review the first new benchmark report."""
    if not controller.is_admin():
        return error_redirect('Not an admin')
    reports = facade.get_reports(only_unanswered=True)
    if len(reports) == 0:
        return info_redirect('No reports available')
    for report in reports:
        if report.get_report_type() == Report.RESULT:
            return redirect('/view_report?' + url_encode({'uuid': report.get_uuid()}), code=302)
    return info_redirect('No result report to review')


@view_report_blueprint.route('/view_report', methods=['GET'])
def view_report():
    """HTTP endpoint for the view report page."""
    if not controller.is_authenticated():
        return error_redirect('Not logged in')

    if not controller.is_admin():
        return error_redirect('Not an admin')

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
        template='review/result.html',
        args=None,
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


@view_report_blueprint.route('/view_report_submit', methods=['POST'])
def view_report_submit():
    """HTTP endpoint to take in the reports."""
    if not controller.is_authenticated():
        return error_json_redirect('Not logged in')

    if not controller.is_authenticated():
        return error_json_redirect('Not an admin')

    uuid = request.form['uuid']

    # validate input
    if uuid is None:
        return error_json_redirect('Incomplete report form submitted (missing UUID)')
    if 'action' not in request.form:
        return error_json_redirect('Incomplete report form submitted (missing verdict)')

    remove = None
    if request.form['action'] == 'remove':
        remove = True
    elif request.form['action'] == 'approve':
        remove = False

    if remove is None:
        return error_json_redirect('Incomplete report form submitted (empty verdict)')

    # handle redirect in a special way because ajax
    if not controller.process_report(not remove, uuid):
        return error_json_redirect('Error while reviewing report')

    return Response(json.dumps({}), mimetype='application/json', status=200)
