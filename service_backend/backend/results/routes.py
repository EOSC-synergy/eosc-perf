"""Result routes."""
from operator import mod
from backend.extensions import auth
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas


blp = Blueprint(
    'results', __name__, description='Operations on results'
)


@blp.route('')
class Root(MethodView):

    @blp.arguments(schemas.FilterQueryArgs, location='query', as_kwargs=True)
    @blp.response(200, schemas.Result(many=True))
    def get(self, tag_names=None, **kwargs):
        """Filters and list results."""
        query = models.Result.query.filter_by(**kwargs)
        if type(tag_names) == list:
            query = query.filter(models.Result.tag_names.in_(tag_names))
        return query.all()

    @auth.login_required()
    @blp.arguments(schemas.CreateQueryArgs, location='query')
    @blp.arguments(schemas.Json)
    @blp.response(201, schemas.Result)
    def post(self, query_args, json):
        """Creates a new result."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        return models.Result.create(
            uploader_sub=token_info['body']['sub'],
            uploader_iss=token_info['body']['iss'],
            json=json,
            benchmark=models.Benchmark.get_by_id(query_args['benchmark_id']),
            site=models.Site.get_by_id(query_args['site_id']),
            flavor=models.Flavor.get_by_id(query_args['flavor_id']),
            tags=[models.Tag.get_by_id(id) for id in query_args['tags_ids']]
        )


@blp.route('/search')
class Search(MethodView):

    @blp.arguments(schemas.SearchQueryArgs, location='query', as_kwargs=True)
    @blp.response(200, schemas.Result(many=True))
    def get(self, terms=[]):
        """Filters and list results."""
        return models.Result.query_with(terms)


@blp.route('/<uuid:result_id>')
class Result(MethodView):

    @blp.response(200, schemas.Result)
    def get(self, result_id):
        """Retrieves result details."""
        return models.Result.get_by_id(result_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditResult, as_kwargs=True)
    @blp.response(204)
    def put(self, result_id, **kwargs):
        """Updates an existing result."""
        result = models.Result.get_by_id(result_id)

        if 'benchmark_id' in kwargs:
            benchmark_id = kwargs.pop('benchmark_id')
            kwargs['benchmark'] = models.Benchmark.get_by_id(benchmark_id)

        if 'site_id' in kwargs:
            site_id = kwargs.pop('site_id')
            kwargs['site'] = models.Site.get_by_id(site_id)

        if 'flavor_id' in kwargs:
            flavor_id = kwargs.pop('flavor_id')
            kwargs['flavor'] = models.Flavor.get_by_id(flavor_id)

        if 'tags_ids' in kwargs:
            tags_ids = kwargs.pop('tags_ids')
            kwargs['tags'] = [models.Tag.get_by_id(id) for id in tags_ids]

        result.update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, result_id):
        """Deletes an existing result."""
        models.Result.get_by_id(result_id).delete()
