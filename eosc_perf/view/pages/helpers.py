"""Helpers for page factories."""
import json
from flask import Response, redirect
from werkzeug.urls import url_encode


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
