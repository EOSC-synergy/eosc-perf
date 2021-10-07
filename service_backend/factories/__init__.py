"""Factories package to with classes to create easily new instances
in the backend database. This package is based into the library`factory boy`
and the subpackage `models` for more information visit the following
links:

- Factory boy: https://factoryboy.readthedocs.io/en/stable/
- Models: :doc:`/_backend/models`

Note that in order to create new instances, you need to implement an
application context. For example, to create a new user you can use:

.. code-block:: python

    import factories    # Import the factories package
    import backend      # Import the backend package

    app = backend.create_app()  # Create an application using a DB
    with app.app_context():     # Use an application context
        # Create your instances from here
        factories.DBUser(email="user1@email.com")

Important: If you want to use the objects produced to be usable
outside the scope of the session, you need to expunge them for the session.
For more examples, see http://flask-sqlalchemy.pocoo.org/contexts/
"""
from .factories import DBBenchmark, DBFlavor, DBResult, DBSite, DBTag, DBUser

__all__ = [
    "DBBenchmark",
    "DBResult",
    "DBSite",
    "DBFlavor",
    "DBTag",
    "DBUser"
]
