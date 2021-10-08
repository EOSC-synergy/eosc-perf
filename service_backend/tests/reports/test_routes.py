"""Functional tests using pytest-flask."""
from backend import models
from pytest import mark
from tests import asserts


@mark.parametrize('endpoint', ['reports.list_submits'], indirect=True)
class TestListSubmits:

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'resource_type': "benchmark"},
        {'resource_type': "site"},
        {'resource_type': "flavor"},
        {'upload_before': "3000-01-01"},
        {'upload_after': "2000-01-01"},
        {},  # Multiple reports
        {'sort_by': "+upload_datetime"},
    ])
    def test_200(self, response_GET, url):
        """GET method succeeded 200."""
        assert response_GET.status_code == 200
        asserts.match_pagination(response_GET.json, url)
        assert response_GET.json['items'] != []
        for item in response_GET.json['items']:
            asserts.match_submit(item)
            asserts.match_query(item, url)

    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"},
    ])
    def test_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"},
    ])
    def test_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True,  argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


@mark.parametrize('endpoint', ['reports.list_claims'], indirect=True)
class TestListClaims:

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"},
        {'upload_after': "1000-01-01"},
        {},  # Empty query
        {'sort_by': "+upload_datetime"},
    ])
    def test_200(self, response_GET, url):
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
        {'upload_before': "3000-01-01"},
    ])
    def test_401(self, response_GET):
        """GET method fails 401 if not logged in."""
        assert response_GET.status_code == 401

    @mark.usefixtures('grant_logged')
    @mark.parametrize('query', indirect=True, argvalues=[
        {'upload_before': "3000-01-01"},
    ])
    def test_403(self, response_GET):
        """GET method fails 403 if forbidden."""
        assert response_GET.status_code == 403

    @mark.usefixtures('grant_admin')
    @mark.parametrize('query', indirect=True,  argvalues=[
        {'bad_key': "This is a non expected query key"},
        {'sort_by': "Bad sort command"}
    ])
    def test_422(self, response_GET):
        """GET method fails 422 if bad request body."""
        assert response_GET.status_code == 422


# @mark.parametrize('endpoint', ['reports.approve_claim'], indirect=True)
# class TestApproveClaim:

#     @fixture(scope='function')
#     def url(request_id, claim, query):
#         request_id = request_id if request_id else claim.id
#         return url_for('reports.approve_claim', id=request_id, **query)

#     @mark.usefixtures('grant_admin')
#     def test_204(self, response_POST, claim):
#         """POST method succeeded 200."""
#         assert response_POST.status_code == 204
#         assert claim.status.name == "approved"

#     def test_401(self, response_POST, claim):
#         """POST method fails 401 if not authorized."""
#         assert response_POST.status_code == 401
#         assert claim.status.name == "on_review"

#     @mark.usefixtures('grant_logged')
#     def test_403(self, response_POST, claim):
#         """POST method fails 403 if method forbidden."""
#         assert response_POST.status_code == 403
#         assert claim.status.name == "on_review"

#     @mark.usefixtures('grant_admin')
#     @mark.parametrize('request_id', [uuid4()], indirect=True)
#     def test_404(self, response_POST, claim):
#         """POST method fails 404 if no id found."""
#         assert response_POST.status_code == 404
#         assert claim.status.name == "on_review"


# @mark.parametrize('endpoint', ['reports.reject_claim'], indirect=True)
# @mark.parametrize('claim_id', indirect=True, argvalues=[
#     uuid4()  # Random uuid4 generation
# ])
# class TestRejectClaim:

#     @mark.usefixtures('grant_admin')
#     def test_204(self, response_POST, claim):
#         """POST method succeeded 200."""
#         assert response_POST.status_code == 204
#         assert None == models.Claim.query.get(claim.id)

#     def test_401(self, response_POST, claim):
#         """POST method fails 401 if not authorized."""
#         assert response_POST.status_code == 401
#         assert claim.status.name == "on_review"

#     @mark.usefixtures('grant_logged')
#     def test_403(self, response_POST, claim):
#         """POST method fails 403 if method forbidden."""
#         assert response_POST.status_code == 403
#         assert claim.status.name == "on_review"

#     @mark.usefixtures('grant_admin')
#     @mark.parametrize('request_id', [uuid4()], indirect=True)
#     def test_404(self, response_POST, claim):
#         """POST method fails 404 if no id found."""
#         assert response_POST.status_code == 404
#         assert claim.status.name == "on_review"
