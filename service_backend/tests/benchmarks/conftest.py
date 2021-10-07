"""Defines fixtures available to benchmarks tests."""
from backend import models
from flask import url_for
from pytest import fixture


@fixture(scope='function')
def benchmark_id(request):
    """Benchmark id of the benchmark to test."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def benchmark(benchmark_id):
    """Returns the benchmark to test."""
    return models.Benchmark.query.get(benchmark_id)


@fixture(scope='function')
def request_id(request, benchmark_id):
    """Benchmark id to use on the url call."""
    return request.param if hasattr(request, 'param') else benchmark_id


@fixture(scope='function')
def url(endpoint, request_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, id=request_id, **query)
