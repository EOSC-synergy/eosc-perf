# -*- coding: utf-8 -*-
"""Defines fixtures available to users tests."""
from flaat import tokentools
from pytest import fixture
from pytest_factoryboy import register
from tests.factories import UserFactory

register(UserFactory)


@fixture
def users(request, user_factory):
    return [user_factory(email=email) for email in request.param]


@fixture
def patch_accesstoken(monkeypatch):
    monkeypatch.setattr(
        tokentools,
        "get_accesstoken_info",
        mock_get_accesstoken_info
    )


def mock_get_accesstoken_info(*args, **kwargs):
    user = UserFactory.build()
    return {
        'body': {
            'iss': user.iss,
            'sub': user.sub
        }
    }
