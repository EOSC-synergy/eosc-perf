# -*- coding: utf-8 -*-
"""Functional tests using pytest-flask."""
from pytest import mark


@mark.parametrize('path', ['sites.Id'], indirect=True)
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, response_GET, site):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json['name'] == site.name
        assert response_GET.json['address'] == site.address
        assert response_GET.json['description'] == site.description
        assert response_GET.json['hidden'] == site.hidden
        assert response_GET.json['flavors'] == site.flavors

    @mark.parametrize('id', ['non_existing_id'], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.parametrize('address', ["test_addr"], indirect=True)
    def test_PUT_204(self, response_PUT, response_GET, site, address):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.json['name'] == site.name
        assert response_GET.json['address'] == address
        assert response_GET.json['description'] == site.description
        assert response_GET.json['hidden'] == site.hidden
        assert response_GET.json['flavors'] == site.flavors

    @mark.parametrize('id', ['non_existing_id'], indirect=True)
    def test_PUT_404(self, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404

    @mark.parametrize('body', [{'bad_field': ""}], indirect=True)
    def test_PUT_422(self, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422

    def test_DELETE_204(self, response_DELETE, response_GET):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert response_GET.status_code == 404

    @mark.parametrize('id', ['non_existing_id'], indirect=True)
    def test_DELETE_404(self, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404


@mark.parametrize('path', ['sites.Query'], indirect=True)
class TestQuery:
    """Tests for 'Query' route in blueprint."""

    @mark.parametrize('query', [{'name'}, {'address'}], indirect=True)
    def test_GET_200(self, response_GET, site):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert type(response_GET.json) is list
        assert len(response_GET.json) >= 1
        for element in response_GET.json:
            assert element['name'] == site.name
            assert element['address'] == site.address
            assert element['description'] == site.description
            assert element['hidden'] == site.hidden
            assert element['flavors'] == site.flavors

    @mark.parametrize('query', [{'bad_key'}, {}], indirect=True)
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('path', ['sites.Submit'], indirect=True)
class TestSubmit:
    """Tests for 'Submit' route in blueprint."""

    @mark.parametrize('name', ["TestSite"], indirect=True)
    @mark.parametrize('address', ["test_addr", None], indirect=True)
    @mark.parametrize('flavors', [["f1", "f2"]], indirect=True)
    def test_POST_201(self, response_POST, name, address, flavors):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        assert response_POST.json['name'] == name
        assert response_POST.json['address'] == address
        assert response_POST.json['description'] == None
        assert response_POST.json['hidden'] == True
        assert set(response_POST.json['flavors']) == {x.name for x in flavors}

    @mark.parametrize('name', [None], indirect=True)
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422
