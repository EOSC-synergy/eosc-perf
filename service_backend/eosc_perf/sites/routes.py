# -*- coding: utf-8 -*-
"""Sites routes."""
from operator import mod
from flask.views import MethodView
from flask_smorest import Blueprint, abort, blueprint

from . import models, schemas
from eosc_perf.authorization import login_required, admin_required

blp = Blueprint(
    'sites', __name__, description='Operations on sites'
)


@blp.route('/<uuid:id>')
class Site(MethodView):

    @blp.response(200, schemas.Site)
    def get(self, id):
        """Retrieves site details"""
        return models.Site.get_by_id(id)

    # @admin_required()
    @blp.arguments(schemas.SitesCreateArgs)
    @blp.response(204)  # https://github.com/marshmallow-code/flask-smorest/issues/166
    def put(self, args, id):
        """Updates (or creates) site."""
        return models.Site.get_by_id(id).update(**args)

    # @admin_required()
    @blp.response(204)
    def delete(self, id):
        """Deletes an existing site"""
        return models.Site.get_by_id(id).delete()


@blp.route('/submit')
class Submit(MethodView):

    # @admin_required()
    @blp.arguments(schemas.SitesCreateArgs)
    @blp.response(201, schemas.Site)
    def post(self, args):
        """Creates a new site"""
        return models.Site.create(**args)


@blp.route('/query')
class Query(MethodView):

    @blp.arguments(schemas.SitesQueryArgs, location='query')
    @blp.response(200, schemas.Site(many=True))
    def get(self, args):
        """Filters and list sites."""
        return models.Site.filter_by(**args)
