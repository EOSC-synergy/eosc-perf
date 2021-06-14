"""Benchmark routes."""
import marshmallow as ma
from backend.authorization import admin_required, login_required
from flask.views import MethodView
from flask_smorest import Blueprint

from . import models, schemas


blp = Blueprint(
    'benchmarks', __name__, description='Operations on benchmarks'
)


@blp.route('')
class Root(MethodView):

    @login_required()  # Mitigate DoS attack
    @blp.arguments(schemas.BenchmarkQueryArgs, location='query')
    @blp.response(200, schemas.Benchmark(many=True))
    def get(self, args):
        """Filters and list benchmarks."""
        return models.Benchmark.filter_by(**args)

    @login_required()
    @blp.arguments(schemas.Benchmark, as_kwargs=True)
    @blp.response(201, schemas.Benchmark)
    def post(self, **kwargs):
        """Creates a new benchmark."""
        return models.Benchmark.create(**kwargs)


@blp.route('/<uuid:benchmark_id>')
class Benchmark(MethodView):

    @blp.response(200, schemas.Benchmark)
    def get(self, benchmark_id):
        """Retrieves benchmark details."""
        return models.Benchmark.get_by_id(benchmark_id)

    @admin_required()
    @blp.arguments(schemas.EditBenchmark, as_kwargs=True)
    @blp.response(204)
    def put(self, benchmark_id, **kwargs):
        """Updates an existing benchmark."""
        models.Benchmark.get_by_id(benchmark_id).update(**kwargs)

    @admin_required()
    @blp.response(204)
    def delete(self, benchmark_id):
        """Deletes an existing benchmark."""
        models.Benchmark.get_by_id(benchmark_id).delete()
