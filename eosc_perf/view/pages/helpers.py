"""Helpers for page factories."""
import json
from typing import Callable, Any

from flask import Response, redirect
from werkzeug.urls import url_encode

from eosc_perf.controller.io_controller import controller


def error_json_redirect(message: str) -> Response:
    """Builder for redirect JSON responses.

    These are necessary because AJAX queries do not follow regular redirects.

    Args:
        message (str): The error message to display.
    Returns:
        Response: A Flask JSON-data response.
    """
    json_data = json.dumps({'redirect': '/error?' + url_encode({'text': message})})
    return Response(json_data, mimetype='application/json', status=302)


def error_redirect(message: str) -> Response:
    """Builder for redirect responses.

    Args:
        message (str): The error message to display.
    Returns:
        Response: A Flask redirect.
    """
    args = {'text': message}
    return redirect('/error?' + url_encode(args), code=302)


def info_redirect(message: str) -> Response:
    """Builder for redirect responses.

    Args:
        message (str): Info message to display:
    Returns:
        Response: A Flask redirect.
    """
    args = {'text': message}
    return redirect('/info?' + url_encode(args), code=302)


def only_authenticated(function: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator helper for authentication.

    Args:
        function (Callable[..., Any]): Function to wrap.
    """
    def wrapper(*args) -> Callable[..., Any]:
        if not controller.is_authenticated():
            return error_redirect("Not allowed: not authenticated.")
        return function(*args)

    # ugly hack for flask decorator name collisions
    wrapper.__name__ = function.__name__

    return wrapper


def only_admin(function: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator helper for authentication.
    """
    def wrapper(*args) -> Callable[..., Any]:
        if not controller.is_admin():
            return error_redirect("Not allowed: not an administrator.")
        return function(args)

    # ugly hack for flask decorator name collisions
    wrapper.__name__ = function.__name__

    return wrapper


def only_authenticated_json(function: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator helper for authentication.

    Args:
        function (Callable[..., Any]): Function to decorate.
    """
    def wrapper(*args) -> Callable[..., Any]:
        if not controller.is_authenticated():
            return error_json_redirect("Not allowed: not authenticated.")
        return function(*args)

    # ugly hack for flask decorator name collisions
    wrapper.__name__ = function.__name__

    return wrapper


def only_admin_json(function: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator helper for authentication.
    """
    def wrapper(*args) -> Callable[..., Any]:
        if not controller.is_admin():
            return error_json_redirect("Not allowed: not an administrator.")
        return function(args)

    # ugly hack for flask decorator name collisions
    wrapper.__name__ = function.__name__

    return wrapper
