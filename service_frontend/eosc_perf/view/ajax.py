"""This module contains the classes responsible for AJAX queries.

 AJAX endpoints are provided to load data without having to reload the entire page. This module mostly contains endpoints
 to GET data, such as searches/queries (with filters/keywords), fetches (all data). Endpoints used to update or submit
 new data are generally defined in the respective page module that makes use of them.

Exposed endpoints:
- /ajax/query/results      - AJAX endpoint for result search queries.
- /ajax/query/benchmarks   - AJAX endpoint for benchmark search queries.
- /ajax/fetch/sites        - AJAX endpoint to fetch sites.
- /ajax/fetch/tags         - AJAX endpoint to fetch tags.
- /ajax/fetch/reports      - AJAX endpoint to fetch reports for administrators.
- /ajax/fetch/notable_keys - AJAX endpoint to fetch JSON-paths for notable values in benchmark JSON data.
- /ajax/update/flavor      - AJAX endpoint to update site flavor metadata.
"""

import json
from abc import abstractmethod
from json import JSONDecodeError
from typing import Optional, Tuple

from flask import request, Response
from flask.blueprints import Blueprint
from deprecated import deprecated

from .pages.helpers import only_admin_json
from ..controller.io_controller import controller
from eosc_perf.utility.type_aliases import JSON
from ..model.facade import facade


class AJAXHandler:
    """Abstract class to represent any AJAX request endpoint."""

    @abstractmethod
    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch data corresponding to given query."""


class ResultSearchAJAX(AJAXHandler):
    """AJAX handler for benchmark result searches with filters.
    """

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch benchmark results corresponding to given query."""
        admin = controller.is_admin()
        try:
            results = facade.query_results(query, not admin)
        except ValueError:
            return "", 401
        results_dict = {"results": []}
        for result in results:
            result_dict = {
                "data": json.loads(result.json),
                "uuid": result.uuid,
                "site": result.site.identifier,
                "benchmark": result.benchmar.docker_name,
                "uploader": result.uploader.email if admin else None,
                "tags": [tag.name for tag in result.tags],
                "flavor": result.flavor.name
            }
            # decode and add to structure to avoid dealing with storing json within json
            results_dict["results"].append(result_dict)

        return json.dumps(results_dict), 200


class BenchmarkSearchAJAX(AJAXHandler):
    """AJAX handler for benchmark searches with keywords."""

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch benchmarks corresponding to given query.

        Args:
            query (JSON): The metadata containing the keywords to filter by.
        Returns:
            JSON: JSON data containing data about all benchmarks whose docker name matches the keywords.
        """
        keywords = json.loads(query)['keywords'] if query is not None else []
        benchmarks = facade.query_benchmarks(keywords)

        results = []
        for benchmark in benchmarks:
            description = benchmark.description
            if benchmark.hidden and not controller.is_admin():
                continue
            result_dict = {
                "hidden": benchmark.hidden,
                "docker_name": benchmark.docker_name,
                "uploader": benchmark.uploader.email if controller.is_admin() else "",
                "description": description if description is not None else "No description found."
            }
            results.append(result_dict)

        return json.dumps({"results": results}), 200


class ReportFetchAJAXHandler(AJAXHandler):
    """AJAX handler for fetching reports."""

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch all benchmarks independent of given query."""
        return self.fetch_reports(), 200

    @staticmethod
    def fetch_reports() -> JSON:
        """Fetch all reports.

        Returns:
            JSON: JSON data containing details about all known reports.
        """

        report_data = []

        for report in facade.get_reports(only_unanswered=False):
            report_data.append({
                'uuid': report.uuid,
                'type': report.get_field_name(),
                'submitter': report.reporter.name,
                'message': report.message,
                'verdict': report.status
            })

        return json.dumps({'reports': report_data})


class SiteFetchAJAXHandler(AJAXHandler):
    """AJAX handler for fetching sites."""

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch all sites independent of given query."""
        return self.fetch_sites()

    @staticmethod
    def fetch_sites() -> Tuple[JSON, Optional[int]]:
        """Fetch all sites.

        Returns:
            JSON: JSON data containing details about every site.
        """
        results_dict = {"results": []}
        sites = facade.get_sites()
        for site in sites:
            result_dict = {}
            # do not display hidden sites
            if site.hidden:
                continue
            result_dict["name"] = site.name
            result_dict["identifier"] = site.identifier
            result_dict["description"] = site.description
            result_dict["address"] = site.address
            result_dict["flavors"] = [{'name': flavor.name, 'description': flavor.description,
                                       'uuid': flavor.uuid} for flavor in site.flavors]
            results_dict["results"].append(result_dict)
        return json.dumps(results_dict), 200


class TagFetchAJAXHandler(AJAXHandler):
    """AJAX handler for fetching tags."""

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch all tags independent of given query.

        Returns:
            JSON: JSON data containing all known tags.
        """
        return self.fetch_tags()

    @staticmethod
    def fetch_tags() -> Tuple[JSON, Optional[int]]:
        """Fetch all tags.

        Returns:
            JSON: JSON data containing all known tags.
        """
        results_dict = {"results": []}
        tags = facade.get_tags()
        for tag in tags:
            result_dict = {
                "name": tag.name,
                "description": tag.description
            }
            results_dict["results"].append(result_dict)
        return json.dumps(results_dict), 200


