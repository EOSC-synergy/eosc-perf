# -*- coding: utf-8 -*-
"""Sites routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from eosc_perf_backend.authorization import login_required, admin_required

blp = Blueprint(
    'sites', __name__, description='Operations on sites'
)


@blp.route('/<uuid:id>')
class Id(MethodView):

    @blp.response(200, schemas.Site)
    def get(self, id):
        """Retrieves site details."""
        return models.Site.get_by_id(id)

    @admin_required()
    @blp.arguments(schemas.SiteEdit, as_kwargs=True)
    @blp.response(204)  # https://github.com/marshmallow-code/flask-smorest/issues/166
    def put(self, id, **kwargs):
        """Updates an existing site."""
        models.Site.get_by_id(id).update(**kwargs)

    @admin_required()
    @blp.response(204)
    def delete(self, id):
        """Deletes an existing site."""
        models.Site.get_by_id(id).delete()


@blp.route('/query')
class Query(MethodView):

    @login_required()  # Mitigate DoS attack
    @blp.arguments(schemas.SiteQuery, location='query')
    @blp.response(200, schemas.Site(many=True))
    def get(self, args):
        """Filters and list sites."""
        if args == {}:  # Avoid long query
            abort(422)
        return models.Site.filter_by(**args)


@blp.route('/submit')
class Submit(MethodView):

    @login_required()
    @blp.arguments(schemas.Site, as_kwargs=True)
    @blp.response(201, schemas.Site)
    def post(self, **kwargs):
        """Creates a new site."""
        return models.Site.create(**kwargs)
