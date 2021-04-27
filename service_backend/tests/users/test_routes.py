# -*- coding: utf-8 -*-
"""Functional tests using pytest-flask."""
import json
from flask import url_for
from pytest import mark


@mark.parametrize('path', ['users.Id'])
@mark.usefixtures("session")
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, client, path, user):
        """GET method succeeded 200."""
        response_GET = client.get(url_for(path, sub=user.sub, iss=user.iss))
        assert response_GET.status_code == 200
        assert response_GET.json['email'] == user.email
        assert response_GET.json['created_at'] == str(user.created_at)

    @mark.parametrize('iss', ["non_existing"])
    @mark.parametrize('sub', ["non_existing"])
    def test_GET_404(self, client, path, iss, sub):
        """GET method fails 404 if no id found."""
        response_GET = client.get(url_for(path, iss=iss, sub=sub))
        assert response_GET.status_code == 404

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'email': 'new_email@gmail.com'}
    ])
    def test_PUT_204(self, client, path, user, body):
        """PUT method succeeded 204."""
        path = url_for(path, iss=user.iss, sub=user.sub)
        response_PUT = client.put(path, json=body)
        assert response_PUT.status_code == 204
        response_GET = client.get(path)
        fields = {'sub', 'iss', 'email'}
        for k in fields - body.keys():
            assert response_GET.json[k] == user.__getattribute__(k)
        for k in body.keys():
            assert response_GET.json[k] == body[k]
        assert response_GET.json['created_at'] == str(user.created_at)

    @mark.parametrize('body', [{'custom_text': 'new_text'}])
    def test_PUT_401(self, client, path, user, body):
        """PUT method fails 401 if not authorized."""
        path = url_for(path, iss=user.iss, sub=user.sub)
        response_PUT = client.put(path, json=body)
        assert response_PUT.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('iss', ["non_existing"])
    @mark.parametrize('sub', ["non_existing"])
    @mark.parametrize('body', [{'email': 'new_email@gmail.com'}])
    def test_PUT_404(self, client, path, iss, sub, body):
        """PUT method fails 404 if no id found."""
        path = url_for(path, iss=iss, sub=sub)
        response_PUT = client.put(path, json=body)
        assert response_PUT.status_code == 404

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'bad_field': ""},
        {'sub': 'new_sub'},  # Should not be editable
        {'iss': 'new_iss'},  # Should not be editable
        {'created_at': '01.01.2020'}  # Should not be editable
    ])
    def test_PUT_422(self, client, path, user, body):
        """PUT method fails 422 if bad request body."""
        path = url_for(path, iss=user.iss, sub=user.sub)
        response_PUT = client.put(path, json=body)
        assert response_PUT.status_code == 422

    @mark.usefixtures("skip_authorization")
    def test_DELETE_204(self, client, path, user):
        """DELETE method succeeded 204."""
        path = url_for(path, iss=user.iss, sub=user.sub)
        response_DELETE = client.delete(path)
        assert response_DELETE.status_code == 204
        response_GET = client.get(path)
        assert response_GET.status_code == 404

    def test_DELETE_401(self, client, path, user):
        """DELETE method fails 401 if not authorized."""
        path = url_for(path, iss=user.iss, sub=user.sub)
        response_DELETE = client.delete(path)
        assert response_DELETE.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('iss', ["non_existing"])
    @mark.parametrize('sub', ["non_existing"])
    def test_DELETE_404(self, client, path, iss, sub):
        """DELETE method fails 404 if no id found."""
        path = url_for(path, iss=iss, sub=sub)
        response_DELETE = client.delete(path)
        assert response_DELETE.status_code == 404


@mark.parametrize('path', ['users.Query'])
@mark.usefixtures("session")
class TestQuery:
    """Tests for 'Query' route in blueprint."""

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('users', [['u1@k.de', 'u2@k.de']], indirect=True)
    @mark.parametrize('query', [
        {'iss': "egi.com"},  # Multiple results
        {'email': 'u1@k.de'},  # Query with 1 field
        {'email': 'u2@k.de', 'iss': "egi.com"}
    ])
    def test_GET_200(self, client, path, query, users):
        """GET method succeeded 200."""
        response_GET = client.get(path=url_for(path, **query))
        assert response_GET.status_code == 200
        assert response_GET.json != []
        assert type(response_GET.json) is list
        fields = {'sub', 'iss', 'email', 'created_at'}
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


@mark.parametrize('path', ['users.Submit'])
@mark.usefixtures("session")
class TestSubmit:
    """Tests for 'Submit' route in blueprint."""

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'sub': "u1", 'iss': "my_iss", 'email': "u1@k.de"}
    ])
    def test_POST_201(self, client, path, body):
        """POST method succeeded 201."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 201
        fields = {'sub', 'iss', 'email', 'created_at'}
        assert all([x in response_POST.json for x in fields])
        assert all([response_POST.json[k] == v for k, v in body.items()])

    @mark.parametrize('body', [
        {'sub': "u1", 'iss': "my_iss", 'email': "u1@k.de"}
    ])
    def test_POST_401(self, client, path, body):
        """POST method fails 401 if not authorized."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 401

    @mark.usefixtures("skip_authorization")
    @mark.parametrize('body', [
        {'sub': "u1", 'iss': "my_iss"},  # Missing email
        {'sub': "u1", 'email': "u1@k.de"},  # Missing iss
        {'iss': "my_iss", 'email': "u1@k.de"}  # Missing sub
    ])
    def test_POST_422(self, client, path, body):
        """POST method fails 422 if missing required."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 422


@mark.parametrize('path', ['users.Admin'])
@mark.usefixtures("session")
class TestAdmin:
    """Tests for 'Admin' route in blueprint."""

    @mark.usefixtures("skip_authorization")
    def test_GET_204(self, client, path):
        """GET method succeeded 201."""
        response_GET = client.get(path=url_for(path))
        assert response_GET.status_code == 204

    def test_POST_401(self, client, path):
        """POST method fails 401 if not authorized."""
        response_GET = client.get(path=url_for(path))
        assert response_GET.status_code == 401


@mark.parametrize('path', ['users.Register'])
@mark.usefixtures("session")
class TestRegister:
    """Tests for 'Register' route in blueprint."""

    @mark.usefixtures("skip_authorization", "patch_accesstoken")
    @mark.parametrize('body', [
        {'email': "u1@k.de"}
    ])
    def test_POST_201(self, client, path, body):
        """POST method succeeded 201."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 201
        fields = {'sub', 'iss', 'email', 'created_at'}
        assert all([x in response_POST.json for x in fields])
        assert all([response_POST.json[k] == v for k, v in body.items()])

    @mark.parametrize('body', [
        {'email': "u1@k.de"}
    ])
    def test_POST_401(self, client, path, body):
        """POST method fails 401 if not authorized."""
        response_POST = client.post(path=url_for(path), json=body)
        assert response_POST.status_code == 401
