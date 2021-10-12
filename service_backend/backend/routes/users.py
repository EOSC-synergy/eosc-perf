"""Users URL routes. Collection of controller methods to create and
operate existing users on the database.
"""
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from .. import models, notifications
from ..extensions import auth, db
from ..schemas import args, schemas
from ..utils import queries
from . import results as results_routes

blp = Blueprint(
    'users', __name__, description='Operations on users'
)


collection_url = ""
resource_url = "/self"


@blp.route(collection_url, methods=["GET"])
@blp.doc(operationId='ListUsers')
@auth.admin_required()
@blp.arguments(args.UserFilter, location='query')
@blp.response(200, schemas.Users)
@queries.to_pagination()
@queries.add_sorting(models.User)
@queries.add_datefilter(models.User)
def list(*args, **kwargs):
    """(Admins) Filters and list users

    Use this method to get a list of users filtered according to your
    requirements. The response returns a pagination object with the
    filtered users (if succeeds).
    """
    return __list(*args, **kwargs)


def __list(query_args):
    """List the registered users.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered users
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    query = models.User.query
    return query.filter_by(**query_args)


@blp.route(collection_url + ':register', methods=["POST"])
@blp.doc(operationId='RegisterSelf')
@auth.token_required()
@blp.response(201, schemas.User)
def register(*args, **kwargs):
    """(OIDC Token) Registers the logged in user

    Use this method to register yourself into the application. By using
    this method, you recognize that you have read and understood our
    terms, conditions and privacy policy at:
    `https://performance.services.fedcloud.eu/privacy_policy`

    The method will return your stored information.
    """
    return __register(*args, **kwargs)


def __register():
    """Registers the current request user.

    :raises Unauthorized: The server could not verify your identity
    :raises Forbidden: You are not registered
    """
    tokeninfo = auth.current_tokeninfo()
    user_info = auth.current_userinfo()
    if not user_info:
        error_msg = "No user info received from 'OP endpoint'"
        abort(500, messages={'error': error_msg})
    elif 'email' not in user_info:
        abort(422, messages={'error': "No scope for email in oidc token"})

    user_properties = {k: tokeninfo[k] for k in ['iss', 'sub']}
    user_properties['email'] = user_info['email']
    user = models.User.create(user_properties)

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = "User already submitted/exists"
        abort(409, messages={'error': error_msg})

    notifications.user_welcome(user)
    return user


@blp.route(collection_url + ':remove', methods=["POST"])
@blp.doc(operationId='RemoveUsers')
@auth.admin_required()
@blp.arguments(args.UserDelete, location='query')
@blp.response(204)
def remove(*args, **kwargs):
    """(Admins) Removes one or multiple users

    Use this method to delete the users filtered according to your
    requirements. To prevent unintentionally delete all users, the
    method requires of query arguments, otherwise UnprocessableEntity
    exception is raised.
    """
    return __remove(*args, **kwargs)


def __remove(query_args):
    """Removes/Deletes the filtered users.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered users
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    if query_args == {}:
        error_msg = "Cancelled, undefined users"
        abort(422, messages={'error': error_msg})

    [user.delete() for user in __list(query_args)]

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = "Conflict deleting users"
        abort(409, messages={'error': error_msg})


@blp.route(collection_url + ':search', methods=["GET"])
@blp.doc(operationId='SearchUsers')
@auth.admin_required()
@blp.arguments(args.UserSearch, location='query')
@blp.response(200, schemas.Users)
@queries.to_pagination()
@queries.add_sorting(models.User)
@queries.add_datefilter(models.User)
def search(*args, **kwargs):
    """(Admins) Filters and list users

    Use this method to get a list of users based on a general search
    of terms. For example, calling this method with
    terms=@hotmail&terms=de returns all users with 'hotmail' and 'de'
    on the 'email'. The response returns a pagination object with the
    filtered users (if succeeds).
    """
    return __search(*args, **kwargs)


