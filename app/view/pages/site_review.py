"""This module contains the factory to generate site review pages.
Provided is:
 - SiteReviewPageFactory
"""

import json

from flask import request, Response, redirect, session
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from ...model.data_types import Report, SiteReport
from ...controller.io_controller import controller

from .helpers import error_json_redirect, error_redirect

class SiteReviewPageFactory(PageFactory):
    """A factory to build site report view pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def report_exists(self, name: str) -> bool:
        """Helper to determine whether a site exists."""

        try:
            facade.get_report(name)
            return True
        except facade.NotFoundError:
            return False

site_review_blueprint = Blueprint('site-review', __name__)

@site_review_blueprint.route('/test_site_review', methods=['GET'])
def test_site_review():
    """Testing helper."""
    reports = facade.get_reports(only_unanswered=False)
    for report in reports:
        if report.get_report_type() == Report.SITE:
            return redirect('/site_review?' + url_encode({'uuid': report.get_uuid()}), code=302)

@site_review_blueprint.route('/site_review', methods=['GET'])
def review_site():
    """HTTP endpoint for the site review page"""

    if not controller.authenticate():
        return error_redirect('Not logged in')

    uuid = request.args.get('uuid')
    if uuid is None:
        return error_redirect('Site review page opened with no uuid')

    factory = SiteReviewPageFactory()
    if not factory.report_exists(uuid):
        return error_redirect('Report given to review page does not exist')

    report: SiteReport = controller.get_report(uuid)

    if report.get_report_type() != Report.SITE:
        return error_redirect('Site review page opened with wrong report type')

    site_name = report.get_site().get_short_name()
    reporter = report.get_reporter()
    uploader_name = reporter.get_name()
    uploader_mail = reporter.get_email()

    date = report.get_date()

    with open('templates/site_review.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
            site_name=site_name,
            site_description=report.get_site().get_description(),
            site_human_name=report.get_site().get_name(),
            uploader_name=uploader_name,
            uploader_mail=uploader_mail,
            date=date,
            uuid=uuid)
    return Response(page, mimetype='text/html')

@site_review_blueprint.route('/site_review_submit', methods=['POST'])
def review_site_submit():
    """HTTP endpoint to take in the reports"""

    if not controller.authenticate():
        return error_json_redirect('Not logged in')

    uuid = request.form['uuid']

    # validate input
    if uuid is None:
        return error_json_redirect('Incomplete review form submitted (missing UUID)')
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

    return Response('{}', mimetype='application/json', status=200)
