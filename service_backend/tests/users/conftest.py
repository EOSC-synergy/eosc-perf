"""Defines fixtures available to users tests."""
from uuid import uuid4

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
