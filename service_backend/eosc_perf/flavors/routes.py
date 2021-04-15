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
class Id(MethodView):

    @blp.response(200, schemas.Flavor)
    def get(self, id):
        """Retrieves flavor details."""
        return models.Flavor.get_by_id(id)

    # @admin_required()
    @blp.arguments(schemas.Flavor(exclude=['id']))
    @blp.response(204)  # https://github.com/marshmallow-code/flask-smorest/issues/166
    def put(self, args, id):
        """Updates an existing flavor."""
        models.Flavor.get_by_id(id).update(**args)

    # @admin_required()
    @blp.response(204)
    def delete(self, id):
        """Deletes an existing flavor."""
        models.Flavor.get_by_id(id).delete()


@blp.route('/query')
class Query(MethodView):

    # @login_required()  # Mitigate DoS attack
    @blp.arguments(schemas.Flavor(exclude=['id']), location='query')
    @blp.response(200, schemas.Flavor(many=True))
    def get(self, args):
        """Filters and list flavors."""
        if args == {}:  # Avoid long query
            abort(422)
        return models.Flavor.filter_by(**args)


@blp.route('/submit')
class Submit(MethodView):

    # @admin_required()
    @blp.arguments(schemas.FlavorsCreateArgs)
    @blp.response(201, schemas.Flavor)
    def post(self, args):
        """Creates a new flavor."""
        return models.Flavor.create(**args)
