"""Functional tests using pytest-flask."""
from datetime import date
from uuid import uuid4

from pytest import mark

from . import asserts


benchmark_1 = {'docker_image': "b1", 'docker_tag': "v1.0"}
benchmark_2 = {'docker_image': "b1", 'docker_tag': "v2.0"}

site_1 = {'name': "site1", 'address': "address1"}
site_1['description'] = "Text"
site_1['flavors'] = ["flavor1", "flavor2", "flavor3"]
site_1['flavors__description'] = "site1 flavor"

site_2 = {'name': "site2", 'address': "address2"}
site_2['description'] = "Text"
site_2['flavors'] = ["flavor1", "flavor2", "flavor3"]
site_2['flavors__description'] = "site2 flavor"

user_1 = {'sub': "sub_1", 'iss': "egi.com"}
user_1['email'] = "sub_1@email.com"


report_1 = {'verified': True, 'verdict': True}
report_1['message'] = "Benchmark report 1"
report_1['date'] = date(2020, 1, 1,)
report_1['benchmark__docker_image'] = benchmark_1['docker_image']
report_1['benchmark__docker_tag'] = benchmark_1['docker_tag']
report_1['uploader__sub'] = user_1['sub']
report_1['uploader__iss'] = user_1['iss']

report_2 = {'verified': True, 'verdict': True}
report_2['message'] = "Benchmark report 2"
report_2['benchmark__docker_image'] = benchmark_2['docker_image']
report_2['benchmark__docker_tag'] = benchmark_2['docker_tag']
report_2['uploader__sub'] = user_1['sub']
report_2['uploader__iss'] = user_1['iss']


