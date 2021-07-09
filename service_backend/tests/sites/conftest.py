"""Defines fixtures available to sites tests."""
from flask import url_for
from pytest import fixture
from pytest_factoryboy import register
from tests.factories import FlavorFactory, SiteFactory

register(SiteFactory)
register(FlavorFactory)


@fixture(scope='function')
def site_id(request):
    """Override site id as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def site__id(site_id):
    """Use, if defined, the id for the site factory."""
    return site_id


@fixture(scope='function')
def flavor_id(request):
    """Override flavor id as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def flavor__id(flavor_id):
    """Use, if defined, the id for the flavor factory."""
    return flavor_id


@fixture(scope='function')
def url(endpoint, site_id, flavor_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, site_id=site_id, flavor_id=flavor_id, **query)


@fixture(scope='function')
def db_sites(request, site_factory):
    return [site_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def db_flavors(request, flavor_factory):
    return [flavor_factory(**kwargs) for kwargs in request.param]
