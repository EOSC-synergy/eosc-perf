# -*- coding: utf-8 -*-
"""Defines fixtures available to sites tests."""
from pytest import fixture
from tests.factories import FlavorFactory, SiteFactory


@fixture
def id(request):
    return request.param if hasattr(request, 'param') else None

@fixture
def name(request):
    return request.param if hasattr(request, 'param') else None

@fixture
def address(request):
    return request.param if hasattr(request, 'param') else None

@fixture
def flavors(request, db):
    if hasattr(request, 'param'):
        return [FlavorFactory(name=name) for name in request.param]
    else:
        return [FlavorFactory(name=name) for name in ["f1", "f2", "f3"]]

@fixture
def flavor_ids(flavors):
    return [flavor.id for flavor in flavors]

@fixture
def site(db, flavors):
    return SiteFactory(flavors=flavors)


@fixture
def query(request, site, id):
    if hasattr(request, 'param'):
        return {x: getattr(site, x, '') for x in request.param}
    else:
        return {'id': id if id else site.id}

@fixture
def body(request, name, address, flavor_ids):
    if hasattr(request, 'param'):
        return request.param
    else:
        body = {}
        if name:
            body['name'] = name
        if address:
            body['address'] = address
        if flavor_ids != []:
            body['flavors'] = flavor_ids
        return body
