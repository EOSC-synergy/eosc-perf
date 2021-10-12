"""Module with tools to handle sql filters."""
from sqlalchemy import Boolean, Float

str_booleans = [
    "true", "True", "TRUE",
    "false", "False", "FALSE",
]


def new_filter(model, filter):
    path, operator, value = tuple(filter.split(' '))
    path = tuple(path.split('.'))

    try:  # Resolve the correct operation
        value = float(value)
        element = model.json[path].astext.cast(Float)
    except ValueError:
        if value in str_booleans:
            element = model.json[path].astext.cast(Boolean)
        else:
            element = model.json[path].astext

    if operator is None:
        raise KeyError("Filter operator not defined")
    elif operator == "<":
        return element < value
    elif operator == ">":
        return element > value
    elif operator == ">=":
        return element <= value
    elif operator == "<=":
        return element <= value
    elif operator == "==":
        return element == value
    else:
        raise KeyError(f"Unknown filter operator: '{operator}'")
