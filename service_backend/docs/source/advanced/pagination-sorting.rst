**********************
Sorting and Pagination
**********************

EOSC Performance database expects to include hundreds of results
from multiple providers. Therefore, every query into the database has
to be optimized to what it is really required by the user.

In addition, multiple list methods are public and available to the
internet. Therefore, it is required for security reasons and performance
that most responses from the API are paginated and limited.


Pagination response
======================
API responses for list methods (called by `GET`) are limited by default
to a maximum of **100** items per page. In order to provide the user with
enough information about the omitted items (if any) on the search, a paginated
body has always the following fields:

 - **has_next**: True if a next page exists.
 - **has_prev**: True if a previous page exists
 - **items**: The items for the current page
 - **next_num**: Number of the next page
 - **prev_num**: Number of the previous page.
 - **page**: The current page number (1 indexed)
 - **pages**: The total number of pages
 - **per_page**: The number of items to displayed on the page.
 - **total**: The total number of items matching the query

To control the returned page, you can configure the following arguments
on the request query:

 - **per_page**: The number of items to be displayed on a page.
 - **page**: The page index to return.

Default query argument values (when not included) are ``per_page=100``
and ``page=1``. The maximum value for ``per_page`` is 100.

.. note::
    Note that modifying the argument ``per_page`` might shift the 
    items returned on previous pages therefore not matching with 
    the expected ``page`` items. The number of global pages depends
    on the ``per_page`` assigned value.


Sorting response items
======================
It is possible to sort the response items including sorting fields into the
the ``sort_by`` argument. This argument is available on every list method for
the main endpoints (``/benchmark``, ``/results``, ``/sites`` and ``/flavors``).

All sorting fields are composed by a **sorting operator** which defines
the order of the sorting and a **field id** which indicates the field to
use. In addition, it is possible to include more than one sorting requirement
into the argument by separating them using commas ``,`` without spaces.
Note the following available sorting operators and equivalent order:

 - ``+``: Sorts the results in ascendant order. For example *sort=+name*
    .. code-block::

            ["item_1", "item_2", "item_3"]


 - ``-``: Sorts the results in descendant order. For example *sort=-name*
    .. code-block::

            ["item_3", "item_2", "item_1"]


In the case of results, you might be interested into sorting by an
specific result field inside the json attribute. This behavior is
similar to the already explained into :doc:`/advanced/json-filters`.

When sorting by a json field use a `path separated by dots` to indicate
where to find the value you desire to use to sort. In addition, remember 
that in general it is a good idea to apply take a look into the benchmark
schema related to the search you want to perform in order to ensure your
filter applies. Sorting fields that are not available on the result are 
ignored.

