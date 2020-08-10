"""This module contains the factory to generate information pages.
Provided is:
 - ReviewPageFactory
"""

import json
import urllib.request

from flask import request, Response, redirect, session
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode
import markdown2

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from ...model.data_types import Report, BenchmarkReport
from ...controller.io_controller import controller
from ...controller.authenticator import AuthenticateError

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

def decompose_dockername(docker_name):
    """Helper to break a model-docker_name into a tuple."""
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
    
    return (username, image, tag)

def build_dockerhub_url(docker_name):
    """Helper function to build a link to a docker hub page."""
    (username, image, tag) = decompose_dockername(docker_name)

    docker_hub_url = 'https://hub.docker.com/r/{}/{}'.format(username, image)
    return docker_hub_url

def build_dockerregistry_url(docker_name):
    """Helper function to build a link to the docker hub registry api."""
    (username, image, tag) = decompose_dockername(docker_name)

    docker_hub_url = 'https://registry.hub.docker.com/v2/repositories/{}/{}/'.format(username, image)
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

    try:
        report: BenchmarkReport = controller.get_report(uuid)
    except AuthenticateError:
        return redirect('/error?' + url_encode({
            'text': 'You are not authenticated'}), code=302)

    if report.get_report_type() != Report.BENCHMARK:
        return redirect('/error?' + url_encode({
            'text': 'Benchmark review page opened with wrong report type'}), code=302)

    docker_name = report.get_benchmark().get_docker_name()
    reporter = report.get_reporter()
    uploader_name = reporter.get_name()
    uploader_mail = reporter.get_email()
    
    date = report.get_date()

    # link to the image on docker hub
    dockerhub_link = build_dockerhub_url(docker_name)

    # sneaky call to their secret terribly documented API
    try:
        dockerhub_content = urllib.request.urlopen(build_dockerregistry_url(docker_name)).read()
        content = json.loads(dockerhub_content)
        dockerhub_desc = content['full_description']
        dockerhub_desc_formatted = markdown2.markdown(dockerhub_desc, extras=["fenced-code-blocks", "tables"])
    except:
        dockerhub_desc_formatted = "Could not load description"

    with open('templates/benchmark_review.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
            docker_name=docker_name,
            docker_link=dockerhub_link,
            docker_desc=dockerhub_desc_formatted,
            uploader_name=uploader_name,
            uploader_mail=uploader_mail,
            date=date,
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
        remove = True
    elif request.form['action'] == 'approve':
        remove = False
    
    if remove is None:
        return Response(json.dumps({'redirect': '/error?' + url_encode({
            'text': 'Incomplete report form submitted (empty verdict)'})}),
            mimetype='application/json', status=302)

    error_page = '/error?' + url_encode({'text': 'Error while reviewing report'})

    # handle redirect in a special way because ajax
    if not controller.process_report(not remove, uuid):
        return Response(
            json.dumps({'redirect': error_page}),
            mimetype='application/json', status=302)

    return Response(json.dumps({}), mimetype='application/json', status=200)
