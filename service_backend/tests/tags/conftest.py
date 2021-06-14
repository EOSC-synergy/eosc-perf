"""Defines fixtures available to tags tests."""
from flask import url_for
from pytest import fixture
from pytest_factoryboy import register
from tests.factories import TagFactory

register(TagFactory)


@fixture(scope='function')
def tag_id(request):
    """Override tag id as a separate fixture."""
    return request.param if hasattr(request, 'param') else None


@fixture(scope='function')
def tag__id(tag_id):
    """Use, if defined, the id for the tag factory."""
    return tag_id if tag_id else None


@fixture(scope='function')
def url(endpoint, tag_id, query):
    """Fixture that return the url for the request."""
    return url_for(endpoint, tag_id=tag_id, **query)


@fixture(scope='function')
def db_tags(request, tag_factory):
    return [tag_factory(**kwargs) for kwargs in request.param]
