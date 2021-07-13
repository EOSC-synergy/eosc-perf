"""Site routes."""
from backend.extensions import auth
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

from . import models, schemas

blp = Blueprint(
    'sites', __name__, description='Operations on sites'
)


@blp.route('')
class Root(MethodView):

    @blp.arguments(schemas.SiteQueryArgs, location='query')
    @blp.response(200, schemas.Site(many=True))
    def get(self, args):
        """Filters and list sites."""
        return models.Site.filter_by(**args)

    @auth.login_required()
    @blp.arguments(schemas.Site, as_kwargs=True)
    @blp.response(201, schemas.Site)
    def post(self, **kwargs):
        """Creates a new site."""
        access_token = tokentools.get_access_token_from_request(request)
        report = models.SiteReport(
            uploader=models.User.get(token=access_token),
        )
        return models.Site.create(report=report, **kwargs)


@blp.route('/search')
class Search(MethodView):

    @blp.arguments(schemas.SearchQueryArgs, location='query')
    @blp.response(200, schemas.Site(many=True))
    def get(self, args):
        """Filters and list sites."""
        return models.Site.query_with(args['terms'])


@blp.route('/<uuid:site_id>')
class Site(MethodView):

    @blp.response(200, schemas.Site)
    def get(self, site_id):
        """Retrieves site details."""
        return models.Site.get_by_id(site_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditSite, as_kwargs=True)
    @blp.response(204)
    def put(self, site_id, **kwargs):
        """Updates an existing site."""
        models.Site.get_by_id(site_id).update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, site_id):
        """Deletes an existing site."""
        models.Site.get_by_id(site_id).delete()


@blp.route('/<uuid:site_id>/flavors')
class Flavors(MethodView):

    @blp.arguments(schemas.FlavorQueryArgs, location='query')
    @blp.response(200, schemas.Flavor(many=True))
    def get(self, args, site_id):
        """Filters and list flavors."""
        site_flavors = models.Site.get_by_id(site_id).flavors
        filter = lambda x, **kw: all(getattr(x, k) == v for k, v in kw.items())
        return [x for x in site_flavors if filter(x, **args)]

    @auth.login_required()
    @blp.arguments(schemas.Flavor, as_kwargs=True)
    @blp.response(201, schemas.Flavor)
    def post(self, site_id, **kwargs):
        """Creates a new flavor on a site."""
        access_token = tokentools.get_access_token_from_request(request)
        site = models.Site.get_by_id(site_id)
        report = models.FlavorReport(
            uploader=models.User.get(token=access_token),
        )
        flavor = models.Flavor(report=report, site_id=site.id, **kwargs)
        site.update(flavors=site.flavors+[flavor])
        return flavor


@blp.route('/flavors/<uuid:flavor_id>')
class Flavor(MethodView):

    @blp.response(200, schemas.Flavor)
    def get(self, flavor_id):
        """Retrieves flavor details."""
        return models.Flavor.get_by_id(id=flavor_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditFlavor, as_kwargs=True)
    @blp.response(204)
    def put(self, flavor_id, **kwargs):
        """Updates an existing site."""
        models.Flavor.get_by_id(id=flavor_id).update(**kwargs)

    @auth.admin_required()
    @blp.response(204)
    def delete(self, flavor_id):
        """Deletes an existing site."""
        models.Flavor.get_by_id(id=flavor_id).delete()
