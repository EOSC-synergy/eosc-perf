"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend import models
from backend.schemas import schemas
from pytest import mark
from tests import asserts
from tests.db_instances import benchmarks, flavors, results, sites, tags, users

post_query = {
    'execution_datetime': "2020-05-21T10:31:00.000Z",
    'benchmark_id': benchmarks[0]['id'],
    'site_id': sites[0]['id'],
    'flavor_id': flavors[0]['id'],
    'tags_ids': [tag['id'] for tag in [tags[0], tags[1]]]
}


@mark.parametrize('endpoint', ['results.Root'], indirect=True)
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        {'docker_image': results[0]["benchmark__docker_image"]},
        {'docker_tag': results[0]["benchmark__docker_tag"]},
        {'site_name': results[0]["site__name"]},
        {'flavor_name': results[0]["flavor__name"]},
        {'tag_names': [tag for tag in results[0]["tags"]]},
        {'upload_before': "3000-01-01"},
        {'upload_after': "1000-01-01"},
        {'filters': ["time < 11", "time > 9"]},
        {}  # Multiple results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            result = models.Result.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_result(item, result)
            assert result.has_open_reports == False

    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'uploader_email': "sub_1@email.com"}  # GDPR protected

    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
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
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json['json'], body)
        result = models.Result.query.get(response_POST.json['id'])
        asserts.match_result(response_POST.json, result)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10},
        {}  # Empty body
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["non-registered"], indirect=True)
    @mark.parametrize('token_iss', ["not-existing"], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        post_query   # Resource can have multiple results
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_POST_403(self, response_POST):
        """POST method fails 403 if user not registered."""
        assert response_POST.status_code == 403

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
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
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {k: post_query[k] for k in post_query.keys() - {'execution_datetime'}},
        {k: post_query[k] for k in post_query.keys() - {'benchmark_id'}},
        {k: post_query[k] for k in post_query.keys() - {'site_id'}},
        {k: post_query[k] for k in post_query.keys() - {'flavor_id'}}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_POST_422_bad_query(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        post_query   # Resource can have multiple results
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'time': "10"}, # Time as string
        {'time': {'hours':1, 'min': 10}}, # Time as object
    ])
    def test_POST_422_bad_body(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.parametrize('endpoint', ['results.Search'], indirect=True)
class TestSearch:
    """Tests for 'Search' route in blueprint."""

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': [results[0]["benchmark__docker_image"]]},
        {'terms': [results[0]["benchmark__docker_tag"]]},
        {'terms': [results[0]["site__name"], results[0]["flavor__name"]]},
        {'terms': [tag for tag in results[0]["tags"]]},
        {'terms': []}   # Empty terms
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            result = models.Result.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_result(item, result)
            assert result.has_open_reports == False

    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['results.Result'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestResult:
    """Tests for 'Result' route in blueprint."""

    def test_GET_200(self, result, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_result(response_GET.json, result)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {'tags_ids': []}    # Delete tags
    ])
    def test_PUT_204_as_user(self, body, response_PUT, result):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Result().dump(result)
        asserts.match_edit(json, body)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {'tags_ids': []}    # Delete tags
    ])
    def test_PUT_204_as_admin(self, body, response_PUT, result):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Result().dump(result)
        asserts.match_edit(json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {}  # Empty body which would fail
    ])
    def test_PUT_401(self, result, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert result == models.Result.query.get(result.id)

    @mark.usefixtures('grant_logged', 'mock_token_info')
    @mark.parametrize('token_sub', [users[1]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[1]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {}  # Empty body which would fail
    ])
    def test_PUT_403(self, result, response_PUT):
        """PUT method fails 403 if forbidden."""
        assert response_PUT.status_code == 403
        assert result == models.Result.query.get(result.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {}  # Empty body which would fail
    ])
    def test_PUT_404(self, result, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
        assert result == models.Result.query.get(result.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_PUT_422(self, result, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422
        assert result == models.Result.query.get(result.id)

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, result, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Result.query.get(result.id) is None
        for tag in result.tags:  # But relations not deleted
            assert models.Tag.query.get(tag.id) is not None
        assert models.Benchmark.query.get(result.benchmark.id) is not None
        assert models.Site.query.get(result.site.id) is not None
        assert models.Flavor.query.get(result.flavor.id) is not None

    def test_DELETE_401(self, result, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Result.query.get(result.id) is not None
        for tag in result.tags:  # But relations not deleted
            assert models.Tag.query.get(tag.id) is not None
        assert models.Benchmark.query.get(result.benchmark.id) is not None
        assert models.Site.query.get(result.site.id) is not None
        assert models.Flavor.query.get(result.flavor.id) is not None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_DELETE_404(self, result, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Result.query.get(result.id) is not None
        for tag in result.tags:  # But relations not deleted
            assert models.Tag.query.get(tag.id) is not None
        assert models.Benchmark.query.get(result.benchmark.id) is not None
        assert models.Site.query.get(result.site.id) is not None
        assert models.Flavor.query.get(result.flavor.id) is not None


@mark.parametrize('endpoint', ['results.Uploader'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestUploader:
    """Tests for 'Uploader' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_GET_200(self, result, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_user(response_GET.json, result.created_by)

    def test_GET_401(self, response_GET):
        """GET method fails 401 if not authorized."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    def test_GET_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404


@mark.parametrize('endpoint', ['results.Report'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestReport:
    """Tests for 'Report' route in blueprint."""

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[1]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[1]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is an example report"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        report = models.Report.query.get(response_POST.json['id'])
        asserts.match_report(response_POST.json, report)

    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', ["non-registered"], indirect=True)
    @mark.parametrize('token_iss', ["not-existing"], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is an example report"}
    ])
    def test_POST_403(self, response_POST):
        """POST method fails 403 if user not registered."""
        assert response_POST.status_code == 403

    @mark.usefixtures('grant_logged')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is an example report"}
    ])
    def test_POST_404(self, response_POST):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[1]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[1]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': "This is a bad field to raise 422"}
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422
