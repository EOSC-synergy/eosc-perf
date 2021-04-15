# -*- coding: utf-8 -*-
"""Functional tests using pytest-flask."""
from pytest import mark


@mark.parametrize('path', ['flavors.Id'], indirect=True)
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, response_GET, flavor):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json['name'] == flavor.name
        assert response_GET.json['custom_text'] == flavor.custom_text

    @mark.parametrize('id', ['non_existing_id'], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.parametrize('custom_text', ["test_text"], indirect=True)
    def test_PUT_204(self, response_PUT, response_GET, flavor, custom_text):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.json['name'] == flavor.name
        assert response_GET.json['custom_text'] == custom_text

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


@mark.parametrize('path', ['flavors.Query'], indirect=True)
class TestQuery:
    """Tests for 'Query' route in blueprint."""

    @mark.parametrize('query', [{'name'}, {'custom_text'}], indirect=True)
    def test_GET_200(self, response_GET, flavor):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert type(response_GET.json) is list
        assert len(response_GET.json) >= 1
        for element in response_GET.json:
            assert element['name'] == flavor.name
            assert element['custom_text'] == flavor.custom_text

    @mark.parametrize('query', [{'bad_key'}, {}], indirect=True)
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('path', ['flavors.Submit'], indirect=True)
class TestSubmit:
    """Tests for 'Submit' route in blueprint."""

    @mark.parametrize('name', ["TestFlavor"], indirect=True)
    @mark.parametrize('custom_text', ["test_text", None], indirect=True)
    def test_POST_201(self, response_POST, name, custom_text):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        assert response_POST.json['name'] == name
        assert response_POST.json['custom_text'] == custom_text

    @mark.parametrize('name', [None], indirect=True)
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422
