"""Defines fixtures available to results tests."""
from flask import url_for
from pytest import fixture
from tests import factories
from pytest_factoryboy import register

register(factories.BenchmarkFactory)
register(factories.ResultFactory)
register(factories.SiteFactory)
register(factories.FlavorFactory)
register(factories.TagFactory)
register(factories.UserFactory)


@fixture(scope='function')
def result_id(request):
    """Override result id as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def result__id(result_id):
    """Use, if defined, the id for the result factory."""
    return result_id


@fixture(scope='function')
def url(endpoint, result_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, result_id=result_id, **query)


@fixture(scope='function')
def db_benchmarks(request, benchmark_factory):
    return [benchmark_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_results(request, result_factory):
    return [result_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_sites(request, site_factory):
    return [site_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_flavors(request, flavor_factory):
    return [flavor_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_tags(request, tag_factory):
    return [tag_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_users(request, user_factory):
    return [user_factory(**kwargs) for kwargs in request.param]
