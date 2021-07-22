"""Defines fixtures available to all tests.
See: https://pytest-flask.readthedocs.io/en/latest/features.html
"""
import logging
import os

from backend import create_app, database
from backend.extensions import auth
from flaat import tokentools
from pytest import fixture
from pytest_factoryboy import register
from pytest_postgresql.janitor import DatabaseJanitor

from factories import factories
from factories import associations as f_associations

TEST_DB = 'test_database'
VERSION = 12.2  # postgresql version number

# Factories registration
register(factories.DBReport)
register(factories.DBTag)
register(factories.DBUser)

register(factories.DBBenchmark)
register(factories.DBResult)
register(factories.DBSite)
register(factories.DBFlavor)

register(f_associations.DBBenchmarkReport)
register(f_associations.DBResultReport)
register(f_associations.DBSiteReport)
register(f_associations.DBFlavorReport)


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
    os.environ['DB_ENGINE'] = 'postgresql'
    os.environ['DB_USER'] = str(sql_database.user)
    os.environ['DB_PASSWORD'] = ""
    os.environ['DB_HOST'] = str(sql_database.host)
    os.environ['DB_PORT'] = str(sql_database.port)
    os.environ['DB_NAME'] = str(sql_database.dbname)
    # OIDC environments
    os.environ['OIDC_CLIENT_ID'] = "eosc-perf"
    os.environ['OIDC_CLIENT_SECRET'] = "not-so-secret-for-testing"
    os.environ['ADMIN_ENTITLEMENTS'] = "admins"


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
    database.db.create_all()
    yield database.db
    database.db.drop_all()


@fixture(scope='function', autouse=True)
def session(db):
    """Creates a new database session for a test."""
    db.session.begin(nested=True)  # Rollback app commits
    yield db.session
    db.session.rollback()   # Discard test changes
    db.session.remove()     # Next test gets a new session


@fixture(scope='function')
def token_sub(request):
    """Returns the sub to include on the user token."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def token_iss(request):
    """Returns the iss to include on the user token."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def mock_token_info(monkeypatch, token_sub, token_iss):
    """Patch fixture to test function with valid oidc token."""
    monkeypatch.setattr(
        tokentools,
        "get_accesstoken_info",
        lambda _: {'body': {'sub': token_sub, 'iss': token_iss}}
    )


@fixture(scope='function')
def introspection_email(request):
    """Returns the email to be returned by the introspection endpoint."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def mock_introspection_info(monkeypatch, introspection_email):
    """Patch fixture to test function with valid oidc token."""
    monkeypatch.setattr(
        auth,
        "get_info_from_introspection_endpoints",
        lambda _: {'email': introspection_email}
    )


@fixture(scope='function')
def grant_logged(monkeypatch, mock_token_info, mock_introspection_info):
    """Patch fixture to test function as logged user."""
    monkeypatch.setattr(
        auth,
        "get_info_from_userinfo_endpoints",
        lambda _: {}
    )
    monkeypatch.setattr(
        tokentools,
        "get_timeleft",
        lambda _: 1000
    )
    monkeypatch.setattr(
        tokentools,
        "get_access_token_from_request",
        lambda _: "mocktoken"
    )


@fixture(scope='function')
def grant_admin(monkeypatch, grant_logged):
    """Patch fixture to test function as admin user."""
    # monkeypatch.setattr(auth, "valid_admin", lambda: True)
    monkeypatch.setattr(
        auth,
        "get_info_from_userinfo_endpoints",
        lambda _: {'eduperson_assurance': ["admins"]}
    )


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


@fixture(scope='function')
def db_benchmarks(request, db_benchmark):
    return [db_benchmark(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_results(request, db_result):
    return [db_result(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_sites(request, db_site):
    return [db_site(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_flavors(request, db_flavor):
    return [db_flavor(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_tags(request, db_tag):
    return [db_tag(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_users(request, db_user):
    return [db_user(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def report(
    db_benchmark, db_result, db_site, db_flavor,
    report__id, report_type, report_verdict,
):
    """Creates a report."""
    kwargs = {
        'report_association__reports': [report__id],
        'report_association__reports__verdict': report_verdict
    }
    if report_type is None:
        raise Exception("report_type undefined")
    elif report_type == "benchmark":
        return db_benchmark(**kwargs).reports[0]
    elif report_type == "result":
        return db_result(**kwargs).reports[0]
    elif report_type == "site":
        return db_site(**kwargs).reports[0]
    elif report_type == "flavor":
        return db_flavor(**kwargs).reports[0]
    else:
        raise Exception(f"Unknown report_type: {report_type}")
