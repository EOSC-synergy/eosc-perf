JSON Filters
===============
Although the usage of all the standard and custom methods should
be enough to collect most of the items for analysis, in the case of
results, some of the required variables to compare or limit in the
search might be inside the result data.

However, the flexibility provided to the ``json`` field to store 
results information impedes the design of specific requests,
the amount of options available are just infinite.

As the usage of conventional queries is not suitable to limit the
results of the search inside json fields, EOSC Performance proposes
a customizable filter argument which can be configured to filter the
results directly into the database following some rules.

Filters are composed by 3 arguments separated by spaces ('%20' on 
URL-encoding): ``<path.separated.by.dots> <operator> <value>`` and 
there are five filter operators:

    - **Equals (==)**: Return results where path value is exact to the
      query value. For example *filters=cpu.count == 5*
    - **Greater than (>)**: Return results where path value strictly
      greater than the query value. For example *filters=cpu.count > 5*
    - **Less than (<)**: Return results where path value strictly lower
      than the query value. For example *filters=cpu.count < 5*
    - **Greater or equal (>=)**: Return results where path value is equal
      or greater than the query value. For example *filters=cpu.count >= 5*
    - **Less or equal (<=)**: Return results where path value is equal or
      lower than the query value. For example *filters=cpu.count <= 5*

.. note::
    Note that in the provided examples the filter is not URL-encoded as
    most libraries do it automatically.

When designing your query using filters, remember that in general it is a
good idea to apply in addition a ``benchmark_id`` argument to limit the search
on results that share the same json structure. Take a look on the required 
fields inside the benchmark schema to ensure that your filter applies. 
Filtering fields that are not available on the result are ignored.
