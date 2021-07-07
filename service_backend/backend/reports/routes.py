"""Report routes."""
from backend.extensions import auth
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from backend.database import NoResultFound, MultipleResultsFound

from . import models, schemas

blp = Blueprint(
    'reports', __name__, description='Operations on reports'
)


@blp.route('/benchmarks')
class Benchmarks(MethodView):

    @auth.admin_required()
    @blp.arguments(schemas.BReportQueryArgs, location='query')
    @blp.response(200, schemas.ReportForBenchmark(many=True))
    def get(self, args):
        """Filters and list benchmark reports."""
        return models.BenchmarkReport.filter_by(**args)

    @auth.login_required()
    @blp.arguments(schemas.BenchmarkQueryArgs, location='query')
    @blp.arguments(schemas.ReportForBenchmark)
    @blp.response(201, schemas.ReportForBenchmark)
    def post(self, query_args, json):
        """Creates a new benchmark report."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        try:
            return models.BenchmarkReport.create(
                uploader_sub=token_info['body']['sub'],
                uploader_iss=token_info['body']['iss'],
                **{**query_args, **json}
            )
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(422, "Benchmark not unique")


@blp.route('/benchmarks/<uuid:report_id>')
class BenchmarkId(MethodView):

    @auth.admin_required()
    @blp.response(200, schemas.ReportForBenchmark)
    def get(self, report_id):
        """Retrieves benchmark report details."""
        return models.BenchmarkReport.get_by_id(report_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditReport, as_kwargs=True)
    @blp.response(204)
    def put(self, report_id, **kwargs):
        """Updates an existing benchmark report."""
        models.BenchmarkReport.get_by_id(report_id).update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, report_id):
        """Deletes an existing benchmark report."""
        models.BenchmarkReport.get_by_id(report_id).delete()


@blp.route('/results')
class Results(MethodView):

    @auth.admin_required()
    @blp.arguments(schemas.RReportQueryArgs, location='query')
    @blp.response(200, schemas.ReportForResult(many=True))
    def get(self, args):
        """Filters and list result reports."""
        return models.ResultReport.filter_by(**args)

    @auth.login_required()
    @blp.arguments(schemas.ResultQueryArgs, location='query')
    @blp.arguments(schemas.ReportForResult)
    @blp.response(201, schemas.ReportForResult)
    def post(self, query_args, json):
        """Creates a new result report."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        try:
            return models.ResultReport.create(
                uploader_sub=token_info['body']['sub'],
                uploader_iss=token_info['body']['iss'],
                **{**query_args, **json}
            )
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(422, "Result not unique")


@blp.route('/results/<uuid:report_id>')
class ResultId(MethodView):

    @auth.admin_required()
    @blp.response(200, schemas.ReportForResult)
    def get(self, report_id):
        """Retrieves result report details."""
        return models.ResultReport.get_by_id(report_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditReport, as_kwargs=True)
    @blp.response(204)
    def put(self, report_id, **kwargs):
        """Updates an existing result report."""
        models.ResultReport.get_by_id(report_id).update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, report_id):
        """Deletes an existing result report."""
        models.ResultReport.get_by_id(report_id).delete()


@blp.route('/sites')
class Sites(MethodView):

    @auth.admin_required()
    @blp.arguments(schemas.SReportQueryArgs, location='query')
    @blp.response(200, schemas.ReportForSite(many=True))
    def get(self, args):
        """Filters and list site reports."""
        return models.SiteReport.filter_by(**args)

    @auth.login_required()
    @blp.arguments(schemas.SiteQueryArgs, location='query')
    @blp.arguments(schemas.ReportForSite)
    @blp.response(201, schemas.ReportForSite)
    def post(self, query_args, json):
        """Creates a new site report."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        try:
            return models.SiteReport.create(
                uploader_sub=token_info['body']['sub'],
                uploader_iss=token_info['body']['iss'],
                **{**query_args, **json}
            )
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(422, "Site not unique")


@blp.route('/sites/<uuid:report_id>')
class SiteId(MethodView):

    @auth.admin_required()
    @blp.response(200, schemas.ReportForSite)
    def get(self, report_id):
        """Retrieves site report details."""
        return models.SiteReport.get_by_id(report_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditReport, as_kwargs=True)
    @blp.response(204)
    def put(self, report_id, **kwargs):
        """Updates an existing site report."""
        models.SiteReport.get_by_id(report_id).update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, report_id):
        """Deletes an existing site report."""
        models.SiteReport.get_by_id(report_id).delete()


@blp.route('/flavors')
class Flavors(MethodView):

    @auth.admin_required()
    @blp.arguments(schemas.FReportQueryArgs, location='query')
    @blp.response(200, schemas.ReportForFlavor(many=True))
    def get(self, args):
        """Filters and list site reports."""
        return models.FlavorReport.filter_by(**args)

    @auth.login_required()
    @blp.arguments(schemas.FlavorQueryArgs, location='query')
    @blp.arguments(schemas.ReportForFlavor)
    @blp.response(201, schemas.ReportForFlavor)
    def post(self, query_args, json):
        """Creates a new flavor report."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        try:
            return models.FlavorReport.create(
                uploader_sub=token_info['body']['sub'],
                uploader_iss=token_info['body']['iss'],
                **{**query_args, **json}
            )
        except NoResultFound:
            abort(404)
        except MultipleResultsFound:
            abort(422, "Flavor not unique")


@blp.route('/flavors/<uuid:report_id>')
class FlavorId(MethodView):

    @auth.admin_required()
    @blp.response(200, schemas.ReportForFlavor)
    def get(self, report_id):
        """Retrieves flavor report details."""
        return models.FlavorReport.get_by_id(report_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditReport, as_kwargs=True)
    @blp.response(204)
    def put(self, report_id, **kwargs):
        """Updates an existing flavor report."""
        models.FlavorReport.get_by_id(report_id).update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, report_id):
        """Deletes an existing flavor report."""
        models.FlavorReport.get_by_id(report_id).delete()
