"""Benchmark routes."""
from backend import models, schemas
from backend.extensions import auth
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'benchmarks', __name__, description='Operations on benchmarks'
)


@blp.route('')
class Root(MethodView):

    @blp.doc(operationId='GetBenchmarks')
    @blp.arguments(schemas.benchmark.FilterArgs, location='query')
    @blp.response(200, schemas.Benchmark(many=True))
    def get(self, args):
        """Filters and list benchmarks."""
        return models.Benchmark.filter_by(**args)

    @auth.login_required()
    @blp.doc(operationId='AddBenchmark')
    @blp.arguments(schemas.benchmark.Create, as_kwargs=True)
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

    @blp.doc(operationId='SearchBenchmarks')
    @blp.arguments(schemas.benchmark.SearchArgs, location='query')
    @blp.response(200, schemas.Benchmark(many=True))
    def get(self, kwargs):
        """Filters and list benchmarks."""
        return models.Benchmark.query_with(**kwargs)


@blp.route('/<uuid:benchmark_id>')
class Benchmark(MethodView):

    @blp.doc(operationId='GetBenchmark')
    @blp.response(200, schemas.Benchmark)
    def get(self, benchmark_id):
        """Retrieves benchmark details."""
        return models.Benchmark.get_by_id(benchmark_id)

    @auth.admin_required()
    @blp.doc(operationId='EditBenchmark')
    @blp.arguments(schemas.benchmark.Edit, as_kwargs=True)
    @blp.response(204)
    def put(self, benchmark_id, **kwargs):
        """Updates an existing benchmark."""
        models.Benchmark.get_by_id(benchmark_id).update(**kwargs)

    @auth.admin_required()
    @blp.doc(operationId='DelBenchmark')
    @blp.response(204)
    def delete(self, benchmark_id):
        """Deletes an existing benchmark."""
        models.Benchmark.get_by_id(benchmark_id).delete()
