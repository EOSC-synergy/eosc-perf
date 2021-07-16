"""Benchmark routes."""
from backend.extensions import auth
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas

blp = Blueprint(
    'benchmarks', __name__, description='Operations on benchmarks'
)


@blp.route('')
class Root(MethodView):

    @blp.arguments(schemas.BenchmarkQueryArgs, location='query')
    @blp.response(200, schemas.Benchmark(many=True))
    def get(self, args):
        """Filters and list benchmarks."""
        return models.Benchmark.filter_by(**args)

    @auth.login_required()
    @blp.arguments(schemas.Benchmark, as_kwargs=True)
    @blp.response(201, schemas.Benchmark)
    def post(self, **kwargs):
        """Creates a new benchmark."""
        access_token = tokentools.get_access_token_from_request(request)
        report = models.Report(
            uploader=models.User.get(token=access_token),
        )
        return models.Benchmark.create(reports=[report], **kwargs)


@blp.route('/search')
class Search(MethodView):

    @blp.arguments(schemas.SearchQueryArgs, location='query', as_kwargs=True)
    @blp.response(200, schemas.Benchmark(many=True))
    def get(self, terms):
        """Filters and list benchmarks."""
        return models.Benchmark.query_with(terms)


@blp.route('/<uuid:benchmark_id>')
class Benchmark(MethodView):

    @blp.response(200, schemas.Benchmark)
    def get(self, benchmark_id):
        """Retrieves benchmark details."""
        return models.Benchmark.get_by_id(benchmark_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditBenchmark, as_kwargs=True)
    @blp.response(204)
    def put(self, benchmark_id, **kwargs):
        """Updates an existing benchmark."""
        models.Benchmark.get_by_id(benchmark_id).update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, benchmark_id):
        """Deletes an existing benchmark."""
        models.Benchmark.get_by_id(benchmark_id).delete()
