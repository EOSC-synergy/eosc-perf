"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend import models
from backend.schemas import schemas
from pytest import mark
from tests import asserts
from tests.db_instances import benchmarks, flavors, results, sites, tags, users

post_query = {
    'execution_datetime': "2020-05-21T10:31:00.000+03:00",
    'benchmark_id': benchmarks[0]['id'],
    'flavor_id': flavors[0]['id'],
    'tags_ids': [tag['id'] for tag in [tags[0], tags[1]]]
}


@mark.parametrize('endpoint', ['results.list'], indirect=True)
class TestList:

    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_id': benchmarks[0]['id']},
        {'site_id': flavors[0]['site__id']},
        {'flavor_id': flavors[0]['id']},
        {'tags_ids': [tag['id'] for tag in [tags[0], tags[1]]]},
        {'tags_ids[]': [tag['id'] for tag in [tags[0], tags[1]]]},
        {'upload_before': "3000-01-01"},
        {'upload_after': "1000-01-01"},
        {'filters': ["type == AMD"]},
        {'filters': ["cpu == True"]},
        {'filters': ["time < 11", "time > 9"]},
        {'filters[]': ["time < 11", "time > 9"]},
        {},  # Multiple reports
        {'sort_by': "+upload_datetime"},
        {'sort_by': "+execution_datetime"},
        {'sort_by': "+benchmark_name"},
        {'sort_by': "+site_name,+flavor_name"},
        {'sort_by': "+json.type"},
        {'sort_by': "+json.time"},
        {'sort_by': "+json.s1.t2"},
        {'sort_by': "+json.other"},
        {'sort_by': "+id"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            result = models.Result.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_result(item, result)
            assert not result.deleted

    @mark.parametrize('query', indirect=True, argvalues=[
        {'filters': ["time <> a"]},
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"},
        {'uploader_email': "sub_1@email.com"}  # GDPR protected
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['results.create'], indirect=True)
class TestCreate:

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
    def test_201(self, response_POST, url, body):
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
    def test_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["non-registered"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        post_query   # Resource can have multiple results
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_403(self, response_POST):
        """POST method fails 403 if user not registered."""
        assert response_POST.status_code == 403

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {**post_query, **{'benchmark_id': uuid4()}},  # Not existing
        {**post_query, **{'flavor_id': uuid4()}},   # Not existing
        {**post_query, **{'tags_ids': [uuid4(), uuid4()]}}  # Not existing
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_404(self, response_POST, url, body):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {k: post_query[k] for k in post_query.keys() - {'execution_datetime'}},
        {k: post_query[k] for k in post_query.keys() - {'benchmark_id'}},
        {k: post_query[k] for k in post_query.keys() - {'flavor_id'}},
        {**post_query, 'execution_datetime': "9999-01-01T00:00:00.000Z"}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'json_field_1': "Content", 'time': 10}
    ])
    def test_422_bad_query(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        post_query   # Resource can have multiple results
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'time': "10"},  # Time as string
        {'time': {'hours': 1, 'min': 10}},  # Time as object
    ])
    def test_422_bad_body(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.parametrize('endpoint', ['results.search'], indirect=True)
class TestSearch:

    @mark.parametrize('query', indirect=True,  argvalues=[
        {'terms': [benchmarks[0]["docker_image"]]},
        {'terms[]': [benchmarks[0]["docker_image"]]},
        {'terms': [benchmarks[0]["docker_tag"]]},
        {'terms[]': [benchmarks[0]["docker_tag"]]},
        {'terms': [sites[0]["name"], flavors[0]["name"]]},
        {'terms[]': [sites[0]["name"], flavors[0]["name"]]},
        {'terms': [tag["name"] for tag in tags[0:1]]},
        {'terms[]': [tag["name"] for tag in tags[0:4:2]]},
        {'terms': []},    # Empty terms
        {'terms[]': []},  # Empty terms
        {'sort_by': "+json"},
        {'sort_by': "+upload_datetime"},
        {'sort_by': "+execution_datetime"},
        {'sort_by': "+benchmark_name"},
        {'sort_by': "+site_name,+flavor_name"},
        {'sort_by': "+id"}
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            result = models.Result.query.get(item['id'])
            asserts.match_query(item, url)
            asserts.match_result(item, result)
            assert not result.deleted

    @mark.parametrize('query', [
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"},
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['results.get'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestGet:

    def test_200(self, result, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_result(response_GET.json, result)

    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404


@mark.parametrize('endpoint', ['results.delete'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestDelete:

    @mark.usefixtures('grant_admin')
    def test_204(self, result, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Result.query.get(result.id) is None
        for tag in result.tags:  # But relations not deleted
            assert models.Tag.query.get(tag.id) is not None
        assert models.Benchmark.query.get(result.benchmark.id) is not None
        assert models.Site.query.get(result.site.id) is not None
        assert models.Flavor.query.get(result.flavor.id) is not None

    def test_401(self, result, response_DELETE):
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
    def test_404(self, result, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Result.query.get(result.id) is not None
        for tag in result.tags:  # But relations not deleted
            assert models.Tag.query.get(tag.id) is not None
        assert models.Benchmark.query.get(result.benchmark.id) is not None
        assert models.Site.query.get(result.site.id) is not None
        assert models.Flavor.query.get(result.flavor.id) is not None


@mark.parametrize('endpoint', ['results.claim'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestClaim:

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[1]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[1]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is a claim example"}
    ])
    def test_201(self, response_POST, url, body, result_id):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)
        assert models.Result._claim_report_class.query.\
            filter_by(resource_id=result_id).first()

    def test_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_accesstoken')
    @mark.parametrize('token_sub', ["non-registered"], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is an example report"}
    ])
    def test_403(self, response_POST):
        """POST method fails 403 if user not registered."""
        assert response_POST.status_code == 403

    @mark.usefixtures('grant_logged')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "This is an example report"}
    ])
    def test_404(self, response_POST):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[1]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[1]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': "This is a bad field to raise 422"}
    ])
    def test_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.parametrize('endpoint', ['results.update_tags'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestUpdateTags:

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {'tags_ids': []}    # Delete tags
    ])
    def test_204_as_user(self, body, response_PUT, result):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Result().dump(result)
        asserts.match_edit(json, body)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {'tags_ids': []}    # Delete tags
    ])
    def test_204_as_admin(self, body, response_PUT, result):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        json = schemas.Result().dump(result)
        asserts.match_edit(json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {}  # Empty body which would fail
    ])
    def test_401(self, result, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401
        assert result == models.Result.query.get(result.id)

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[1]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[1]['iss']], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {}  # Empty body which would fail
    ])
    def test_403(self, result, response_PUT):
        """PUT method fails 403 if forbidden."""
        assert response_PUT.status_code == 403
        assert result == models.Result.query.get(result.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('body', indirect=True, argvalues=[
        {'tags_ids': [tag['id'] for tag in [tags[2], tags[1]]]},
        {}  # Empty body which would fail
    ])
    def test_404(self, result, response_PUT):
        """PUT method fails 404 if no id found."""
        assert response_PUT.status_code == 404
        assert result == models.Result.query.get(result.id)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': ""}
    ])
    def test_422(self, result, response_PUT):
        """PUT method fails 422 if bad request body."""
        assert response_PUT.status_code == 422
        assert result == models.Result.query.get(result.id)


