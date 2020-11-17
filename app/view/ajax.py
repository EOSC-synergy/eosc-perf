"""This module contains the classes responsible for AJAX queries.
Provided are:
 - AjaxHandler (abstract)
 - SearchAjaxHandler (abstract)
 - ResultSearchAJAX
 - BenchmarkSearchAJAX
 """

import json
from abc import ABC, abstractmethod
from typing import List

from flask import request, Response
from flask.blueprints import Blueprint
from .type_aliases import JSON
from ..model.data_types import Benchmark
from ..model.facade import DatabaseFacade, facade


class AJAXHandler(ABC):
    """Abstract class to represent any AJAX request endpoint."""

    @abstractmethod
    def fetch_data(self, query: JSON) -> JSON:
        """Fetch data corresponding to given query."""


class SearchAJAXHandler(AJAXHandler):
    """Abstract class to represent a search AJAX request endpoint."""

    def fetch_data(self, query: JSON) -> JSON:
        """Fetch data corresponding to given query."""
        return self.find_results(query)

    @abstractmethod
    def find_results(self, query: JSON) -> JSON:
        """Fetch search results corresponding to given query."""


class ResultSearchAJAX(SearchAJAXHandler):
    """AJAX handler for benchmark result searches with filters."""

    def __init__(self, facade_: DatabaseFacade):
        """Set up a new ResultSearchAJAX using the DatabaseFacade."""
        self._facade = facade_

    def find_results(self, query: JSON) -> JSON:
        """Fetch benchmark results corresponding to given query."""
        results_dict = {"results": []}
        results = self._facade.query_results(query)
        for result in results:
            result_dict = {
                "data": json.loads(result.get_json()), "uuid": result.get_uuid(),
                "site": result.get_site().get_short_name(),
                "benchmark": result.get_benchmark().get_docker_name(),
                "uploader": result.get_uploader().get_email(),
                "tags": [tag.get_name() for tag in result.get_tags()]
            }
            # decode and add to structure to avoid dealing with storing json within json
            results_dict["results"].append(result_dict)

        return json.dumps(results_dict)


def _pack_benchmarks(benchmarks: List[Benchmark]):
    results_dict = {"results": []}
    for benchmark in benchmarks:
        result_dict = {}
        # do not display hidden benchmarks (= new ones)
        if benchmark.get_hidden():
            continue
        # decode and add to structure to avoid dealing with storing json within json
        result_dict["docker_name"] = benchmark.get_docker_name()
        result_dict["uploader"] = benchmark.get_uploader().get_email()
        results_dict["results"].append(result_dict)

    return json.dumps(results_dict)


class BenchmarkSearchAJAX(SearchAJAXHandler):
    """AJAX handler for benchmark searches with keywords."""

    def __init__(self, facade_: DatabaseFacade):
        """Set up a new BenchmarkAJAXBase using the DatabaseFacade."""
        self._facade = facade_

    def find_results(self, query: JSON) -> JSON:
        """Fetch benchmarks corresponding to given query."""

        keywords = json.loads(query)['keywords']
        benchmarks = self._facade.query_benchmarks(keywords)
        return _pack_benchmarks(benchmarks)


class BenchmarkFetchAJAXHandler(AJAXHandler):
    """AJAX handler for fetching benchmarks."""

    def __init__(self, facade_: DatabaseFacade):
        """Set up a new BenchmarkAJAXBase using the DatabaseFacade."""
        self._facade = facade_

    def fetch_data(self, query: JSON = None) -> JSON:
        """Fetch all benchmarks independent of given query."""
        return self.fetch_benchmarks()

    def fetch_benchmarks(self) -> JSON:
        """Fetch all benchmarks."""

        benchmarks = self._facade.get_benchmarks()
        return _pack_benchmarks(benchmarks)


class SiteFetchAJAXHandler(AJAXHandler):
    """AJAX handler for fetching sites."""

    def __init__(self, facade_: DatabaseFacade):
        """Set up a new SiteFetchAJAXHandler using the DatabaseFacade."""
        self._facade = facade_

    def fetch_data(self, query: JSON = None) -> JSON:
        """Fetch all sites independent of given query."""
        return self.fetch_sites()

    def fetch_sites(self) -> JSON:
        """Fetch all sites."""
        results_dict = {"results": []}
        sites = self._facade.get_sites()
        for site in sites:
            result_dict = {}
            # do not display hidden sites
            if site.get_hidden():
                continue
            result_dict["name"] = site.get_name()
            result_dict["short_name"] = site.get_short_name()
            result_dict["description"] = site.get_description()
            result_dict["address"] = site.get_address()
            results_dict["results"].append(result_dict)
        return json.dumps(results_dict)


class TagFetchAJAXHandler(AJAXHandler):
    """AJAX handler for fetching tags."""

    def __init__(self, facade_: DatabaseFacade):
        """Set up a new TagFetchAJAXHandler using the DatabaseFacade."""
        self._facade = facade_

    def fetch_data(self, query: JSON = None) -> JSON:
        """Fetch all tags independent of given query."""
        return self.fetch_tags()

    def fetch_tags(self) -> JSON:
        """Fetch all tags."""
        results_dict = {"results": []}
        tags = self._facade.get_tags()
        for tag in tags:
            result_dict = {
                "name": tag.get_name(),
                "description": tag.get_description()
            }
            results_dict["results"].append(result_dict)
        return json.dumps(results_dict)


ajax_blueprint = Blueprint('ajax', __name__)


@ajax_blueprint.route('/query_results')
def query_results():
    """HTTP endpoint for result AJAX queries."""
    query_json = request.args.get('query_json')
    if query_json is None:
        query_json = "{}"
    handler = ResultSearchAJAX(facade)
    return Response(handler.fetch_data(query_json), mimetype='application/json')


@ajax_blueprint.route('/query_benchmarks')
def query_benchmarks():
    """HTTP endpoint for benchmark AJAX queries."""
    query_json = request.args.get('query_json')
    if query_json is None:
        query_json = "{}"
    handler = BenchmarkSearchAJAX(facade)
    return Response(handler.fetch_data(query_json), mimetype='application/json')


@ajax_blueprint.route('/fetch_sites')
def fetch_sites():
    """HTTP endpoint for site AJAX fetches."""
    handler = SiteFetchAJAXHandler(facade)
    return Response(handler.fetch_data(), mimetype='application/json')


@ajax_blueprint.route('/fetch_tags')
def fetch_tags():
    """HTTP endpoint for tag AJAX fetches."""
    handler = TagFetchAJAXHandler(facade)
    return Response(handler.fetch_data(), mimetype='application/json')


@ajax_blueprint.route('/fetch_benchmarks')
def fetch_benchmarks():
    """HTTP endpoint for benchmark AJAX fetches."""
    handler = BenchmarkFetchAJAXHandler(facade)
    return Response(handler.fetch_data(), mimetype='application/json')
