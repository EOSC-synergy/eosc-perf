"""Result routes."""
from backend.extensions import auth
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from . import models, schemas


blp = Blueprint(
    'results', __name__, description='Operations on results'
)


@blp.route('')
class Root(MethodView):

    @auth.login_required()  # Mitigate DoS attack
    @blp.arguments(schemas.FilterQueryArgs, location='query', as_kwargs=True)
    @blp.response(200, schemas.Result(many=True))
    def get(self, tag_names=None, **kwargs):
        """Filters and list results."""
        query = models.Result.query.filter_by(**kwargs)
        if type(tag_names) == list:
            query = query.filter(models.Result.tag_names.in_(tag_names))
        return query.all()

    @auth.login_required()
    @blp.arguments(schemas.CreateQueryArgs, location='query')
    @blp.arguments(schemas.Json)
    @blp.response(201, schemas.Result)
    def post(self, query_args, json):
        """Creates a new result."""
        access_token = tokentools.get_access_token_from_request(request)
        token_info = tokentools.get_accesstoken_info(access_token)
        try:
            return models.Result.create(
                uploader_sub=token_info['body']['sub'],
                uploader_iss=token_info['body']['iss'],
                json=json, **query_args
            )
        except models.db.exc.NoResultFound:
            abort(404)
        except models.db.exc.MultipleResultsFound:
            abort(422, "Provided query returns multiple results")


@blp.route('/<uuid:result_id>')
class Result(MethodView):

    @blp.response(200, schemas.Result)
    def get(self, result_id):
        """Retrieves result details."""
        return models.Result.get_by_id(result_id)

    @auth.admin_required()
    @blp.arguments(schemas.EditResult, as_kwargs=True)
    @blp.response(204)
    def put(self, result_id, **kwargs):
        """Updates an existing result."""
        try:
            result = models.Result.get_by_id(result_id)
            result.update(**kwargs)
        except models.db.exc.NoResultFound:
            abort(404)
        except models.db.exc.MultipleResultsFound:
            abort(422, "Provided relation returns multiple results")

    @auth.admin_required()
    @blp.response(204)
    def delete(self, result_id):
        """Deletes an existing result."""
        models.Result.get_by_id(result_id).delete()
