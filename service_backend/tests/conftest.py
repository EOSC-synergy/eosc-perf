# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests.
See: https://pytest-flask.readthedocs.io/en/latest/features.html
"""
import logging

from eosc_perf.app import create_app
from eosc_perf.database import db as _db
from flask import url_for
from pytest import fixture


@fixture(scope="session")
def app():
    """Create application for the tests."""
    app = create_app(config_object="eosc_perf.settings.TestingConfig")
    app.logger.setLevel(logging.CRITICAL)
    return app


@fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    _db.create_all()
    yield _db
    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


# General parametrization for indirect marks
@fixture
def query(request):
    raise NotImplementedError

@fixture
def path(request, query):
    return url_for(request.param, **query)

@fixture
def body(request):
    return request.param if hasattr(request, 'param') else None


# Method response fixtures
@fixture
def response_GET(client, path, body):
    return client.get(path=path, json=body)

@fixture
def response_POST(client, path, body):
    return client.post(path=path, json=body)

@fixture
def response_PUT(client, path, body):
    return client.put(path=path, json=body)

@fixture
def response_DELETE(client, path, body):
    return client.delete(path=path, json=body)
