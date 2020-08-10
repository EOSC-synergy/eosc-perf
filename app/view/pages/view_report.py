"""This module contains the factory to generate report review pages.
Provided is:
 - ViewReportPageFactory
"""

import json

from flask import request, Response, redirect
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from ...model.data_types import Report, ResultReport
from ...controller.io_controller import controller
from ...configuration import configuration

from .helpers import error_json_redirect, error_redirect

class ViewReportPageFactory(PageFactory):
    """A factory to build result report view pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def report_exists(self, uuid: str) -> bool:
        """Helper to determine whether a result exists."""

        try:
            facade.get_report(uuid)
            return True
        except facade.NotFoundError:
            return False

view_report_blueprint = Blueprint('view-report', __name__)

@view_report_blueprint.route('/test_view_report', methods=['GET'])
def test_view_report():
    """Testing helper."""
    if not configuration['debug']:
        return error_redirect('This endpoint is not available in production')
    reports = facade.get_reports(only_unanswered=False)
    for report in reports:
        if report.get_report_type() == Report.RESULT:
            return redirect('/view_report?' + url_encode({'uuid': report.get_uuid()}), code=302)

@view_report_blueprint.route('/view_report', methods=['GET'])
def view_report():
    """HTTP endpoint for the view report page"""

    if not controller.authenticate():
        return error_redirect('Not logged in')

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

    with open('templates/view_report.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
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
    """HTTP endpoint to take in the reports"""

    if not controller.authenticate():
        return error_json_redirect('Not logged in')

    uuid = request.form['uuid']

    # validate input
    if uuid is None:
        return error_json_redirect('Incomplete report form submitted (missing UUID)')
    if not 'action' in request.form:
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
