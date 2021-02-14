"""The sandbox module exposes methods to add sample data in the scenario where one wants to try out the eosc-perf
application but does not have any real world data to use it on.

To add the sample data, use `add_demo()`.
"""

import json
from .data_types import Uploader, Site, Benchmark, Result, SiteFlavor
from .facade import facade
from ..controller.io_controller import controller


def _add_result(result):
    facade.add_result(result.get_json(),
        result.get_uploader().get_id(),
        result.get_site().get_short_name(),
        result.get_benchmark().get_docker_name(),
        result.get_flavor().get_uuid(),
        [tag.get_name() for tag in result.get_tags()]
    )


def add_demo():
    """Add sample data to the database."""

    demo_uploader = Uploader(
        # cannot collide with UUIDs
        identifier='DEMO_USER',
        # not putting my real email in
        email='christophe@example.com',
        name='Christophe [Example data]')

    try:
        facade.get_uploader(demo_uploader.get_id())
    except facade.NotFoundError:
        facade.add_uploader(demo_uploader.get_id(), demo_uploader.get_name(), demo_uploader.get_email())

    # virtualbox archlinux installation I use for development
    demo_site = Site(
        short_name='ch-virt',
        name="VirtualboxTestbed",
        address='127.0.0.1',
        description='Locally generated demo data [Example data]')

    try:
        site = facade.get_site(demo_site.get_short_name())
        demo_flavor = site.get_flavors()[0]
    except facade.NotFoundError:
        facade.add_site(demo_site.get_short_name(), demo_site.get_address(), description=demo_site.get_description(),
                        full_name=demo_site.get_name())

        # todo: one flavor per core-count adjustment?
        demo_flavor = SiteFlavor("virtualbox-arch", facade.get_site(demo_site.get_short_name()),
                                 custom_text="Example data obtained with virtualbox core-adjustment")
    facade.get_site(demo_site.get_short_name()).set_hidden(False)

    with open('eosc_perf/model/sample_data/template.json') as file:
        # the benchmark is real
        demo_benchmark = Benchmark(docker_name='thechristophe/openbench-c-ray', uploader=demo_uploader,
                                   description="Example description :)", template=file.read())

    try:
        facade.get_benchmark(demo_benchmark.get_docker_name())
    except facade.NotFoundError:
        facade.add_benchmark(
            demo_benchmark.get_docker_name(),
            demo_benchmark.get_uploader().get_id(),
            description=demo_benchmark.get_description(),
            template=demo_benchmark.get_template())
    facade.get_benchmark(demo_benchmark.get_docker_name()).set_hidden(False)

    # load demo results
    demo_results = []
    for i in [1, 2, 4, 8, 12, 16, 20, 24]:
        with open('eosc_perf/model/sample_data/result-{}.json'.format(i)) as file:
            data_raw = file.read()
            data = json.loads(data_raw)
        if not controller._result_validator.validate_json(data_raw, demo_benchmark.get_template()):
            raise ValueError("demo data " + str(i) + " does *not* pass demo template")
        demo_results.append(Result(
            json_data=json.dumps(data),
            uploader=demo_uploader,
            site=demo_site,
            benchmark=demo_benchmark,
            flavor=demo_flavor))

    filters = {'filters': [
        {'type': 'site', 'value': demo_site.get_short_name()},
        {'type': 'benchmark', 'value': demo_benchmark.get_docker_name()}
    ]}
    results = facade.query_results(json.dumps(filters))
    # only add test results if there aren't any results
    if len(results) <= 0:
        for result in demo_results:
            _add_result(result)
