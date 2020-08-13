"""This module contains the factory to generate result-comparison diagram
pages.
Provided is:
 - DiagramFactory
"""

import json

from flask import request, Response, redirect
from flask.blueprints import Blueprint
from werkzeug.urls import url_encode

from ..page_factory import PageFactory
from ..type_aliases import HTML, JSON

from ...model.facade import facade
from ...configuration import configuration

from .helpers import error_redirect

class DiagramFactory(PageFactory):
    """A factory to build diagram pages."""

    def _generate_content(self, args: JSON) -> HTML:
        pass

    def generate_script_content(self, uuids) -> HTML:
        """Generate script data for the diagram."""
        results = []
        for uuid in uuids:
            result_json = facade.get_result(uuid)
            # pulling at straws here, but hoping this is useful data
            result = json.loads(result_json.get_json())
            core_count = result['user_args']['num_gpus']
            score = result['evaluation']['result']['average_examples_per_sec']
            results.append({'core_count': core_count, 'score': score})

        # sort them by core_count
        results.sort(key=lambda result: result['core_count'])
        script_content = ', '.join([json.dumps(result) for result in results])
        return script_content

    def generate_page_content(self, uuids) -> HTML:
        """Generate page body code.

        This contains a list of compared results."""
        list_start = 'Comparing elements:'
        list_elements = []
        results = [facade.get_result(uuid) for uuid in uuids]
        for result in results:
            core_count = json.loads(result.get_json())['user_args']['num_gpus']
            list_elements.append('[{} - {} - {}]'.format(
                result.get_site().get_name(),
                result.get_benchmark().get_docker_name(),
                core_count))
        return list_start + ', '.join(list_elements)

    def check_if_results_exist(self, uuids) -> bool:
        """Helper method."""
        for uuid in uuids:
            try:
                facade.get_result(uuid)
            except facade.NotFoundError:
                return False
        return True


diagram_blueprint = Blueprint('diagram-factory', __name__)

@diagram_blueprint.route('/test_make_diagram', methods=['GET'])
def make_diagram_example():
    """Testing helper."""
    if not configuration['debug']:
        return error_redirect('This endpoint is not available in production')
    results = facade.query_results(json.dumps({
        'filters': [
            {
                'type': 'benchmark',
                'value': 'user/bench:version'
            },
            {
                'type': 'site',
                'value': 'rpi'
            }
        ]
    }))
    return redirect(
        '/make_diagram?' + url_encode({
            'result_uuids': [result.get_uuid() for result in results]}), code=302)

@diagram_blueprint.route('/make_diagram')
def query_results():
    """HTTP endpoint for diagram generation page"""
    uuids = request.args.getlist('result_uuids')
    if len(uuids) == 0:
        return redirect('/error?' + url_encode({
            'text': 'Diagram page called with invalid arguments'}), code=302)

    factory = DiagramFactory()

    if not factory.check_if_results_exist(uuids):
        return redirect('/error?' + url_encode({
            'text': 'At least one result given to diagram does not exist'}), code=302)

    args = {'uuids': uuids}

    with open('templates/diagram.html') as file:
        page = factory.generate_page(
            args=json.dumps(args),
            template=file.read(),
            page_content=factory.generate_page_content(uuids),
            script_content=factory.generate_script_content(uuids))
    return Response(page, mimetype='text/html')
