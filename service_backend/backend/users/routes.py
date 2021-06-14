"""User routes."""
from backend.authorization import admin_required, login_required
from backend.extensions import flaat
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from . import models, schemas

blp = Blueprint(
    'users', __name__, description='Operations on users'
)


@blp.route('')
class Root(MethodView):

    @admin_required()
    @blp.arguments(schemas.UserQuery, location='query')
    @blp.response(200, schemas.User(many=True))
    def get(self, args):
        """Filters and list users."""
        return models.User.filter_by(**args)


@blp.route('/<string:user_iss>/<string:user_sub>')
class User(MethodView):

    @admin_required()
    @blp.response(200, schemas.User)
    def get(self, user_iss, user_sub):
        """Retrieves user details."""
        return models.User.get_by_subiss(user_sub, user_iss)

    @admin_required()
    @blp.response(204)
    def delete(self, user_iss, user_sub):
        """Deletes an existing user."""
        models.User.get_by_subiss(user_sub, user_iss).delete()


@blp.route('/admin')
class Admin(MethodView):

    @admin_required()
    @blp.response(204)
    def get(self):
        """Returns 204 if you are admin."""
        pass


@blp.route('/self')
class Register(MethodView):

    @login_required()
    @blp.response(200, schemas.User)
    def get(self):
        """Retrieves the logged in user info."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        return models.User.get_by_subiss(
            sub=token_info['body']['sub'],
            iss=token_info['body']['iss']
        )

    @login_required()
    @blp.response(201, schemas.User)
    def post(self):
        """Registers the logged in user."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        user_info = flaat.get_info_from_introspection_endpoints(access_token)
        return models.User.create(
            sub=token_info['body']['sub'],
            iss=token_info['body']['iss'],
            email=user_info['email']
        )

    @login_required()
    @blp.response(204)
    def put(self):
        """Updates the logged in user info."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        user_info = flaat.get_info_from_introspection_endpoints(access_token)
        user = models.User.get_by_subiss(
            sub=token_info['body']['sub'],
            iss=token_info['body']['iss']
        )
        user.update(email=user_info['email'])
