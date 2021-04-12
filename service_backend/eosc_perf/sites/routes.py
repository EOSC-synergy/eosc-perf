# -*- coding: utf-8 -*-
"""Sites routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from eosc_perf.authorization import login_required, admin_required

blp = Blueprint(
    'sites', __name__, description='Sites operations'
)


@blp.route('/query')
class Query(MethodView):

    @blp.arguments(schemas.SitesQueryArgs, location='query')
    @blp.response(200, schemas.Site(many=True))
    def get(self, args):
        """List sites."""
        return models.Site.get(filters=args)


@blp.route('/update/<uuid:id>')
class Update(MethodView):

    @blp.arguments(schemas.SitesQueryArgs, location='query')
    @blp.response(200, schemas.Site)
    @blp.response(204)
    def put(self, id, args):
        """Updates (or creates) site."""
        site = models.Site.get_by_id(record_id=id)
        if site:
            return models.Site.update(**args)
        else:
            return models.Site.create(id=id, **args)
