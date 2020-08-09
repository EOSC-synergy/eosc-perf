"""This module contains the factory to generate information pages.
Provided is:
 - ReviewPageFactory
"""

import json

from flask import request, Response, redirect, session
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from ...model.data_types import Report, BenchmarkReport
#from ...controller.io_controller import controller
# mock class because the actual class doesn't work...
class Controller():
    """Mock class."""
    def get_report(self, uuid) -> Report:
        """Mock method."""
        return facade.get_report(uuid)

    def process_report(self, verdict: bool, user: str, uuid: str) -> bool:
        """Mock method."""
        return True

    def get_current_email(self) -> str:
        """Mock method."""
        try:
            email = session['user']
            return email
        except KeyError:
            return 'nobody'

controller = Controller()

class BenchmarkReviewPageFactory(PageFactory):
    """A factory to build benchmark report view pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def report_exists(self, name: str) -> bool:
        """Helper to determine whether a benchmark exists."""

        try:
            facade.get_report(name)
            return True
        except facade.NotFoundError:
            return False

def build_dockerhub_url(docker_name):
    """Helper function to build a link to a docker hub page."""
    slash = docker_name.find('/')
    if slash == -1:
        # this should not have passed input validation
        pass
    username = docker_name[:slash]
    colon = docker_name.find(':')
    if colon == -1:
        image = docker_name[slash + 1:]
        tag = ''
    else:
        image = docker_name[slash + 1:colon]
        tag = docker_name[colon + 1:]

    docker_hub_url = 'https://hub.docker.com/r/{}/{}'.format(username, image)
    return docker_hub_url

benchmark_review_blueprint = Blueprint('benchmark-review', __name__)

@benchmark_review_blueprint.route('/test_benchmark_review', methods=['GET'])
def test_benchmark_review():
    """Testing helper."""
    reports = facade.get_reports(only_unanswered=False)
    for report in reports:
        if report.get_report_type() == Report.BENCHMARK:
            return redirect('/benchmark_review?' + url_encode({'uuid': report.get_uuid()}), code=302)

@benchmark_review_blueprint.route('/benchmark_review', methods=['GET'])
def review_benchmark():
    """HTTP endpoint for the benchmark review page"""
    uuid = request.args.get('uuid')
    if uuid is None:
        return redirect('/error?' + url_encode({
            'text': 'Benchmark review page opened with no uuid'}), code=302)

    factory = BenchmarkReviewPageFactory()
    if not factory.report_exists(uuid):
        return redirect('/error?' + url_encode({
            'text': 'Report given to review page does not exist'}), code=302)

    report: BenchmarkReport = controller.get_report(uuid)

    if report.get_report_type() != Report.BENCHMARK:
        return redirect('/error?' + url_encode({
            'text': 'Benchmark review page opened with wrong report type'}), code=302)

    docker_name = report.get_benchmark().get_docker_name()

    with open('templates/benchmark_review.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
            docker_name=docker_name,
            dockerhub_link=build_dockerhub_url(docker_name),
            uuid=uuid)
    return Response(page, mimetype='text/html')

@benchmark_review_blueprint.route('/benchmark_review_submit', methods=['POST'])
def review_benchmark_submit():
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
