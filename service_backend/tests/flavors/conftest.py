# -*- coding: utf-8 -*-
"""Defines fixtures available to flavors tests."""
from pytest import fixture
from pytest_factoryboy import register
from tests.factories import FlavorFactory

register(FlavorFactory)

@fixture
def flavors(request, flavor_factory):
    return [flavor_factory(name=name) for name in request.param]
