"""Tag routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import args, schemas
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'tags', __name__, description='Operations on tags'
)


@blp.route('')
class Root(MethodView):

    @blp.doc(operationId='GetTags')
    @blp.arguments(args.TagFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Tags)
    def get(self, page=1, per_page=100, **kwargs):
        """Filters and list tags."""
        query = models.Tag.query.filter_by(**kwargs)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddTag')
    @blp.arguments(schemas.TagCreate, as_kwargs=True)
    @blp.response(201, schemas.Tag)
    def post(self, **kwargs):
        """Creates a new tag."""
        return models.Tag.create(**kwargs)


@blp.route('/search')
class Search(MethodView):

    @blp.arguments(args.TagSearch, location='query', as_kwargs=True)
    @blp.response(200, schemas.Tags)
    def get(self, terms, page=1, per_page=100):
        """Filters and list tags."""
        search = models.Tag.search(terms)
        return search.paginate(page, per_page)


@blp.route('/<uuid:tag_id>')
class Tag(MethodView):

    @blp.doc(operationId='GetTag')
    @blp.response(200, schemas.Tag)
    def get(self, tag_id):
        """Retrieves tag details."""
        return models.Tag.get(tag_id)

    @auth.admin_required()
    @blp.doc(operationId='EditTag')
    @blp.arguments(schemas.TagEdit, as_kwargs=True)
    @blp.response(204)
    def put(self, tag_id, **kwargs):
        """Updates an existing tag."""
        models.Tag.get(tag_id).update(**kwargs)

    @auth.admin_required()
    @blp.doc(operationId='DelTag')
    @blp.response(204)
    def delete(self, tag_id):
        """Deletes an existing tag."""
        models.Tag.get(tag_id).delete()
