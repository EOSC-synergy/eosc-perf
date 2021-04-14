# -*- coding: utf-8 -*-
"""User routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from eosc_perf.authorization import login_required, admin_required

blp = Blueprint(
    'users', __name__, description='Operations on users'
)


@blp.route('/<uuid:id>')
class User(MethodView):

    @blp.response(200, schemas.User)
    def get(self, id):
        """Retrieves user details."""
        return models.User.get_by_id(id)

    # @admin_required()
    @blp.arguments(schemas.UsersCreateArgs)
    @blp.response(204)  # https://github.com/marshmallow-code/flask-smorest/issues/166
    def put(self, args, id):
        """Updates an existing user."""
        return models.User.get_by_id(id).update(**args)

    # @admin_required()
    @blp.response(204)
    def delete(self, id):
        """Deletes an existing user."""
        return models.User.get_by_id(id).delete()


@blp.route('/submit')
class Submit(MethodView):

    # @login_required()
    @blp.arguments(schemas.UsersCreateArgs)
    @blp.response(201, schemas.User)
    def post(self, args):
        """Creates a new user."""
        return models.User.create(**args)


@blp.route('/query')
class Query(MethodView):

    @blp.arguments(schemas.UsersQueryArgs, location='query')
    @blp.response(200, schemas.User(many=True))
    def get(self, args):
        """Filters and list users."""
        return models.User.filter_by(**args)


@blp.route('/admin')
class Admin(MethodView):

    @admin_required()
    @blp.response(204)
    def get(self):
        """Returns 204 if you are admin."""
        return True
