"""This module contains the factory to generate benchmark review pages.

Exposed endpoints:
    /review/benchmark      - Benchmark review page for administrators.
    /ajax/review/benchmark - AJAX endpoint for the verdict.
"""

import json
import urllib.request
from typing import Tuple, Dict, Any
from urllib.error import URLError

import markdown2
from flask import request, Response
from flask.blueprints import Blueprint

from eosc_perf.controller.authenticator import AuthenticateError
from eosc_perf.controller.io_controller import controller
from eosc_perf.model.data_types import Report, BenchmarkReport
from eosc_perf.model.facade import facade
from eosc_perf.utility.dockerhub import build_dockerhub_url, build_dockerregistry_url
from eosc_perf.utility.type_aliases import HTML
from eosc_perf.view.page_factory import PageFactory
from eosc_perf.view.pages.helpers import error_redirect, only_admin, only_admin_json
from view.pages.review.helper import process_report_review


def report_exists(uuid: str) -> bool:
    """Helper to determine whether a benchmark exists.

    Args:
        uuid (str): The UUID to check for.
    """
    try:
        facade.get_report(uuid)
        return True
    except facade.NotFoundError:
        return False


class BenchmarkReviewPageFactory(PageFactory):
    """A factory to build benchmark report view pages."""

    def __init__(self):
        super().__init__('review/benchmark.jinja2.html')

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}


benchmark_review_blueprint = Blueprint('benchmark-review', __name__)


@benchmark_review_blueprint.route('/review/benchmark', methods=['GET'])
@only_admin
def review_benchmark():
    """HTTP endpoint for the benchmark review page."""
    uuid = request.args.get('uuid')
    if uuid is None:
        return error_redirect('Benchmark review page opened with no uuid')

    factory = BenchmarkReviewPageFactory()
    if not report_exists(uuid):
        return error_redirect('Report given to review page does not exist')

    try:
        report: BenchmarkReport = controller.get_report(uuid)
    except AuthenticateError:
        return error_redirect('Could not find report')

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
    except (json.JSONDecodeError, URLError, KeyError):
        dockerhub_desc_formatted = "Could not load description"

    page = factory.generate_page(
        docker_name=docker_name,
        docker_link=dockerhub_link,
        docker_desc=dockerhub_desc_formatted,
        desc=report.get_message(),
        uploader_name=uploader_name,
        uploader_mail=uploader_mail,
        date=date,
        uuid=uuid)
    return Response(page, mimetype='text/html')


@benchmark_review_blueprint.route('/ajax/review/benchmark', methods=['POST'])
@only_admin_json
def review_benchmark_submit():
    """HTTP endpoint to take in the reports."""
    return process_report_review(request)
