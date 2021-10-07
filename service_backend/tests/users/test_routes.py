"""Functional tests using pytest-flask."""
from backend import models
from pytest import mark
from tests import asserts
from tests.db_instances import benchmarks, flavors, results, sites, tags, users


@mark.parametrize('endpoint', ['users.list'], indirect=True)
class TestList:

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'sub': 'sub_0'},
        {'iss': 'https://aai-dev.egi.eu/oidc'},
        {'email': "sub_0@email.com"},
        {},  # Multiple results
        {'sort_by': "+iss,-sub"},
        {'sort_by': "+registration_datetime"},
        {'sort_by': "+email"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            user = models.User.query.get((item['sub'], item['iss']))
            asserts.match_query(item, url)
            asserts.match_user(item, user)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_0@email.com"}
    ])
    def test_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_0@email.com"}
    ])
    def test_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['users.register'], indirect=True)
class TestRegister:

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["new_user"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_201(self, response_POST, user, url):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.match_query(response_POST.json, url)
        asserts.match_user(response_POST.json, user)
        asserts.user_welcome(user)

    @mark.usefixtures('mock_introspection')
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409


@mark.parametrize('endpoint', ['users.remove'], indirect=True)
class TestRemove:

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'sub': 'sub_1'},
        {'email': "sub_1@email.com"}
    ])
    def test_204(self, query, response_POST):
        """POST method succeeded 204."""
        assert response_POST.status_code == 204
        assert models.User.query.filter_by(**query).all() == []
        # Check the deletion is cascaded
        assert models.Benchmark.query.get(benchmarks[2]['id']) is None
        assert models.Result.query.get(results[2]['id']) is None
        assert models.Site.query.get(sites[2]['id']) is None
        assert models.Flavor.query.get(flavors[4]['id']) is None

    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_1@email.com"}
    ])
    def test_401(self, query, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401
        assert models.User.query.filter_by(**query).all() != []

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'email': "sub_1@email.com"}
    ])
    def test_403(self, query, response_POST):
        """POST method fails 403 if forbidden."""
        assert response_POST.status_code == 403
        assert models.User.query.filter_by(**query).all() != []

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {}  # Attempt to POST all users should be forbiden
    ])
    def test_422(self, response_POST):
        """POST method fails 422 if bad request body."""
        assert response_POST.status_code == 422
        assert models.User.query.all() != []


@mark.parametrize('endpoint', ['users.search'], indirect=True)
class TestSearch:

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["sub_0@email.com"]},
        {'terms[]': ["sub_0@email.com"]},
        {'terms': ["sub", "email.com"]},
        {'terms[]': ["sub", "email.com"]},
        {'terms': []},   # Empty query
        {'terms[]': []},  # Empty query
        {'sort_by': "+iss,-sub"},
        {'sort_by': "+registration_datetime"},
        {'sort_by': "+email"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            user = models.User.query.get((item['sub'], item['iss']))
            asserts.match_query(item, url)
            asserts.match_user(item, user)

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["sub_0@email.com"]}
    ])
    def test_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'terms': ["sub_0@email.com"]}
    ])
    def test_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['users.get'], indirect=True)
class TestGet:

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    def test_200(self, user, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_user(response_GET.json, user)

    @mark.usefixtures('mock_accesstoken')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    def test_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["non_existing"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    def test_403(self, response_GET):
        """GET method fails 403 if not registered."""
        assert response_GET.status_code == 403


@mark.parametrize('endpoint', ['users.update'], indirect=True)
class TestUpdate:

    @mark.usefixtures('grant_logged', 'grant_accesstoken')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_204(self, introspection_email, response_POST, user):
        """POST method succeeded 204."""
        assert response_POST.status_code == 204
        assert user.email == introspection_email

    @mark.usefixtures('mock_introspection')
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_401(self, token_sub, token_iss, user, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401
        assert user == models.User.query.get((token_sub, token_iss))

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["not-registered"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('introspection_email', ["user@email.com"], indirect=True)
    def test_403(self, response_POST):
        """POST method fails 403 if not registered."""
        assert response_POST.status_code == 403


@mark.parametrize('endpoint', ['users.try_admin'], indirect=True)
class TestAdmin:
    """Tests for 'Admin' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_204(self, response_GET):
        """GET method succeeded 204."""
        assert response_GET.status_code == 204

    def test_401(self, response_GET):
        """GET method fails 401 if not authorized."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    def test_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403


@mark.parametrize('endpoint', ['users.results'], indirect=True)
class TestResults:

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_id': benchmarks[0]['id']},
        {'site_id': sites[0]['id']},
        {'flavor_id': flavors[0]['id']},
        {'tags_ids': [tag['id'] for tag in [tags[0], tags[1]]]},
        {'tags_ids[]': [tag['id'] for tag in [tags[0], tags[1]]]},
        {'upload_before': "3000-01-01"},
        {'upload_after': "1000-01-01"},
        {'filters': ["time < 11", "time > 9"]},
        {'filters[]': ["time < 11", "time > 9"]},
        {},  # Multiple reports
        {'sort_by': "+json"},
        {'sort_by': "+upload_datetime"},
        {'sort_by': "+execution_datetime"},
        {'sort_by': "+id"}
    ])
    def test_200(self, response_GET, url, user):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            result = models.Result.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_result(item, result)
            assert not result.deleted
            assert result.uploader == user

    def test_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["non_existing"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    def test_403(self, response_GET):
        """GET method fails 403 if not registered."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"},
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


# @mark.parametrize('endpoint', ['users.claims'], indirect=True)
# class TestClaims:
