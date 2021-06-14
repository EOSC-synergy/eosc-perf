"""This module contains the factory to generate information pages.

Provided endpoints:
 - /info - (deprecated) Simple info text page.
 - /instructions - Benchmark upload instructions page.
 - /reports - Page with reports viewer for administrators.
 - /code_guidelines - Guidelines and requirements for benchmark development page.
 - /error - (deprecated) Simple error text page.
 - /privacy_policy  - Privacy policy page.
"""

import json
from typing import Tuple, Any, Dict

from deprecated import deprecated
from flask import request, Response
from flask.blueprints import Blueprint

from frontend.utility.type_aliases import HTML
from .helpers import error_redirect, only_admin
from ..page_factory import PageFactory


class SimplePageFactory(PageFactory):
    """A factory to build pages that are static or take in minimal arguments and provide no interaction."""

    def __init__(self, template):
        super().__init__(template)

    def _generate_content(self, args: Any = "") -> Tuple[HTML, Dict]:
        return args, {}


basic_pages = Blueprint('simple-factory', __name__)


@basic_pages.route('/info')
@deprecated(reason="Use modals and popups instead")
def info_page():
    """Info page to show text information to the user.
    """
    info = request.args.get('text')
    if info is None:
        return error_redirect('Empty information page opened')

    factory = SimplePageFactory('information.jinja2.html')
    return Response(factory.generate_page(args=info), mimetype='text/html')


@basic_pages.route('/instructions')
def instructions():
    """This is the page that includes upload instructions on how to submit new benchmarks.

    TODO: is this page necessary, should the instructions be embedded into the benchmark upload page directly?
    This page is currently unused.
    """
    factory = SimplePageFactory('submission/benchmark_upload_instruction.jinja2.html')
    return Response(factory.generate_page(), mimetype='text/html')


@basic_pages.route('/reports')
@only_admin
def report_list():
    """Page for the reports viewer available to administrators.
    """
    factory = SimplePageFactory('review/report_list.jinja2.html')
    return Response(factory.generate_page(), mimetype='text/html')


@basic_pages.route('/code_guidelines')
def code_guidelines():
    """Page containing the guidelines and requirements for benchmark development.
    """
    factory = SimplePageFactory('submission/benchmark_code_guidelines.jinja2.html')
    try:
        with open('frontend/model/sample_data/template.json') as min_template:
            info = json.loads(min_template.read())
    except OSError:
        info = "<Could not load template>"
    json_template = json.dumps(info, indent=4, sort_keys=True)
    return Response(factory.generate_page(args=json_template), mimetype='text/html')


@basic_pages.route('/error')
@deprecated(reason="Use modals and popups instead")
def error():
    """Generic error page to be redirected to in case of errors.

    TODO: this is deprecated, errors should be displayed as modals whenever possible.
    """
    info = request.args.get('text', default="Unknown error")

    factory = SimplePageFactory('error.jinja2.html')
    return Response(factory.generate_page(args=info), mimetype='text/html')


@basic_pages.route('/privacy_policy')
def privacy_page():
    """The page containing the privacy policy.
    This page is accessible by a link in the footer.
    """
    factory = SimplePageFactory('privacy_policy.jinja2.html')
    return Response(factory.generate_page(), mimetype='text/html')
