"""Helpers for page factories."""
import json
from flask import Response, redirect
from werkzeug.urls import url_encode

def error_json_redirect(message: str) -> Response:
    """Builder for redirect JSON responses.

    These are necessary because AJAX queries do not follow regular redirects."""
    json_data = json.dumps({'redirect': '/error?' + url_encode({'text': message})})
    return Response(json_data, mimetype='application/json', status=302)

def error_redirect(message: str) -> Response:
    """Builder for redirect responses."""
    args = {'text': message}
    return redirect('/error?' + url_encode(args), code=302)
