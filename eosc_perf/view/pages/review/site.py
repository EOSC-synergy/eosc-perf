"""This module contains the factory to generate site review pages."""
from typing import Tuple, Any, Dict

from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.controller.io_controller import controller
from eosc_perf.model.data_types import Report, SiteReport
from eosc_perf.model.facade import facade
from eosc_perf.utility.type_aliases import HTML
from eosc_perf.view.page_factory import PageFactory
from eosc_perf.view.pages.helpers import error_json_redirect, error_redirect, only_admin, only_admin_json


class SiteReviewPageFactory(PageFactory):
    """A factory to build site report view pages."""

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}

    @staticmethod
    def report_exists(uuid: str) -> bool:
        """Helper to determine whether a report exists.

        Args:
            uuid (str): The UUID of the report to check for.
        Returns:
            bool: True if the report exists.
        """
        try:
            facade.get_report(uuid)
            return True
        except facade.NotFoundError:
            return False


site_review_blueprint = Blueprint('site-review', __name__)


@site_review_blueprint.route('/review/site', methods=['GET'])
@only_admin
def review_site():
    """HTTP endpoint for the site review page."""
    uuid = request.args.get('uuid')
    if uuid is None:
        return error_redirect('Site review page opened with no uuid')

    factory = SiteReviewPageFactory()
    if not factory.report_exists(uuid):
        return error_redirect('Report given to review page does not exist')

    report: SiteReport = controller.get_report(uuid)

    if report.get_report_type() != Report.SITE:
        return error_redirect('Site review page opened with wrong report type')

    site_name = report.get_site().get_identifier()
    reporter = report.get_reporter()
    uploader_name = reporter.get_name()
    uploader_mail = reporter.get_email()

    date = report.get_date()

    page = factory.generate_page(
        template='review/site.jinja2.html',
        args=None,
        site_name=site_name,
        site_description=report.get_site().get_description(),
        site_human_name=report.get_site().get_name(),
        uploader_name=uploader_name,
        uploader_mail=uploader_mail,
        date=date,
        uuid=uuid)
    return Response(page, mimetype='text/html')


@site_review_blueprint.route('/ajax/review/site', methods=['POST'])
@only_admin_json
def review_site_submit():
    """HTTP endpoint to take in the reports."""
    uuid = request.form['uuid']

    # validate input
    if uuid is None:
        return error_json_redirect('Incomplete review form submitted (missing UUID)')
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

    return Response('{}', mimetype='application/json', status=200)