@mark.usefixtures('session', 'db_benchmark_reports')
@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['reports.Benchmarks'], indirect=True)
@mark.parametrize('db_benchmark_reports', indirect=True, argvalues=[
    [report_1, report_2]
])
class TestBenchmarkReports:
    """Tests for 'Benchmarks' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        {'date': report_1['date']},
        {'verified': True},
        {'verdict': True},
        {'benchmark_image': report_1['benchmark__docker_image']},
        {'benchmark_tag': report_1['benchmark__docker_tag']},
        {}  # Multiple reports
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        for element in response_GET.json:
            asserts.correct_benchmark_report(element)
            asserts.match_query(element, url)

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': benchmark_1["docker_image"],
         'benchmark_tag': benchmark_1["docker_tag"]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_benchmark_report(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': benchmark_1["docker_image"],
         'benchmark_tag': benchmark_1["docker_tag"]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"},
        {'message': "New report"},  # Only message
        {}
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': "-", 'benchmark_tag': benchmark_1["docker_tag"]},
        {'benchmark_tag': "-", 'benchmark_image': benchmark_1["docker_image"]},
        
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_404(self, response_POST, url, body):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': benchmark_1["docker_image"],
         'benchmark_tag': benchmark_1["docker_tag"]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': "", 'message': "New report"},
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'benchmark_report')
@mark.parametrize('endpoint', ['reports.BenchmarkId'], indirect=True)
@mark.parametrize('report_id', [uuid4()], indirect=True)
class TestBenchmarkReport:
    """Tests for 'Report' route in blueprint."""

    def test_GET_200(self, benchmark_report, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_benchmark_report(response_GET.json)
        asserts.match_report(response_GET.json, benchmark_report)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True},
        {'verdict': True},
        {'message': "Edited report message"}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_benchmark_report(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('benchmark_report__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
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
    @mark.parametrize('benchmark_report__id', [uuid4()])
    def test_DELETE_404(self, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404


report_1 = {'verified': True, 'verdict': True}
report_1['message'] = "Result report 1"
report_1['date'] = date(2020, 1, 1,)
report_1['result__benchmark__docker_image'] = benchmark_1['docker_image']
report_1['result__benchmark__docker_tag'] = benchmark_1['docker_tag']
report_1['result__site__name'] = site_1['name']
report_1['result__flavor__name'] = site_1['flavors'][0]
report_1['uploader__sub'] = user_1['sub']
report_1['uploader__iss'] = user_1['iss']

report_2 = {'verified': True, 'verdict': True}
report_2['message'] = "Result report 2"
report_2['result__benchmark__docker_image'] = benchmark_2['docker_image']
report_2['result__benchmark__docker_tag'] = benchmark_2['docker_tag']
report_2['result__site__name'] = site_1['name']
report_2['result__flavor__name'] = site_1['flavors'][0]
report_2['uploader__sub'] = user_1['sub']
report_2['uploader__iss'] = user_1['iss']


@mark.usefixtures('session', 'db_result_reports')
@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['reports.Results'], indirect=True)
@mark.parametrize('db_result_reports', indirect=True, argvalues=[
    [report_1, report_2]
])
class TestResultReports:
    """Tests for 'Results' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        {'date': report_1['date']},
        {'verified': True},
        {'verdict': True},
        {'benchmark_image': report_1['result__benchmark__docker_image']},
        {'benchmark_tag': report_1['result__benchmark__docker_tag']},
        {'site_name': report_1['result__site__name']},
        {'flavor_name': report_1['result__flavor__name']},
        {}  # Multiple reports
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        for element in response_GET.json:
            asserts.correct_result_report(element)
            asserts.match_query(element, url)

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': benchmark_1['docker_image'],
         'benchmark_tag': benchmark_1['docker_tag'],
         'site_name': site_1['name'],
         'flavor_name': site_1['flavors'][0]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_result_report(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': benchmark_1['docker_image'],
         'benchmark_tag': benchmark_1['docker_tag'],
         'site_name': site_1['name'],
         'flavor_name': site_1['flavors'][0]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"},
        {'message': "New report"},  # Only message
        {}
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': benchmark_1['docker_image'],
         'benchmark_tag': benchmark_1['docker_tag'],
         'site_name': "non-existing-site",  # Fail by site
         'flavor_name': site_1['flavors'][0]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_404(self, response_POST, url, body):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'benchmark_image': benchmark_1['docker_image'],
         'benchmark_tag': benchmark_1['docker_tag'],
         'flavor_name': site_1['flavors'][0]}  # Missing site
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': "", 'message': "New report"},
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'result_report')
@mark.parametrize('endpoint', ['reports.ResultId'], indirect=True)
@mark.parametrize('report_id', [uuid4()], indirect=True)
class TestResultReport:
    """Tests for 'Report' route in blueprint."""

    def test_GET_200(self, result_report, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_result_report(response_GET.json)
        asserts.match_report(response_GET.json, result_report)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True},
        {'verdict': True},
        {'message': "Edited report message"}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_result_report(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('result_report__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
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
    @mark.parametrize('result_report__id', [uuid4()])
    def test_DELETE_404(self, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404


report_1 = {'verified': True, 'verdict': True}
report_1['message'] = "Site report 1"
report_1['date'] = date(2020, 1, 1,)
report_1['site__name'] = site_1['name']
report_1['site__flavors'] = site_1['flavors']
report_1['uploader__sub'] = user_1['sub']
report_1['uploader__iss'] = user_1['iss']

report_2 = {'verified': True, 'verdict': True}
report_2['message'] = "Site report 2"
report_2['date'] = date(2020, 1, 1,)
report_2['site__name'] = site_2['name']
report_2['site__flavors'] = site_2['flavors']
report_2['uploader__sub'] = user_1['sub']
report_2['uploader__iss'] = user_1['iss']


@mark.usefixtures('session', 'db_site_reports')
@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['reports.Sites'], indirect=True)
@mark.parametrize('db_site_reports', indirect=True, argvalues=[
    [report_1, report_2]
])
class TestSiteReports:
    """Tests for 'Sites' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        {'date': report_1['date']},
        {'verified': True},
        {'verdict': True},
        {'site_name': report_1['site__name']},
        {}  # Multiple reports,
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        for element in response_GET.json:
            asserts.correct_site_report(element)
            asserts.match_query(element, url)

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'site_name': site_1['name']}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_site_report(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'site_name': site_1['name']}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"},
        {'message': "New report"},  # Only message
        {}
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'site_name': "non-existing-site"}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_404(self, response_POST, url, body):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {}  # Missing site_name
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': "", 'message': "New report"},
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'site_report')
@mark.parametrize('endpoint', ['reports.SiteId'], indirect=True)
@mark.parametrize('report_id', [uuid4()], indirect=True)
class TestSiteReport:
    """Tests for 'Report' route in blueprint."""

    def test_GET_200(self, site_report, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_site_report(response_GET.json)
        asserts.match_report(response_GET.json, site_report)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True},
        {'verdict': True},
        {'message': "Edited report message"}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_site_report(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('site_report__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
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
    @mark.parametrize('site_report__id', [uuid4()])
    def test_DELETE_404(self, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404


report_1 = {'verified': True, 'verdict': True}
report_1['message'] = "Flavor report 1"
report_1['date'] = date(2020, 1, 1,)
report_1['site__name'] = site_1['name']
report_1['flavor__name'] = site_1['flavors'][0]
report_1['uploader__sub'] = user_1['sub']
report_1['uploader__iss'] = user_1['iss']

report_2 = {'verified': True, 'verdict': True}
report_2['message'] = "Flavor report 2"
report_2['date'] = date(2020, 1, 1,)
report_2['site__name'] = site_1['name']
report_2['flavor__name'] = site_1['flavors'][1]
report_2['uploader__sub'] = user_1['sub']
report_2['uploader__iss'] = user_1['iss']


@mark.usefixtures('session', 'db_flavor_reports')
@mark.usefixtures('mock_token_info')
@mark.parametrize('endpoint', ['reports.Flavors'], indirect=True)
@mark.parametrize('db_flavor_reports', indirect=True, argvalues=[
    [report_1, report_2]
])
class TestFlavorReports:
    """Tests for 'Flavors' route in blueprint."""

    @mark.parametrize('query', indirect=True, argvalues=[
        {'date': report_1['date']},
        {'verified': True},
        {'verdict': True},
        {'site_name': report_1['site__name']},
        {'flavor_name': report_1['flavor__name']},
        {}  # Multiple reports,
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        for element in response_GET.json:
            asserts.correct_flavor_report(element)
            asserts.match_query(element, url)

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'bad_key': "This is a non expected query key"}
    ])
    def test_GET_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'site_name': site_1['name'], 'flavor_name': site_1['flavors'][0]},
        {'site_name': site_1['name'], 'flavor_name': site_1['flavors'][1]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_201(self, response_POST, url, body):
        """POST method succeeded 201."""
        assert response_POST.status_code == 201
        asserts.correct_flavor_report(response_POST.json)
        asserts.match_query(response_POST.json, url)
        asserts.match_body(response_POST.json, body)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'site_name': site_1['name'], 'flavor_name': site_1['flavors'][0]}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"},
        {'message': "New report"},  # Only message
        {}
    ])
    def test_POST_401(self, response_POST):
        """POST method fails 401 if not authorized."""
        assert response_POST.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'site_name': "non-existing", 'flavor_name': site_1['flavors'][0]},
        {'flavor_name': "non-existing", 'site_name': site_1['name']},
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True, 'verdict': True, 'message': "New report"}
    ])
    def test_POST_404(self, response_POST, url, body):
        """POST method fails 404 if no id found."""
        assert response_POST.status_code == 404

    @mark.usefixtures('grant_logged')
    @mark.parametrize('token_sub', [user_1['sub']], indirect=True)
    @mark.parametrize('token_iss', [user_1['iss']], indirect=True)
    @mark.parametrize('query', indirect=True, argvalues=[
        {'flavor_name': site_1['flavors'][0]},  # Missing site_name
        {'site_name': site_1['name']},  # Missing flavor_name
        {}
    ])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'bad_field': "", 'message': "New report"},
        {}  # Empty body
    ])
    def test_POST_422(self, response_POST):
        """POST method fails 422 if missing required."""
        assert response_POST.status_code == 422


@mark.usefixtures('session', 'flavor_report')
@mark.parametrize('endpoint', ['reports.FlavorId'], indirect=True)
@mark.parametrize('report_id', [uuid4()], indirect=True)
class TestFlavorReport:
    """Tests for 'Report' route in blueprint."""

    def test_GET_200(self, flavor_report, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_flavor_report(response_GET.json)
        asserts.match_report(response_GET.json, flavor_report)

    @mark.usefixtures('grant_admin')
    @mark.parametrize('body', indirect=True, argvalues=[
        {'verified': True},
        {'verdict': True},
        {'message': "Edited report message"}
    ])
    def test_PUT_204(self, response_PUT, response_GET, body):
        """PUT method succeeded 204."""
        assert response_PUT.status_code == 204
        assert response_GET.status_code == 200
        asserts.correct_flavor_report(response_GET.json)
        asserts.match_body(response_GET.json, body)

    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
    ])
    def test_PUT_401(self, response_PUT):
        """PUT method fails 401 if not authorized."""
        assert response_PUT.status_code == 401

    @mark.usefixtures('grant_admin')
    @mark.parametrize('flavor_report__id', [uuid4()])
    @mark.parametrize('body', indirect=True, argvalues=[
        {'message': "Edited report message"}
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
    @mark.parametrize('flavor_report__id', [uuid4()])
    def test_DELETE_404(self, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
