# -*- coding: utf-8 -*-
"""User routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from eosc_perf.authorization import login_required, admin_required

blp = Blueprint(
    'benchmarks', __name__, description='Benchmark operations'
)


@blp.route('/query')
class Query(MethodView):

    @blp.arguments(schemas.BenchmarksQueryArgs, location='query')
    @blp.response(200, schemas.Benchmark(many=True))
    def get(self, args):
        """List benchmarks"""
        return models.Benchmark.get(filters=args)


@blp.route('/submit')
class Submit(MethodView):

    @blp.arguments(schemas.BenchmarksQueryArgs, location='query')
    @blp.response(201, schemas.Benchmark)
    def post(self, args):
        """Posts a new benchmark"""
        return models.Benchmark.create(**args)
