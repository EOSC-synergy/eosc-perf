"""This module contains the classes responsible for AJAX queries."""

import json
from abc import ABC, abstractmethod
from json import JSONDecodeError
from typing import List, Optional, Tuple

from flask import request, Response
from flask.blueprints import Blueprint

from ..controller.io_controller import controller
from eosc_perf.utility.type_aliases import JSON
from ..model.data_types import Benchmark
from ..model.facade import facade


class AJAXHandler(ABC):
    """Abstract class to represent any AJAX request endpoint."""

    @abstractmethod
    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch data corresponding to given query."""


class SearchAJAXHandler(AJAXHandler):
    """Abstract class to represent a search AJAX request endpoint."""

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch data corresponding to given query.

        Args:
            query (JSON): The metadata containing the query to fulfill.
        Returns:
            JSON: A JSON response carrying the requested data.
        """
        return self.find_results(query)

    # TODO: why is this separate?
    @abstractmethod
    def find_results(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch search results corresponding to given query.

        Args:
            query (JSON): The metadata containing the query to fulfill.
        Returns:
            JSON: A JSON response carrying the requested data.
        """


class ResultSearchAJAX(SearchAJAXHandler):
    """AJAX handler for benchmark result searches with filters."""

    def find_results(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch benchmark results corresponding to given query."""
        results_dict = {"results": []}
        results = facade.query_results(query)
        for result in results:
            result_dict = {
                "data": json.loads(result.get_json()), "uuid": result.get_uuid(),
                "site": result.get_site().get_short_name(),
                "benchmark": result.get_benchmark().get_docker_name(),
                "uploader": result.get_uploader().get_email(),
                "tags": [tag.get_name() for tag in result.get_tags()],
                "flavor": result.get_flavor().get_name()
            }
            # decode and add to structure to avoid dealing with storing json within json
            results_dict["results"].append(result_dict)

        return json.dumps(results_dict), 200


def _pack_benchmarks(benchmarks: List[Benchmark]) -> JSON:
    """Generate JSON data containing info about all supplied benchmarks.

    Args:
        benchmarks (List[Benchmark]): All benchmarks to fill into the response.
    Returns:
        JSON: JSON data containing query results to display.
    """
    results_dict = {"results": []}
    for benchmark in benchmarks:
        result_dict = {}
        # do not display hidden benchmarks (= new ones)
        if benchmark.get_hidden():
            continue
        # decode and add to structure to avoid dealing with storing json within json
        result_dict["docker_name"] = benchmark.get_docker_name()
        result_dict["uploader"] = benchmark.get_uploader().get_email()
        description = benchmark.get_description()
        result_dict["description"] = description if description is not None else "No description found."
        results_dict["results"].append(result_dict)

    return json.dumps(results_dict)


class BenchmarkSearchAJAX(SearchAJAXHandler):
    """AJAX handler for benchmark searches with keywords."""

    def find_results(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch benchmarks corresponding to given query.

        Args:
            query (JSON): The metadata containing the keywords to filter by.
        Returns:
            JSON: JSON data containing data about all benchmarks whose docker name matches the keywords.
        """

        keywords = json.loads(query)['keywords'] if query is not None else []
        benchmarks = facade.query_benchmarks(keywords)
        return _pack_benchmarks(benchmarks), 200


class BenchmarkFetchAJAXHandler(AJAXHandler):
    """AJAX handler for fetching benchmarks."""

    def process(self, query: Optional[JSON] = None) -> Tuple[JSON, Optional[int]]:
        """Fetch all benchmarks independent of given query."""
        return self.fetch_benchmarks(), 200

    @staticmethod
    def fetch_benchmarks() -> JSON:
        """Fetch all benchmarks.

        Returns:
            JSON: JSON data containing details about all known benchmarks.
        """

        benchmarks = facade.get_benchmarks()
        return _pack_benchmarks(benchmarks)


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
            if site.get_hidden():
                continue
            result_dict["name"] = site.get_name()
            result_dict["short_name"] = site.get_short_name()
            result_dict["description"] = site.get_description()
            result_dict["address"] = site.get_address()
            result_dict["flavors"] = [{'name': flavor.get_name(), 'description': flavor.get_description(),
                                       'uuid': flavor.get_uuid()} for flavor in site.get_flavors()]
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
                "name": tag.get_name(),
                "description": tag.get_description()
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
            new_uuid = controller.submit_flavor(name=new_name, description=new_description, site_name=site_name)
            if new_uuid is None:
                return '{"error": "An error occurred while adding the flavor."}', 400
            return '{"uuid": "' + new_uuid + '"}', 200

        if not controller.update_flavor(uuid=uuid, name=new_name, description=new_description):
            return '{"error": "An error occurred while updating the flavor."}', 400

        return "{}", 200


ajax_blueprint = Blueprint('ajax', __name__)


@ajax_blueprint.route('/query_results')
def query_results():
    """HTTP endpoint for result AJAX queries."""
    query_json = request.args.get('query_json')
    if query_json is None:
        query_json = "{}"
    handler = ResultSearchAJAX()
    response, code = handler.process(query_json)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/query_benchmarks')
def query_benchmarks():
    """HTTP endpoint for benchmark AJAX queries."""
    query_json = request.args.get('query_json')
    handler = BenchmarkSearchAJAX()
    response, code = handler.process(query_json)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/fetch_sites')
def fetch_sites():
    """HTTP endpoint for site AJAX fetches."""
    handler = SiteFetchAJAXHandler()
    response, code = handler.process(None)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/fetch_tags')
def fetch_tags():
    """HTTP endpoint for tag AJAX fetches."""
    handler = TagFetchAJAXHandler()
    response, code = handler.process()
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/fetch_benchmarks')
def fetch_benchmarks():
    """HTTP endpoint for benchmark AJAX fetches."""
    handler = BenchmarkFetchAJAXHandler()
    response, code = handler.process()
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/fetch_notable_benchmark_keys')
def fetch_notable_benchmark_keys():
    """HTTP endpoint for notable benchmark keys AJAX queries."""
    query_json = request.args.get('query_json')
    handler = BenchmarkNotableKeysFetchAJAXHandler()
    response, code = handler.process(query_json)
    return Response(response, mimetype='application/json', status=code)


@ajax_blueprint.route('/update/flavor', methods=["POST"])
def update_flavor():
    handler = FlavorUpdateAJAX()
    response, code = handler.process(request.get_json())
    return Response(response, mimetype="application/json", status=code)

