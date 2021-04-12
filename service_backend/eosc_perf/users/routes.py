# -*- coding: utf-8 -*-
"""User routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from eosc_perf.authorization import login_required, admin_required

blp = Blueprint(
    'user', __name__, description='Operations on users'
)


@blp.route('/profile')
class Profile(MethodView):

    @blp.arguments(schemas.UsersQueryId, location='query')
    @blp.response(200, schemas.User)
    def get(self, args):
        """Return user details"""
        return models.User.get_by_id(**args)

    @blp.arguments(schemas.UsersQueryArgs)
    @blp.response(201, schemas.User)
    def post(self, args):
        """Add a new user"""
        return models.User.create(**args)


@blp.route('/admin')
class Admin(MethodView):

    @blp.response(200)
    @admin_required()
    def get(self):
        return "you are admin"


@blp.route('/query')
class Query(MethodView):

    @blp.arguments(schemas.UsersQueryArgs, location='query')
    @blp.response(200, schemas.User(many=True))
    def get(self, args):
        """List users"""
        return models.User.get(filters=args)
