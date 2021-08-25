"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend import models
from backend.schemas import schemas
from pytest import mark
from tests import asserts
from tests.db_instances import flavors, sites, users


@mark.parametrize('endpoint', ['flavors.Flavor'], indirect=True)
@mark.parametrize('flavor_id', indirect=True, argvalues=[
    flavors[0]['id'],
    flavors[1]['id'],
    flavors[2]['id'],
    flavors[3]['id']
])
class TestFlavor:
    """Tests for 'Flavor' route in blueprint."""

    def test_GET_200(self, flavor, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_flavor(response_GET.json, flavor)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "new_name", 'description': "new_text"},
        {'name': "new_name"},
        {'description': "new_text"},
        {}
    ])
    def test_PUT_204(self, body, response_PUT, flavor):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Flavor().dump(flavor)
        asserts.match_body(json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "new_text"}
    ])
    def test_PUT_401(self, flavor, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert flavor == models.Flavor.query.get(flavor.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "new_text"}
    ])
    def test_PUT_404(self, flavor, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
        assert flavor == models.Flavor.query.get(flavor.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_PUT_422(self, flavor, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422
        assert flavor == models.Flavor.query.get(flavor.id)

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, flavor, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Flavor.query.get(flavor.id) is None
        site = models.Site.query.get(flavor.site_id)
        assert site is not None
        assert flavor not in site.flavors

    def test_DELETE_401(self, flavor, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Flavor.query.get(flavor.id) is not None
        site = models.Site.query.get(flavor.site_id)
        assert site is not None
        assert flavor in site.flavors

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_DELETE_404(self, flavor, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Flavor.query.get(flavor.id) is not None
        site = models.Site.query.get(flavor.site_id)
        assert site is not None
        assert flavor in site.flavors


@mark.parametrize('endpoint', ['flavors.Site'], indirect=True)
@mark.parametrize('flavor_id', indirect=True, argvalues=[
    flavors[0]['id'],
    flavors[1]['id'],
    flavors[2]['id'],
    flavors[3]['id']
])
class TestSite:
    """Tests for 'Site' route in blueprint."""

    def test_GET_200(self, flavor, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        site = models.Site.query.get(flavor.site_id)
        asserts.match_site(response_GET.json, site)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404
