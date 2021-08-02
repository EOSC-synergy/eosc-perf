"""Site URL routes. Collection of controller methods to create and
operate existing sites on the database.
"""
from backend import models, notifications
from backend.extensions import auth
from backend.schemas import args, schemas
from backend.utils import queries
from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy import or_

blp = Blueprint(
    'sites', __name__, description='Operations on sites'
)


@blp.route('')
class Root(MethodView):
    """Class defining the main endpoint methods for sites"""

    @blp.doc(operationId='GetSites')
    @blp.arguments(args.SiteFilter, location='query')
    @blp.response(200, schemas.Sites)
    @queries.to_pagination()
    @queries.add_sorting(models.Site)
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
        query = models.Site.query.filter_by(**query_args)
        return query.filter(~models.Site.has_open_reports)

    @auth.login_required()
    @blp.doc(operationId='AddSite')
    @blp.arguments(schemas.SiteCreate)
    @blp.response(201, schemas.Site)
    def post(self, body_args):
        """(Users) Uploads a new site

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
        site = models.Site.create(body_args)
        notifications.report_created(site.reports[0])
        return site


@blp.route('/search')
class Search(MethodView):
    """Class defining the search endpoint for sites"""

    @blp.doc(operationId='SearchSites')
    @blp.arguments(args.Search, location='query')
    @blp.response(200, schemas.Sites)
    @queries.to_pagination()
    @queries.add_sorting(models.Site)
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
        search = models.Site.query
        for keyword in query_args['terms']:
            search = search.filter(
                or_(
                    models.Site.name.contains(keyword),
                    models.Site.address.contains(keyword),
                    models.Site.description.contains(keyword)
                ))
        return search.filter(~models.Site.has_open_reports)


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
        # Only admins can access this function so it is safe to set force
        models.Site.get(site_id).update(body_args, force=True)

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
    @queries.to_pagination()
    @queries.add_sorting(models.Flavor)
    def get(self, query_args, site_id):
        """(Free) Filters and list flavors

        Use this method to get a list of flavors filtered according to your 
        requirements. The response returns a pagination object with the
        filtered flavors (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :param site_id: The id of the site to query the flavors
        :type site_id: uuid
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered flavors
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        query = models.Flavor.query.filter_by(site_id=site_id, **query_args)
        return query.filter(~models.Flavor.has_open_reports)

    @auth.login_required()
    @blp.doc(operationId='AddFlavor')
    @blp.arguments(schemas.FlavorCreate)
    @blp.response(201, schemas.Flavor)
    def post(self, body_args, site_id):
        """(Users) Uploads a new flavor

        Use this method to create a new flavors in the database so it can
        be accessed by the application users. The method returns the complete
        created flavor (if succeeds).
        ---

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :param site_id: The id of the site where to add the flavor
        :type site_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user is not registered
        :raises Conflict: Created object conflicts a database item
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: The flavor created into the database.
        :rtype: :class:`models.Flavor`
        """
        site_id = models.Site.get(site_id).id,  # Trigger NotFound
        flavor = models.Flavor.create(dict(site_id=site_id, **body_args))
        notifications.report_created(flavor.reports[0])
        return flavor


@blp.route('/<uuid:site_id>/flavors/search')
class SearchFlavors(MethodView):
    """Class defining the search endpoint for flavors"""

    @blp.doc(operationId='SearchFlavor')
    @blp.arguments(args.Search, location='query')
    @blp.response(200, schemas.Flavors)
    @queries.to_pagination()
    @queries.add_sorting(models.Flavor)
    def get(self, query_args, site_id):
        """(Free) Filters and list flavors

        Use this method to get a list of flavors based on a general search
        of terms. For example, calling this method with terms=K&terms=T
        returns all flavors with 'K' and 'T' on the 'name', 
        or 'description' fields. The response returns a pagination object
        with the filtered flavors (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered flavors
        :rtype: :class:`flask_sqlalchemy.Pagination`        
        """
        search = models.Flavor.query
        search = search.filter_by(site_id=site_id)
        for keyword in query_args['terms']:
            search = search.filter(
                or_(
                    models.Flavor.name.contains(keyword),
                    models.Flavor.description.contains(keyword)
                ))
        return search.filter(~models.Flavor.has_open_reports)