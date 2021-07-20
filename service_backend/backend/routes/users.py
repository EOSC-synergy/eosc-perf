"""User routes."""
from backend.extensions import auth
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from backend import models, schemas


blp = Blueprint(
    'users', __name__, description='Operations on users'
)


@blp.route('')
class Root(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='GetUsers')
    @blp.arguments(schemas.user.ListQueryArgs, location='query')
    @blp.response(200, schemas.User(many=True))
    def get(self, args):
        """Filters and list users."""
        return models.User.filter_by(**args)


@blp.route('email_search')
class Search(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='SearchUsers')
    @blp.arguments(schemas.user.SearchQueryArgs, location='query')
    @blp.response(200, schemas.User(many=True))
    def get(self, kwargs):
        """Filters and list users."""
        return models.User.query_emails_with(**kwargs)


@blp.route('/<string:user_iss>/<string:user_sub>')
class User(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='GetUser')
    @blp.response(200, schemas.User)
    def get(self, user_iss, user_sub):
        """Retrieves user details."""
        return models.User.get(sub=user_sub, iss=user_iss)

    @auth.admin_required()
    @blp.doc(operationId='DelUser')
    @blp.response(204)
    def delete(self, user_iss, user_sub):
        """Deletes an existing user."""
        user = models.User.get(sub=user_sub, iss=user_iss)
        user.delete()


@blp.route('/admin')
class Admin(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='Admin')
    @blp.response(204)
    def get(self):
        """Returns 204 if you are admin."""
        pass


@blp.route('/self')
class Register(MethodView):

    @auth.login_required()
    @blp.doc(operationId='MyUser')
    @blp.response(200, schemas.User)
    def get(self):
        """Retrieves the logged in user info."""
        access_token = tokentools.get_access_token_from_request(request)
        return models.User.get(token=access_token)

    @auth.login_required()
    @blp.doc(operationId='RegisterMe')
    @blp.response(201, schemas.User)
    def post(self):
        """Registers the logged in user."""
        access_token = tokentools.get_access_token_from_request(request)
        return models.User.create(token=access_token)

    @auth.login_required()
    @blp.doc(operationId='UpdateMe')
    @blp.response(204)
    def put(self):
        """Updates the logged in user info."""
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        user.update_info(token=access_token)
