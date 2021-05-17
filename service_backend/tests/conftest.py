# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests.
See: https://pytest-flask.readthedocs.io/en/latest/features.html
"""
import logging

from backend import authorization, create_app, database
from pytest import fixture
from pytest_postgresql.factories import DatabaseJanitor
from sqlalchemy import orm

TEST_DB = 'test_database'
VERSION = 12.2  # postgresql version number
Session = orm.scoped_session(orm.sessionmaker())


@fixture(scope='session')
def connection(postgresql_proc):
    """Create a temp Postgres database for the tests."""
    USER = postgresql_proc.user
    HOST = postgresql_proc.host
    PORT = postgresql_proc.port
    with DatabaseJanitor(USER, HOST, PORT, TEST_DB, VERSION):
        yield f'postgresql://{USER}:@{HOST}:{PORT}/{TEST_DB}'


@fixture(scope="session")
def app(connection):
    """Create application for the tests."""
    app = create_app(
        config_base="backend.settings",
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=connection)
    app.logger.setLevel(logging.CRITICAL)
    return app


@fixture(scope='session')
def db(app):
    """Create database for the tests."""
    database.db.app = app
    Session.configure(bind=database.db.engine)
    database.db.session = Session
    database.db.create_all()
    yield database.db
    database.db.drop_all()


@fixture(scope='function')
def session(db):
    """Creates a new database session for a test."""
    session = Session()  # Prepare a new, clean session
    session.begin(nested=True)  # Rollback app commits
    yield session
    session.rollback()  # Discard test changes
    Session.remove()  # Next test gets a new Session()


@fixture(scope='function')
def grant_logged(monkeypatch):
    """Patch fixture to test function as logged user."""
    monkeypatch.setenv(
        "DISABLE_AUTHENTICATION_AND_ASSUME_AUTHENTICATED_USER",
        "YES"
    )


@fixture(scope='function')
def grant_admin(monkeypatch, grant_logged):
    """Patch fixture to test function as admin user."""
    monkeypatch.setenv(
        "DISABLE_AUTHENTICATION_AND_ASSUME_VALID_GROUPS",
        "YES"
    )
