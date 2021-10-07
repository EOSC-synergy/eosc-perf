"""Defines fixtures available to all tests.
See: https://pytest-flask.readthedocs.io/en/latest/features.html
"""
import logging
import os

import factories
from backend import create_app
from backend.extensions import auth as authentication
from backend.extensions import db as database
from backend.utils import dockerhub
from flaat import tokentools
from pytest import fixture
from pytest_postgresql.janitor import DatabaseJanitor

from tests import db_instances

TEST_DB = 'test_database'
VERSION = 12.2  # postgresql version number


@fixture(scope='session')
def sql_database(postgresql_proc):
    """Create a temp Postgres database for the tests."""
    USER = postgresql_proc.user
    HOST = postgresql_proc.host
    PORT = postgresql_proc.port
    with DatabaseJanitor(USER, HOST, PORT, TEST_DB, VERSION) as db:
        yield db


@fixture(scope='session')
def session_environment(sql_database):
    """Patch fixture to set test env variables."""
    # Flask framework environments
    os.environ['SECRET_KEY'] = 'not-so-secret-for-testing'
    # Database environments
    os.environ['DB_USER'] = str(sql_database.user)
    os.environ['DB_PASSWORD'] = ""
    os.environ['DB_HOST'] = str(sql_database.host)
    os.environ['DB_PORT'] = str(sql_database.port)
    os.environ['DB_NAME'] = str(sql_database.dbname)
    # OIDC environments
    os.environ['OIDC_CLIENT_ID'] = "eosc-perf"
    os.environ['OIDC_CLIENT_SECRET'] = "not-so-secret-for-testing"
    os.environ['ADMIN_ENTITLEMENTS'] = "admins"
    # Email and notification configuration.
    os.environ['MAIL_SUPPORT'] = "support@example.com"
    os.environ['MAIL_SERVER'] = "localhost"
    os.environ['MAIL_PORT'] = str(5025)
    os.environ['MAIL_FROM'] = "no-reply@example.com"


@fixture(scope="session")
def app(session_environment):
    """Create application for the tests."""
    app = create_app(config_base="backend.settings", TESTING=True)
    app.logger.setLevel(logging.CRITICAL)
    with app.app_context():
        yield app


@fixture(scope='session')
def db(app):
    """Create database for the tests."""
    database.create_all()
    [factories.DBUser(**x) for x in db_instances.users]
    [factories.DBTag(**x) for x in db_instances.tags]
    [factories.DBBenchmark(**x) for x in db_instances.benchmarks]
    [factories.DBSite(**x) for x in db_instances.sites]
    [factories.DBFlavor(**x) for x in db_instances.flavors]
    [factories.DBResult(**x) for x in db_instances.results]
    database.session.commit()
    yield database
    database.drop_all()


@fixture(scope='function', autouse=True)
def session(db):
    """Uploads a new database session for a test."""
    db.session.begin(nested=True)  # Rollback app commits
    yield db.session
    db.session.rollback()   # Discard test changes
    db.session.close()      # Next test gets a new session


@fixture(scope='function')
def token_sub(request):
    """Returns the sub to include on the user token."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def token_iss(request):
    """Returns the iss to include on the user token."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def mock_accesstoken(monkeypatch, token_sub, token_iss):
    """Patch fixture to test function with valid oidc token."""
    monkeypatch.setattr(
        tokentools,
        "get_accesstoken_info",
        lambda _: {
            'body': {'sub': token_sub, 'iss': token_iss},
            'exp': 99999999999
        }
    )
    monkeypatch.setattr(
        tokentools,
        "get_access_token_from_request",
        lambda _: "mocktoken"
    )


@fixture(scope='function')
def mock_endpoints(monkeypatch):
    """Patch fixture to edit information from tokenuser endpoints."""
    monkeypatch.setattr(
        authentication,
        "get_info_from_userinfo_endpoints",
        lambda _: {}
    )


@fixture(scope='function')
def introspection_email(request):
    """Returns the email to be returned by the introspection endpoint."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def mock_introspection(monkeypatch, introspection_email):
    """Patch function to provide custom introspection information."""
    monkeypatch.setattr(
        authentication,
        "get_info_from_introspection_endpoints",
        lambda _: {'email': introspection_email}
    )


@fixture(scope='function')
def grant_accesstoken(mock_accesstoken, mock_endpoints, mock_introspection):
    """Patch fixture to test function with valid oidc token."""
    pass


@fixture(scope='function')
def grant_logged(monkeypatch, grant_accesstoken):
    """Patch fixture to test function as logged user."""
    monkeypatch.setattr(authentication, "valid_user", lambda: True)


@fixture(scope='function')
def grant_admin(monkeypatch, grant_logged):
    """Patch fixture to test function as admin user."""
    monkeypatch.setattr(authentication, "valid_admin", lambda: True)


@fixture(scope='function')
def mock_docker_registry(monkeypatch):
    """Patch fixture to test function with valid oidc token."""
    def always_true(*arg, **kwarg): return True
    monkeypatch.setattr(dockerhub, "valid_image", always_true)


@fixture(scope='function')
def endpoint(request):
    """Fixture that return the endpoint for the request."""
    return request.param


@fixture(scope='function')
def query(request):
    """Fixture that return the query for the request."""
    return request.param if hasattr(request, 'param') else {}


@fixture(scope='function')
def body(request):
    """Fixture that return the body for the request."""
    return request.param if hasattr(request, 'param') else {}


@fixture(scope='function')
def response_GET(client, url):
    """Fixture that return the result of a GET request."""
    return client.get(url)


@fixture(scope='function')
def response_POST(client, url, body):
    """Fixture that return the result of a POST request."""
    return client.post(url, json=body)


@fixture(scope='function')
def response_PUT(client, url, body):
    """Fixture that return the result of a PUT request."""
    return client.put(url, json=body)


@fixture(scope='function')
def response_PATCH(client, url, body):
    """Fixture that return the result of a PATCH request."""
    return client.patch(url, json=body)


@fixture(scope='function')
def response_DELETE(client, url):
    """Fixture that return the result of a DELETE request."""
    return client.delete(url)
