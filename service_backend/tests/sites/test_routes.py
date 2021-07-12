"""Functional tests using pytest-flask."""
from uuid import uuid4

from pytest import mark
from tests.elements import flavor_1, flavor_2, flavor_3, site_1, site_2
from backend.sites import models

from . import asserts


@mark.usefixtures('session', 'db_sites', 'db_flavors')
@mark.parametrize('db_sites', indirect=True, argvalues=[
    [site_1, site_2]
])
@mark.parametrize('db_flavors', indirect=True, argvalues=[
    [flavor_1, flavor_2, flavor_3]
])
@mark.parametrize('endpoint', ['sites.Root'], indirect=True)
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        {'name': 'site1', 'address': "address1"},
        {'address': "address1"},  # Query with 1 field
        {}  # Multiple results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_site(element)
            asserts.match_query(element, url)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "s3", 'address': "addr2", 'description': "Text"},
        {'name': "s3", 'address': "addr2"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_site(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        asserts.match_site_in_db(response_POST.json)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "s3", 'address': "addr2", 'description': "Text"},
        {}  # Empty body
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "site1", 'address': "address1"},
        {'name': "site2", 'address': "address2"}
    ])
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "site"},  # Missingaddress
        {'address': "address"},  # Missingname
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'db_sites')
@mark.parametrize('endpoint', ['sites.Search'], indirect=True)
@mark.parametrize('db_sites', indirect=True, argvalues=[
    [site_1, site_2]
])
class TestSearch:
    """Tests for 'Search' route in blueprint."""

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': [site_1["name"]]},
        {'terms': [site_1["address"]]},
        {'terms': [site_1["description"]]},
        {'terms': [site_1["name"], site_1["description"]]},
        {'terms': []}   # Empty terms
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_site(element)
            asserts.match_search(element, url)

    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.usefixtures('session', 'site')
@mark.parametrize('endpoint', ['sites.Site'], indirect=True)
@mark.parametrize('site_id', [uuid4()], indirect=True)
@mark.parametrize('site__flavors', [["f1", "f2"]])
class TestSite:
    """Tests for 'Site' route in blueprint."""

    def test_GET_200(self, site, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_site(response_GET.json)
        asserts.match_site(response_GET.json, site)

    @mark.parametrize('site__id', [uuid4()])
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "new_name", 'address': "addr1"},
        {'name': "new_name"},
        {'address': "new_addr"}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_site(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': 'new_name', 'address': "new_addr"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('site__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': 'new_name', 'address': "new_addr"}
    ])
    def test_PUT_404(self, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_PUT_422(self, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, site, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Site.query.get(site.id) == None
        for flavor in site.flavors:  # Flavors are removed
            assert models.Flavor.query.get(flavor.id) == None

    def test_DELETE_401(self, site, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Site.query.get(site.id) != None
        for flavor in site.flavors:  # Flavors exist
            assert models.Flavor.query.get(flavor.id) != None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('site__id', [uuid4()])
    def test_DELETE_404(self, site, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Site.query.get(site.id) != None
        for flavor in site.flavors:  # Flavors exist
            assert models.Flavor.query.get(flavor.id) != None


@mark.usefixtures('session', 'db_sites', 'db_flavors')
@mark.parametrize('db_sites', indirect=True, argvalues=[
    [site_1, site_2]
])
@mark.parametrize('db_flavors', indirect=True, argvalues=[
    [flavor_1, flavor_2, flavor_3]
])
@mark.parametrize('endpoint', ['sites.Flavors'], indirect=True)
@mark.parametrize('site_id', [site_1['id']], indirect=True)
class TestFlavors:
    """Tests for 'Flavors' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        {'name': 'flavor1'},
        {'name': 'flavor2'},
        {}  # Multiple results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_flavor(element)
            asserts.match_query(element, url)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "flavor3", 'description': "Flavor3 site1"},
        {'name': "flavor3"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_flavor(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        asserts.site_has_flavor(response_POST.json, url)
        asserts.match_flavor_in_db(response_POST.json)

    @mark.parametrize('body', indirect=True, argvalues=[
        flavor_3,
        {}  # Empty body
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "flavor1"},
        {'name': "flavor2"}
    ])
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {k: flavor_1[k] for k in flavor_1.keys() - {'name'}},  # Missingname
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'site', 'flavor')
@mark.parametrize('endpoint', ['sites.Flavor'], indirect=True)
@mark.parametrize('flavor_id', [uuid4()], indirect=True)
class TestFlavor:
    """Tests for 'Flavor' route in blueprint."""

    def test_GET_200(self, flavor, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_flavor(response_GET.json)
        asserts.match_flavor(response_GET.json, flavor)

    @mark.parametrize('flavor__id', [uuid4()])
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
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        asserts.correct_flavor(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "new_text"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('flavor__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "new_text"}
    ])
    def test_PUT_404(self, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_PUT_422(self, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, flavor, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Flavor.query.get(flavor.id) == None

    def test_DELETE_401(self, flavor, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Flavor.query.get(flavor.id) != None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('flavor__id', [uuid4()])
    def test_DELETE_404(self, flavor, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Flavor.query.get(flavor.id) != None
