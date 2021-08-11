"""User routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import args, schemas
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

blp = Blueprint(
    'users', __name__, description='Operations on users'
)


@blp.route('')
class Root(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='GetUsers')
    @blp.arguments(args.UserFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Users)
    def get(self, page=1, per_page=100, **kwargs):
        """Filters and list users."""
        query = models.User.query.filter_by(**kwargs)
        return query.paginate(page, per_page)

    @auth.admin_required()
    @blp.doc(operationId='DelUsers')
    @blp.arguments(args.UserDelete, location='query')
    @blp.response(204)
    def delete(self, args):
        """Deletes an existing user."""
        if args != {}:
            for user in models.User.query.filter_by(**args):
                user.delete()
        else:
            abort(422, messages={'cancelled': "Undefined users"})


@blp.route('search')
class Search(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='SearchUsers')
    @blp.arguments(args.UserSearch, location='query', as_kwargs=True)
    @blp.response(200, schemas.Users)
    def get(self, terms, page=1, per_page=100):
        """Filters and list users."""
        search = models.User.search(terms)
        return search.paginate(page, per_page)


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
        user.update(token=access_token)
