"""This module contains the factory to generate result-comparison diagram pages."""

import json
from typing import Tuple, Dict, Any, List

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

    def _generate_content(self, args: Any) -> Tuple[HTML, Dict]:
        return "", {}

    def generate_script_content(self, uuids: List[str]) -> HTML:
        """Generate script data for the diagram.
        Args:
            uuids (List[str]): A list containing multiple UUIDs of results to display.
        Returns:
            HTML: JavaScript data containing the needed data about every result for a diagram.
        """
        results = []
        for uuid in uuids:
            result_json = facade.get_result(uuid)
            # pulling at straws here, but hoping this is useful data
            result = json.loads(result_json.get_json())
            core_count = int(result['user_args']['num_gpus'])
            score = float(result['training']['result']['average_examples_per_sec'])
            results.append(
                {
                    'core_count': core_count,
                    'score': score,
                    'site': result_json.get_site().get_short_name()
                })

        # sort them by core_count
        results.sort(key=lambda result: result['core_count'])
        script_content = ', '.join([json.dumps(result) for result in results])
        return script_content

    def generate_page_content(self, uuids: List[str]) -> HTML:
        """Generate page body code.

        This contains a list of compared results.

        Args:
            uuids (List[str]): A list containing multiple UUIDs of results to display.
        Returns:
            HTML: HTML code to display a list of all results in the diagram.
        """
        list_start = '<div class="card"><div class="card-header">' \
            'Compared results: site, benchmark, num_gpus' \
            '</div><ul class="list-group list-group-flush">'
        list_end = '</ul></div>'
        list_elements = []
        results = [facade.get_result(uuid) for uuid in uuids]

        # sort list in same order as diagram
        results.sort(key=lambda result: int(json.loads(result.get_json())['user_args']['num_gpus']))
        
        for result in results:
            core_count = json.loads(result.get_json())['user_args']['num_gpus']
            list_elements.append('<li class="list-group-item result-info">{}, {}, {}</li>'.format(
                result.get_site().get_name(),
                result.get_benchmark().get_docker_name(),
                core_count))
        return list_start + ''.join(list_elements) + list_end

    def check_if_results_exist(self, uuids: List[str]) -> bool:
        """Helper method.
        Args:
            uuids (List[str]): A list of UUIDs of results to check existence for.
        Returns:
            bool: True if all results exist.
        """
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
    if not configuration.get('debug'):
        return error_redirect('This endpoint is not available in production')
    results = facade.query_results(json.dumps({
        'filters': [
            {
                'type': 'benchmark',
                'value': 'donotuse/diagram:test'
            },
            {
                'type': 'site',
                'value': 'diagram_site'
            }
        ]
    }))
    return redirect(
        '/make_diagram?' + url_encode({
            'result_uuids': [result.get_uuid() for result in results]}), code=302)

@diagram_blueprint.route('/make_diagram')
def query_results():
    """HTTP endpoint for diagram generation page."""
    uuids = request.args.getlist('result_uuids')
    if len(uuids) == 0:
        return error_redirect('Diagram page called with invalid arguments')

    factory = DiagramFactory()

    if not factory.check_if_results_exist(uuids):
        return error_redirect('At least one result given to diagram does not exist')

    args = {'uuids': uuids}

    try:
        script_content = factory.generate_script_content(uuids)
    except ValueError:
        return error_redirect('At least one result provided has invalid fields')

    page = factory.generate_page(
        template='diagram.html',
        args=json.dumps(args),
        page_content=factory.generate_page_content(uuids),
        script_content=script_content)
    return Response(page, mimetype='text/html')
