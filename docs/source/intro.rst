Introduction
============

EOSC-Perf: An application to compare benchmark results
------------------------------------------------------

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse university server clusters.

Benchmark results are associated with execution sites, a type of benchmark, an uploader, and optionally a set of user-created tags which may be used for annotation or search filtering.

Users can search through all results and filter results by sites, benchmarks, tags, uploaders, and even specific JSON data-points that are part of the result data.
Users can then select multiple results and generate various types of comparison pages, like speedup graphs.

If results are inaccurate, users may report them to administrators.

It supports submitting new benchmark types by packing them in docker images and submitting their names here. After this, you may submit new benchmark results associated to this kind of benchmark.

Users may authenticate themselves through EGI AAI Check-In, which lets them connect using their university account of choice.

Motivation
----------

The landscape of european university servers is very diverse, so it is at times difficult to pick which servers or platform to use.
EOSC-Perf is intended to help scientists identify the ideal server for a given task by letting them compare benchmark results that were ran on different servers to identify the server with the best performance for a given task.

The platform itself is intended to gather data from multiple users running benchmarks, so one does not need to re-run benchmarks if matching data already exists.
Once data is available for all platforms, the platforms can be easily compared using the existing data.

Limitations
-----------

- This application was developed to be used in a docker-compose environment, as is thus configured with certain fixed resource links that are to be served by nginx, which is also set-up in this docker-compose environment.
  This includes all routes prefixed with /static/, which generally refer to css and js files, which you may find in the /static folder of the same name in the project root. This can also be used to serve other assets like pictures.

.. warning:: This page is a work-in-progress.
 
