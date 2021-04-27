# -*- coding: utf-8 -*-
"""Functional tests using pytest-flask."""
from flask import url_for
from pytest import mark


@mark.parametrize('path', ['sites.Id'])
@mark.usefixtures("session")
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, client, path, site):
        """GET method succeeded 200."""
        response_GET = client.get(path=url_for(path, id=site.id))
        assert response_GET.status_code == 200
        assert response_GET.json['name'] == site.name
        assert response_GET.json['address'] == site.address
        assert response_GET.json['description'] == site.description
        assert response_GET.json['hidden'] == site.hidden
        assert response_GET.json['flavors'] == [x.name for x in site.flavors]

    @mark.parametrize('site_id', ["non_existing"])
    def test_GET_404(self, client, path, site_id):
        """GET method fails 404 if no id found."""
        response_GET = client.get(path=url_for(path, id=site_id))
        assert response_GET.status_code == 404

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('flavors', [['f1', 'f2']], indirect=True)
    @mark.parametrize('body', [
        {'address': "new_addr"},
        {'flavors': ["f1", "f2"]},
    ])
    def test_PUT_204(self, client, path, site, body, flavors):
        """PUT method succeeded 204."""
        response_PUT = client.put(path=url_for(path, id=site.id), json=body)
        assert response_PUT.status_code == 204
        response_GET = client.get(path=url_for(path, id=site.id))
        fields = {'name', 'address', 'description', 'hidden'}
        for k in fields - body.keys():
            assert response_GET.json[k] == site.__getattribute__(k)
        for k in body.keys():
            assert response_GET.json[k] == body[k]
        if 'flavors' not in body:
            flavors = [x.name for x in site.flavors]
            assert response_GET.json['flavors'] == flavors
        else:
            assert response_GET.json['flavors'] == body['flavors']

    @mark.parametrize('body', [{'address': 'new_addr'}])
    def test_PUT_401(self, client, path, flavor, body):
        """PUT method fails 401 if not authorized."""
        response_PUT = client.put(path=url_for(path, id=flavor.id), json=body)
        assert response_PUT.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('site_id', ["non_existing"])
    @mark.parametrize('body', [{'address': 'new_addr'}])
    def test_PUT_404(self, client, path, site_id, body):
        """PUT method fails 404 if no id found."""
        response_PUT = client.put(path=url_for(path, id=site_id), json=body)
        assert response_PUT.status_code == 404

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [{'bad_field': ""}])
    def test_PUT_422(self, client, path, site, body):
        """PUT method fails 422 if bad request body."""
        response_PUT = client.put(path=url_for(path, id=site.id), json=body)
        assert response_PUT.status_code == 422

    @mark.usefixtures("skip_authorization")
    def test_DELETE_204(self, client, path, site):
        """DELETE method succeeded 204."""
        response_DELETE = client.delete(path=url_for(path, id=site.id))
        assert response_DELETE.status_code == 204
        response_GET = client.get(path=url_for(path, id=site.id))
        assert response_GET.status_code == 404

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('site_id', ["non_existing"])
    def test_DELETE_404(self, client, path, site_id):
        """DELETE method fails 404 if no id found."""
        response_DELETE = client.delete(path=url_for(path, id=site_id))
        assert response_DELETE.status_code == 404


@mark.parametrize('path', ['sites.Query'])
@mark.usefixtures("session")
class TestQuery:
    """Tests for 'Query' route in blueprint."""

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('sites', [['s1', 's2']], indirect=True)
    @mark.parametrize('query', [
        {'name': 's1', 'hidden': True},
        {'name': 's2'},  # Query with 1 field
        {'hidden': True}  # Multiple results
    ])
    def test_GET_200(self, client, path, query, sites):
        """GET method succeeded 200."""
        response_GET = client.get(path=url_for(path, **query))
        assert response_GET.status_code == 200
        assert response_GET.json != []
        assert type(response_GET.json) is list
        fields = ['name', 'address', 'description', 'hidden', 'flavors']
        for element in response_GET.json:
            assert all([x in element for x in fields])
            assert all([element[k] == v for k, v in query.items()])

    @mark.parametrize('query', [{'hidden': True}])
    def test_GET_401(self, client, path, query):
        """GET method fails 401 if not authorized."""
        response_GET = client.get(path=url_for(path, **query))
        assert response_GET.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('query', [
        {},  # Empty queries should return error
        {'flavors': ['f1', 'f2']},  # flavors search not supported
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, client, path, query):
        """GET method fails 422 if bad request body."""
        response_GET = client.get(path=url_for(path, **query))
        assert response_GET.status_code == 422


@mark.parametrize('path', ['sites.Submit'])
@mark.usefixtures("session")
class TestSubmit:
    """Tests for 'Submit' route in blueprint."""

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('flavors', [['f1', 'f2']], indirect=True)
    @mark.parametrize('body', [
        {'name': "f1", 'address': "a1"},
        {'name': "f1", 'address': "a1", "flavors": ["f1", "f2"]}
    ])
    def test_POST_201(self, client, path, body, flavors):
        """POST method succeeded 201."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 201
        fields = ['name', 'address', 'description', 'hidden', 'flavors']
        assert all([x in response_POST.json for x in fields])
        assert all([response_POST.json[k] == v for k, v in body.items()])

    @mark.parametrize('body', [
        {'name': "f1", 'address': "a1"},
        {'address': "this body is missing a name"}
    ])
    def test_POST_401(self, client, path, body):
        """POST method fails 401 if not authorized."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'address': "this body is missing a name"},
        {'name': "f1", 'address': "a1", 'hidden': False},
    ])
    def test_POST_422(self, client, path, body):
        """POST method fails 422 if missing required."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 422
