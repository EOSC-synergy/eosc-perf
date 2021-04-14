# -*- coding: utf-8 -*-
"""Flavors routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from eosc_perf.authorization import login_required, admin_required

blp = Blueprint(
    'flavors', __name__, description='Operations on flavors'
)


@blp.route('/<uuid:id>')
class Flavor(MethodView):

    @blp.response(200, schemas.Flavor)
    def get(self, id):
        """Retrieves flavor details."""
        return models.Flavor.get_by_id(id)

    # @admin_required()
    @blp.arguments(schemas.FlavorsCreateArgs)
    @blp.response(204)  # https://github.com/marshmallow-code/flask-smorest/issues/166
    def put(self, args, id):
        """Updates an existing flavor."""
        return models.Flavor.get_by_id(id).update(**args)

    # @admin_required()
    @blp.response(204)
    def delete(self, id):
        """Deletes an existing flavor."""
        return models.Flavor.get_by_id(id).delete()


@blp.route('/submit')
class Submit(MethodView):

    # @admin_required()
    @blp.arguments(schemas.FlavorsCreateArgs)
    @blp.response(201, schemas.Flavor)
    def post(self, args):
        """Creates a new flavor."""
        return models.Flavor.create(**args)


@blp.route('/query')
class Query(MethodView):

    @blp.arguments(schemas.FlavorsQueryArgs, location='query')
    @blp.response(200, schemas.Flavor(many=True))
    def get(self, args):
        """Filters and list flavors."""
        return models.Flavor.filter_by(**args)
