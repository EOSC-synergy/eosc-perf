# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests.
See: https://pytest-flask.readthedocs.io/en/latest/features.html
"""
import logging

import pytest
from eosc_perf.app import create_app
from eosc_perf.database import db as _db


@pytest.fixture(scope="session")
def app():
    """Create application for the tests."""
    app = create_app(config_object="eosc_perf.settings.TestingConfig")
    app.logger.setLevel(logging.CRITICAL)
    return app


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    _db.create_all()
    yield _db
    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()
