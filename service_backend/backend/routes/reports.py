"""Report URL routes. Collection of controller methods to create and
operate existing reports on the database.
"""
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from .. import models, notifications
from ..extensions import auth, db
from ..schemas import args, schemas
from ..utils import queries

blp = Blueprint(
    'reports', __name__, description='Operations on reports'
)

submits_url = '/submits'
result_claims_url = '/claims'
result_claim_url = result_claims_url + '/<uuid:id>'


@blp.route(submits_url, methods=['GET'])
@auth.admin_required()
@blp.doc(operationId='ListSubmits')
@blp.arguments(args.SubmitFilter, location='query')
@blp.response(200, schemas.Submits)
@queries.to_pagination()
@queries.add_sorting(models.Submit)
@queries.add_datefilter(models.Submit)
def list_submits(*args, **kwargs):
    """(Admins) Filters and list  submits

    Use this method to get a list of submits filtered according to your
    requirements. The response returns a pagination object with the
    filtered submits (if succeeds).
    """
    return __list_submits(*args, **kwargs)


def __list_submits(query_args):
    """ Returns a list of submit reports.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered submits
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    query = models.Submit.query
    return query.filter_by(**query_args)


@blp.route(result_claims_url, methods=['GET'])
@blp.doc(operationId='ListClaims')
@auth.admin_required()
@blp.arguments(args.ClaimFilter, location='query')
@blp.response(200, schemas.Claims)
@queries.to_pagination()
@queries.add_sorting(models.Claim)
@queries.add_datefilter(models.Claim)
def list_claims(*args, **kwargs):
    """(Admins) Filters and lists claims

    Use this method to get a list of claims filtered according to your
    requirements. The response returns a pagination object with the
    filtered claims (if succeeds).
    """
    return __list_claims(*args, **kwargs)


def __list_claims(query_args):
    """Returns a list of claims reports.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered claims
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    query = models.Claim.query
    return query.filter_by(**query_args)


@blp.route(result_claim_url, methods=['GET'])
@blp.doc(operationId='GetClaim')
@auth.admin_required()
@blp.response(200, schemas.Claim)
def get(*args, **kwargs):
    """(Public) Retrieves claim details

    Use this method to retrieve a specific claim from the database.
    """
    return __get(*args, **kwargs)


def __get(id):
    """Returns the id matching claim.

    If no result exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the claim to retrieve
    :type id: uuid
    :raises NotFound: No claim with id found
    :return: The database result using the described id
    :rtype: :class:`models.Claim`
    """
    claim = models.Claim.read(id)
    if claim is None:
        error_msg = f"Claim {id} not found in the database"
        abort(404, messages={'error': error_msg})
    else:
        return claim


@blp.route(result_claim_url + ':approve', methods=['POST'])
@blp.doc(operationId='ApproveClaim')
@auth.admin_required()
@blp.arguments(args.Schema(), location='query', as_kwargs=True)
@blp.response(204)
def approve_claim(*args, **kwargs):
    """(Admin) Accepts an existing claim

    Use this method to approve an specific resource submitted by an user.
    It is a custom method, as side effect, it removes the submit report
    associated as it is no longer needed.
    """
    return __approve_claim(*args, **kwargs)


def __approve_claim(id):
    """Accepts the id matching claim.

    If no submit exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the submit to approve
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No submit with id found
    :raises UnprocessableEntity: Resource already approved
    """
    claim = models.Claim.read(id)
    if claim is None:
        error_msg = f"Claim {id} not found in the database"
        abort(404, messages={'error': error_msg})

    try:  # Approve claim resource
        claim.approve()
    except RuntimeError:
        error_msg = f"Resource {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_approved(claim)


@blp.route(result_claim_url + ':reject', methods=['POST'])
@blp.doc(operationId='RejectClaim')
@auth.admin_required()
@blp.arguments(args.Schema(), location='query', as_kwargs=True)
@blp.response(204)
def reject_claim(*args, **kwargs):
    """(Admin) Refuses an existing claim

    Use this method to reject an specific resource submitted by an user.
    It is a custom method, as side effect, it removes the resource and
    the submit report associated as it is no longer needed.
    """
    return __reject_claim(*args, **kwargs)


def __reject_claim(id):
    """Refuses the id matching claim.

    If no submit exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the submit to reject
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No benchmark with id found
    :raises UnprocessableEntity: Resource already approved
    """
    claim = models.Claim.read(id)
    if claim is None:
        error_msg = f"Claim {id} not found in the database"
        abort(404, messages={'error': error_msg})

    uploader = claim.uploader
    try:  # Reject claim resource
        claim.reject()
    except RuntimeError:
        error_msg = f"Resource {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_rejected(uploader, claim)
    if not claim.resource.deleted:
        notifications.result_restored(claim.resource)
