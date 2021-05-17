# -*- coding: utf-8 -*-
"""User routes."""
from backend.authorization import admin_required, login_required
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas

blp = Blueprint(
    'users', __name__, description='Operations on users'
)


@blp.route('/iss/<string:iss>/sub/<string:sub>')
class Id(MethodView):

    @blp.response(200, schemas.User)
    def get(self, iss, sub):
        """Retrieves user details."""
        return models.User.get_by_subiss(sub, iss)

    @admin_required()
    @blp.arguments(schemas.UserEdit, as_kwargs=True)
    @blp.response(204)
    def put(self, iss, sub, **kwargs):
        """Updates an existing user."""
        models.User.get_by_subiss(sub, iss).update(**kwargs)

    @admin_required()
    @blp.response(204)
    def delete(self, iss, sub):
        """Deletes an existing user."""
        models.User.get_by_subiss(sub, iss).delete()


@blp.route('/query')
class Query(MethodView):

    @admin_required()
    @blp.arguments(schemas.UserQuery, location='query')
    @blp.response(200, schemas.User(many=True))
    def get(self, args):
        """Filters and list users."""
        if args == {}:  # Avoid long query
            abort(422)
        return models.User.filter_by(**args)


@blp.route('/submit')
class Submit(MethodView):

    @admin_required()
    @blp.arguments(schemas.User, as_kwargs=True)
    @blp.response(201, schemas.User)
    def post(self, **kwargs):
        """Creates a new user."""
        return models.User.create(**kwargs)


@blp.route('/am-I-admin')
class Admin(MethodView):

    @admin_required()
    @blp.response(204)
    def get(self):
        """Returns 204 if you are admin."""
        pass


@blp.route('/register-me')
class Register(MethodView):

    @login_required()
    @blp.arguments(schemas.UserEdit, as_kwargs=True)
    @blp.response(201, schemas.User)
    def post(self, email):
        """Registers the logged in user."""
        access_token = tokentools.get_access_token_from_request(request)
        info = tokentools.get_accesstoken_info(access_token)
        return models.User.get_by_subiss_or_create(
            sub=info['body']['sub'],
            iss=info['body']['iss'],
            email=email
        )
