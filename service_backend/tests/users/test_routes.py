"""Functional tests using pytest-flask."""
from backend.users import models
from pytest import mark
from tests.elements import user_1, user_2

from . import asserts


@mark.usefixtures('session', 'db_users')
@mark.parametrize('endpoint', ['users.Root'], indirect=True)
@mark.parametrize('db_users', indirect=True,  argvalues=[
    [user_1, user_2]
])
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', [
        {'iss': "egi.com", 'email': 'sub_1@email.com'},
        {'iss': "egi.com"},  # Query with 1 field
        {'email': "sub_1@email.com"},  # Query with 1 field
        {}  # Multiple results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_user(element)
            asserts.match_query(element, url)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'iss': "egi.com"}
    ])
    def test_GET_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.usefixtures('session', 'db_users')
@mark.parametrize('endpoint', ['users.Search'], indirect=True)
@mark.parametrize('db_users', indirect=True,  argvalues=[
    [user_1, user_2]
])
class TestSearch:
    """Tests for 'Search' route in blueprint."""

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["sub_1@email.com"]},
        {'terms': ["sub", "email.com"]},
        {'terms': []}
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_user(element)
            asserts.match_search(element, url)

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["sub_1@email.com"]}
    ])
    def test_GET_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'terms': ["sub_1@email.com"]}
    ])
    def test_GET_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.usefixtures('session', 'user')
@mark.parametrize('endpoint', ['users.User'], indirect=True)
@mark.parametrize('user_sub', ["sub_1"], indirect=True)
@mark.parametrize('user_iss', ["egi.com"], indirect=True)
class TestId:
    """Tests for 'Id' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_GET_200(self, user, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_user(response_GET.json)
        asserts.match_user(response_GET.json, user)

    def test_GET_401(self, response_GET):
        """GET method fails 401 if not authorized."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    def test_GET_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('user__sub', ["sub_2"])
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, user, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.User.query.get((user.sub, user.iss)) == None

    def test_DELETE_401(self, user, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.User.query.get((user.sub, user.iss)) != None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('user__sub', ["sub_2"])
    def test_DELETE_404(self, user, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.User.query.get((user.sub, user.iss)) != None


@mark.usefixtures('session')
@mark.parametrize('endpoint', ['users.Admin'], indirect=True)
class TestAdmin:
    """Tests for 'Admin' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_GET_204(self, response_GET):
        """GET method succeeded 204."""
        assert response_GET.status_code == 204

    def test_GET_401(self, response_GET):
        """GET method fails 401 if not authorized."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    def test_GET_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403


@mark.usefixtures('session', 'db_users')
@mark.usefixtures('mock_token_info', 'mock_introspection_info')
@mark.parametrize('endpoint', ['users.Register'], indirect=True)
@mark.parametrize('db_users', indirect=True,  argvalues=[
    [user_1, user_2]
])
class TestSelf:
    """Tests for 'Self' route in blueprint."""

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["sub_1"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    def test_GET_200(self, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_user(response_GET.json)

    @mark.parametrize('token_sub', ["sub_1"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    def test_GET_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["sub_3"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["sub_3"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_POST_201(self, response_POST, url):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_user(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_user_in_db(response_POST.json)

    @mark.parametrize('token_sub', ["sub_3"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["sub_1"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["sub_1"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_PUT_204(self, response_PUT, response_GET, introspection_email):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_user(response_GET.json)
        assert response_GET.json['email'] == introspection_email

    @mark.parametrize('token_sub', ["sub_1"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_PUT_401(self, response_PUT, ):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["sub_3"], indirect=True)
    @mark.parametrize('token_iss', ["egi.com"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_PUT_404(self, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
