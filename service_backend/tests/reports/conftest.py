"""Defines fixtures available to reports tests."""
from flask import url_for
from pytest import fixture
from pytest_factoryboy import register
from tests import factories


register(factories.ReportFactory)
register(factories.BenchmarkReportAssociationFactory)
register(factories.ResultReportAssociationFactory)
register(factories.SiteReportAssociationFactory)
register(factories.FlavorReportAssociationFactory)

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
def report_type(request):
    """Selects the type of resource the report points to."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def report_verdict(request):
    """Selects the initialization value for report.verdict."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def report__id(request, report_id):
    """Use the id for the report factory if defined."""
    return request.param if hasattr(request, 'param') else report_id


@fixture(scope='function')
def report(
    benchmark_factory, result_factory, site_factory, flavor_factory,
    report__id, report_type, report_verdict,
):
    """Creates a report."""
    kwargs = {
        'report_association__reports': [report__id],
        'report_association__reports__verdict': report_verdict
    }
    if report_type == None:
        raise Exception("report_type undefined")
    elif report_type == "benchmark":
        return benchmark_factory(**kwargs).reports[0]
    elif report_type == "result":
        return result_factory(**kwargs).reports[0]
    elif report_type == "site":
        return site_factory(**kwargs).reports[0]
    elif report_type == "flavor":
        return flavor_factory(**kwargs).reports[0]
    else:
        raise Exception(f"Unknown report_type: {report_type}")


@fixture(scope='function')
def url(endpoint, report_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, report_id=report_id, **query)


@fixture(scope='function')
def db_results(request, result_factory):
    return [result_factory(**kwargs) for kwargs in request.param]
