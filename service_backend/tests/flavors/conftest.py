# -*- coding: utf-8 -*-
"""Defines fixtures available to flavors tests."""
from pytest import fixture
from tests.factories import FlavorFactory


@fixture
def id(request):
    return request.param if hasattr(request, 'param') else None

@fixture
def name(request):
    return request.param if hasattr(request, 'param') else None

@fixture
def custom_text(request):
    return request.param if hasattr(request, 'param') else None

@fixture
def query(request, flavor, id):
    if hasattr(request, 'param'):
        return {x: getattr(flavor, x, '') for x in request.param}
    else:
        return {'id': id if id else flavor.id}

@fixture
def body(request, name, custom_text):
    if hasattr(request, 'param'):
        return request.param
    else:
        body = {}
        if name:
            body['name'] = name
        if custom_text:
            body['custom_text'] = custom_text
        return body

@fixture
def flavor(db):
    flavor = FlavorFactory()
    db.session.commit()
    return flavor
