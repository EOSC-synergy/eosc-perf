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
    uuid = request.args.get('uuid')
    if uuid is None:
        return redirect('/error?' + url_encode({
            'text': 'Site review page opened with no uuid'}), code=302)

    factory = SiteReviewPageFactory()
    if not factory.report_exists(uuid):
        return redirect('/error?' + url_encode({
            'text': 'Report given to review page does not exist'}), code=302)

    report: SiteReport = controller.get_report(uuid)

    if report.get_report_type() != Report.SITE:
        return redirect('/error?' + url_encode({
            'text': 'Site review page opened with wrong report type'}), code=302)

    site_name = report.get_site().get_short_name()

    with open('templates/site_review.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
            site_name=site_name,
            site_description=report.get_site().get_description(),
            site_human_name=report.get_site().get_name(),
            uuid=uuid)
    return Response(page, mimetype='text/html')

@site_review_blueprint.route('/site_review_submit', methods=['POST'])
def review_site_submit():
    """HTTP endpoint to take in the reports"""
    uuid = request.form['uuid']

    # validate input
    if uuid is None:
        return Response(json.dumps({'redirect': '/error?' + url_encode({
            'text': 'Incomplete review form submitted (missing UUID)'})}),
            mimetype='application/json', status=302)
    if not 'action' in request.form:
        return Response(json.dumps({'redirect': '/error?' + url_encode({
            'text': 'Incomplete report form submitted (missing verdict)'})}),
            mimetype='application/json', status=302)
    
    remove = None
    if request.form['action'] == 'remove':
        # something
        remove = True
    elif request.form['action'] == 'approve':
        # something else
        remove = False
    
    if remove is None:
        return Response(json.dumps({'redirect': '/error?' + url_encode({
            'text': 'Incomplete report form submitted (empty verdict)'})}),
            mimetype='application/json', status=302)

    # parse input
    # TODO: this functionality is MISSING from IOController/Authenticator
    email = controller.get_current_email()

    error_page = '/error?' + url_encode({'text': 'Error while reviewing report'})

    # TODO: this is NOT FUNCTIONAL in IOController/Authenticator
    # handle redirect in a special way because ajax
    if not controller.process_report(not remove, email, uuid):
        return Response(
            json.dumps({'redirect': error_page}),
            mimetype='application/json', status=302)

    return Response(json.dumps({}), mimetype='application/json', status=200)