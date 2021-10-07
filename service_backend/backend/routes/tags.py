"""Tag URL routes. Collection of controller methods to create and
operate existing user tags on the database.
"""
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .. import models
from ..extensions import auth, db
from ..schemas import args, schemas
from ..utils import queries

blp = Blueprint(
    'tags', __name__, description='Operations on tags'
)

collection_url = ""
resource_url = "/<uuid:id>"


@blp.route(collection_url, methods=["GET"])
@blp.doc(operationId='ListTags')
@blp.arguments(args.TagFilter, location='query')
@blp.response(200, schemas.Tags)
@queries.to_pagination()
@queries.add_sorting(models.Tag)
def list(*args, **kwargs):
    """(Public) Filters and list tags

    Use this method to get a list of tags filtered according to your
    requirements. The response returns a pagination object with the
    filtered tags (if succeeds).
    """
    return __list(*args, **kwargs)


def __list(query_args):
    """Returns a list of filtered tags.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered tags
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    query = models.Tag.query
    return query.filter_by(**query_args)


@blp.route(collection_url, methods=["POST"])
@blp.doc(operationId='CreateTag')
@auth.login_required()
@blp.arguments(schemas.CreateTag)
@blp.response(201, schemas.Tag)
def create(*args, **kwargs):
    """(Users) Uploads a new tag

    Use this method to create a new tags in the database so it can
    be accessed by the application users. The method returns the complete
    created tag (if succeeds).
    """
    return __create(*args, **kwargs)


def __create(body_args):
    """Creates a new tag in the database.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user is not registered
    :raises Conflict: Created object conflicts a database item
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: The tag created into the database.
    :rtype: :class:`models.Tag`
    """
    tag = models.Tag.create(body_args)

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Tag {body_args['name']} already submitted/exists"
        abort(409, messages={'error': error_msg})

    return tag


@blp.route(collection_url + ":search", methods=["GET"])
@blp.doc(operationId='SearchTag')
@blp.arguments(args.TagSearch, location='query')
@blp.response(200, schemas.Tags)
@queries.to_pagination()
@queries.add_sorting(models.Tag)
def search(*args, **kwargs):
    """(Public) Filters and list tags

    Use this method to get a list of tags based on a general search
    of terms. For example, calling this method with terms=v1&terms=0
    returns all tags with 'v1' and '0' on the 'name' or 'description'
    fields. The response returns a pagination object with the filtered
    tags (if succeeds).
    """
    return __search(*args, **kwargs)


def __search(query_args):
    """Filters and list tags using generic terms.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered tags
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    search = models.Tag.query
    for keyword in query_args.pop('terms'):
        search = search.filter(
            or_(
                models.Tag.name.contains(keyword),
                models.Tag.description.contains(keyword)
            ))
    return search.filter_by(**query_args)


@blp.route(resource_url, methods=["GET"])
@blp.doc(operationId='GetTag')
@blp.response(200, schemas.Tag)
def get(*args, **kwargs):
    """(Public) Retrieves tag details

    Use this method to retrieve a specific tag from the database.
    """
    return __get(*args, **kwargs)


def __get(id):
    """Returns the id matching tag.

    If no tag exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the tag to retrieve
    :type id: uuid
    :raises NotFound: No tag with id found
    :return: The database tag using the described id
    :rtype: :class:`models.Tag`
    """
    tag = models.Tag.read(id)
    if tag is None:
        error_msg = f"Record {id} not found in the database"
        abort(404, messages={'error': error_msg})
    else:
        return tag


@blp.route(resource_url, methods=["PUT"])
@blp.doc(operationId='UpdateTag')
@auth.admin_required()
@blp.arguments(schemas.Tag)
@blp.response(204)
def update(*args, **kwargs):
    """(Admins) Updates an existing tag

    Use this method to update a specific tag from the database.
    """
    return __update(*args, **kwargs)


def __update(body_args, id):
    """Updates a benchmark specific fields.

    If no tag exists with the indicated id, then 404 NotFound
    exception is raised.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :param id: The id of the tag to update
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No tag with id found
    :raises UnprocessableEntity: Wrong query/body parameters
    """
    tag = __get(id)
    tag.update(body_args)  # Only admins reach here

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = "Changes conflict submitted/existing tag"
        abort(409, messages={'error': error_msg})


@blp.route(resource_url, methods=["DELETE"])
@blp.doc(operationId='DeleteTag')
@auth.admin_required()
@blp.response(204)
def delete(*args, **kwargs):
    """(Admins) Deletes an existing tag

    Use this method to delete a specific tag from the database.
    """
    return __delete(*args, **kwargs)


def __delete(id):
    """Deletes the id matching tag.

    If no tag exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the tag to delete
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No tag with id found
    """
    tag = __get(id)
    tag.delete()

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})
