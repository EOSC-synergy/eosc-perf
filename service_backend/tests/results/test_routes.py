"""Functional tests using pytest-flask."""
from uuid import uuid4

from pytest import mark
from . import asserts


benchmark_1 = {'docker_image': "b1", 'docker_tag': "latest"}
benchmark_2 = {'docker_image': "b1", 'docker_tag': "v1.0"}
benchmark_3 = {'docker_image': "b2", 'docker_tag': "latest"}

site_1 = {'name': "site1", 'address': "address1"}
site_1['description'] = "Text"
site_1['flavors'] = ["flavor1", "flavor2", "flavor3"]
site_1['flavors__description'] = "site1 flavor"

site_2 = {'name': "site2", 'address': "address2"}
site_2['description'] = "Text"
site_2['flavors'] = ["flavor1", "flavor2", "flavor3"]
site_2['flavors__description'] = "site2 flavor"

tag_1 = {'name': "tag1", 'description': "Description"}
tag_2 = {'name': "tag2", 'description': "Description"}

result_1 = {'json': {'time': 10}}
result_1['uploader__sub'] = "sub_1"
result_1['uploader__iss'] = "egi.com"
result_1['uploader__email'] = "sub_1@email.com"
result_1['benchmark__docker_image'] = benchmark_1['docker_image']
result_1['site__name'] = site_1['name']
result_1['flavor__name'] = site_1['flavors'][0]
result_1['tags'] = [tag_1, tag_2]

result_2 = {'json': {'time': 12}}
result_2['uploader__sub'] = "sub_1"
result_2['benchmark__docker_image'] = benchmark_1['docker_image']
result_2['site__name'] = site_2['name']
result_2['flavor__name'] = site_2['flavors'][0]
result_2['tags'] = [tag_1, tag_2]


post_query = {
    'benchmark_image': benchmark_1['docker_image'],
    'benchmark_tag': benchmark_1['docker_tag'],
    'site_name': site_1['name'],
    'flavor_name': site_1['flavors'][0],
    'tags': [tag['name'] for tag in result_1['tags']]
}


@mark.usefixtures('session', 'db_results')
@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['results.Root'], indirect=True)
@mark.parametrize('db_results', indirect=True, argvalues=[
    [result_1, result_2]
])
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': "b1"},
        {'site_name': "s1"},
        {'flavor_name': "f1"},
        {'tags': ["tag1", "tag2"]},
        {}  # Multiple results
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        for element in response_GET.json:
            asserts.correct_result(element)
            asserts.match_query(element, url)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': "b1"}
    ])
    def test_GET_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
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
        {k: post_query[k] for k in post_query.keys() - {'tags'}}  # No tags
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
        {**post_query, **{'benchmark_image': "not-existing"}},
        {**post_query, **{'site_name': "not-existing"}},
        {**post_query, **{'flavor_name': "not-existing"}},
        {**post_query, **{'tags': ["tag1", "tag2", "not-existing"]}}
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
        {k: post_query[k] for k in post_query.keys() - {'benchmark_image'}},
        {k: post_query[k] for k in post_query.keys() - {'benchmark_tag'}},
        {k: post_query[k] for k in post_query.keys() - {'site_name'}},
        {k: post_query[k] for k in post_query.keys() - {'flavor_name'}}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session')
@mark.usefixtures('db_benchmarks', 'db_sites', 'db_tags', 'result')
@mark.parametrize('db_benchmarks', indirect=True, argvalues=[
    [benchmark_1, benchmark_2, benchmark_3]
])
@mark.parametrize('db_sites', indirect=True, argvalues=[
    [site_1, site_2]
])
@mark.parametrize('db_tags', indirect=True, argvalues=[
    [tag_1, tag_2]
])
@mark.parametrize('endpoint', ['results.Result'], indirect=True)
@mark.parametrize('result_id', [uuid4()], indirect=True)
@mark.parametrize('result', indirect=True, argvalues=[
    result_1,
    result_2
])
class TestResult:
    """Tests for 'Result' route in blueprint."""

    def test_GET_200(self, result, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_result(response_GET.json)
        asserts.match_result(response_GET.json, result)

    @mark.parametrize('result__id', [uuid4()], indirect=True)
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'benchmark_image': "b2"},
        {'benchmark_tag': "v1.0"},
        {'site_name': "site2"},
        {'flavor_name': "flavor3"},
        {'tags': ["tag1"]}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_result(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.usefixtures('grant_logged')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'benchmark_image': "b2"},
        {}  # Empty body which would fail
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('result__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'benchmark_image': "b2"},
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
    def test_DELETE_204(self, response_DELETE, response_GET):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert response_GET.status_code == 404

    def test_DELETE_401(self, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('result__id', [uuid4()])
    def test_DELETE_404(self, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
