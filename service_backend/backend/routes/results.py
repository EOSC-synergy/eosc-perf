"""Result routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import query_args, schemas
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint(
    'results', __name__, description='Operations on results'
)


@blp.route('')
class Root(MethodView):

    @blp.doc(operationId='GetResults')
    @blp.arguments(query_args.ResultFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Result(many=True))
    def get(self, tag_names=None, before=None, after=None, **kwargs):
        """Filters and list results."""
        query = models.Result.query.filter_by(**kwargs)
        if type(tag_names) == list:
            query = query.filter(models.Result.tag_names.in_(tag_names))
        if before:
            query = query.filter(models.Result.upload_date < before)
        if after:
            query = query.filter(models.Result.upload_date > after)

        return query.all()

    @auth.login_required()
    @blp.doc(operationId='AddResult')
    @blp.arguments(query_args.ResultContext, location='query')
    @blp.arguments(schemas.Json)
    @blp.response(201, schemas.Result)
    def post(self, query_args, json):
        """Creates a new result."""
        access_token = tokentools.get_access_token_from_request(request)
        return models.Result.create(
            uploader=models.User.get(token=access_token),
            json=json,
            reports=[],
            benchmark=models.Benchmark.get_by_id(query_args['benchmark_id']),
            site=models.Site.get_by_id(query_args['site_id']),
            flavor=models.Flavor.get_by_id(query_args['flavor_id']),
            tags=[models.Tag.get_by_id(id) for id in query_args['tags_ids']]
        )


@blp.route('/search')
class Search(MethodView):

    @blp.doc(operationId='SearchResults')
    @blp.arguments(query_args.ResultSearch, location='query')
    @blp.response(200, schemas.Result(many=True))
    def get(self, search):
        """Filters and list results."""
        return models.Result.query_with(**search)


@blp.route('/<uuid:result_id>')
class Result(MethodView):

    @blp.doc(operationId='GetResult')
    @blp.response(200, schemas.Result)
    def get(self, result_id):
        """Retrieves result details."""
        return models.Result.get_by_id(result_id)

    @auth.login_required()
    @blp.doc(operationId='EditResult')
    @blp.arguments(schemas.TagsIds, as_kwargs=True)
    @blp.response(204)
    def put(self, result_id, tags_ids=None):
        """Updates an existing result tags."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        result = models.Result.get_by_id(result_id)
        valid_uploader = all([
            result.uploader_iss == token_info['body']['iss'],
            result.uploader_sub == token_info['body']['sub']
        ])
        if auth.valid_admin() or valid_uploader:
            if tags_ids is not None:  # Empty list should pass
                tags = [models.Tag.get_by_id(id) for id in tags_ids]
                result.update(tags=tags)
        else:
            abort(403)

    @auth.admin_required()
    @blp.doc(operationId='DelResult')
    @blp.response(204)
    def delete(self, result_id):
        """Deletes an existing result."""
        models.Result.get_by_id(result_id).delete()


@blp.route('/<uuid:result_id>/uploader')
class Uploader(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='GetResultUploader')
    @blp.response(200, schemas.User)
    def get(self, result_id):
        """Retrieves result uploader."""
        return models.Result.get_by_id(result_id).uploader


@blp.route('/<uuid:result_id>/report')
class Report(MethodView):

    @auth.login_required()
    @blp.doc(operationId='AddResultReport')
    @blp.arguments(schemas.ReportCreate)
    @blp.response(201, schemas.Report)
    def post(self, json, result_id):
        """Creates a result report."""
        access_token = tokentools.get_access_token_from_request(request)
        result = models.Result.get_by_id(result_id)
        report = models.Report(
            uploader=models.User.get(token=access_token),
            message=json['message']
        )
        result.update(reports=result.reports+[report])
        return report
