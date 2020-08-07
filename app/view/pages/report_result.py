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
#from ...controller.io_controller import controller
# mock class because the actual class doesn't work...
class Controller():
    def report(self, email: str, metadata: JSON) -> bool:
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
    iterator = ResultIterator(db.session)
    results = []
    for value in iterator:
        results.append(value)
    return Response(', '.join([result.get_uuid() for result in results]))

@result_report_blueprint.route('/report_result', methods=['GET'])
def report_result():
    """HTTP endpoint for the result report submission page"""
    uuid = request.args.get('uuid')
    if uuid is None:
        return redirect('/error?' + url_encode({
            'text': 'Report result page called with no result'}), code=302)

    factory = ResultReportPageFactory()
    if not factory.result_exists(uuid):
        return redirect('/error?' + url_encode({'text':
            'Result does not exist'}), code=302)

    with open('templates/report_result.html') as file:
        page = factory.generate_page(args='{}', template=file.read(),
            page_content=factory.generate_page_content(uuid),
            uuid=uuid)
    return Response(page, mimetype='text/html')

@result_report_blueprint.route('/report_result_submit', methods=['POST'])
def report_result_submit():
    """HTTP endpoint to take in the reports"""
    uuid = request.form['uuid']
    message = request.form['message']
    #uploader = request.args.get('uploader')
    # validate input
    if uuid is None:
        return redirect('/error?' + url_encode({'text':
            'Incomplete result report form submitted (missing UUID)'}), code=302)
    if message is None:
        return redirect('/error?' + url_encode({'text':
            'Incomplete result report form submitted (missing message)'}), code=302)

    # parse input
    # TODO: this functionality is MISSING from IOController/Authenticator
    email = controller.get_current_email()

    metadata = {
        'type': 'result',
        'value': uuid,
        'message': message,
        'uploader': email
    }

    error_page = '/error?' + url_encode({'text': 'Failed to submit report'})

    # TODO: this is NOT FUNTIONAL in IOController/Authenticator
    # handle redirect in a special way because ajax
    if not controller.report(email, metadata):
        return Response(json.dumps({'redirect': error_page}),
            mimetype='application/json', status=302)

    return Response(json.dumps({}), mimetype='application/json', status=200)
