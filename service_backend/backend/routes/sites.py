"""Site URL routes. Collection of controller methods to create and
operate existing sites on the database.
"""
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .. import models, notifications
from ..extensions import auth, db
from ..schemas import args, schemas
from ..utils import queries

blp = Blueprint(
    'sites', __name__, description='Operations on sites'
)

collection_url = ""
resource_url = "/<uuid:id>"


@blp.route(collection_url, methods=['GET'])
@blp.doc(operationId='ListSites')
@blp.arguments(args.SiteFilter, location='query')
@blp.response(200, schemas.Sites)
@queries.to_pagination()
@queries.add_sorting(models.Site)
@queries.add_datefilter(models.Site)
def list(*args, **kwargs):
    """(Public) Filters and list sites

    Use this method to get a list of sites filtered according to your
    requirements. The response returns a pagination object with the
    filtered sites (if succeeds).
    """
    return __list(*args, **kwargs)


def __list(query_args):
    """Returns a list of filtered sites.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered sites
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    query = models.Site.query
    return query.filter_by(**query_args)


@blp.route(collection_url, methods=['POST'])
@auth.login_required()
@blp.doc(operationId='CreateSite')
@blp.arguments(schemas.CreateSite)
@blp.response(201, schemas.Site)
def create(*args, **kwargs):
    """(Users) Uploads a new site

    Use this method to create a new site in the database so it can
    be accessed by the application users. The method returns the complete
    created site (if succeeds).
    """
    return __create(*args, **kwargs)


def __create(body_args):
    """Creates a new site in the database.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user is not registered
    :raises Conflict: Created object conflicts a database item
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: The site created into the database.
    :rtype: :class:`models.Site`
    """
    site = models.Site.create(body_args)

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Site {body_args['name']} already submitted/exists"
        abort(409, messages={'error': error_msg})

    notifications.resource_submitted(site)
    return site


@blp.route(collection_url + ':search')
@blp.doc(operationId='SearchSites')
@blp.arguments(args.SiteSearch, location='query')
@blp.response(200, schemas.Sites)
@queries.to_pagination()
@queries.add_sorting(models.Site)
@queries.add_datefilter(models.Site)
def search(*args, **kwargs):
    """(Public) Filters and list sites

    Use this method to get a list of sites based on a general search
    of terms. For example, calling this method with terms=K&terms=T
    returns all sites with 'K' and 'T' on the 'name', 'address',
    or 'description' fields. The response returns a pagination object
    with the filtered sites (if succeeds).
    """
    return __search(*args, **kwargs)


def __search(query_args):
    """Filters and list sites.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered sites
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    search = models.Site.query
    for keyword in query_args.pop('terms'):
        search = search.filter(
            or_(
                models.Site.name.contains(keyword),
                models.Site.address.contains(keyword),
                models.Site.description.contains(keyword)
            ))
    return search.filter_by(**query_args)


@blp.route(resource_url, methods=['GET'])
@blp.doc(operationId='GetSite')
@blp.response(200, schemas.Site)
def get(*args, **kwargs):
    """(Public) Retrieves site details

    Use this method to retrieve a specific site from the database.
    """
    return __get(*args, **kwargs)


def __get(id):
    """Returns the id matching site.

    If no site exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the site to retrieve
    :type id: uuid
    :raises NotFound: No site with id found
    :return: The database site using the described id
    :rtype: :class:`models.Site`
    """
    site = models.Site.read(id)
    if site is None:
        error_msg = f"Record {id} not found in the database"
        abort(404, messages={'error': error_msg})
    else:
        return site


@blp.route(resource_url, methods=['PUT'])
@auth.admin_required()
@blp.doc(operationId='UpdateSite')
@blp.arguments(schemas.Site)
@blp.response(204)
def update(*args, **kwargs):
    """(Admins) Updates an existing site

    Use this method to update a specific site from the database.
    """
    return __update(*args, **kwargs)


def __update(body_args, id):
    """Updates a site specific fields.

    If no site exists with the indicated id, then 404 NotFound
    exception is raised.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :param id: The id of the site to update
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No site with id found
    :raises UnprocessableEntity: Wrong query/body parameters
    """
    site = __get(id)
    site.update(body_args, force=True)  # Only admins reach here

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = "Changes conflict submitted/existing site"
        abort(409, messages={'error': error_msg})


@blp.route(resource_url, methods=['DELETE'])
@auth.admin_required()
@blp.doc(operationId='DeleteSite')
@blp.response(204)
def delete(*args, **kwargs):
    """(Admins) Deletes an existing site

    Use this method to delete a specific site from the database.
    """
    return __delete(*args, **kwargs)


