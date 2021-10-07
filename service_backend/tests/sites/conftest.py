"""Defines fixtures available to sites tests."""
from backend import models
from flask import url_for
from pytest import fixture


@fixture(scope='function')
def site_id(request):
    """Site id of the site to test."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def site(site_id):
    """Returns the site to test."""
    return models.Site.query.get(site_id)


@fixture(scope='function')
def request_id(request, site_id):
    """Site id to use on the url call."""
    return request.param if hasattr(request, 'param') else site_id


@fixture(scope='function')
def url(endpoint, request_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, id=request_id, **query)
