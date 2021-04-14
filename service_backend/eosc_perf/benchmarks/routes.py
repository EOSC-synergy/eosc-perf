# -*- coding: utf-8 -*-
"""User routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from eosc_perf.authorization import login_required, admin_required

from eosc_perf import benchmarks

blp = Blueprint(
    'benchmarks', __name__, description='Operations on benchmarks'
)


@blp.route('/<uuid:id>')
class Benchmark(MethodView):

    @blp.response(200, schemas.Benchmark)
    def get(self, id):
        """Retrieves benchmark details."""
        return models.Benchmark.get_by_id(id)

    # @admin_required()
    @blp.arguments(schemas.BenchmarksCreateArgs)
    @blp.response(204)  # https://github.com/marshmallow-code/flask-smorest/issues/166
    def put(self, args, id):
        """Updates an existing benchmark."""
        return models.Benchmark.get_by_id(id).update(**args)

    # @admin_required()
    @blp.response(204)
    def delete(self, id):
        """Deletes an existing benchmark."""
        return models.Benchmark.get_by_id(id).delete()


@blp.route('/submit')
class Submit(MethodView):

    # @login_required()
    @blp.arguments(schemas.BenchmarksCreateArgs)
    @blp.response(201, schemas.Benchmark)
    def post(self, args):
        """Creates a new benchmark."""
        return models.Benchmark.create(**args)


@blp.route('/query')
class Query(MethodView):

    @blp.arguments(schemas.BenchmarksQueryArgs, location='query')
    @blp.response(200, schemas.Benchmark(many=True))
    def get(self, args):
        """Filters and list benchmarks."""
        return models.Benchmark.filter_by(**args)