@mark.parametrize('endpoint', ['results.list_claims'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[3]['id']
])
class TestListClaims:

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[0]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[0]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"},
        {'upload_after': "1000-01-01"},
        {},  # Empty query
        {'sort_by': "+upload_datetime"},
    ])
    def test_200_as_user(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            asserts.match_query(item, url)
            item.pop('uploader')
            item.pop('resource_type')
            assert models.Result._claim_report_class.query\
                .filter_by(**item)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"},
        {'upload_after': "1000-01-01"},
        {},  # Empty query
        {'sort_by': "+upload_datetime"},
    ])
    def test_200_as_admin(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            asserts.match_query(item, url)
            item.pop('uploader')
            item.pop('resource_type')
            assert models.Result._claim_report_class.query.\
                filter_by(**item).first()

    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"}
    ])
    def test_401(self, response_GET):
        """GET method fails 401 if not authorized."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [users[1]['sub']], indirect=True)
    @mark.parametrize('token_iss', [users[1]['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"}
    ])
    def test_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"}
    ])
    def test_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'unknown-argument': ""}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['results.get_uploader'], indirect=True)
@mark.parametrize('result_id', indirect=True, argvalues=[
    results[0]['id'],
    results[1]['id']
])
class TestGetUploader:

    @mark.usefixtures('grant_admin')
    def test_200(self, result, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_user(response_GET.json, result.uploader)

    def test_401(self, response_GET):
        """GET method fails 401 if not authorized."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    def test_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404
