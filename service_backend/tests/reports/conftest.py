"""Defines fixtures available to reports tests."""
from backend import models
from flask import url_for
from pytest import fixture


@fixture(scope='function')
def resource_type_id(request):
    """Type and Id of the resource which report to test."""
    return request.param if hasattr(request, 'param') else ("", None)


@fixture(scope='function')
def resource_model(resource_type_id):
    """Model of resource which report to test."""
    (resource_type, _) = resource_type_id
    if resource_type.lower() == "benchmark":
        return models.Benchmark
    elif resource_type.lower() == "result":
        return models.Result
    elif resource_type.lower() == "site":
        return models.Site
    elif resource_type.lower() == "flavor":
        return models.Flavor
    else:
        return None


@fixture(scope='function')
def resource_id(resource_type_id):
    """Id of resource which report to test."""
    (_, resource_id) = resource_type_id
    return resource_id


@fixture(scope='function')
def resource(resource_model, resource_id):
    """Returns the resource which reports to test."""
    if resource_model:
        return resource_model.query.get(resource_id)


@fixture(scope='function')
def report(resource):
    """Returns a first resource report (creation report)."""
    return resource.reports[0] if resource else None


@fixture(scope='function')
def report_id(report):
    """Returns a first resource report id (creation report)."""
    return report.id if report else None


@fixture(scope='function')
def report_verdict(request, report):
    """Sets the value for report verdict."""
    report.update({'verdict': request.param}, force=True)


@fixture(scope='function')
def request_id(request, report_id):
    """Report id to use on the url call."""
    return request.param if hasattr(request, 'param') else report_id


@fixture(scope='function')
def url(endpoint, request_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, report_id=request_id, **query)
