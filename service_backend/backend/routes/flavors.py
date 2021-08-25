"""Flavor URL routes. Collection of controller methods to 
operate existing flavors on the database.
"""
from backend import models
from backend.extensions import auth
from backend.schemas import schemas
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'flavors', __name__, description='Operations on sites'
)

@blp.route('/<uuid:flavor_id>')
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
        # Only admins can access this function so it is safe to set force
        models.Flavor.get(id=flavor_id).update(body_args, force=True)

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


@blp.route('/<uuid:flavor_id>/site')
class Site(MethodView):
    """Class defining the specific flavor site endpoint"""

    @blp.response(200, schemas.Site)
    @blp.doc(operationId='GetFlavorSite')
    def get(self, flavor_id):
        """(Free) Retrieves flavor site details

        Use this method to retrieve the site information from a
        specific flavor in the database.
        ---

        If no flavor exists with the indicated id, then 404 NotFound
        exception is raised.

        :param flavor_id: The id of the flavor which contains the site
        :type flavor_id: uuid
        :raises NotFound: No flavor with id found
        :return: The database site which contains the described flavor_id
        :rtype: :class:`models.Site`
        """
        flavor = models.Flavor.get(id=flavor_id)
        return models.Site.get(id=flavor.site_id)