class BenchmarkNotableKeysFetchAJAXHandler(AJAXHandler):
    """AJAX handler for queries about notable benchmark keys."""

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        if query is None or query == '{}':
            return '{}', 200
        return json.dumps(
            {'notable_keys': facade.get_benchmark(json.loads(query)['docker_name']).determine_notable_keys()}), 200


class FlavorUpdateAJAX(AJAXHandler):
    """AJAX handler to update site flavor metadata.
    """

    def process(self, query: Optional[dict] = None) -> Tuple[JSON, Optional[int]]:
        if not controller.is_admin():
            return '{"error": "You are not permitted to view this page."}', 403
        if query is None:
            return '{"error": "Empty query."}', 400
        try:
            data = query
            new_name: str = data["name"]
            new_description = data["description"]
            uuid = data["uuid"]
        except JSONDecodeError:
            return '{"error": "Invalid form"}', 400

        if uuid == "new_flavor":
            try:
                site_name = data["site"]
            except JSONDecodeError:
                return '{"error": "Invalid form"}', 400
            new_uuid = controller.submit_flavor(name=new_name, description=new_description, site_identifier=site_name)
            if new_uuid is None:
                return '{"error": "An error occurred while adding the flavor."}', 400
            return '{"uuid": "' + new_uuid + '"}', 200

        if not controller.update_flavor(uuid=uuid, name=new_name, description=new_description):
            return '{"error": "An error occurred while updating the flavor."}', 400

        return "{}", 200


ajax_blueprint = Blueprint('ajax', __name__)


@ajax_blueprint.route('/ajax/query/results')
def query_results():
    """HTTP endpoint for result AJAX queries.

    JSON Args:
        Refer to facade.query_results()
    """
    query_json = request.args.get('query_json')
    if query_json is None:
        query_json = "{}"
    handler = ResultSearchAJAX()
    response, code = handler.process(query_json)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/ajax/query/benchmarks')
def query_benchmarks():
    """HTTP endpoint for benchmark AJAX queries.

    JSON Args:
        keywords - Array of keywords.
    """
    query = request.args.get('query')
    handler = BenchmarkSearchAJAX()
    response, code = handler.process(query)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/ajax/fetch/sites')
def fetch_sites():
    """HTTP endpoint for site AJAX fetches.
    """
    handler = SiteFetchAJAXHandler()
    response, code = handler.process(None)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/ajax/fetch/tags')
def fetch_tags():
    """HTTP endpoint for tag AJAX fetches."""
    handler = TagFetchAJAXHandler()
    response, code = handler.process()
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/ajax/fetch/benchmarks')
@deprecated(reason="Use /ajax/query/benchmarks")
def fetch_benchmarks():
    """HTTP endpoint for benchmark AJAX fetches.
    """
    handler = BenchmarkSearchAJAX()
    response, code = handler.process()
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/ajax/fetch/reports')
@only_admin_json
def fetch_reports():
    """HTTP endpoint for benchmark AJAX fetches.
    """
    handler = ReportFetchAJAXHandler()
    response, code = handler.process()
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/ajax/fetch/notable_benchmark_keys')
def fetch_notable_benchmark_keys():
    """HTTP endpoint for notable benchmark keys AJAX queries.

    JSON Args:
        docker_name - Benchmark name.
    """
    query_json = request.args.get('query_json')
    handler = BenchmarkNotableKeysFetchAJAXHandler()
    response, code = handler.process(query_json)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/ajax/update/flavor', methods=["POST"])
def update_flavor():
    """HTTP endpoint to update site flavor metadata.

    JSON Args:
        name         - New flavor name
        description  - New flavor description
        uuid         - The flavor's identifier
    """
    handler = FlavorUpdateAJAX()
    response, code = handler.process(request.get_json())
    return Response(response, mimetype="application/json", status=code)
