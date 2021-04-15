# -*- coding: utf-8 -*-
"""Functional tests using pytest-flask."""
from pytest import mark


@mark.parametrize('route', ['Id'], indirect=True)
class TestID:
    """Tests for ID route in blueprint."""

    def test_GET_200(self, response_GET, flavor):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json['name'] == flavor.name
        assert response_GET.json['custom_text'] == flavor.custom_text

    @mark.parametrize('id', ['non_existing_id'], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.parametrize('body', [{'custom_text': "test_text"}], indirect=True)
    def test_PUT_204(self, response_PUT, response_GET, flavor, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.json['name'] == flavor.name
        assert response_GET.json['custom_text'] == body['custom_text']

    @mark.parametrize('id', ['non_existing_id'], indirect=True)
    @mark.parametrize('body', [{'custom_text': "test_text"}], indirect=True)
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
