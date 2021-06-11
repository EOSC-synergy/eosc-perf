"""Tag routes."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas
from backend.authorization import login_required, admin_required

blp = Blueprint(
    'tags', __name__, description='Operations on tags'
)


@blp.route('')
class Root(MethodView):

    @login_required()  # Mitigate DoS attack
    @blp.arguments(schemas.TagsQueryArgs, location='query')
    @blp.response(200, schemas.Tag(many=True))
    def get(self, args):
        """Filters and list tags."""
        return models.Tag.filter_by(**args)

    @login_required()
    @blp.arguments(schemas.Tag, as_kwargs=True)
    @blp.response(201, schemas.Tag)
    def post(self, **kwargs):
        """Creates a new tag."""
        return models.Tag.create(**kwargs)


@blp.route('/<uuid:tag_id>')
class Tag(MethodView):

    @blp.response(200, schemas.Tag)
    def get(self, tag_id):
        """Retrieves tag details."""
        return models.Tag.get_by_id(tag_id)

    @admin_required()
    @blp.arguments(schemas.EditTag, as_kwargs=True)
    @blp.response(204)
    def put(self, tag_id, **kwargs):
        """Updates an existing tag."""
        models.Tag.get_by_id(tag_id).update(**kwargs)

    @admin_required()
    @blp.response(204)
    def delete(self, tag_id):
        """Deletes an existing tag."""
        models.Tag.get_by_id(tag_id).delete()
