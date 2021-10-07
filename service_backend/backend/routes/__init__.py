"""Backend package for the collection of the API URLs routes definitions.

The API uses routes to determine which controller and action method to
execute. Routes should use meaningful URL users can remember and use
directly when interfacing the API.

All routes defined in this package are build based on flask blueprints
and the extension flask_smorest. This allows to split the routes between
multiple sections collecting the related methods per module.

The flask extension flask_smorest allows to produce a OpenAPI JSON
specification which can be used by automation tools. For example swagger
can use such specification to produce an user friendly GUI for the API.
"""
from . import benchmarks, flavors, reports, results, sites, tags, users

__all__ = ["benchmarks", "flavors", "reports",
           "results", "sites", "tags", "users"]
