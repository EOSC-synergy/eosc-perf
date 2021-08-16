"""Tag routes."""
from backend import models
from backend.extensions import auth
from backend.schemas import args, schemas
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'tags', __name__, description='Operations on tags'
)


@blp.route('')
class Root(MethodView):
    """Class defining the main endpoint methods for tags"""

    @blp.doc(operationId='GetTags')
    @blp.arguments(args.TagFilter, location='query')
    @blp.response(200, schemas.Tags)
    def get(self, query_args):
        """(Free) Filters and list tags

        Use this method to get a list of tags filtered according to your 
        requirements. The response returns a pagination object with the
        filtered tags (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered tags
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        query = models.Tag.query.filter_by(**query_args)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddTag')
    @blp.arguments(schemas.TagCreate)
    @blp.response(201, schemas.Tag)
    def post(self, body_args):
        """(Users) Creates a new tag

        Use this method to create a new tags in the database so it can
        be accessed by the application users. The method returns the complete
        created tag (if succeeds).
        ---

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user is not registered
        :raises Conflict: Created object conflicts a database item
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: The tag created into the database.
        :rtype: :class:`models.Tag`
        """
        access_token = tokentools.get_access_token_from_request(request)
        models.User.get(token=access_token)  # Check user is registered
        return models.Tag.create(**body_args)


@blp.route('/search')
class Search(MethodView):
    """Class defining the search endpoint for tags"""

    @blp.arguments(args.Search, location='query')
    @blp.response(200, schemas.Tags)
    def get(self, query_args):
        """(Free) Filters and list tags

        Use this method to get a list of tags based on a general search
        of terms. For example, calling this method with terms=v1&terms=0
        returns all tags with 'v1' and '0' on the 'name' or 'description'
        fields. The response returns a pagination object with the filtered
        tags (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered tags
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        search = models.Tag.search(query_args['terms'])
        return search.paginate(page, per_page)


@blp.route('/<uuid:tag_id>')
class Tag(MethodView):
    """Class defining the specific tag endpoint"""

    @blp.doc(operationId='GetTag')
    @blp.response(200, schemas.Tag)
    def get(self, tag_id):
        """(Free) Retrieves tag details

        Use this method to retrieve a specific tag from the database.
        ---

        If no tag exists with the indicated id, then 404 NotFound
        exception is raised.

        :param tag_id: The id of the tag to retrieve
        :type tag_id: uuid
        :raises NotFound: No tag with id found
        :return: The database tag using the described id
        :rtype: :class:`models.Tag`
        """
        return models.Tag.get(tag_id)

    @auth.admin_required()
    @blp.doc(operationId='EditTag')
    @blp.arguments(schemas.TagEdit)
    @blp.response(204)
    def put(self, body_args, tag_id):
        """(Admins) Updates an existing tag

        Use this method to update a specific tag from the database.
        ---

        If no tag exists with the indicated id, then 404 NotFound
        exception is raised.

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :param tag_id: The id of the tag to update
        :type tag_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No tag with id found
        :raises UnprocessableEntity: Wrong query/body parameters 
        """
        models.Tag.get(tag_id).update(**body_args)

    @auth.admin_required()
    @blp.doc(operationId='DelTag')
    @blp.response(204)
    def delete(self, tag_id):
        """(Admins) Deletes an existing tag

        Use this method to delete a specific tag from the database.
        ---

        If no tag exists with the indicated id, then 404 NotFound
        exception is raised.

        :param tag_id: The id of the tag to delete
        :type tag_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No tag with id found
        """
        models.Tag.get(tag_id).delete()
