"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend import models
from backend.schemas import schemas
from pytest import mark
from tests import asserts
from tests.db_instances import tags, users


@mark.parametrize('endpoint', ['tags.list'], indirect=True)
class TestList:

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'name': "tag1"},  # Query with 1 field
        {},  # All results
        {'sort_by': "+name,-description"},
        {'sort_by': "+id"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            tag = models.Tag.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_tag(item, tag)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['tags.create'], indirect=True)
class TestCreate:

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "tag4", 'description': "desc_1"},
        {'name': "tag4"}
    ])
    def test_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        tag = models.Tag.query.get(response_POST.json['id'])
        asserts.match_tag(response_POST.json, tag)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "tag4", 'description': "desc_1"},
        {}  # Empty body which would fail
    ])
    def test_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["non-registered"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "tag4", 'description': "desc_1"}
    ])
    def test_403(self, response_POST):
        """POST method fails 403 if user not registered."""
        assert response_POST.status_code == 403

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "tag1", 'description': "desc_1"},
        {'name': "tag1"}
    ])
    def test_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "desc_1"},  # Missing name
        {}  # Empty body
    ])
    def test_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.parametrize('endpoint', ['tags.search'], indirect=True)
class TestSearch:

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["tag1"]},
        {'terms[]': ["tag1"]},
        {'terms': ["tag", " 2"]},
        {'terms[]': ["tag", " 2"]},
        {'terms': []},   # Empty query
        {'terms[]': []},  # Empty query
        {'sort_by': "+name,-description"},
        {'sort_by': "+id"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            tag = models.Tag.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_tag(item, tag)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['tags.get'], indirect=True)
@mark.parametrize('tag_id',  indirect=True, argvalues=[
    tags[0]['id'],
    tags[1]['id'],
    tags[2]['id'],
    tags[3]['id']
])
class TestGet:

    def test_200(self, tag, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_tag(response_GET.json, tag)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404


@mark.parametrize('endpoint', ['tags.update'], indirect=True)
@mark.parametrize('tag_id',  indirect=True, argvalues=[
    tags[0]['id'],
    tags[1]['id'],
    tags[2]['id'],
    tags[3]['id']
])
class TestUpdate:

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "new_name1", 'description': "new_desc"},
        {'name': "new_name2"},
    ])
    def test_204(self, body, response_PUT, tag):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Tag().dump(tag)
        asserts.match_body(json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "new_desc"}
    ])
    def test_401(self, tag, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert tag == models.Tag.query.get(tag.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "new_name1", 'description': "new_desc"},
    ])
    def test_404(self, tag, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
        assert tag == models.Tag.query.get(tag.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_422(self, tag, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422
        assert tag == models.Tag.query.get(tag.id)


@mark.parametrize('endpoint', ['tags.delete'], indirect=True)
@mark.parametrize('tag_id',  indirect=True, argvalues=[
    tags[0]['id'],
    tags[1]['id'],
    tags[2]['id'],
    tags[3]['id']
])
class TestDelete:

    @mark.usefixtures('grant_admin')
    def test_204(self, tag, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Tag.query.get(tag.id) is None

    def test_401(self, tag, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Tag.query.get(tag.id) is not None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, tag, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Tag.query.get(tag.id) is not None
