"""Tag routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import query_args, schemas
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'tags', __name__, description='Operations on tags'
)


@blp.route('')
class Root(MethodView):

    @blp.doc(operationId='GetTags')
    @blp.arguments(query_args.TagFilter, location='query')
    @blp.response(200, schemas.Tag(many=True))
    def get(self, args):
        """Filters and list tags."""
        return models.Tag.filter_by(**args)

    @auth.login_required()
    @blp.doc(operationId='AddTag')
    @blp.arguments(schemas.TagCreate, as_kwargs=True)
    @blp.response(201, schemas.Tag)
    def post(self, **kwargs):
        """Creates a new tag."""
        return models.Tag.create(**kwargs)


@blp.route('/search')
class Search(MethodView):

    @blp.doc(operationId='SearchTags')
    @blp.arguments(query_args.TagSearch, location='query')
    @blp.response(200, schemas.Tag(many=True))
    def get(self, search):
        """Filters and list tags."""
        return models.Tag.query_with(**search)


@blp.route('/<uuid:tag_id>')
class Tag(MethodView):

    @blp.doc(operationId='GetTag')
    @blp.response(200, schemas.Tag)
    def get(self, tag_id):
        """Retrieves tag details."""
        return models.Tag.get_by_id(tag_id)

    @auth.admin_required()
    @blp.doc(operationId='EditTag')
    @blp.arguments(schemas.TagEdit, as_kwargs=True)
    @blp.response(204)
    def put(self, tag_id, **kwargs):
        """Updates an existing tag."""
        models.Tag.get_by_id(tag_id).update(**kwargs)

    @auth.admin_required()
    @blp.doc(operationId='DelTag')
    @blp.response(204)
    def delete(self, tag_id):
        """Deletes an existing tag."""
        models.Tag.get_by_id(tag_id).delete()