def __delete(id):
    """Deletes the id matching site.

    If no site exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the site to delete
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No site with id found
    """
    site = __get(id)
    site.delete()

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})


@blp.route(resource_url + ":approve", methods=["POST"])
@auth.admin_required()
@blp.doc(operationId='ApproveSite')
@blp.response(204)
def approve(*args, **kwargs):
    """(Admins) Approves a site to include it on default list methods

    Use this method to approve an specific site submitted by an user.
    It is a custom method, as side effect, it removes the submit report
    associated as it is no longer needed.
    """
    return __approve(*args, **kwargs)


def __approve(id):
    """Approves a site to include it on default list methods.

    :param id: The id of the site to approve
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No site with id found
    """
    site = __get(id)

    try:  # Approve site
        site.approve()
    except RuntimeError:
        error_msg = f"Site {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_approved(site)


@blp.route(resource_url + ":reject", methods=["POST"])
@blp.doc(operationId='RejectSite')
@auth.admin_required()
@blp.response(204)
def reject(*args, **kwargs):
    """(Admins) Rejects a site to safe delete it.

    Use this method instead of DELETE as it raises 422 in case the
    resource was already approved.

    Use this method to reject an specific site submitted by an user.
    It is a custom method, as side effect, it removes the submit report
    associated as it is no longer needed.
    """
    return __reject(*args, **kwargs)


def __reject(id):
    """Rejects a site to safe delete it.

    :param id: The id of the site to reject
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No site with id found
    """
    site = __get(id)
    uploader = site.uploader

    try:  # Reject site
        site.reject()
    except RuntimeError:
        error_msg = f"Site {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_rejected(uploader, site)


@blp.route(resource_url + '/flavors', methods=['GET'])
@blp.doc(operationId='ListFlavors')
@blp.arguments(args.FlavorFilter, location='query')
@blp.response(200, schemas.Flavors)
@queries.to_pagination()
@queries.add_sorting(models.Flavor)
@queries.add_datefilter(models.Flavor)
def list_flavors(*args, **kwargs):
    """(Public) Filters and list flavors

    Use this method to get a list of flavors filtered according to your
    requirements. The response returns a pagination object with the
    filtered flavors (if succeeds).
    """
    return __list_flavors(*args, **kwargs)


def __list_flavors(query_args, id):
    """ Lists the site flavors.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :param id: The id of the site to query the flavors
    :type id: uuid
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered flavors
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    __get(id)   # Return 404 if the site does not exist
    query = models.Flavor.query
    return query.filter_by(site_id=id, **query_args)


@blp.route(resource_url + '/flavors', methods=['POST'])
@auth.login_required()
@blp.doc(operationId='AddFlavor')
@blp.arguments(schemas.CreateFlavor)
@blp.response(201, schemas.Flavor)
def create_flavor(*args, **kwargs):
    """(Users) Uploads a new flavor

    Use this method to create a new flavors in the database so it can
    be accessed by the application users. The method returns the complete
    created flavor (if succeeds).
    """
    return __create_flavor(*args, **kwargs)


def __create_flavor(body_args, id):
    """Creates a flavor linked to a site id.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :param id: The id of the site where to add the flavor
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user is not registered
    :raises Conflict: Created object conflicts a database item
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: The flavor created into the database.
    :rtype: :class:`models.Flavor`
    """
    __get(id)   # Return 404 if the site does not exist
    body_args['site_id'] = id
    flavor = models.Flavor.create(body_args)

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Flavor {body_args['name']} already submitted/exists"
        abort(409, messages={'error': error_msg})

    notifications.resource_submitted(flavor)
    return flavor


@blp.route(resource_url + '/flavors:search', methods=['GET'])
@blp.doc(operationId='SearchFlavor')
@blp.arguments(args.FlavorSearch, location='query')
@blp.response(200, schemas.Flavors)
@queries.to_pagination()
@queries.add_sorting(models.Flavor)
@queries.add_datefilter(models.Flavor)
def search_flavors(*args, **kwargs):
    """(Public) Filters and list flavors

    Use this method to get a list of flavors based on a general search
    of terms. For example, calling this method with terms=K&terms=T
    returns all flavors with 'K' and 'T' on the 'name',
    or 'description' fields. The response returns a pagination object
    with the filtered flavors (if succeeds).
    """
    return __search_flavors(*args, **kwargs)


def __search_flavors(query_args, id):
    """Search flavors inside a site following generic terms.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered flavors
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    __get(id)   # Return 404 if the site does not exist
    search = models.Flavor.query.filter_by(site_id=id)
    for keyword in query_args.pop('terms'):
        search = search.filter(
            or_(
                models.Flavor.name.contains(keyword),
                models.Flavor.description.contains(keyword)
            ))
    return search.filter_by(**query_args)
