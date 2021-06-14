"""Functional tests using pytest-flask."""
from uuid import uuid4

from pytest import mark
from . import asserts


tag_1 = {'name': "tag1", 'description': "desc_1"}
tag_2 = {'name': "tag2", 'description': "desc_2"}


@mark.usefixtures('session', 'db_tags')
@mark.parametrize('endpoint', ['tags.Root'], indirect=True)
@mark.parametrize('db_tags', indirect=True,  argvalues=[
    [tag_1, tag_2]
])
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True,  argvalues=[
        {'name': "tag1"},  # Query with 1 field
        {}  # All results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        for element in response_GET.json:
            asserts.correct_tag(element)
            asserts.match_query(element, url)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'name': "tag1"}
    ])
    def test_GET_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', [
        {'name': "tag3", 'description': "desc_1"},
        {'name': "tag4", 'description': "desc_4"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_tag(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)

    @mark.parametrize('body', [
        {'name': "tag3", 'description': "desc_1"},
        {}  # Empty body
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', [
        {'name': "tag1", 'description': "desc_1"},
        {'name': "tag1", 'description': "desc_3"}
    ])
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', [
        {'name': "tag1"},  # Missing description
        {'description': "desc_1"},  # Missing name
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'tag')
@mark.parametrize('endpoint', ['tags.Tag'], indirect=True)
@mark.parametrize('tag_id', [uuid4()], indirect=True)
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, tag, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_tag(response_GET.json)
        asserts.match_tag(response_GET.json, tag)

    @mark.parametrize('tag__id', [uuid4()])
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', [
        {'name': "new_name", 'description': "new_desc"},
        {'name': "new_name"},
        {'description': "new_desc"}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_tag(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', [
        {'description': "new_desc"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('tag__id', [uuid4()])
    @mark.parametrize('body', [
        {'description': "new_desc"}
    ])
    def test_PUT_404(self, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', [
        {'bad_field': ""}
    ])
    def test_PUT_422(self, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, response_DELETE, response_GET):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert response_GET.status_code == 404

    def test_DELETE_401(self, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('tag__id', [uuid4()])
    def test_DELETE_404(self, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
