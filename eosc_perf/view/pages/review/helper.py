from flask import Response

from controller.io_controller import controller
from view.pages.helpers import error_json_redirect


def process_report_review(request):
    """Process report response.

    All reports are identified by an UUID, and processing them does not require referencing the reported object, so all
    reports can be processed similarly.
    """
    uuid = request.form.get('uuid')

    # validate input
    if uuid is None:
        return error_json_redirect('Incomplete report form submitted (missing UUID)')

    action = request.form.get('action')

    if action is None or action not in ['remove', 'approve']:
        return error_json_redirect('Incomplete report form submitted (invalid verdict)')

    remove = False
    if request.form['action'] == 'remove':
        remove = True

    # handle redirect in a special way because ajax
    if not controller.process_report(not remove, uuid):
        return error_json_redirect('Error while reviewing report')

    return Response("{}", mimetype='application/json', status=200)
