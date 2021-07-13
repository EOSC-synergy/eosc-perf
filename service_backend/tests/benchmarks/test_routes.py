"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend.benchmarks import models
from pytest import mark
from tests.elements import benchmark_1, benchmark_2, benchmark_3, user_1

from . import asserts


@mark.usefixtures('session', 'db_benchmarks', 'db_users')
@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['benchmarks.Root'], indirect=True)
@mark.parametrize('db_benchmarks', indirect=True,  argvalues=[
    [benchmark_1, benchmark_2]
])
@mark.parametrize('db_users', indirect=True,  argvalues=[
    [user_1]    # User to assign the generated report
])
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
        for element in response_GET.json:
            asserts.correct_benchmark(element)
            asserts.match_query(element, url)

    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('body', [
        {'docker_image': "b1", 'docker_tag': "t3"},
        {'docker_image': "b3", 'docker_tag': "t1"},
        {'docker_image': "b3", 'docker_tag': "t1", 'description': "test"},
        {'docker_image': "b3", 'docker_tag': "t1", 'json_template': {'x': 1}}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_benchmark(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        asserts.match_benchmark_in_db(response_POST.json)

    @mark.parametrize('body', [
        {'docker_image': "b1", 'docker_tag': "t3"},
        {}  # Empty body
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('body', [
        {'docker_image': "b1", 'docker_tag': "v1.0"},
        {'docker_image': "b1", 'docker_tag': "v2.0"}
    ])
    def test_POST_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('body', [
        {'docker_image': "b1"},  # Missing docker_tag
        {'docker_tag': "t1"},  # Missing docker_image
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'db_benchmarks')
@mark.parametrize('endpoint', ['benchmarks.Search'], indirect=True)
@mark.parametrize('db_benchmarks', indirect=True,  argvalues=[
    [benchmark_1, benchmark_2, benchmark_3]
])
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
        for element in response_GET.json:
            asserts.correct_benchmark(element)
            asserts.match_search(element, url)

    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.usefixtures('session', 'benchmark')
@mark.parametrize('endpoint', ['benchmarks.Benchmark'], indirect=True)
@mark.parametrize('benchmark_id', [uuid4()], indirect=True)
class TestId:
    """Tests for 'Id' route in blueprint."""

    def test_GET_200(self, benchmark, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_benchmark(response_GET.json)
        asserts.match_benchmark(response_GET.json, benchmark)

    @mark.parametrize('benchmark__id', [uuid4()])
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', [
        {'docker_image': "new_name", 'docker_tag': "v1.0"},
        {'docker_image': "new_name"},
        {'docker_tag': "new_tag"},
        {'description': "new_description"},
        {'json_template': {"x": 2}}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_benchmark(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', [
        {'docker_tag': "new_tag"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('benchmark__id', [uuid4()])
    @mark.parametrize('body', [
        {'docker_tag': "new_tag"}
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
    def test_DELETE_204(self, benchmark, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Benchmark.query.get(benchmark.id) == None

    def test_DELETE_401(self, benchmark, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Benchmark.query.get(benchmark.id) != None

    @mark.usefixtures('grant_logged')
    def test_DELETE_403(self, benchmark, response_PUT):
        """DELETE method fails 403 if method forbidden."""
        assert response_PUT.status_code == 403
        assert models.Benchmark.query.get(benchmark.id) != None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('benchmark__id', [uuid4()])
    def test_DELETE_404(self, benchmark, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Benchmark.query.get(benchmark.id) != None
