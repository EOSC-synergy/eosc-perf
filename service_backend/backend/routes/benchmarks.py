"""Benchmark routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import args, schemas
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
    @blp.arguments(args.BenchmarkFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Benchmarks)
    def get(self, page=1, per_page=100, **kwargs):
        """Filters and list benchmarks."""
        query = models.Benchmark.query.filter_by(**kwargs)
        query = query.filter(~models.Benchmark.has_open_reports)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddBenchmark')
    @blp.arguments(schemas.BenchmarkCreate, as_kwargs=True)
    @blp.response(201, schemas.Benchmark)
    def post(self, **kwargs):
        """Creates a new benchmark."""
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        report = models.Report(created_by=user)
        return models.Benchmark.create(created_by=user, reports=[report], **kwargs)


@blp.route('/search')
class Search(MethodView):

    @blp.doc(operationId='SearchBenchmarks')
    @blp.arguments(args.BenchmarkSearch, location='query', as_kwargs=True)
    @blp.response(200, schemas.Benchmarks)
    def get(self, terms, page=1, per_page=100):
        """Filters and list benchmarks."""
        search = models.Benchmark.search(terms)
        search = search.filter(~models.Benchmark.has_open_reports)
        return search.paginate(page, per_page)


@blp.route('/<uuid:benchmark_id>')
class Benchmark(MethodView):

    @blp.doc(operationId='GetBenchmark')
    @blp.response(200, schemas.Benchmark)
    def get(self, benchmark_id):
        """Retrieves benchmark details."""
        return models.Benchmark.get(benchmark_id)

    @auth.admin_required()
    @blp.doc(operationId='EditBenchmark')
    @blp.arguments(schemas.BenchmarkEdit, as_kwargs=True)
    @blp.response(204)
    def put(self, benchmark_id, **kwargs):
        """Updates an existing benchmark."""
        models.Benchmark.get(benchmark_id).update(**kwargs)

    @auth.admin_required()
    @blp.doc(operationId='DelBenchmark')
    @blp.response(204)
    def delete(self, benchmark_id):
        """Deletes an existing benchmark."""
        models.Benchmark.get(benchmark_id).delete()
