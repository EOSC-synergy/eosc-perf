"""Benchmark URL routes. Collection of controller methods to create and
operate existing benchmarks on the database.
"""
from flask_smorest import Blueprint, abort
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .. import models, notifications, utils
from ..extensions import auth, db
from ..schemas import args, schemas
from ..utils import queries

blp = Blueprint(
    'benchmarks', __name__, description='Operations on benchmarks'
)

collection_url = ""
resource_url = "/<uuid:id>"


@blp.route(collection_url, methods=["GET"])
@blp.doc(operationId='ListBenchmarks')
@blp.arguments(args.BenchmarkFilter, location='query')
@blp.response(200, schemas.Benchmarks)
@queries.to_pagination()
@queries.add_sorting(models.Benchmark)
@queries.add_datefilter(models.Benchmark)
def list(*args, **kwargs):
    """(Public) Filters and list benchmarks

    Use this method to get a list of benchmarks filtered according to your
    requirements. The response returns a pagination object with the
    filtered benchmarks (if succeeds).
    """
    return __list(*args, **kwargs)


def __list(query_args):
    """Returns a list of filtered benchmarks.

    :param query_args: The request query arguments as python dictionary
    :type query_args: dict
    :raises UnprocessableEntity: Wrong query/body parameters
    :return: Pagination object with filtered benchmarks
    :rtype: :class:`flask_sqlalchemy.Pagination`
    """
    query = models.Benchmark.query
    return query.filter_by(**query_args)


@blp.route(collection_url, methods=["POST"])
@blp.doc(operationId='CreateBenchmark')
@auth.login_required()
@blp.arguments(schemas.CreateBenchmark)
@blp.response(201, schemas.Benchmark)
def create(*args, **kwargs):
    """(Users) Uploads a new benchmark

    Use this method to create a new benchmarks in the database so it can
    be accessed by the application users. The method returns the complete
    created benchmark (if succeeds).

    Note: Benchmark use JSON Schemas to implement results validation.
    """
    return __create(*args, **kwargs)


def __create(body_args):
    """Creates a new benchmark in the database.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user is not registered
    :raises UnprocessableEntity: Wrong query/body parameters
    :raises Conflict: Created object conflicts a database item
    :return: The benchmark created into the database.
    :rtype: :class:`models.Benchmark`
    """
    image, tag = body_args['docker_image'], body_args['docker_tag']
    if not utils.dockerhub.valid_image(image, tag):
        error_msg = f"Image {image}:{tag} not found in dockerhub"
        abort(422, messages={'error': error_msg})

    benchmark = models.Benchmark.create(body_args)

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Benchmark {image}:{tag} already submitted/exists"
        abort(409, messages={'error': error_msg})

    notifications.resource_submitted(benchmark)
    return benchmark


@blp.route(collection_url + ":search", methods=["GET"])
@blp.doc(operationId='SearchBenchmarks')
@blp.arguments(args.BenchmarkSearch, location='query')
@blp.response(200, schemas.Benchmarks)
@queries.to_pagination()
@queries.add_sorting(models.Benchmark)
@queries.add_datefilter(models.Benchmark)
def search(*args, **kwargs):
    """(Public) Filters and list benchmarks

    Use this method to get a list of benchmarks based on a general search
    of terms. For example, calling this method with terms=v1&terms=0
    returns all benchmarks with 'v1' and '0' on the 'docker_image',
    'docker_tag' or 'description' fields. The response returns a
    pagination object with the filtered benchmarks (if succeeds).
    """
    return __search(*args, **kwargs)


