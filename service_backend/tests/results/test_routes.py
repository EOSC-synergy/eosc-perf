"""Functional tests using pytest-flask."""
from uuid import uuid4
from tests.reports import asserts as report_asserts

from backend.results import models
from pytest import mark
from tests.elements import (benchmark_1, flavor_1, result_1, result_2, site_1,
                            tag_1, tag_2, tag_3, user_1, user_2)

from . import asserts

post_query = {
    'benchmark_id': benchmark_1['id'],
    'site_id': site_1['id'],
    'flavor_id': flavor_1['id'],
    'tags_ids': [tag['id'] for tag in [tag_1, tag_2]]
}


@mark.usefixtures('session', 'db_results')
@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['results.Root'], indirect=True)
@mark.parametrize('db_results', indirect=True, argvalues=[
    [result_1, result_2]
])
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        # TODO: Json field instance
        {'docker_image': result_1["benchmark__docker_image"]},
        {'docker_tag': result_1["benchmark__docker_tag"]},
        {'site_name': result_1["site__name"]},
        {'flavor_name': result_1["flavor__name"]},
        {'tag_names': [tag['name'] for tag in result_1["tags"]]},
        {'upload_before': "3000-01-01"},
        {'upload_after': "2000-01-01"},
        {}  # Multiple results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_result(element)
            asserts.match_query(element, url)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'uploader_email': "sub_1@email.com"}  # GDPR protected

    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [result_1['uploader__sub']], indirect=True)
    @mark.parametrize('token_iss', [result_1['uploader__iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        post_query,  # Resource can have multiple results
        {k: post_query[k] for k in post_query.keys() - {'tags_ids'}}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_result(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json['json'], body)
        asserts.match_result_in_db(response_POST.json)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10},
        {}  # Empty body
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [result_1['uploader__sub']], indirect=True)
    @mark.parametrize('token_iss', [result_1['uploader__iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {**post_query, **{'benchmark_id': uuid4()}},  # Not existing
        {**post_query, **{'site_id': uuid4()}},     # Not existing
        {**post_query, **{'flavor_id': uuid4()}},   # Not existing
        {**post_query, **{'tags_ids': [uuid4(), uuid4()]}}  # Not existing
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_POST_404(self, response_POST, url, body):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [result_1['uploader__sub']], indirect=True)
    @mark.parametrize('token_iss', [result_1['uploader__iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {k: post_query[k] for k in post_query.keys() - {'benchmark_id'}},
        {k: post_query[k] for k in post_query.keys() - {'site_id'}},
        {k: post_query[k] for k in post_query.keys() - {'flavor_id'}}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'db_results')
@mark.parametrize('endpoint', ['results.Search'], indirect=True)
@mark.parametrize('db_results', indirect=True, argvalues=[
    [result_1, result_2]
])
class TestSearch:
    """Tests for 'Search' route in blueprint."""

    @mark.parametrize('query', indirect=True,  argvalues=[
        # TODO: {'terms': ["time"]},
        {'terms': [result_1["benchmark__docker_image"]]},
        {'terms': [result_1["benchmark__docker_tag"]]},
        {'terms': [result_1["site__name"], result_1["flavor__name"]]},
        {'terms': [tag['name'] for tag in result_1["tags"]]},
        {'terms': []}   # Empty terms
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_result(element)
            asserts.match_search(element, url)

    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.usefixtures('session')
@mark.usefixtures('db_tags', 'result')
@mark.parametrize('db_tags', indirect=True, argvalues=[
    [tag_1, tag_2, tag_3]
])
@mark.parametrize('endpoint', ['results.Result'], indirect=True)
@mark.parametrize('result_id', [uuid4()], indirect=True)
@mark.parametrize('benchmark__docker_image', [benchmark_1['docker_image']])
@mark.parametrize('benchmark__docker_tag', [benchmark_1['docker_tag']])
@mark.parametrize('site__name', [site_1['name']])
@mark.parametrize('site__id', [site_1['id']])
@mark.parametrize('flavor__name', [flavor_1['name']])
@mark.parametrize('flavor__site_id', [site_1['id']])
@mark.parametrize('user__sub', [user_1['sub']])
@mark.parametrize('user__iss', [user_1['iss']])
@mark.parametrize('result__tags', [[tag_1, tag_2]])
class TestResult:
    """Tests for 'Result' route in blueprint."""

    def test_GET_200(self, result, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_result(response_GET.json)
        asserts.match_result(response_GET.json, result)

    @mark.parametrize('result__id', [uuid4()])
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_logged', 'mock_token_info')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tag_3, tag_2]]},
        {'tags_ids': []}    # Delete tags
    ])
    def test_PUT_204_as_user(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_result(response_GET.json)
        asserts.match_edit(response_GET.json, body)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tag_3, tag_2]]},
        {'tags_ids': []}    # Delete tags
    ])
    def test_PUT_204_as_admin(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_result(response_GET.json)
        asserts.match_edit(response_GET.json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tag_3, tag_2]]},
        {}  # Empty body which would fail
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tag_3, tag_2]]},
        {}  # Empty body which would fail
    ])
    def test_PUT_403(self, response_PUT):
        """PUT method fails 403 if forbidden."""
        assert response_PUT.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('result__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tag_3, tag_2]]},
        {}  # Empty body which would fail
    ])
    def test_PUT_404(self, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_PUT_422(self, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, result, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Result.query.get(result.id) is None

    def test_DELETE_401(self, result, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Result.query.get(result.id) is not None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('result__id', [uuid4()])
    def test_DELETE_404(self, result, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Result.query.get(result.id) is not None


@mark.usefixtures('session', 'result', 'user')
@mark.parametrize('endpoint', ['results.Uploader'], indirect=True)
@mark.parametrize('result_id', [uuid4()], indirect=True)
@mark.parametrize('user__sub', [user_1['sub']])
@mark.parametrize('user__iss', [user_1['iss']])
@mark.parametrize('user__email', [user_1['email']])
class TestUploader:
    """Tests for 'Uploader' route in blueprint."""

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
    @mark.parametrize('result__id', [uuid4()])
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404


@mark.usefixtures('session', 'result', 'db_users')
@mark.parametrize('endpoint', ['results.Report'], indirect=True)
@mark.parametrize('result_id', [uuid4()], indirect=True)
@mark.parametrize('user__sub', [user_1['sub']])
@mark.parametrize('user__iss', [user_1['iss']])
@mark.parametrize('user__email', [user_1['email']])
@mark.parametrize('db_users', indirect=True, argvalues=[
    [user_1, user_2]
])
class TestReport:
    """Tests for 'Report' route in blueprint."""

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_2['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_2['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is an example report"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        report_asserts.correct_report(response_POST.json)
        report_asserts.match_body(response_POST.json, body)
        report_asserts.match_report_in_db(response_POST.json)

    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('result__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is an example report"}
    ])
    def test_POST_404(self, response_POST):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_2['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_2['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': "This is a bad field to raise 422"}
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422
