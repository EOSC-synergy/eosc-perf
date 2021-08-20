"""This is the main web application package for the EOSC Performance
Application Program Interface (API).

The application is developed using python and flask as main engines.
By default, Flask does not provide database or specific web abstraction
layers. API and any other functionality such database or authentication
are handled by independent libraries and extension.
"""
from .app import create_app

all = ["create_app"]