def __search(query_args):
    """Filters and list benchmarks using generic terms.

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
    search = models.Benchmark.query
    for keyword in query_args.pop('terms'):
        search = search.filter(
            or_(
                models.Benchmark.docker_image.contains(keyword),
                models.Benchmark.docker_tag.contains(keyword),
                models.Benchmark.description.contains(keyword)
            ))
    return search.filter_by(**query_args)


@blp.route(resource_url, methods=["GET"])
@blp.doc(operationId='GetBenchmark')
@blp.arguments(args.Schema(), location='query', as_kwargs=True)
@blp.response(200, schemas.Benchmark)
def get(*args, **kwargs):
    """(Public) Retrieves benchmark details

    Use this method to retrieve a specific benchmark from the database.
    """
    return __get(*args, **kwargs)


def __get(id):
    """Returns the id matching benchmark.

    If no benchmark exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the benchmark to retrieve
    :type id: uuid
    :raises NotFound: No benchmark with id found
    :return: The database benchmark using the described id
    :rtype: :class:`models.Benchmark`
    """
    benchmark = models.Benchmark.read(id)
    if benchmark is None:
        error_msg = f"Benchmark {id} not found in the database"
        abort(404, messages={'error': error_msg})
    else:
        return benchmark


@blp.route(resource_url, methods=["PUT"])
@blp.doc(operationId='UpdateBenchmark')
@auth.admin_required()
@blp.arguments(schemas.Benchmark)
@blp.response(204)
def update(*args, **kwargs):
    """ (Admins) Implements JSON Put for benchmarks

    Use this method to update a specific benchmark from the database.
    """
    return __update(*args, **kwargs)


def __update(body_args, id):
    """Updates a benchmark specific fields.

    If no benchmark exists with the indicated id, then 404 NotFound
    exception is raised.

    :param body_args: The request body arguments as python dictionary
    :type body_args: dict
    :param id: The id of the benchmark to update
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No benchmark with id found
    :raises UnprocessableEntity: Wrong query/body parameters
    """
    image, tag = body_args['docker_image'], body_args['docker_tag']
    if not utils.dockerhub.valid_image(image, tag):
        error_msg = f"Image {image}:{tag} not found in dockerhub"
        abort(422, messages={'error': error_msg})

    benchmark = __get(id)
    benchmark.update(body_args, force=True)  # Only admins reach here

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = "Changes conflict submitted/existing benchmark"
        abort(409, messages={'error': error_msg})


@blp.route(resource_url, methods=["DELETE"])
@blp.doc(operationId='DeleteBenchmark')
@auth.admin_required()
@blp.arguments(args.Schema(), location='query', as_kwargs=True)
@blp.response(204)
def delete(*args, **kwargs):
    """(Admins) Deletes an existing benchmark

    Use this method to delete a specific benchmark from the database.
    """
    return __delete(*args, **kwargs)


def __delete(id):
    """Deletes the id matching benchmark.

    If no benchmark exists with the indicated id, then 404 NotFound
    exception is raised.

    :param id: The id of the benchmark to delete
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No benchmark with id found
    """
    benchmark = __get(id)
    benchmark.delete()

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})


@blp.route(resource_url + ":approve", methods=["POST"])
@blp.doc(operationId='ApproveBenchmark')
@auth.admin_required()
@blp.arguments(args.Schema(), location='query', as_kwargs=True)
@blp.response(204)
def approve(*args, **kwargs):
    """(Admins) Approves a benchmark to include it on default list methods

    Use this method to approve an specific benchmark submitted by an user.
    It is a custom method, as side effect, it removes the submit report
    associated as it is no longer needed.
    """
    return __approve(*args, **kwargs)


def __approve(id):
    """Approves a benchmark to include it on default list methods.

    :param id: The id of the benchmark to approve
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No benchmark with id found
    """
    benchmark = __get(id)

    try:  # Approve benchmark
        benchmark.approve()
    except RuntimeError:
        error_msg = f"Benchmark {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_approved(benchmark)


@blp.route(resource_url + ":reject", methods=["POST"])
@blp.doc(operationId='RejectBenchmark')
@auth.admin_required()
@blp.arguments(args.Schema(), location='query', as_kwargs=True)
@blp.response(204)
def reject(*args, **kwargs):
    """(Admins) Rejects a benchmark to safe delete it.

    Use this method instead of DELETE as it raises 422 in case the
    resource was already approved.
    Use this method to reject an specific benchmark submitted by an user.
    It is a custom method, as side effect, it removes the submit report
    associated as it is no longer needed.
    """
    return __reject(*args, **kwargs)


def __reject(id):
    """Rejects a benchmark to safe delete it.
    :param id: The id of the benchmark to reject
    :type id: uuid
    :raises Unauthorized: The server could not verify the user identity
    :raises Forbidden: The user has not the required privileges
    :raises NotFound: No benchmark with id found
    """
    benchmark = __get(id)
    uploader = benchmark.uploader

    try:  # Reject benchmark
        benchmark.reject()
    except RuntimeError:
        error_msg = f"Benchmark {id} was already approved"
        abort(422, messages={'error': error_msg})

    try:  # Transaction execution
        db.session.commit()
    except IntegrityError:
        error_msg = f"Conflict deleting {id}"
        abort(409, messages={'error': error_msg})

    notifications.resource_rejected(uploader, benchmark)
