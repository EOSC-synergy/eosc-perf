# -*- coding: utf-8 -*-
"""Defines fixtures available to flavors tests."""
from flask import url_for
from pytest import fixture
from tests.factories import FlavorFactory


@fixture
def route(request):
    return request.param

@fixture
def body(request):
    return request.param

@fixture
def flavor(db):
    flavor = FlavorFactory()
    db.session.commit()
    return flavor

@fixture
def id(request, flavor):
    return request.param if hasattr(request, 'param') else flavor.id


@fixture
def response_GET(client, route, id):
    return client.get(url_for(f'flavors.{route}', id=id))

@fixture
def response_PUT(client, route, id, body):
    return client.put(url_for(f'flavors.{route}', id=id), json=body)

@fixture
def response_DELETE(client, route, id):
    return client.delete(url_for(f'flavors.{route}', id=id))
