"""This module contains the factory to generate information pages.
Provided is:
 - ResultReportPageFactory
"""

import json

from flask import request, Response, redirect, session
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from ...controller.io_controller import controller

from .helpers import error_json_redirect, error_redirect

class ResultReportPageFactory(PageFactory):
    """A factory to build information pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def generate_page_content(self, uuid) -> HTML:
        """Generate page body code.

        This contains the result json for the template."""
        result = facade.get_result(uuid)

        # return a pretty-printed version
        result_json = json.loads(result.get_json())
        string = json.dumps(result_json, indent=4, sort_keys=True)
        return string

    def result_exists(self, uuid: str) -> bool:
        """Helper to determine whether a result exists."""
        try:
            facade.get_result(uuid)
            return True
        except facade.NotFoundError:
            return False

result_report_blueprint = Blueprint('result-report-factory', __name__)

# temporary helper function for testing
from ...model.database import db
from ...model.data_types import ResultIterator
@result_report_blueprint.route('/get_some_result_id', methods=['GET'])
def get_some_result_id():
    """Mock helper."""
    iterator = ResultIterator(db.session)
    results = []
    for value in iterator:
        results.append(value)
    return Response(', '.join([result.get_uuid() for result in results]))

@result_report_blueprint.route('/report_result', methods=['GET'])
def report_result():
    """HTTP endpoint for the result report submission page"""

    if not controller.authenticate():
        return error_redirect('Not logged in')

    uuid = request.args.get('uuid')
    if uuid is None:
        return error_redirect('Report result page called with no result')

    factory = ResultReportPageFactory()
    if not factory.result_exists(uuid):
        return error_redirect('Result does not exist')

    with open('templates/report_result.html') as file:
        page = factory.generate_page(
            args='{}',
            template=file.read(),
            page_content=factory.generate_page_content(uuid),
            uuid=uuid)
    return Response(page, mimetype='text/html')

@result_report_blueprint.route('/report_result_submit', methods=['POST'])
def report_result_submit():
    """HTTP endpoint to take in the reports"""

    if not controller.authenticate():
        return error_json_redirect('Not logged in')

    uuid = request.form['uuid']
    message = request.form['message']
    # validate input
    if uuid is None:
        return error_json_redirect('Incomplete report form submitted (missing UUID)')

    if message is None:
        return error_json_redirect('Incomplete report form submitted (missing message)')

    # parse input
    uid = controller.get_user_id()
    if uid is None or len(uid) == 0:
        return error_json_redirect('Could not submit report (not logged in?)')

    metadata = {
        'type': 'result',
        'value': uuid,
        'message': message,
        'uploader': uid
    }

    # handle redirect in a special way because ajax
    if not controller.report(json.dumps(metadata)):
        return error_json_redirect('Failed to submit report')

    return Response('{}', mimetype='application/json', status=200)
