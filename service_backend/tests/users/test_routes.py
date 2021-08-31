"""Functional tests using pytest-flask."""
from backend import models
from pytest import mark
from tests import asserts
from tests.db_instances import benchmarks, flavors, results, sites, users


@mark.parametrize('endpoint', ['users.Root'], indirect=True)
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'sub': 'sub_0'},
        {'iss': 'https://aai-dev.egi.eu/oidc'},
        {'email': "sub_1@email.com"},
        {},  # Multiple results
        {'sort_by': "+iss,-sub"},
        {'sort_by': "+upload_datetime"},
        {'sort_by': "+email"}
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            user = models.User.query.get((item['sub'], item['iss']))
            asserts.match_query(item, url)
            asserts.match_user(item, user)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_1@email.com"}
    ])
    def test_GET_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_1@email.com"}
    ])
    def test_GET_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'sub': 'sub_0'},
        {'email': "sub_0@email.com"}
    ])
    def test_DELETE_204(self, query, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.User.query.filter_by(**query).all() == []
        # Check delete is cascaded
        assert models.Benchmark.query.get(benchmarks[0]['id']) == None
        assert models.Result.query.get(results[0]['id']) == None
        assert models.Site.query.get(sites[0]['id']) == None
        assert models.Flavor.query.get(flavors[0]['id']) == None

    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_1@email.com"}
    ])
    def test_DELETE_401(self, query, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.User.query.filter_by(**query).all() != []

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_1@email.com"}
    ])
    def test_DELETE_403(self, query, response_DELETE):
        """DELETE method fails 403 if forbidden."""
        assert response_DELETE.status_code == 403
        assert models.User.query.filter_by(**query).all() != []

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {}  # Attempt to delete all users should be forbiden
    ])
    def test_DELETE_422(self, response_DELETE):
        """DELETE method fails 422 if bad request body."""
        assert response_DELETE.status_code == 422
        assert models.User.query.all() != []


@mark.parametrize('endpoint', ['users.Search'], indirect=True)
class TestSearch:
    """Tests for 'Search' route in blueprint."""

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["sub_1@email.com"]},
        {'terms[]': ["sub_1@email.com"]},
        {'terms': ["sub", "email.com"]},
        {'terms[]': ["sub", "email.com"]},
        {'terms': []},   # Empty query
        {'terms[]': []},  # Empty query
        {'sort_by': "+iss,-sub"},
        {'sort_by': "+upload_datetime"},
        {'sort_by': "+email"}
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            user = models.User.query.get((item['sub'], item['iss']))
            asserts.match_query(item, url)
            asserts.match_user(item, user)

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
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


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


@mark.parametrize('endpoint', ['users.Register'], indirect=True)
class TestSelf:
    """Tests for 'Self' route in blueprint."""

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    def test_GET_200(self, user, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_user(response_GET.json, user)

    @mark.usefixtures('mock_accesstoken')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    def test_GET_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["non_existing"], indirect=True)
    @mark.parametrize('token_iss', ["https://aai-dev.egi.eu/oidc"], indirect=True)
    def test_GET_403(self, response_GET):
        """GET method fails 403 if not registered."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["new_user"], indirect=True)
    @mark.parametrize('token_iss', ["https://aai-dev.egi.eu/oidc"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_POST_201(self, response_POST, user, url):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.match_query(response_POST.json, url)
        asserts.match_user(response_POST.json, user)
        asserts.user_welcome(user)

    @mark.usefixtures('mock_introspection')
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged', 'grant_accesstoken')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_PUT_204(self, introspection_email, response_PUT, user):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert user.email == introspection_email

    @mark.usefixtures('mock_introspection')
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_PUT_401(self, token_sub, token_iss, user, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert user == models.User.query.get((token_sub, token_iss))

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["not-registered"], indirect=True)
    @mark.parametrize('token_iss', ["https://aai-dev.egi.eu/oidc"], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_PUT_403(self, response_PUT):
        """PUT method fails 403 if not registered."""
        assert response_PUT.status_code == 403
