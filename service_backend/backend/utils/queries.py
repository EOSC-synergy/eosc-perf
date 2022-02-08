"""Module with tools to unify query common operations."""
import functools

import flask_smorest


def to_pagination():
    """Decorator to convert the result query into a pagination object.

    :return: Decorated function
    :rtype: fun
    """
    def decorator_add_sorting(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            """Converts the query into a pagination object."""
            query_args = args[0]
            per_page = query_args.pop("per_page")
            page = query_args.pop("page")
            query = func(*args, **kwargs)
            return query.paginate(page, per_page)
        return decorator
    return decorator_add_sorting


def add_sorting(model):
    """Decorator to add sorting functionality to a controller method.

    :param model: Model with containing the sorting field
    :type model: :class:`backend.model.core.BaseModel`
    :return: Decorated function
    :rtype: fun
    """
    def decorator_add_sorting(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            """Returns a sorting sql object from a model and a field control.
            The field must be preceded with a control character:
            - '+' return an ascending sort object
            - '-' return a descending sort object
            """
            query_args = args[0]
            sort_by = query_args.pop("sort_by")
            sort_by = sort_by if sort_by is not None else ""
            query = func(*args, **kwargs)
            split = sort_by.split(",")
            sorting = [parse_sort(model, x) for x in split if x != ""]
            return query.order_by(*sorting)
        return decorator
    return decorator_add_sorting


def parse_sort(model, control_field):
    if hasattr(model, "json") and control_field[1:6] == "json.":
        field = json_field(model, control_field)
    else:
        field = generic_field(model, control_field)
    operator = control_field[0]
    if operator == "+":
        return field.asc()
    if operator == "-":
        return field.desc()
    else:
        flask_smorest.abort(
            422,
            message={
                "KeyError": f"Unknown order operator '{operator}'",
                "hint": "Use '+'(asc) or '-'(desc) before sort field",
            },
        )


def json_field(model, control_field):
    path = control_field[6:]
    return path_iter(model.json, path.split("."))


def path_iter(fields, path):
    if path == []:
        return fields
    else:
        return path_iter(fields[path[0]], path[1:])


def generic_field(model, control_field):
    try:
        return model.__dict__[control_field[1:]]
    except KeyError as err:
        flask_smorest.abort(
            422,
            message={
                "KeyError": f"Unexpected field '{err.args[0]}'",
                "hint": "Use ',' to separate fields",
            },
        )


def add_datefilter(model):
    """Decorator to add date filter to the request.

    :return: Decorated function
    :rtype: fun
    """
    def decorator_add_datefilter(func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            """Extends the returned function query with time filters."""
            query_args = args[0]
            before = query_args.pop("upload_before", None)
            after = query_args.pop("upload_after", None)
            query = func(*args, **kwargs)
            if before:
                query = query.filter(model.upload_datetime < before)
            if after:
                query = query.filter(model.upload_datetime > after)
            return query
        return decorator
    return decorator_add_datefilter
