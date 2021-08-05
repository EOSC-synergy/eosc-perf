"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend.models import models
from backend.schemas import schemas
from pytest import mark
from tests.db_instances import benchmarks, users

from . import asserts


@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['benchmarks.Root'], indirect=True)
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v1.0"},
        {'docker_image': "b1"},  # Query with 1 field
        {'docker_tag': "v1.0"},    # Query with 1 field
        {}  # All results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for json in response_GET.json:
            benchmark = models.Benchmark.query.get(json['id'])
            asserts.match_query(json, url)
            asserts.match_benchmark(json, benchmark)

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v2.0"},
        {'docker_image': "b2", 'docker_tag': "v2.0"},
        {'docker_image': "b3", 'docker_tag': "v1.0", 'description': "test"},
        {'docker_image': "b3", 'docker_tag': "v1.0", 'json_template': {'x': 1}}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        benchmark = models.Benchmark.query.get(response_POST.json['id'])
        asserts.match_benchmark(response_POST.json, benchmark)

    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v1.0"},
        {}  # Empty body
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v1.0"},
        {'docker_image': "b2", 'docker_tag': "v1.0"}
    ])
    @mark.filterwarnings("ignore:.*conflicts.*:sqlalchemy.exc.SAWarning")
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "b1"},  # Missing docker_tag
        {'docker_tag': "t1"},  # Missing docker_image
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.parametrize('endpoint', ['benchmarks.Search'], indirect=True)
class TestSearch:
    """Tests for 'Search' route in blueprint."""

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["b1"]},
        {'terms': ["b1", "v1.0"]},
        {'terms': []}
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for json in response_GET.json:
            benchmark = models.Benchmark.query.get(json['id'])
            asserts.match_search(json, url)
            asserts.match_benchmark(json, benchmark)

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['benchmarks.Benchmark'], indirect=True)
@mark.parametrize('benchmark_id', indirect=True, argvalues=[
    benchmarks[0]['id'],
    benchmarks[1]['id'],
    benchmarks[2]['id']
])
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, benchmark, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_benchmark(response_GET.json, benchmark)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "new_name", 'docker_tag': "v1.0"},
        {'docker_image': "new_name"},
        {'docker_tag': "new_tag"},
        {'description': "new_description"},
        {'json_template': {"x": 2}}
    ])
    def test_PUT_204(self, body, response_PUT, benchmark):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Benchmark().dump(benchmark)
        asserts.match_body(json, body)

    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_tag': "new_tag"}
    ])
    def test_PUT_401(self, benchmark, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert benchmark == models.Benchmark.query.get(benchmark.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_tag': "new_tag"}
    ])
    def test_PUT_404(self, benchmark, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
        assert benchmark == models.Benchmark.query.get(benchmark.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'bad_field': ""}
    ])
    def test_PUT_422(self, benchmark, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422
        assert benchmark == models.Benchmark.query.get(benchmark.id)

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, benchmark, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Benchmark.query.get(benchmark.id) is None

    def test_DELETE_401(self, benchmark, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Benchmark.query.get(benchmark.id) is not None

    @mark.usefixtures('grant_logged')
    def test_DELETE_403(self, benchmark, response_PUT):
        """DELETE method fails 403 if method forbidden."""
        assert response_PUT.status_code == 403
        assert models.Benchmark.query.get(benchmark.id) is not None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_DELETE_404(self, benchmark, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Benchmark.query.get(benchmark.id) is not None
