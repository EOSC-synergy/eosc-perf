"""Site routes."""
from backend import models
from backend.extensions import auth
from backend.schemas import args, schemas
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'sites', __name__, description='Operations on sites'
)


@blp.route('')
class Root(MethodView):
    """Class defining the main endpoint methods for sites"""

    @blp.doc(operationId='GetSites')
    @blp.arguments(args.SiteFilter, location='query')
    @blp.response(200, schemas.Sites)
    def get(self, query_args):
        """(Free) Filters and list sites
        
        Use this method to get a list of sites filtered according to your 
        requirements. The response returns a pagination object with the
        filtered sites (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered sites
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        query = models.Site.query.filter_by(**query_args)
        query = query.filter(~models.Site.has_open_reports)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddSite')
    @blp.arguments(schemas.SiteCreate)
    @blp.response(201, schemas.Site)
    def post(self, body_args):
        """(Users) Creates a new site

        Use this method to create a new site in the database so it can
        be accessed by the application users. The method returns the complete
        created site (if succeeds).
        ---

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user is not registered
        :raises Conflict: Created object conflicts a database item
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: The site created into the database.
        :rtype: :class:`models.Site`
        """
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        return models.Site.create(
            reports = [models.Report(created_by=user, message="New site")],
            created_by=user, **body_args
        )


@blp.route('/search')
class Search(MethodView):
    """Class defining the search endpoint for sites"""

    @blp.doc(operationId='SearchSites')
    @blp.arguments(args.Search, location='query')
    @blp.response(200, schemas.Sites)
    def get(self, query_args):
        """(Free) Filters and list sites
        
        Use this method to get a list of sites based on a general search
        of terms. For example, calling this method with terms=K&terms=T
        returns all sites with 'K' and 'T' on the 'name', 'address', 
        or 'description' fields. The response returns a pagination object
        with the filtered sites (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered sites
        :rtype: :class:`flask_sqlalchemy.Pagination`        
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        search = models.Site.search(query_args['terms'])
        search = search.filter(~models.Site.has_open_reports)
        return search.paginate(page, per_page)


@blp.route('/<uuid:site_id>')
class Site(MethodView):
    """Class defining the specific site endpoint"""

    @blp.doc(operationId='GetSite')
    @blp.response(200, schemas.Site)
    def get(self, site_id):
        """(Free) Retrieves site details

        Use this method to retrieve a specific site from the database.
        ---

        If no site exists with the indicated id, then 404 NotFound
        exception is raised.

        :param site_id: The id of the site to retrieve
        :type site_id: uuid
        :raises NotFound: No site with id found
        :return: The database site using the described id
        :rtype: :class:`models.Site`
        """
        return models.Site.get(site_id)

    @auth.admin_required()
    @blp.doc(operationId='EditSite')
    @blp.arguments(schemas.SiteEdit)
    @blp.response(204)
    def put(self, body_args, site_id):
        """(Admins) Updates an existing site

        Use this method to update a specific site from the database.
        ---

        If no site exists with the indicated id, then 404 NotFound
        exception is raised.

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :param site_id: The id of the site to update
        :type site_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No site with id found
        :raises UnprocessableEntity: Wrong query/body parameters 
        """
        models.Site.get(site_id).update(**body_args)

    @auth.admin_required()
    @blp.doc(operationId='DelSite')
    @blp.response(204)
    def delete(self, site_id):
        """(Admins) Deletes an existing site

        Use this method to delete a specific site from the database.
        ---

        If no site exists with the indicated id, then 404 NotFound
        exception is raised.

        :param site_id: The id of the site to delete
        :type site_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No site with id found
        """
        models.Site.get(site_id).delete()


@blp.route('/<uuid:site_id>/flavors')
class Flavors(MethodView):

    @blp.doc(operationId='GetFlavors')
    @blp.arguments(args.FlavorFilter, location='query')
    @blp.response(200, schemas.Flavors)
    def get(self, query_args, site_id):
        """(Free) Filters and list flavors

        Use this method to get a list of flavors filtered according to your 
        requirements. The response returns a pagination object with the
        filtered flavors (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered flavors
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        query = models.Flavor.query.filter_by(site_id=site_id, **query_args)
        query = query.filter(~models.Flavor.has_open_reports)
        return query.paginate(page, per_page)


    @auth.login_required()
    @blp.doc(operationId='AddFlavor')
    @blp.arguments(schemas.FlavorCreate)
    @blp.response(201, schemas.Flavor)
    def post(self, body_args, site_id):
        """(Users) Creates a new flavor

        Use this method to create a new flavors in the database so it can
        be accessed by the application users. The method returns the complete
        created flavor (if succeeds).
        ---

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user is not registered
        :raises Conflict: Created object conflicts a database item
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: The flavor created into the database.
        :rtype: :class:`models.Flavor`
        """
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        return models.Flavor.create(
            site_id=models.Site.get(site_id).id,  # Trigger NotFound
            reports=[models.Report(created_by=user, message="New flavor")],
            created_by=user, **body_args
        )


@blp.route('/flavors/<uuid:flavor_id>')
class Flavor(MethodView):
    """Class defining the specific flavor endpoint"""

    @blp.response(200, schemas.Flavor)
    @blp.doc(operationId='GetFlavor')
    def get(self, flavor_id):
        """(Free) Retrieves flavor details

        Use this method to retrieve a specific flavor from the database.
        ---

        If no flavor exists with the indicated id, then 404 NotFound
        exception is raised.

        :param flavor_id: The id of the flavor to retrieve
        :type flavor_id: uuid
        :raises NotFound: No flavor with id found
        :return: The database flavor using the described id
        :rtype: :class:`models.Flavor`
        """
        return models.Flavor.get(id=flavor_id)

    @auth.admin_required()
    @blp.doc(operationId='EditFlavor')
    @blp.arguments(schemas.FlavorEdit)
    @blp.response(204)
    def put(self, body_args, flavor_id):
        """(Admins) Updates an existing flavor

        Use this method to update a specific flavor from the database.
        ---

        If no flavor exists with the indicated id, then 404 NotFound
        exception is raised.

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :param flavor_id: The id of the flavor to update
        :type flavor_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No flavor with id found
        :raises UnprocessableEntity: Wrong query/body parameters 
        """
        models.Flavor.get(id=flavor_id).update(**body_args)

    @auth.admin_required()
    @blp.doc(operationId='DelFlavor')
    @blp.response(204)
    def delete(self, flavor_id):
        """(Admins) Deletes an existing flavor

        Use this method to delete a specific flavor from the database.
        ---

        If no flavor exists with the indicated id, then 404 NotFound
        exception is raised.

        :param flavor_id: The id of the flavor to delete
        :type flavor_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No flavor with id found
        """
        models.Flavor.get(id=flavor_id).delete()
