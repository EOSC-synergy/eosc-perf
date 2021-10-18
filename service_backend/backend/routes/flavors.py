"""Flavor URL routes. Collection of controller methods to
operate existing flavors on the database.
"""
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from .. import models, notifications
from ..extensions import auth, db
from ..schemas import schemas

blp = Blueprint(
    'flavors', __name__, description='Operations on flavors'
)

collection_url = ""
resource_url = "/<uuid:id>"


@blp.route(resource_url, methods=["GET"])
@blp.doc(operationId='GetFlavor')
@blp.response(200, schemas.Flavor)
def get(*args, **kwargs):
    """(Public) Retrieves flavor details

    Use this method to retrieve a specific flavor from the database.
    """
    return __get(*args, **kwargs)


def __get(id):
    """Returns the id matching flavor.

    If no flavor exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the flavor to retrieve
    :type id: uuid
    :raises NotFound: No flavor with id found
    :return: The database flavor using the described id
    :rtype: :class:`models.Flavor`
    """
    flavor = models.Flavor.read(id)
    if flavor is None:
        error_msg = f"Record {id} not found in the database"
        abort(404, messages={'error': error_msg})
    else:
        return flavor


@blp.route(resource_url, methods=["PUT"])
@blp.doc(operationId='UpdateFlavor')
@auth.admin_required()
@blp.arguments(schemas.Flavor)
@blp.response(204)
def update(*args, **kwargs):
    """(Admins) Updates an existing flavor

    Use this method to update a specific flavor from the database.
    """
    return __update(*args, **kwargs)


def __update(body_args, id):
    """Updates a flavor specific fields.

    If no flavor exists with the indicated id, then 404 NotFound
    exception is raised.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :param id: The id of the flavor to update
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No flavor with id found
    :raises UnprocessableEntity: Wrong query/body parameters
    """
    flavor = models.Flavor.read(id)
    if flavor is None:
        error_msg = f"Record {id} not found in the database"
        abort(404, messages={'error': error_msg})

    flavor.update(body_args, force=True)  # Only admins reach here

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = "Changes conflict submitted/existing flavor"
        abort(409, messages={'error': error_msg})


@blp.route(resource_url, methods=["DELETE"])
@blp.doc(operationId='DeleteFlavor')
@auth.admin_required()
@blp.response(204)
def delete(*args, **kwargs):
    """(Admins) Deletes an existing flavor

    Use this method to delete a specific flavor from the database.
    """
    return __delete(*args, **kwargs)


def __delete(id):
    """Deletes the id matching flavor.

    If no flavor exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the flavor to delete
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No flavor with id found
    """
    flavor = models.Flavor.read(id)
    if flavor is None:
        error_msg = f"Record {id} not found in the database"
        abort(404, messages={'error': error_msg})

    flavor.delete()

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})


@blp.route(resource_url + ":approve", methods=["POST"])
@blp.doc(operationId='ApproveFlavor')
@auth.admin_required()
@blp.response(204)
def approve(*args, **kwargs):
    """(Admins) Approves a flavor to include it on default list methods

    Use this method to approve an specific flavor submitted by an user.
    It is a custom method, as side effect, it removes the submit report
    associated as it is no longer needed.
    """
    return __approve(*args, **kwargs)


def __approve(id):
    """Approves a flavor to include it on default list methods.

    :param id: The id of the flavor to approve
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No flavor with id found
    """
    flavor = __get(id)

    try:  # Approve flavor
        flavor.approve()
    except RuntimeError:
        error_msg = f"Flavor {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_approved(flavor)


@blp.route(resource_url + ":reject", methods=["POST"])
@blp.doc(operationId='RejectFlavor')
@auth.admin_required()
@blp.response(204)
def reject(*args, **kwargs):
    """(Admins) Rejects a flavor to safe delete it.

    Use this method instead of DELETE as it raises 422 in case the
    resource was already approved.

    Use this method to reject an specific flavor submitted by an user.
    It is a custom method, as side effect, it removes the submit report
    associated as it is no longer needed.
    """
    return __reject(*args, **kwargs)


def __reject(id):
    """Rejects a flavor to safe delete it.

    :param id: The id of the flavor to reject
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No flavor with id found
    """
    flavor = __get(id)
    uploader = flavor.uploader

    try:  # Reject flavor
        flavor.reject()
    except RuntimeError:
        error_msg = f"Flavor {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_rejected(uploader, flavor)


@blp.route(resource_url + '/site', methods=["GET"])
@blp.response(200, schemas.Site)
@blp.doc(operationId='GetFlavorSite')
def site(*args, **kwargs):
    """(Public) Retrieves flavor site details

    Use this method to retrieve the site information from a
    specific flavor in the database.
    """
    return __site(*args, **kwargs)


def __site(id):
    """Returns the flavor site.

    If no flavor exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the flavor contained by the site
    :type id: uuid
    :raises NotFound: No flavor with id found
    :return: The database site which contains the described id
    :rtype: :class:`models.Site`
    """
    flavor = __get(id)
    return models.Site.read(flavor.site_id)
