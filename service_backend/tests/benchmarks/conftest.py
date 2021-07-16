"""Defines fixtures available to benchmarks tests."""
from flask import url_for
from pytest import fixture
from pytest_factoryboy import register
from tests import factories

register(factories.UserFactory)
register(factories.BenchmarkReportAssociationFactory)
register(factories.BenchmarkFactory)


@fixture(scope='function')
def benchmark_id(request):
    """Override benchmark id as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def benchmark__id(benchmark_id):
    """Use, if defined, the id for the benchmark factory."""
    return benchmark_id if benchmark_id else None


@fixture(scope='function')
def url(endpoint, benchmark_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, benchmark_id=benchmark_id, **query)


@fixture(scope='function')
def db_benchmarks(request, benchmark_factory):
    return [benchmark_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_users(request, user_factory):
    return [user_factory(**kwargs) for kwargs in request.param]
