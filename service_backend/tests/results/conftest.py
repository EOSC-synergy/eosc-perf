"""Defines fixtures available to results tests."""
from flask import url_for
from pytest import fixture


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
