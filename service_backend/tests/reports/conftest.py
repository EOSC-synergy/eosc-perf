"""Defines fixtures available to reports tests."""
from flask import url_for
from pytest import fixture
from factories import DBResult
from backend.extensions import db


@fixture(scope='function')
def result():
    """Result id of the result to test."""
    result = DBResult(claims=["Result claim"])
    db.session.commit()
    return result


@fixture(scope='function')
def claim(result):
    """Returns the result to test."""
    return result.claims[0]


@fixture(scope='function')
def request_id(request):
    """Claim id to use on the url call."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def url(endpoint, request_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, id=request_id, **query)
