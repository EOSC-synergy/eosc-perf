"""Test data generation module."""

import json
from .data_types import Uploader, Site, Benchmark, Result, SiteFlavor
from .facade import facade
from ..controller.io_controller import controller


def _add_result(result):
    facade.add_result(result.get_json(), json.dumps({
        'uploader': result.get_uploader().get_id(),
        'site': result.get_site().get_short_name(),
        'benchmark': result.get_benchmark().get_docker_name(),
        'tags': [tag.get_name() for tag in result.get_tags()],
        'site_flavor': result.get_flavor().get_uuid()
    }))


def add_demo():
    """Add data that is good for demonstration."""

    demo_uploader = Uploader(
        # cannot collide with UUIDs
        identifier='DEMO_USER',
        # not putting my real email in
        email='christophe@example.com',
        name='Christophe [Example data]')

    try:
        facade.get_uploader(demo_uploader.get_id())
    except facade.NotFoundError:
        facade.add_uploader(json.dumps({
            'id': demo_uploader.get_id(),
            'email': demo_uploader.get_email(),
            'name': demo_uploader.get_name()
        }))

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
        facade.add_site(json.dumps({
            'short_name': demo_site.get_short_name(),
            'address': demo_site.get_address(),
            'name': demo_site.get_name(),
            'description': demo_site.get_description()
        }))

        # todo: one flavor per core-count adjustment?
        demo_flavor = SiteFlavor("virtualbox-arch", facade.get_site(demo_site.get_short_name()),
                                 custom_text="Example data obtained with virtualbox core-adjustment")

        facade.add_flavor(demo_flavor.get_name(), demo_flavor.get_description(),
                          demo_flavor.get_site().get_short_name())
    facade.get_site(demo_site.get_short_name()).set_hidden(False)

    with open('eosc_perf/model/sample_data/template.json') as file:
        # the benchmark is real
        demo_benchmark = Benchmark(docker_name='thechristophe/phoronix-c-ray', uploader=demo_uploader,
                                   template=file.read())

    try:
        facade.get_benchmark(demo_benchmark.get_docker_name())
    except facade.NotFoundError:
        facade.add_benchmark(
            demo_benchmark.get_docker_name(),
            demo_benchmark.get_uploader().get_id(),
            demo_benchmark.get_template())
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
