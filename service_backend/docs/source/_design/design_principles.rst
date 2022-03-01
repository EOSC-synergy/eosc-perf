Design principles
*******************
EOSC Performance API is designed to run as a container service so it can
be deployed with container technologies such as Docker and Kubernetes.

.. graphviz:: ../../diagrams/services.dot

You should be able to access the backend from the frontend network.
in production it is recommended to run a reverse proxy container which
provides HTTPS layer although for development it can be enough just to
export the port 5000 where Flask normally runs.


Data storage
===================
The main container includes all the dependencies to run the software,
however, it is designed to store the data into an external postgresql_
database, normally deployed as a `container <postgresql_container_>`_.
See the :doc:`configuration settings</_backend/settings>` to know more
details about how to configure the application to connect to the external
database.

.. _postgresql: https://www.postgresql.org/
.. _postgresql_container: https://hub.docker.com/_/postgres

When deploying the database as a container using a container orchestrator,
it recommended to connect it to the "backend-net" network so all the
backend related containers such as the backend itself or a backup service
can access the required ports.

In case the database has to be managed outside the container network, it
is generally a good idea to export the port where postgresql listens the
incoming connections. By default it is the 5432, although for security
reasons is always recommended to use a different port and always keep the
container running with the last security updates.


Production vs development
=========================
You can control the environment as production or development configuring
the environmental variable `FLASK_ENV`. This variable can take the following
values and behaviors:

 - `production`: Backend service runs enforcing security requirements and
   performance processing. You should always run the application as production
   except for specific short executions for development. Testing should run
   as well in production to ensure the correct behavior of components.

 - `development`: Backend service runs with minimum security requirements and
   with additional loads for debugging. When running in development the number
   open queries might be limited to the specific used extension. Therefore it is
   not suitable for long running operations. In addition, some variables
   required for production might be optional, see :doc:`configuration settings</_backend/settings>`
   for more details about defaults when running on development mode.


Settings
=========================
You can get a full list of configurable environment variables from
the :doc:`configuration settings</_backend/settings>` page.


