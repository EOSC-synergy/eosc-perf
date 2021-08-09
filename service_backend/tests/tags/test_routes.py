"""Functional tests using pytest-flask."""
from operator import mod
from uuid import uuid4

from backend.models import models
from backend.schemas import schemas
from pytest import mark
from tests import asserts
from tests.db_instances import tags

@mark.parametrize('endpoint', ['tags.Root'], indirect=True)
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'name': "tag1"},  # Query with 1 field
        {}  # All results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json.items != []
        for item in response_GET.json['items']:
            tag = models.Tag.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_tag(item, tag)


    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "tag4", 'description': "desc_1"},
        {'name': "tag4"}
    ])
    def test_POST_201(self, response_POST, url, body):
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
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "tag1", 'description': "desc_1"},
        {'name': "tag1"}
    ])
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "desc_1"},  # Missing name
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.parametrize('endpoint', ['tags.Search'], indirect=True)
class TestSearch:
    """Tests for 'Search' route in blueprint."""

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["tag1"]},
        {'terms': ["tag", " 2"]},
        {'terms': []}
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json.items != []
        for item in response_GET.json['items']:
            tag = models.Tag.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_tag(item, tag)


    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['tags.Tag'], indirect=True)
@mark.parametrize('tag_id',  indirect=True, argvalues=[
    tags[0]['id'],
    tags[1]['id'],
    tags[2]['id'],
    tags[3]['id']
])
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, tag, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_tag(response_GET.json, tag)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'name': "new_name1", 'description': "new_desc"},
        {'name': "new_name2"},
        {'description': "new_desc"}
    ])
    def test_PUT_204(self, body, response_PUT, tag):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Tag().dump(tag)
        asserts.match_body(json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "new_desc"}
    ])
    def test_PUT_401(self, tag, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert tag == models.Tag.query.get(tag.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'description': "new_desc"}
    ])
    def test_PUT_404(self, tag, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
        assert tag == models.Tag.query.get(tag.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_PUT_422(self, tag, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422
        assert tag == models.Tag.query.get(tag.id)

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, tag, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Tag.query.get(tag.id) is None

    def test_DELETE_401(self, tag, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Tag.query.get(tag.id) is not None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_DELETE_404(self, tag, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Tag.query.get(tag.id) is not None