def __search(query_args):
    """Alternative to list for fetching data using string terms.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered users
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    search = models.User.query
    for keyword in query_args.pop('terms'):
        search = search.filter(
            models.User.email.contains(keyword)
        )
    return search.filter_by(**query_args)


@blp.route(resource_url, methods=["GET"])
@blp.doc(operationId='GetSelf')
@auth.login_required()
@blp.response(200, schemas.User)
def get(*args, **kwargs):
    """(Users) Retrieves the logged in user info

    Use this method to retrieve your user data stored in the database.
    """
    return __get(*args, **kwargs)


def __get():
    """Retrieves the current request user.

    :raises Unauthorized: The server could not verify your identity
    :raises Forbidden: You are not registered
    :return: The database user matching the oidc token information
    :rtype: :class:`models.User`
    """
    user = models.User.current_user()
    if user is None:
        error_msg = "User not registered"
        abort(404, messages={'error': error_msg})
    else:
        return user


@blp.route(resource_url + ':update', methods=["POST"])
@blp.doc(operationId='UpdateSelf')
@auth.login_required()
@blp.response(204)
def update(*args, **kwargs):
    """(Users) Updates the logged in user info

    Use this method to update your user data in the database. The method
    returns by default 204, use a GET method to retrieve the new status
    of your data.
    """
    return __update(*args, **kwargs)


def __update():
    """ Updates the user information from introspection endpoint.

    :raises Unauthorized: The server could not verify your identity
    :raises Forbidden: You are not registered
    """
    user = __get()
    user_info = auth.current_userinfo()
    if not user_info:
        error_msg = "No user info received from 'introspection endpoint'"
        abort(500, messages={'error': error_msg})
    elif 'email' not in user_info:
        abort(422, messages={'error': "No scope for email in oidc token"})

    user.update({'email': user_info['email']})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = "Existing user already using email"
        abort(409, messages={'error': error_msg})

    notifications.email_updated(user)


@blp.route(resource_url + ":try_admin", methods=["GET"])
@blp.doc(operationId='TryAdmin')
@auth.admin_required()
@blp.response(204)
def try_admin():
    """(Admins) Returns 204 if you are admin

    Use this method to check that you have the administration rights.
    If so, the access returns 204, otherwise 401 or 403 are expected.
    ---

    :raises Unauthorized: The server could not verify your identity
    :raises Forbidden: You don't have the administrator rights
    """
    pass


@blp.route(resource_url + "/results", methods=["GET"])
@blp.doc(operationId='ListUserResults')
@auth.login_required()
@blp.arguments(args.ResultFilter, location='query')
@blp.response(200, schemas.Results)
@queries.to_pagination()
@queries.add_sorting(models.Result)
@queries.add_datefilter(models.Result)
def results(*args, **kwargs):
    """(Users) Returns your uploaded results

    Use this method to retrieve all the results uploaded by your user.
    You can use the query parameter to retrieve also those with pending
    claims.
    """
    return __results(*args, **kwargs)


def __results(query_args):
    """Returns the user uploaded results filtered by the query args.

    :raises Unauthorized: The server could not verify your identity
    :raises Forbidden: You don't have the administrator rights
    """
    user = __get()
    query = results_routes.__list(query_args)
    return query.with_deleted().filter_by(uploader=user)


@blp.route(resource_url + "/claims", methods=["GET"])
@blp.doc(operationId='ListUserClaims')
@auth.login_required()
@blp.arguments(args.ClaimFilter, location='query')
@blp.response(200, schemas.Claims)
@queries.to_pagination()
@queries.add_sorting(models.Claim)
@queries.add_datefilter(models.Claim)
def claims(*args, **kwargs):
    """(Users) Returns your uploaded pending claims

    Use this method to retrieve all the claims uploaded by your user.
    """
    return __claims(*args, **kwargs)


def __claims(query_args):
    """Returns the user uploaded claims filtered by the query args.

    :raises Unauthorized: The server could not verify your identity
    :raises Forbidden: You don't have the administrator rights
    """
    user = __get()
    query = models.Claim.query
    return query.filter_by(uploader=user, **query_args)
