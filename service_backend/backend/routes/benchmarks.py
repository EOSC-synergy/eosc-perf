"""Benchmark routes."""
from backend.extensions import auth
from backend.models import models
from backend.schemas import args, schemas
from flaat import tokentools
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint

blp = Blueprint(
    'benchmarks', __name__, description='Operations on benchmarks'
)


@blp.route('')
class Root(MethodView):
    """Class defining the main endpoint methods for benchmarks"""

    @blp.doc(operationId='GetBenchmarks')
    @blp.arguments(args.BenchmarkFilter, location='query')
    @blp.response(200, schemas.Benchmarks)
    def get(self, query_args):
        """(Free) Filters and list benchmarks

        Use this method to get a list of benchmarks filtered according to your 
        requirements. The response returns a pagination object with the
        filtered benchmarks (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered benchmarks
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        query = models.Benchmark.query.filter_by(**query_args)
        query = query.filter(~models.Benchmark.has_open_reports)
        return query.paginate(page, per_page)

    @auth.login_required()
    @blp.doc(operationId='AddBenchmark')
    @blp.arguments(schemas.BenchmarkCreate)
    @blp.response(201, schemas.Benchmark)
    def post(self, body_args):
        """(Users) Creates a new benchmark

        Use this method to create a new benchmarks in the database so it can
        be accessed by the application users. The method returns the complete
        created benchmark (if succeeds).
        ---

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user is not registered
        :raises UnprocessableEntity: Wrong query/body parameters 
        :raises Conflict: Created object conflicts a database item
        :return: The benchmark created into the database.
        :rtype: :class:`models.Benchmark`
        """
        access_token = tokentools.get_access_token_from_request(request)
        user = models.User.get(token=access_token)
        return models.Benchmark.create(
            reports=[models.Report(created_by=user, message="New benchmark")],
            created_by=user, **body_args
        )


@blp.route('/search')
class Search(MethodView):
    """Class defining the search endpoint for benchmarks"""

    @blp.doc(operationId='SearchBenchmarks')
    @blp.arguments(args.Search, location='query')
    @blp.response(200, schemas.Benchmarks)
    def get(self, query_args):
        """(Free) Filters and list benchmarks

        Use this method to get a list of benchmarks based on a general search
        of terms. For example, calling this method with terms=v1&terms=0
        returns all benchmarks with 'v1' and '0' on the 'docker_image',
        'docker_tag' or 'description' fields. The response returns a
        pagination object with the filtered benchmarks (if succeeds).
        ---

        :param query_args: The request query arguments as python dictionary
        :type query_args: dict
        :raises UnprocessableEntity: Wrong query/body parameters 
        :return: Pagination object with filtered benchmarks
        :rtype: :class:`flask_sqlalchemy.Pagination`
        """
        per_page = query_args.pop('per_page')
        page = query_args.pop('page')
        search = models.Benchmark.search(query_args['terms'])
        search = search.filter(~models.Benchmark.has_open_reports)
        return search.paginate(page, per_page)


@blp.route('/<uuid:benchmark_id>')
class Benchmark(MethodView):
    """Class defining the specific benchmark endpoint"""

    @blp.doc(operationId='GetBenchmark')
    @blp.response(200, schemas.Benchmark)
    def get(self, benchmark_id):
        """(Free) Retrieves benchmark details

        Use this method to retrieve a specific benchmark from the database.
        ---

        If no benchmark exists with the indicated id, then 404 NotFound
        exception is raised.

        :param benchmark_id: The id of the benchmark to retrieve
        :type benchmark_id: uuid
        :raises NotFound: No benchmark with id found
        :return: The database benchmark using the described id
        :rtype: :class:`models.Benchmark`
        """
        return models.Benchmark.get(benchmark_id)

    @auth.admin_required()
    @blp.doc(operationId='EditBenchmark')
    @blp.arguments(schemas.BenchmarkEdit)
    @blp.response(204)
    def put(self, body_args, benchmark_id):
        """(Admins) Updates an existing benchmark

        Use this method to update a specific benchmark from the database.
        ---

        If no benchmark exists with the indicated id, then 404 NotFound
        exception is raised.

        :param body_args: The request body arguments as python dictionary
        :type body_args: dict
        :param benchmark_id: The id of the benchmark to update
        :type benchmark_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No benchmark with id found
        :raises UnprocessableEntity: Wrong query/body parameters 
        """
        models.Benchmark.get(benchmark_id).update(**body_args)

    @auth.admin_required()
    @blp.doc(operationId='DelBenchmark')
    @blp.response(204)
    def delete(self, benchmark_id):
        """(Admins) Deletes an existing benchmark

        Use this method to delete a specific benchmark from the database.
        ---

        If no benchmark exists with the indicated id, then 404 NotFound
        exception is raised.

        :param benchmark_id: The id of the benchmark to delete
        :type benchmark_id: uuid
        :raises Unauthorized: The server could not verify the user identity
        :raises Forbidden: The user has not the required privileges
        :raises NotFound: No benchmark with id found
        """
        models.Benchmark.get(benchmark_id).delete()
