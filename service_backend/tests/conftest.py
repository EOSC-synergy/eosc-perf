# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import logging

import pytest
from webtest import TestApp

from eosc_perf.app import create_app
from eosc_perf.database import db as _db

from .factories import UserFactory


@pytest.fixture(scope="session")
def app():
    """Create application for the tests."""
    app = create_app("tests.settings")
    app.logger.setLevel(logging.CRITICAL)
    return app


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    _db.create_all()
    yield _db
    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """Create user for the tests."""
    user = UserFactory()
    db.session.commit()
    return user
