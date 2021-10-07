"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend import models
from backend.schemas import schemas
from pytest import mark
from tests import asserts
from tests.db_instances import benchmarks, users


@mark.parametrize('endpoint', ['benchmarks.list'], indirect=True)
class TestList:

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v1.0"},
        {'docker_image': "b1"},  # Query with 1 field
        {'docker_tag': "v1.0"},  # Query with 1 field
        {},  # All results
        {'sort_by': "+docker_image,+docker_tag"},
        {'sort_by': "+upload_datetime"},
        {'sort_by': "+id"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            benchmark = models.Benchmark.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_benchmark(item, benchmark)
            assert benchmark.status.name == "approved"

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['benchmarks.create'], indirect=True)
class TestCreate:

    @mark.usefixtures('grant_logged', 'mock_docker_registry')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v2.0", 'json_schema': {'x': 1}},
        {'docker_image': "b2", 'docker_tag': "v2.0", 'json_schema': {'x': 1},
         'description': "This is a long benchmark description"},
    ])
    def test_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        benchmark = models.Benchmark.query.get(response_POST.json['id'])
        asserts.match_benchmark(response_POST.json, benchmark)
        asserts.submit_notification(benchmark.submit_report)

    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v2.0",
         'json_schema': {'x': 1}},
        {}  # Empty body
    ])
    def test_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_accesstoken', 'mock_docker_registry')
    @mark.parametrize('token_sub', ["non-registered"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'docker_image': "b1", 'docker_tag': "v2.0", 'json_schema': {'x': 1}}
    ])
    def test_403(self, response_POST):
        """POST method fails 403 if user not registered."""
        assert response_POST.status_code == 403

    @mark.usefixtures('grant_logged', 'mock_docker_registry')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "b1", 'docker_tag': "v1.0", 'json_schema': {'x': 1}},
        {'docker_image': "b2", 'docker_tag': "v1.0", 'json_schema': {'x': 1}}
    ])
    @mark.filterwarnings("ignore:.*conflicts.*:sqlalchemy.exc.SAWarning")
    def test_409(self, response_POST):
        """POST method fails 409 if resource already exists."""
        assert response_POST.status_code == 409

    @mark.usefixtures('grant_logged', 'mock_docker_registry')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "_", 'docker_tag': "_", 'json_schema': {'type': 'x'}},
        {'docker_image': "b1", 'docker_tag': "v1.0"},   # Missing json_schema
        {'docker_image': "b1", 'json_schema': {'x': 1}},  # Missing docker_tag
        {'docker_tag': "v1.0", 'json_schema': {'x': 1}},  # Missing docker_im
        {'docker_image': "b1"},
        {'docker_tag': "t1"},
        {'json_schema': {'x': 1}},
        {}  # Empty body
    ])
    def test_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.parametrize('endpoint', ['benchmarks.search'], indirect=True)
class TestSearch:

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': ["b1"]},
        {'terms[]': ["b1"]},
        {'terms': ["b1", "v1.0"]},
        {'terms[]': ["b1", "v1.0"]},
        {'terms': []},    # Empty query
        {'terms[]': []},  # Empty query
        {'sort_by': "+docker_image,+docker_tag"},
        {'sort_by': "+upload_datetime"},
        {'sort_by': "+id"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            benchmark = models.Benchmark.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_benchmark(item, benchmark)
            assert benchmark.status.name == "approved"

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['benchmarks.get'], indirect=True)
@mark.parametrize('benchmark_id', indirect=True, argvalues=[
    benchmarks[0]['id'],
    benchmarks[1]['id'],
    benchmarks[2]['id']
])
class TestGet:

    def test_200(self, benchmark, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_benchmark(response_GET.json, benchmark)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404


@mark.parametrize('endpoint', ['benchmarks.update'], indirect=True)
@mark.parametrize('benchmark_id', indirect=True, argvalues=[
    benchmarks[0]['id'],
    benchmarks[1]['id'],
    benchmarks[2]['id']
])
class TestUpdate:

    @mark.usefixtures('grant_admin', 'mock_docker_registry')
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "new_name", 'docker_tag': "v1.0",
         'json_schema': {"x": 2}},
    ])
    def test_204(self, body, response_PUT, benchmark):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Benchmark().dump(benchmark)
        asserts.match_body(json, body)

    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_tag': "new_tag"}
    ])
    def test_401(self, benchmark, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert benchmark == models.Benchmark.query.get(benchmark.id)

    @mark.usefixtures('grant_admin', 'mock_docker_registry')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'docker_image': "new_name", 'docker_tag': "v1.0",
         'json_schema': {"x": 2}},
    ])
    def test_404(self, benchmark, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
        assert benchmark == models.Benchmark.query.get(benchmark.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True,  argvalues=[
        {'bad_field': ""}
    ])
    def test_422(self, benchmark, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422
        assert benchmark == models.Benchmark.query.get(benchmark.id)


@mark.parametrize('endpoint', ['benchmarks.delete'], indirect=True)
@mark.parametrize('benchmark_id', indirect=True, argvalues=[
    benchmarks[0]['id'],
    benchmarks[1]['id'],
    benchmarks[2]['id']
])
class TestDelete:

    @mark.usefixtures('grant_admin')
    def test_204(self, benchmark, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Benchmark.query.get(benchmark.id) is None

    def test_401(self, benchmark, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Benchmark.query.get(benchmark.id) is not None

    @mark.usefixtures('grant_logged')
    def test_403(self, benchmark, response_PUT):
        """DELETE method fails 403 if method forbidden."""
        assert response_PUT.status_code == 403
        assert models.Benchmark.query.get(benchmark.id) is not None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, benchmark, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Benchmark.query.get(benchmark.id) is not None


@mark.parametrize('endpoint', ['benchmarks.approve'], indirect=True)
@mark.parametrize('benchmark_id', indirect=True, argvalues=[
    benchmarks[3]['id'],
])
class TestApprove:

    @mark.usefixtures('grant_admin')
    def test_204(self, response_POST, benchmark):
        """POST method succeeded 200."""
        assert response_POST.status_code == 204
        assert benchmark.status.name == "approved"

    def test_401(self, response_POST, benchmark):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401
        assert benchmark.status.name == "on_review"

    @mark.usefixtures('grant_logged')
    def test_403(self, response_POST, benchmark):
        """POST method fails 403 if method forbidden."""
        assert response_POST.status_code == 403
        assert benchmark.status.name == "on_review"

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, response_POST, benchmark):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404
        assert benchmark.status.name == "on_review"


@mark.parametrize('endpoint', ['benchmarks.reject'], indirect=True)
@mark.parametrize('benchmark_id', indirect=True, argvalues=[
    benchmarks[4]['id'],
])
class TestReject:

    @mark.usefixtures('grant_admin')
    def test_204(self, response_POST, benchmark):
        """POST method succeeded 200."""
        assert response_POST.status_code == 204
        assert benchmark is None

    def test_401(self, response_POST, benchmark):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401
        assert benchmark.status.name == "on_review"

    @mark.usefixtures('grant_logged')
    def test_403(self, response_POST, benchmark):
        """POST method fails 403 if method forbidden."""
        assert response_POST.status_code == 403
        assert benchmark.status.name == "on_review"

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, response_POST, benchmark):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404
        assert benchmark.status.name == "on_review"
