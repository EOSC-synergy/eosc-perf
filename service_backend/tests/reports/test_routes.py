"""Functional tests using pytest-flask."""
from backend.reports.routes import ReportId
from uuid import uuid4

from backend.reports import models
from backend.results.models import Result
from backend.users.models import User
from pytest import mark
from tests.elements import result_1, result_2

from . import asserts


@mark.usefixtures('session', 'mock_token_info')
@mark.parametrize('endpoint', ['reports.Root'], indirect=True)
@mark.usefixtures('db_results')
@mark.parametrize('db_results', indirect=True, argvalues=[
    [result_1, result_2]
])
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'verdict': True},
        {'resource_type': "benchmark_report"},
        {'resource_type': "result_report"},
        {'resource_type': "site_report"},
        {'resource_type': "flavor_report"},
        {'created_before': "3000-01-01"},
        {'created_after': "2000-01-01"},
        {}  # Multiple reports
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for element in response_GET.json:
            asserts.correct_report(element)
            asserts.match_query(element, url)


@mark.usefixtures('session', 'report')
@mark.parametrize('endpoint', ['reports.ReportId'], indirect=True)
@mark.parametrize('report_id', [uuid4()], indirect=True)
@mark.parametrize('report_type', indirect=True, argvalues=[
    "benchmark",    # Tests using a report pointing a benchmark
    "result",   # Tests using a report pointing a result
    "site",     # Tests using a report pointing a site
    "flavor"    # Tests using a report pointing a flavor
])
class TestReport:
    """Tests for 'ReportId' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_GET_200(self, report, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.correct_report(response_GET.json)
        asserts.match_report(response_GET.json, report)

    def test_GET_401(self, response_GET):
        """GET method fails 401 if not authorized."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    def test_GET_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('report__id', [uuid4()])
    def test_GET_404(self, response_GET):
        """GET method fails 404 if no id found."""
        assert response_GET.status_code == 404

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, report, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Report.query.get(report.id) == None

        if report.resource_type == "result":
            resource = Result.query.get(report.resource_id)
            assert resource != None  # Is not deleted
            assert report not in resource.reports

    def test_DELETE_401(self, report, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Report.query.get(report.id) != None

        if report.resource_type == "result":
            resource = Result.query.get(report.resource_id)
            assert resource != None  # Is not deleted
            assert report in resource.reports

    @mark.usefixtures('grant_admin')
    @mark.parametrize('report__id', [uuid4()])
    def test_DELETE_404(self, report, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Report.query.get(report.id) != None

        if report.resource_type == "result":
            resource = Result.query.get(report.resource_id)
            assert resource != None  # Is not deleted
            assert report in resource.reports


@mark.usefixtures('session', 'report')
@mark.parametrize('endpoint', ['reports.Approve'], indirect=True)
@mark.parametrize('report_id', [uuid4()], indirect=True)
@mark.parametrize('report_type', indirect=True, argvalues=[
    "benchmark",    # Tests using a report pointing a benchmark
    "result",   # Tests using a report pointing a result
    "site",     # Tests using a report pointing a site
    "flavor"    # Tests using a report pointing a flavor
])
@mark.parametrize('report_verdict', indirect=True, argvalues=[
    None,   # Tests when verdict value is not initialized
    False   # Tests when verdict value initialized as False
])
class TestApprove:
    """Tests for 'Approve' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_PATCH_204(self, report, response_PATCH):
        """PATCH method succeeded 204."""
        assert response_PATCH.status_code == 204
        assert models.Report.query.get(report.id).verdict == True

    def test_PATCH_401(self, report, response_PATCH):
        """PATCH method fails 401 if not authorized."""
        assert response_PATCH.status_code == 401
        assert models.Report.query.get(report.id).verdict != True

    @mark.usefixtures('grant_logged')
    def test_PATCH_403(self, report, response_PATCH):
        """PATCH method fails 403 if forbidden."""
        assert response_PATCH.status_code == 403
        assert models.Report.query.get(report.id).verdict != True

    @mark.usefixtures('grant_admin')
    @mark.parametrize('report__id', [uuid4()])
    def test_PATCH_404(self, report, response_PATCH):
        """PATCH method fails 404 if no id found."""
        assert response_PATCH.status_code == 404
        assert models.Report.query.get(report.id).verdict != True


@mark.usefixtures('session', 'report')
@mark.parametrize('endpoint', ['reports.Reject'], indirect=True)
@mark.parametrize('report_id', [uuid4()], indirect=True)
@mark.parametrize('report_type', indirect=True, argvalues=[
    "benchmark",    # Tests using a report pointing a benchmark
    "result",   # Tests using a report pointing a result
    "site",     # Tests using a report pointing a site
    "flavor"    # Tests using a report pointing a flavor
])
@mark.parametrize('report_verdict', indirect=True, argvalues=[
    True    # Tests when verdict value initialized as True
])
class TestReject:
    """Tests for 'Approve' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_PATCH_204(self, report, response_PATCH):
        """PATCH method succeeded 204."""
        assert response_PATCH.status_code == 204
        assert models.Report.query.get(report.id).verdict == False

    def test_PATCH_401(self, report, response_PATCH):
        """PATCH method fails 401 if not authorized."""
        assert response_PATCH.status_code == 401
        assert models.Report.query.get(report.id).verdict == True

    @mark.usefixtures('grant_logged')
    def test_PATCH_403(self, report, response_PATCH):
        """PATCH method fails 403 if forbidden."""
        assert response_PATCH.status_code == 403
        assert models.Report.query.get(report.id).verdict == True

    @mark.usefixtures('grant_admin')
    @mark.parametrize('report__id', [uuid4()])
    def test_PATCH_404(self, report, response_PATCH):
        """PATCH method fails 404 if no id found."""
        assert response_PATCH.status_code == 404
        assert models.Report.query.get(report.id).verdict == True
