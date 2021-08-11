"""Result routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import args, schemas
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import and_

blp = Blueprint(
    'results', __name__, description='Operations on results'
)


@blp.route('')
class Root(MethodView):

    @blp.doc(operationId='GetResults')
    @blp.arguments(args.ResultFilter, location='query', as_kwargs=True)
    @blp.response(200, schemas.Results)
    def get(
        self, tag_names=None, before=None, after=None, filters=None, 
        page=1, per_page=100, **kwargs
    ):
        """Filters and list results.

        Method to get a list of results based on a query based matching
        conditions:

         - **docker_image**: Returns results matching the docker image.
         - **docker_tag**: Returns results matching the docker tag.
         - **site_name**: Returns results matching the site name.
         - **flavor_name**: Returns results matching the flavor name.
         - **tag_names**: Returns results matching the list of tag names.
         - **upload_before**: Returns results uploaded before a ISO8601 date.
         - **upload_after**: Returns results uploaded after a ISO8601 date.
         - **filters**: A set of matching conditions (to describe bellow).

        This method allows to return results filtered by values inside the
        result. The filter is composed by 3 arguments separated by spaces
        ('%20' on URL-encoding): <path.separated.by.dots> <operator> <value>

        There are five filter operators:

         - **Equals ( == :: %3D%3D )**: Return results where path value is
           exact to the query value. 
           For example *filters=cpu.count%20%3D%3D%205*
         - **Greater than ( > :: %3E )**: Return results where path value 
           strictly greater than the query value.
           For example *filters=cpu.count%20%3E%205*
         - **Less than ( < :: %3C )**: Return results where path value strictly
           lower than the query value.
           For example *filters=cpu.count%20%3C%205*
         - **Greater or equal ( >= :: %3E%3D )**: Return results where path value
           is equal or greater than the query value.
           For example *filters=cpu.count%20%3E%3D%205*
         - **Less or equal ( <= :: %3C%3D )**: Return results where path value is
           equal or lower than the query value.
           For example *filters=cpu.count%20%3C%3D%205*

        Note that all the components of the filter must be URL-encoded in
        order to be included in URL query strings. You can use the swagger GUI
        to automatically handle the codification, but the space separator must
        be included.

        ---

        :param docker_image: Constraints the results returned to only those
               using a benchmark with a specific docker image
        :type docker_image: String, optional
        :param docker_tag: Constraints the results returned to only those
               using a benchmark with a specific docker tag
        :type docker_tag: String, optional
        :param site_name: Constraints the results returned to only those
               performed on a specific site
        :type site_name: String, optional
        :param flavor_name: Constraints the results returned to only those
               performed with an specific VM flavor
        :type flavor_name: String, optional
        :param tag_names: Constraints the results returned to only those
               containing a specific set of tags
        :type tag_names: List[String], optional
        :param before: Constraints the results returned to only those
               uploaded before an specific ISO8601 date
        :type before: ISO8601 date, optional
        :param after: Constraints the results returned to only those
               uploaded after an specific ISO8601 date
        :type after: ISO8601 date, optional
        :param filters: Constraints the results returned to only those
               that pass a certain list of conditions (filters)
        :type filters: List[String], optional
        :return: An sqlalchemy query which returns the filtered results.
        :rtype: flask_sqlalchemy.BaseQuery
        """
        # First query definition using main filters
        query = models.Result.query.filter_by(**kwargs)

        # Extend query with tags
        if type(tag_names) == list:
            for tag_name in tag_names:
                query = query.filter(
                    models.Result.tag_names.in_([tag_name]))

        # Extend query with date filter
        if before:
            query = query.filter(models.Result.created_at < before)
        if after:
            query = query.filter(models.Result.created_at > after)

        # Extend query with filters
        parsed_filters = []
        for filter in filters:
            try:
                path, operator, value = tuple(filter.split(' '))
            except ValueError as err:
                abort(422, messages={
                    'filter': filter, 'reason': err.args,
                    'hint': "Probably missing spaces (%20)",
                    'example': "filters=machine.cpu.count%20%3E%205"
                })
            path = tuple(path.split('.'))
            if operator is None:
                abort(422, "filter operator not defined")
            elif operator == "<":
                parsed_filters.append(models.Result.json[path] < value)
            elif operator == ">":
                parsed_filters.append(models.Result.json[path] > value)
            elif operator == ">=":
                parsed_filters.append(models.Result.json[path] >= value)
            elif operator == "<=":
                parsed_filters.append(models.Result.json[path] <= value)
            elif operator == "==":
                parsed_filters.append(models.Result.json[path] == value)
            else:
                abort(422, message={
                    'filter': f"Unknown filter operator: '{operator}'",
                    'hint': "Use only one of ['==', '>', '<', '>=', '<=']"
                })
        try:
            query = query.filter(and_(True, *parsed_filters))
        except Exception as err:
            abort(422, message={'filter': err.args})

        query = query.filter(~models.Result.has_open_reports)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddResult')
    @blp.arguments(args.ResultContext, location='query')
    @blp.arguments(schemas.Json)
    @blp.response(201, schemas.Result)
    def post(self, args, json):
        """Creates a new result."""
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        report = models.Report(
            created_by=user, message="New result created",
            verdict=True  # Does not require accept from admin
        )
        return models.Result.create(
            json=json, created_by=user, reports=[report],
            benchmark=models.Benchmark.get(args['benchmark_id']),
            site=models.Site.get(args['site_id']),
            flavor=models.Flavor.get(args['flavor_id']),
            tags=[models.Tag.get(id) for id in args['tags_ids']]
        )


@blp.route('/search')
class Search(MethodView):

    @blp.doc(operationId='SearchResults')
    @blp.arguments(args.Search, location='query', as_kwargs=True)
    @blp.response(200, schemas.Results)
    def get(self, terms, page=1, per_page=100):
        """Filters and list results."""
        search = models.Result.search(terms)
        search = search.filter(~models.Result.has_open_reports)
        return search.paginate(page, per_page)


@blp.route('/<uuid:result_id>')
class Result(MethodView):

    @blp.doc(operationId='GetResult')
    @blp.response(200, schemas.Result)
    def get(self, result_id):
        """Retrieves result details."""
        return models.Result.get(result_id)

    @auth.login_required()
    @blp.doc(operationId='EditResult')
    @blp.arguments(schemas.TagsIds, as_kwargs=True)
    @blp.response(204)
    def put(self, result_id, tags_ids=None):
        """Updates an existing result tags."""
        access_token = tokentools.get_access_token_from_request(request)
        result = models.Result.get(result_id)
        def is_owner(): 
            user = models.User.get(token=access_token)
            return result.created_by.email == user.email
        if auth.valid_admin() or is_owner():
            if tags_ids is not None:  # Empty list should pass
                tags = [models.Tag.get(id) for id in tags_ids]
                result.update(tags=tags)
        else:
            abort(403)

    @auth.admin_required()
    @blp.doc(operationId='DelResult')
    @blp.response(204)
    def delete(self, result_id):
        """Deletes an existing result."""
        models.Result.get(result_id).delete()


@blp.route('/<uuid:result_id>/uploader')
class Uploader(MethodView):

    @auth.admin_required()
    @blp.doc(operationId='GetResultUploader')
    @blp.response(200, schemas.User)
    def get(self, result_id):
        """Retrieves result uploader."""
        return models.Result.get(result_id).created_by


@blp.route('/<uuid:result_id>/report')
class Report(MethodView):

    @auth.login_required()
    @blp.doc(operationId='AddResultReport')
    @blp.arguments(schemas.ReportCreate)
    @blp.response(201, schemas.Report)
    def post(self, json, result_id):
        """Creates a result report."""
        access_token = tokentools.get_access_token_from_request(request)
        result = models.Result.get(result_id)
        report = models.Report(
            created_by=models.User.get(token=access_token),
            message=json['message']
        )
        result.update(reports=result.reports+[report])
        return report
