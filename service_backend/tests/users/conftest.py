"""Defines fixtures available to users tests."""
from uuid import uuid4

from backend.extensions import flaat
from flaat import tokentools
from flask import url_for
from pytest import fixture, mark
from pytest_factoryboy import register
from tests.factories import UserFactory

register(UserFactory)


@fixture(scope='function')
def user_iss(request):
    """Override user iss as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def user__iss(user_iss):
    """Use, if defined, the iss for the user factory."""
    return user_iss if user_iss else None


@fixture(scope='function')
def user_sub(request):
    """Override user sub as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def user__sub(user_sub):
    """Use, if defined, the sub for the user factory."""
    return user_sub if user_sub else None


@fixture(scope='function')
def url(endpoint, user_iss, user_sub, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, user_iss=user_iss, user_sub=user_sub, **query)


@fixture(scope='function')
def db_users(request, user_factory):
    return [user_factory(**kwargs) for kwargs in request.param]


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
        flaat,
        "get_info_from_introspection_endpoints",
        lambda _: {'email': introspection_email}
    )
