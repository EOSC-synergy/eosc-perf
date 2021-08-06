"""Functional tests using pytest-flask."""
from uuid import uuid4

from backend.models import models
from pytest import mark
from tests.db_instances import benchmarks, results, sites, flavors, users

from . import asserts


@mark.parametrize('endpoint', ['reports.Root'], indirect=True)
class TestRoot:
    """Tests for 'Root' route in blueprint."""

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'verdict': True},
        {'resource_type': "benchmark"},
        {'resource_type': "result"},
        {'resource_type': "site"},
        {'resource_type': "flavor"},
        {'created_before': "3000-01-01"},
        {'created_after': "2000-01-01"},
        {}  # Multiple reports
    ])
    def test_GET_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        assert response_GET.json != []
        for json in response_GET.json:
            report = models.Report.query.get(json['id'])
            asserts.match_query(json, url)
            asserts.match_report(json, report)


@mark.parametrize('endpoint', ['reports.ReportId'], indirect=True)
@mark.parametrize('resource_type_id', indirect=True, argvalues=[
    ("benchmark", benchmarks[0]['id']),
    ("result",    results[1]['id']),
    ("site",      sites[0]['id']),
    ("flavor",    flavors[0]['id'])
])
class TestReport:
    """Tests for 'ReportId' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_GET_200(self, report, response_GET):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_report(response_GET.json, report)

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

    @mark.usefixtures('grant_admin')
    def test_DELETE_204(self, report, resource_model, response_DELETE):
        """DELETE method succeeded 204."""
        assert response_DELETE.status_code == 204
        assert models.Report.query.get(report.id) is None
        assert resource_model.query.get(report.resource.id) is not None

    def test_DELETE_204(self, report, resource_model, response_DELETE):
        """DELETE method fails 401 if not authorized."""
        assert response_DELETE.status_code == 401
        assert models.Report.query.get(report.id) is not None
        assert resource_model.query.get(report.resource.id) is not None

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_DELETE_204(self, report, resource_model, response_DELETE):
        """DELETE method fails 404 if no id found."""
        assert response_DELETE.status_code == 404
        assert models.Report.query.get(report.id) is not None
        assert resource_model.query.get(report.resource.id) is not None


@mark.parametrize('endpoint', ['reports.Approve'], indirect=True)
@mark.parametrize('resource_type_id', indirect=True, argvalues=[
    ("benchmark", benchmarks[0]['id']),
    ("result",    results[1]['id']),
    ("site",      sites[0]['id']),
    ("flavor",    flavors[0]['id'])
])
@mark.parametrize('report_verdict', indirect=True, argvalues=[
    None,   # Tests when verdict value is not initialized
    False   # Tests when verdict value initialized as False
])
class TestApprove:
    """Tests for 'Approve' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_PATCH_204(self, report, report_verdict, response_PATCH):
        """PATCH method succeeded 204."""
        assert response_PATCH.status_code == 204
        assert models.Report.query.get(report.id).verdict is True

    def test_PATCH_401(self, report, report_verdict, response_PATCH):
        """PATCH method fails 401 if not authorized."""
        assert response_PATCH.status_code == 401
        assert models.Report.query.get(report.id).verdict is not True

    @mark.usefixtures('grant_logged')
    def test_PATCH_403(self, report, report_verdict, response_PATCH):
        """PATCH method fails 403 if forbidden."""
        assert response_PATCH.status_code == 403
        assert models.Report.query.get(report.id).verdict is not True

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_PATCH_404(self, report, report_verdict, response_PATCH):
        """PATCH method fails 404 if no id found."""
        assert response_PATCH.status_code == 404
        assert models.Report.query.get(report.id).verdict is not True


@mark.parametrize('endpoint', ['reports.Reject'], indirect=True)
@mark.parametrize('resource_type_id', indirect=True, argvalues=[
    ("benchmark", benchmarks[0]['id']),
    ("result",    results[1]['id']),
    ("site",      sites[0]['id']),
    ("flavor",    flavors[0]['id'])
])
@mark.parametrize('report_verdict', indirect=True, argvalues=[
    True    # Tests when verdict value initialized as True
])
class TestReject:
    """Tests for 'Approve' route in blueprint."""

    @mark.usefixtures('grant_admin')
    def test_PATCH_204(self, report, report_verdict, response_PATCH):
        """PATCH method succeeded 204."""
        assert response_PATCH.status_code == 204
        assert models.Report.query.get(report.id).verdict is False

    def test_PATCH_401(self, report, report_verdict, response_PATCH):
        """PATCH method fails 401 if not authorized."""
        assert response_PATCH.status_code == 401
        assert models.Report.query.get(report.id).verdict is True

    @mark.usefixtures('grant_logged')
    def test_PATCH_403(self, report, report_verdict, response_PATCH):
        """PATCH method fails 403 if forbidden."""
        assert response_PATCH.status_code == 403
        assert models.Report.query.get(report.id).verdict is True

    @mark.usefixtures('grant_admin')
    @mark.parametrize('request_id', [uuid4()], indirect=True)
    def test_PATCH_404(self, report, report_verdict, response_PATCH):
        """PATCH method fails 404 if no id found."""
        assert response_PATCH.status_code == 404
        assert models.Report.query.get(report.id).verdict is True

