# -*- coding: utf-8 -*-
"""Functional tests using pytest-flask."""
from flask import url_for
from pytest import mark


@mark.parametrize('path', ['flavors.Id'])
@mark.usefixtures("session")
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, client, path, flavor):
        """GET method succeeded 200."""
        response_GET = client.get(path=url_for(path, id=flavor.id))
        assert response_GET.status_code == 200
        assert response_GET.json['name'] == flavor.name
        assert response_GET.json['custom_text'] == flavor.custom_text

    @mark.parametrize('flavor_id', ["non_existing"])
    def test_GET_404(self, client, path, flavor_id):
        """GET method fails 404 if no id found."""
        response_GET = client.get(path=url_for(path, id=flavor_id))
        assert response_GET.status_code == 404

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'name': 'new_name'},
        {'custom_text': 'new_text'}
    ])
    def test_PUT_204(self, client, path, flavor, body):
        """PUT method succeeded 204."""
        response_PUT = client.put(path=url_for(path, id=flavor.id), json=body)
        assert response_PUT.status_code == 204
        response_GET = client.get(path=url_for(path, id=flavor.id))
        fields = {'name', 'custom_text'}
        for k in fields - body.keys():
            assert response_GET.json[k] == flavor.__getattribute__(k)
        for k in body.keys():
            assert response_GET.json[k] == body[k]

    @mark.parametrize('body', [{'custom_text': 'new_text'}])
    def test_PUT_401(self, client, path, flavor, body):
        """PUT method fails 401 if not authorized."""
        response_PUT = client.put(path=url_for(path, id=flavor.id), json=body)
        assert response_PUT.status_code == 401

    @mark.parametrize('flavor_id', ['non_existing'])
    @mark.parametrize('body', [{'custom_text': 'new_text'}])
    def test_PUT_404(self, client, path, flavor_id, body):
        """PUT method fails 404 if no id found."""
        response_PUT = client.put(path=url_for(path, id=flavor_id), json=body)
        assert response_PUT.status_code == 404

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [{'bad_field': ""}])
    def test_PUT_422(self, client, path, flavor, body):
        """PUT method fails 422 if bad request body."""
        response_PUT = client.put(path=url_for(path, id=flavor.id), json=body)
        assert response_PUT.status_code == 422

    @mark.usefixtures("skip_authorization")
    def test_DELETE_204(self, client, path, flavor):
        """DELETE method succeeded 204."""
        response_DELETE = client.delete(path=url_for(path, id=flavor.id))
        assert response_DELETE.status_code == 204
        response_GET = client.get(path=url_for(path, id=flavor.id))
        assert response_GET.status_code == 404

    def test_DELETE_401(self, client, path, flavor):
        """DELETE method fails 401 if not authorized."""
        response_DELETE = client.delete(path=url_for(path, id=flavor.id))
        assert response_DELETE.status_code == 401

    @mark.parametrize('flavor_id', ['non_existing'])
    def test_DELETE_404(self, client, path, flavor_id):
        """DELETE method fails 404 if no id found."""
        response_DELETE = client.delete(path=url_for(path, id=flavor_id))
        assert response_DELETE.status_code == 404


@mark.parametrize('path', ['flavors.Query'])
@mark.usefixtures("session")
class TestQuery:
    """Tests for 'Query' route in blueprint."""

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('flavors', [['f1', 'f2']], indirect=True)
    @mark.parametrize('query', [
        {'name': 'f1', 'custom_text': "Text"},
        {'name': 'f2'},  # Query with 1 field
        {'custom_text': "Text"}  # Multiple results
    ])
    def test_GET_200(self, client, path, query, flavors):
        """GET method succeeded 200."""
        response_GET = client.get(path=url_for(path, **query))
        assert response_GET.status_code == 200
        assert response_GET.json != []
        assert type(response_GET.json) is list
        fields = {'name', 'custom_text'}
        for element in response_GET.json:
            assert all([x in element for x in fields])
            assert all([element[k] == v for k, v in query.items()])

    @mark.parametrize('query', [{'name': 'f2'}])
    def test_GET_401(self, client, path, query):
        """GET method fails 401 if not authorized."""
        response_GET = client.get(path=url_for(path, **query))
        assert response_GET.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('query', [
        {},  # This is an empty query
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, client, path, query):
        """GET method fails 422 if bad request body."""
        response_GET = client.get(path=url_for(path, **query))
        assert response_GET.status_code == 422


@mark.parametrize('path', ['flavors.Submit'])
@mark.usefixtures("session")
class TestSubmit:
    """Tests for 'Submit' route in blueprint."""

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'name': "f1", 'custom_text': None},
        {'name': "f1", 'custom_text': "text"}
    ])
    def test_POST_201(self, client, path, body):
        """POST method succeeded 201."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 201
        fields = {'name', 'custom_text'}
        assert all([x in response_POST.json for x in fields])
        assert all([response_POST.json[k] == v for k, v in body.items()])

    @mark.parametrize('body', [
        {'name': "f1", 'custom_text': "text"},
        {'custom_text': "this body is missing a name"}
    ])
    def test_POST_401(self, client, path, body):
        """POST method fails 401 if not authorized."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'custom_text': "this body is missing a name"}
    ])
    def test_POST_422(self, client, path, body):
        """POST method fails 422 if missing required."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 422
