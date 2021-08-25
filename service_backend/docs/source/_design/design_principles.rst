Design principles
*******************
EOSC Performance API is designed to run as a container service so it can
be deployed with container technologies such as Docker and Kubernetes.

.. graphviz:: ../../diagrams/services.dot

You should be able to access the backend from the frontend network.
in production it is recommended to run a reverse proxy container which
provides HTTPS layer althoug for development it can be enough just to 
export the port 5000 where Flask normally runs.


Container network
===================




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
incomming connections. By default it is the 5432, althoug for security 
reasons is always recommended to use a different port and always keep the
container running with the last security updates.



Production vs development
=========================



Settings
=========================
You can get a full list of configurable environment variables from
the :doc:`configuration settings</_backend/settings>` page.


