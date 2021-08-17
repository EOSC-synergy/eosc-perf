"""User routes."""
from backend import models
from backend.extensions import auth
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
    """Class defining the main endpoint methods for users"""

    @auth.admin_required()
    @blp.doc(operationId='GetUsers')
    @blp.arguments(args.UserFilter, location='query')
    @blp.response(200, schemas.Users)
    def get(self, query_args):
        """(Admins) Filters and list users

        Use this method to get a list of users filtered according to your 
        requirements. The response returns a pagination object with the
        filtered users (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered users
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        query = models.User.query.filter_by(**query_args)
        return query.paginate(page, per_page)

    @auth.admin_required()
    @blp.doc(operationId='DelUsers')
    @blp.arguments(args.UserDelete, location='query')
    @blp.response(204)
    def delete(self, query_args):
        """(Admins) Delete one or multiple users

        Use this method to delete the users filtered according to your 
        requirements. To prevent unintentionally delete all users, the
        method requires of query arguments, otherwise UnprocessableEntity
        exception is raised.
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered users
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """        
        if query_args != {}:
            for user in models.User.query.filter_by(**query_args):
                user.delete()
        else:
            abort(422, messages={'cancelled': "Undefined users"})


@blp.route('search')
class Search(MethodView):
    """Class defining the search endpoint for users"""

    @auth.admin_required()
    @blp.doc(operationId='SearchUsers')
    @blp.arguments(args.Search, location='query')
    @blp.response(200, schemas.Users)
    def get(self, query_args):
        """(Admins) Filters and list users

        Use this method to get a list of users based on a general search
        of terms. For example, calling this method with 
        terms=@hotmail&terms=de returns all users with 'hotmail' and 'de'
        on the 'email'. The response returns a pagination object with the
        filtered users (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered users
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        search = models.User.query
        for keyword in query_args['terms']:
            search = search.filter(
                models.User.email.contains(keyword)
            )
        return search.paginate(page, per_page)


@blp.route('/admin')
class Admin(MethodView):
    """Class defining the specific administrator tools"""

    @auth.admin_required()
    @blp.doc(operationId='Admin')
    @blp.response(204)
    def get(self):
        """(Admins) Returns 204 if you are admin

        Use this method to check that you have the administration rights.
        If so, the access returns 204, otherwise 401 or 403 are expected.
        ---

        :raises Unauthorized: The server could not verify your identity
        :raises Forbidden: You don't have the administrator rights
        """
        pass


@blp.route('/self')
class Register(MethodView):
    """Class defining the specific user tools"""

    @auth.login_required()
    @blp.doc(operationId='MyUser')
    @blp.response(200, schemas.User)
    def get(self):
        """(Users) Retrieves the logged in user info

        Use this method to retrieve your user data stored in the database.
        ---

        :raises Unauthorized: The server could not verify your identity
        :raises Forbidden: You are not registered
        :return: The database user matching the oidc token information 
        :rtype: :class:`models.User`
        """
        access_token = tokentools.get_access_token_from_request(request)
        return models.User.get(token=access_token)

    @auth.token_required()
    @blp.doc(operationId='RegisterMe')
    @blp.response(201, schemas.User)
    def post(self):
        """(OIDC Token) Registers the logged in user

        Use this method to register yourself into the application. By using
        this method, you recognize that you have read and understood our 
        terms, conditions and privacy policy at: 
        `https://performance.services.fedcloud.eu/privacy_policy`

        The method will return your stored information.
        ---

        :raises Unauthorized: The server could not verify your identity
        :raises Forbidden: You are not registered
        :return: The database user matching the oidc token information 
        :rtype: :class:`models.User`
        """
        token = tokentools.get_access_token_from_request(request)
        user_info = auth.get_info_from_introspection_endpoints(token)
        if not user_info:
            abort(500, messages={'introspection endpoint': "No user info"})
        elif 'email' not in user_info:
            abort(422, messages={'token': "No scope for email"})
        else:
            return models.User.create(token, {'email': user_info['email']})

    @auth.login_required()
    @blp.doc(operationId='UpdateMe')
    @blp.response(204)
    def put(self):
        """(Users) Updates the logged in user info

        Use this method to update your user data in the database. The 
        method returns by default 204. You can use GET after to retrieve
        the new status of your data. 
        ---

        :raises Unauthorized: The server could not verify your identity
        :raises Forbidden: You are not registered
        """
        token = tokentools.get_access_token_from_request(request)
        user_info = auth.get_info_from_introspection_endpoints(token)
        if not user_info:
            abort(500, messages={'introspection endpoint': "No user info"})
        elif 'email' not in user_info:
            abort(422, messages={'token': "No scope for email"})
        else:
            user = models.User.get(token=token)
            user.update({'email': user_info['email']})
