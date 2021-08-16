"""Defines fixtures available to users tests."""
from backend import models
from flask import url_for
from pytest import fixture


@fixture(scope='function')
def user(token_sub, token_iss):
    """Fixture that returns the tested user."""
    return models.User.query.get((token_sub, token_iss))


@fixture(scope='function')
def url(endpoint, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, **query)
