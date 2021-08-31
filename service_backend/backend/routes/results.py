"""Results URL routes. Collection of controller methods to create and
operate existing benchmark results on the database.
"""
from backend import models, notifications
from backend.extensions import auth
from backend.schemas import args, schemas
from backend.utils import queries
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy import and_, or_

blp = Blueprint(
    'results', __name__, description='Operations on results'
)


@blp.route('')
class Root(MethodView):
    """Class defining the main endpoint methods for results"""

    @blp.doc(operationId='GetResults')
    @blp.arguments(args.ResultFilter, location='query')
    @blp.response(200, schemas.Results)
    @queries.to_pagination()
    @queries.add_sorting(models.Result)
    def get(self, query_args):
        """(Free) Filters and list results

        Use this method to get a list of results filtered according to your 
        requirements. The response returns a pagination object with the
        filtered results (if succeeds).

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

        Note the URL-encoding is only needed when accessing the function as 
        HTTP request. The python call handles the filters only as strings. 

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered results
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        query = models.Result.query  # Create the base query

        # Extend query with tags
        for tag_name in query_args.pop('tag_names'):
            query = query.filter(models.Result.tag_names.in_([tag_name]))

        # Extend query with date filter
        before = query_args.pop('before')
        if before:
            query = query.filter(models.Result.upload_datetime < before)
        after = query_args.pop('after')
        if after:
            query = query.filter(models.Result.upload_datetime > after)

        # Extend query with filters
        parsed_filters = []
        for filter in query_args.pop('filters'):
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

        # Model filter with remaining standard parameters
        query = query.filter(~models.Result.has_open_reports)
        return query.filter_by(**query_args)

    @auth.login_required()
    @blp.doc(operationId='AddResult')
    @blp.arguments(args.ResultContext, location='query')
    @blp.arguments(schemas.Json)
    @blp.response(201, schemas.Result)
    def post(self, query_args, body_args):
        """(Users) Uploads a new result

        Use this method to create a new result in the database so it can
        be accessed by the application users. The method returns the complete
        created result (if succeeds).

        Note: The uploaded result must pass the benchmark JSON Schema to be
        accepted, otherwise 422 UnprocessableEntity is produced.
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dic
        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user is not registered
        :raises NotFound: One or more query items do not exist in the database
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: The result created into the database.
        :rtype: :class:`models.Result`
        """
        return models.Result.create(dict(
            json=body_args,
            benchmark=models.Benchmark.get(query_args.pop('benchmark_id')),
            site=models.Site.get(query_args.pop('site_id')),
            flavor=models.Flavor.get(query_args.pop('flavor_id')),
            tags=[models.Tag.get(id) for id in query_args.pop('tags_ids')],
            **query_args
        ))


@blp.route('/search')
class Search(MethodView):
    """Class defining the search endpoint for results"""

    @blp.doc(operationId='SearchResults')
    @blp.arguments(args.Search, location='query')
    @blp.response(200, schemas.Results)
    @queries.to_pagination()
    @queries.add_sorting(models.Result)
    def get(self, query_args):
        """(Free) Filters and list results

        Use this method to get a list of results based on a general search
        of terms. For example, calling this method with terms=v1&terms=0
        returns all results with 'v1' and '0' on the 'docker_image',
        'docker_tag', 'site_name', 'flavor_name' fields or 'tags'. 
        The response returns a pagination object with the filtered results
        (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered results
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        search = models.Result.query
        for keyword in query_args['terms']:
            search = search.filter(
                or_(
                    models.Result.docker_image.contains(keyword),
                    models.Result.docker_tag.contains(keyword),
                    models.Result.site_name.contains(keyword),
                    models.Result.flavor_name.contains(keyword),
                    models.Result.tag_names == keyword
                ))
        return search.filter(~models.Result.has_open_reports)


@blp.route('/<uuid:result_id>')
class Result(MethodView):
    """Class defining the specific result endpoint"""

    @blp.doc(operationId='GetResult')
    @blp.response(200, schemas.Result)
    def get(self, result_id):
        """(Free) Retrieves result details

        Use this method to retrieve a specific result from the database.
        ---

        If no result exists with the indicated id, then 404 NotFound
        exception is raised.

        :param result_id: The id of the result to retrieve
        :type result_id: uuid
        :raises NotFound: No result with id found
        :return: The database result using the described id
        :rtype: :class:`models.Result`
        """
        return models.Result.get(result_id)

    @auth.login_required()
    @blp.doc(operationId='EditResult')
    @blp.arguments(schemas.TagsIds)
    @blp.response(204)
    def put(self, body_args, result_id):
        """(Owner) Updates an existing result tags

        Use this method to update tags on a specific result from the database.
        ---

        If no result exists with the indicated id, then 404 NotFound
        exception is raised.

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :param result_id: The id of the result to update
        :type result_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No result with id found
        :raises UnprocessableEntity: Wrong query/body parameters 
        """
        result = models.Result.get(result_id)
        if 'tags_ids' in body_args:
            tags_ids = body_args.pop('tags_ids')
            body_args['tags'] = [models.Tag.get(id) for id in tags_ids]
        result.update(body_args, force=auth.valid_admin())

    @auth.admin_required()
    @blp.doc(operationId='DelResult')
    @blp.response(204)
    def delete(self, result_id):
        """(Admins) Deletes an existing result

        Use this method to delete a specific result from the database.
        ---

        If no result exists with the indicated id, then 404 NotFound
        exception is raised.

        :param result_id: The id of the result to delete
        :type result_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No result with id found
        """
        models.Result.get(result_id).delete()


@blp.route('/<uuid:result_id>/uploader')
class Uploader(MethodView):
    """Class defining the endpoint to retrieve a result uploader"""

    @auth.admin_required()
    @blp.doc(operationId='GetResultUploader')
    @blp.response(200, schemas.User)
    def get(self, result_id):
        """(Admins) Retrieves result uploader

        Use this method to retrieve the uploader of a specific result
        from the database.
        ---

        If no result exists with the indicated id, then 404 NotFound
        exception is raised.        

        :param result_id: The id of the result created by the returned user
        :type result_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No result with id found
        """
        return models.Result.get(result_id).uploader


@blp.route('/<uuid:result_id>/report')
class Report(MethodView):
    """Class defining the endpoint to create result reports"""

    @auth.login_required()
    @blp.doc(operationId='AddResultReport')
    @blp.arguments(schemas.ReportCreate)
    @blp.response(201, schemas.Report)
    def post(self, body_args, result_id):
        """(Users) Creates a result report

        Use this method to create a report for a specific result so the
        administrators are aware of issues. The reported result is hidden
        from generic responses until the issue is corrected and approved
        by the administrators. 
        ---

        If no result exists with the indicated id, then 404 NotFound
        exception is raised.        

        :param result_id: The id of the result created by the returned user
        :type result_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user is not registered
        :raises NotFound: No result with id found
        :raises UnprocessableEntity: Wrong query/body parameters 
        """
        result = models.Result.get(result_id)
        report = models.Report(message=body_args['message'])
        # Any user is able to add result reports
        result.update({'reports': result.reports+[report]}, force=True)
        notifications.report_created(report)
        return report
