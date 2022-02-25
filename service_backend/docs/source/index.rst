Welcome to EOSC Performance API's documentation!
================================================

.. meta::
    :description lang=en: Use EOSC Performance as a REST API.

Compare and analyze benchmark results from diverse cluster providers at the
European Open Science Cloud (EOSC) using our Representational State Transfer
(REST) Application Program Interface (API).


Getting started with EOSC Performance API
-----------------------------------------

Learn more about how to use our endpoints to get valuable benchmark results
from multiple providers or how to submit yours.

* **First steps**:
  :doc:`Getting started </getting-started/introduction>` |
  :doc:`First example </getting-started/first_example>`

* **Overview of core features**:
  :doc:`benchmarks </features/benchmarks>` |
  :doc:`reports </features/reports>` |
  :doc:`results </features/results>` |
  :doc:`sites </features/sites>` |
  :doc:`tags </features/tags>`

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Getting started

    /getting-started/introduction
    /getting-started/first_example

    /features/benchmarks
    /features/reports
    /features/results
    /features/sites
    /features/tags


Advanced features of EOSC Performance API
-----------------------------------------

EOSC Performance API offers many advanced features and options.
Learn more about these integrations and how you can get the most
out of your application when using our endpoints.

* **Advanced search and result filtering**:
  :doc:`Using advanced search </advanced/generic-search>` |
  :doc:`Filter results by json values </advanced/json-filters>` |

* **Pagination and sorting of responses**:
  :doc:`How to use sorting and pagination </advanced/pagination-sorting>`

.. toctree::
    :maxdepth: 2
    :hidden:
    :glob:
    :caption: Advanced features

    /advanced/generic-search
    /advanced/json-filters
    /advanced/pagination-sorting


Extending EOSC Performance
-----------------------------------------

EOSC Performance is an open source project which hopes to evolve and
provide with the time better functionalities to the users. Our source
code was build in order to be understandable and easy to maintain by
the community. Any help is welcome, therefore we have prepare a section
where developers can understand better the bases of the application.

* **Design principles**:
  :doc:`containers, networks and databases </_design/design_principles>`

* **Application package documentation**:
  :doc:`Modules, Classes and Functions </_backend/backend>`

* **Database interface with Python**:
  :doc:`Instantiate multiple models with Factories </_factories/factories/>`

.. toctree::
    :maxdepth: 2
    :hidden:
    :glob:
    :caption: Developers

    /_design/design_principles
    /_backend/backend
    /_factories/factories


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
