"""This module contains the factory to generate information pages."""

import json
import urllib.request
from typing import Tuple, Dict, Any

from flask import request, Response, redirect
from flask.blueprints import Blueprint
import markdown2
from werkzeug.urls import url_encode

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade, DatabaseFacade
from ...model.data_types import Report, BenchmarkReport
from ...controller.io_controller import controller
from ...controller.authenticator import AuthenticateError

from .helpers import error_json_redirect, error_redirect, info_redirect


def report_exists(uuid: str) -> bool:
    """Helper to determine whether a benchmark exists.

    Args:
        uuid (str): Report UUID
    """
    try:
        facade.get_report(uuid)
        return True
    except facade.NotFoundError:
        return False


class BenchmarkReviewPageFactory(PageFactory):
    """A factory to build benchmark report view pages."""
    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


def decompose_dockername(docker_name: str) -> Tuple[str, str, str]:
    """Helper to break a model-docker_name into a tuple.

    Args:
        docker_name (str): full docker name
    """
    slash = docker_name.find('/')
    if slash == -1:
        # this should not have passed input validation
        pass
    username = docker_name[:slash]
    colon = docker_name.find(':')
    if colon == -1:
        image = docker_name[slash + 1:]
        tag = None
    else:
        image = docker_name[slash + 1:colon]
        tag = docker_name[colon + 1:]

    return username, image, tag


def build_dockerhub_url(docker_name):
    """Helper function to build a link to a docker hub page."""
    (username, image, tag) = decompose_dockername(docker_name)

    url = 'https://hub.docker.com/r/{}/{}'.format(username, image)
    return url


def build_dockerregistry_url(docker_name):
    """Helper function to build a link to the docker hub registry api."""
    (username, image, tag) = decompose_dockername(docker_name)

    url = 'https://registry.hub.docker.com/v2/repositories/{}/{}/'.format(username, image)
    return url


benchmark_review_blueprint = Blueprint('benchmark-review', __name__)


@benchmark_review_blueprint.route('/benchmark_review_fetch_first', methods=['GET'])
def get_benchmark_review():
    """Review the first new benchmark."""
    if not controller.is_admin():
        return error_redirect('Not an admin')
    reports = facade.get_reports(only_unanswered=True)
    if len(reports) == 0:
        return info_redirect('No reports available')
    # use first benchmark report we can find
    for report in reports:
        if report.get_report_type() == Report.BENCHMARK:
            return redirect(
                '/benchmark_review?' + url_encode({'uuid': report.get_uuid()}), code=302)
    return info_redirect('No benchmark to review')


@benchmark_review_blueprint.route('/benchmark_review', methods=['GET'])
def review_benchmark():
    """HTTP endpoint for the benchmark review page"""

    if not controller.is_authenticated():
        return error_redirect('Not logged in')

    if not controller.is_admin():
        return error_redirect('Not an administrator')

    uuid = request.args.get('uuid')
    if uuid is None:
        return error_redirect('Benchmark review page opened with no uuid')

    factory = BenchmarkReviewPageFactory()
    if not report_exists(uuid):
        return error_redirect('Report given to review page does not exist')

    try:
        report: BenchmarkReport = controller.get_report(uuid)
    except AuthenticateError:
        return error_redirect('You are not authenticated')

    if report.get_report_type() != Report.BENCHMARK:
        return error_redirect('Benchmark review page opened with wrong report type')

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
        dockerhub_desc_formatted = markdown2.markdown(dockerhub_desc, extras=[
            "fenced-code-blocks", "tables", "break-on-newline", "cuddled-lists"])
    except:
        dockerhub_desc_formatted = "Could not load description"

    page = factory.generate_page(
        template='benchmark_review.html',
        args=None,
        docker_name=docker_name,
        docker_link=dockerhub_link,
        docker_desc=dockerhub_desc_formatted,
        desc=report.get_message(),
        uploader_name=uploader_name,
        uploader_mail=uploader_mail,
        date=date,
        uuid=uuid)
    return Response(page, mimetype='text/html')


@benchmark_review_blueprint.route('/benchmark_review_submit', methods=['POST'])
def review_benchmark_submit():
    """HTTP endpoint to take in the reports"""

    if not controller.is_authenticated():
        return error_json_redirect('Not logged in')

    if not controller.is_authenticated():
        return error_json_redirect('Not an admin')

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
