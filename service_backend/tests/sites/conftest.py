# -*- coding: utf-8 -*-
"""Defines fixtures available to sites tests."""
from pytest import fixture
from pytest_factoryboy import register
from tests.factories import FlavorFactory, SiteFactory

register(FlavorFactory)
register(SiteFactory)


@fixture
def flavors(request, flavor_factory):
    names = request.param if hasattr(request, 'param') else ["f1", "f2"]
    return [flavor_factory(name=x) for x in names]

@fixture
def sites(request, site_factory):
    return [site_factory(name=name) for name in request.param]
