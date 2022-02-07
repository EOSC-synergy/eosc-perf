Introduction
============

EOSC-Perf: A web service to compare computing resources
---------------------------------------------------------

EOSC-Perf is a webapp made to host, search, compare and analyze benchmark results from many very diverse computing resources 
primarily available within the `European Open Science Cloud <https://eosc-portal.eu/>`__ (EOSC).

The main entry point is |perf-web-url|.

The service is also provided via the `EOSC Marketplace <https://marketplace.eosc-portal.eu/services/eosc-performance>`__

The landscape of European university servers is very diverse, so it is at times difficult to pick which servers or
platform to use.
EOSC-Perf is intended to help scientists identify the ideal server for a given task by letting them compare benchmark
results that were ran on different servers to identify the server with the best performance for a given task.

The platform itself is intended to gather data from multiple users running benchmarks, so one does not need to re-run
benchmarks if matching data already exists.
Once data is available for a variety of platforms, the platforms can be easily compared using the existing data.


Main features
--------------

Benchmark results are associated with execution sites, a type of benchmark, an uploader, and optionally a set of
user-created tags which may be used for annotation or search filtering.

Users can search through all results and filter results by sites, benchmarks, tags, uploaders, and even specific JSON
data-points that are part of the result data.
Users can then select multiple results and generate various types of comparison pages, like speedup graphs.

If results are inaccurate, users may report them to administrators.

It supports submitting new benchmark types by packing them in Docker images and submitting their names here. After this,
you may submit new benchmark results associated to this kind of benchmark.
The benchmark software has to generate a JSON output in order to be integrated in the service.

Users may authenticate themselves through `EGI AAI Check-In <https://wiki.egi.eu/wiki/AAI>`_, which lets them connect
using their university account of choice.

The service also provides the full-featured `API <https://performance.services.fedcloud.eu/api/v1/>`__ allowing to communicate
with the service from external applications, e.g to add new results by automated scripts.

Please, check our :doc:`Tutorials <tutorials>` for more details on how to use the service.


Legal
------

By using our service you agree to our `Privacy Policy <https://performance.services.fedcloud.eu/privacy-policy>`__ 
and the `Terms of Service <https://performance.services.fedcloud.eu/terms-of-service>`__.


Contact us
-----------

In the case of questions, suggestions, or for any feedback, please |contact-us|.

