"""Defines fixtures available to reports tests."""
from flask import url_for
from pytest import fixture


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
def url(endpoint, report_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, report_id=report_id, **query)
