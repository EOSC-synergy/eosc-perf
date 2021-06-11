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
def flavor_name(request):
    """Override flavor name as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def flavor__name(flavor_name):
    """Use, if defined, the name for the flavor factory."""
    return flavor_name


@fixture(scope='function')
def url(endpoint, site_id, flavor_name, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, site_id=site_id, flavor_name=flavor_name, **query)


@fixture(scope='function')
def db_sites(request, site_factory):
    return [site_factory(**kwargs) for kwargs in request.param]


@fixture(scope='function')
def flavor(flavor_factory, flavor__name, site):
    flavor = flavor_factory(site_id=site.id, name=flavor__name)
    return flavor


@fixture(scope='function')
def db_flavors(request, flavor_factory, site):
    flavors = [flavor_factory(site_id=site.id, **kwargs)
               for kwargs in request.param]
    return flavors
