"""Defines fixtures available to reports tests."""
from flask import url_for
from pytest import fixture
from pytest_factoryboy import register
from tests import factories


register(factories.BenchmarkReportFactory)
register(factories.ResultReportFactory)
register(factories.SiteReportFactory)
register(factories.FlavorReportFactory)

register(factories.BenchmarkFactory)
register(factories.ResultFactory)
register(factories.SiteFactory)
register(factories.FlavorFactory)
register(factories.UserFactory)


@fixture(scope='function')
def report_id(request):
    """Override report id as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def benchmark_report__id(report_id):
    """Use, if defined, the id for the report factory."""
    return report_id


@fixture(scope='function')
def result_report__id(report_id):
    """Use, if defined, the id for the report factory."""
    return report_id


@fixture(scope='function')
def site_report__id(report_id):
    """Use, if defined, the id for the report factory."""
    return report_id


@fixture(scope='function')
def flavor_report__id(report_id):
    """Use, if defined, the id for the report factory."""
    return report_id


@fixture(scope='function')
def url(endpoint, report_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, report_id=report_id, **query)


@fixture(scope='function')
def db_benchmark_reports(request, benchmark_report_factory):
    return [benchmark_report_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_result_reports(request, result_report_factory):
    return [result_report_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_site_reports(request, site_report_factory):
    return [site_report_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_flavor_reports(request, flavor_report_factory):
    flavors = [flavor_report_factory(**kwargs) for kwargs in request.param]
    return flavors
