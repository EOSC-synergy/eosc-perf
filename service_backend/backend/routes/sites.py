"""Site routes."""
from backend.extensions import auth
from backend.models import models
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

    @blp.doc(operationId='GetSites')
    @blp.arguments(args.SiteFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Sites)
    def get(self, page=1, per_page=100, **kwargs):
        """Filters and list sites."""
        query = models.Site.query.filter_by(**kwargs)
        query = query.filter(~models.Site.has_open_reports)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddSite')
    @blp.arguments(schemas.SiteCreate, as_kwargs=True)
    @blp.response(201, schemas.Site)
    def post(self, **kwargs):
        """Creates a new site."""
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        report = models.Report(created_by=user)
        return models.Site.create(created_by=user, reports=[report], **kwargs)


@blp.route('/search')
class Search(MethodView):

    @blp.doc(operationId='SearchSites')
    @blp.arguments(args.SiteSearch, location='query', as_kwargs=True)
    @blp.response(200, schemas.Sites)
    def get(self, terms, page=1, per_page=100):
        """Filters and list sites."""
        search = models.Site.search(terms)
        search = search.filter(~models.Site.has_open_reports)
        return search.paginate(page, per_page)


@blp.route('/<uuid:site_id>')
class Site(MethodView):

    @blp.doc(operationId='GetSite')
    @blp.response(200, schemas.Site)
    def get(self, site_id):
        """Retrieves site details."""
        return models.Site.get(site_id)

    @auth.admin_required()
    @blp.doc(operationId='EditSite')
    @blp.arguments(schemas.SiteEdit, as_kwargs=True)
    @blp.response(204)
    def put(self, site_id, **kwargs):
        """Updates an existing site."""
        models.Site.get(site_id).update(**kwargs)

    @auth.admin_required()
    @blp.doc(operationId='DelSite')
    @blp.response(204)
    def delete(self, site_id):
        """Deletes an existing site."""
        models.Site.get(site_id).delete()


@blp.route('/<uuid:site_id>/flavors')
class Flavors(MethodView):

    @blp.doc(operationId='GetFlavors')
    @blp.arguments(args.FlavorFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Flavors)
    def get(self, site_id, page=1, per_page=100, **kwargs):
        """Filters and list flavors."""
        query = models.Flavor.query.filter_by(site_id=site_id, **kwargs)
        query = query.filter(~models.Flavor.has_open_reports)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddFlavor')
    @blp.arguments(schemas.FlavorCreate, as_kwargs=True)
    @blp.response(201, schemas.Flavor)
    def post(self, site_id, **kwargs):
        """Creates a new flavor on a site."""
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        site = models.Site.get(site_id)
        report = models.Report(created_by=user)
        return models.Flavor.create(
            created_by=user, reports=[report],
            site_id=site.id, **kwargs
        )


@blp.route('/flavors/<uuid:flavor_id>')
class Flavor(MethodView):

    @blp.response(200, schemas.Flavor)
    @blp.doc(operationId='GetFlavor')
    def get(self, flavor_id):
        """Retrieves flavor details."""
        return models.Flavor.get(id=flavor_id)

    @auth.admin_required()
    @blp.doc(operationId='EditFlavor')
    @blp.arguments(schemas.FlavorEdit, as_kwargs=True)
    @blp.response(204)
    def put(self, flavor_id, **kwargs):
        """Updates an existing site."""
        models.Flavor.get(id=flavor_id).update(**kwargs)

    @auth.admin_required()
    @blp.doc(operationId='DelFlavor')
    @blp.response(204)
    def delete(self, flavor_id):
        """Deletes an existing site."""
        models.Flavor.get(id=flavor_id).delete()
