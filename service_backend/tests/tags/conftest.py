"""Defines fixtures available to tags tests."""
from backend import models
from flask import url_for
from pytest import fixture


@fixture(scope='function')
def tag_id(request):
    """Tag id of the tag to test."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def tag(tag_id):
    """Returns the tag to test."""
    return models.Tag.query.get(tag_id)


@fixture(scope='function')
def request_id(request, tag_id):
    """Tag id to use on the url call."""
    return request.param if hasattr(request, 'param') else tag_id


@fixture(scope='function')
def url(endpoint, request_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, id=request_id, **query)
