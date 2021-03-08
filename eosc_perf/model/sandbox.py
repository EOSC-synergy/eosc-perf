"""The sandbox module exposes methods to add sample data in the scenario where one wants to try out the eosc-perf
application but does not have any real world data to use it on.

To add the sample data, use `add_demo()`.
"""

import json

from .data_types import Uploader, Site, Benchmark, Result, SiteFlavor
from .database import db
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
        email='sample-data@example.com',
        name='Mister Example')

    try:
        uploader = facade.get_uploader(demo_uploader.get_id())
    except facade.NotFoundError:
        facade.add_uploader(demo_uploader.get_id(), demo_uploader.get_name(), demo_uploader.get_email())
        uploader = facade.get_uploader(demo_uploader.get_id())

    # virtualbox archlinux installation I use for development
    sample_sites = [
        {
            'site': Site(short_name='ch-virt', name="VirtualboxTestbed", address='127.0.0.1', description=''),
            'flavors': ['virtualbox-arch']
        },
        {
            'site': Site(short_name='cesga', name='CESGA', address='unknown', description=''),
            'flavors': ['cor1mem2h10', 'cor2mem2hd20', 'cor4mem4hd40']
        },
        {
            'site': Site(short_name='cesnet-mcc', name='CESNET-MCC', address='unknown', description=''),
            'flavors': ['standard.small', 'standard.medium', 'standard.large', 'hpc.8core-16ram']
        },
        {
            'site': Site(short_name='ifca-lcg2', name='IFCA-LCG2', address='unknown', description=''),
            'flavors': ['m1.small', 'cm4.large', 'm1.large', 'm1.xlarge', 'cm4.4xlarge']
        },
        {
            'site': Site(short_name='iisas-fedcloud', name='IISAS-FedCloud', address='unknown', description=''),
            'flavors': ['m1.small', 'm1.medium', 'm1.large', 'm1.xlarge']
        },
        {
            'site': Site(short_name='ncg-ingrid-pt', name='NCG-INGRID-PT', address='unknown', description=''),
            'flavors': ['svc1.s', 'svc2.s', 'svc2.m', 'svc2.l', 'svc2.xl', 'svc2.xxl']
        }
    ]

    for entry in sample_sites:
        site_info = entry['site']
        try:
            site = facade.get_site(site_info.get_short_name())
        except facade.NotFoundError:
            facade.add_site(site_info.get_short_name(), site_info.get_address(),
                            description=site_info.get_description(),
                            full_name=site_info.get_name())
            site = facade.get_site(site_info.get_short_name())
            # add 'unknown' flavor to mirror controller behaviour
            facade.add_flavor('unknown', "Pick this if you don't know the flavor or it is not listed",
                              site.get_short_name())

        for flavor_name in entry['flavors']:
            try:
                facade.get_site_flavor_by_name(site.get_short_name(), flavor_name)
            except facade.NotFoundError:
                facade.add_flavor(flavor_name, '', site.get_short_name())
                facade.get_site_flavor_by_name(site.get_short_name(), flavor_name)

        site.set_hidden(False)

    with open('eosc_perf/model/sample_data/template.json') as file:
        # the benchmark is real
        demo_benchmark = Benchmark(docker_name='thechristophe/openbench-c-ray', uploader=uploader,
                                   description="Compare cpu perf with multithreaded raytracing", template=file.read())

    try:
        benchmark = facade.get_benchmark(demo_benchmark.get_docker_name())
    except facade.NotFoundError:
        facade.add_benchmark(
            demo_benchmark.get_docker_name(),
            uploader.get_id(),
            description=demo_benchmark.get_description(),
            template=demo_benchmark.get_template())
        benchmark = facade.get_benchmark(demo_benchmark.get_docker_name())
    benchmark.set_hidden(False)

    # load demo results
    demo_results = []
    results = [
        {'site': 'ch-virt', 'flavor': 'virtualbox-arch', 'file': 'result-1.json'},
        {'site': 'ch-virt', 'flavor': 'virtualbox-arch', 'file': 'result-2.json'},
        {'site': 'ch-virt', 'flavor': 'virtualbox-arch', 'file': 'result-4.json'},
        {'site': 'ch-virt', 'flavor': 'virtualbox-arch', 'file': 'result-8.json'},
        {'site': 'ch-virt', 'flavor': 'virtualbox-arch', 'file': 'result-12.json'},
        {'site': 'cesga', 'flavor': 'cor1mem2h10', 'file': 'c-ray/cesga-1.json'},
        {'site': 'cesnet-mcc', 'flavor': 'standard.small', 'file': 'c-ray/cesnet-mcc-1.json'},
        {'site': 'cesnet-mcc', 'flavor': 'standard.medium', 'file': 'c-ray/cesnet-mcc-2.json'},
        {'site': 'cesnet-mcc', 'flavor': 'standard.large', 'file': 'c-ray/cesnet-mcc-4.json'},
        {'site': 'cesnet-mcc', 'flavor': 'hpc.8core-16ram', 'file': 'c-ray/cesnet-mcc-8.json'},
        {'site': 'ifca-lcg2', 'flavor': 'm1.small', 'file': 'c-ray/ifca-lcg2-1.json'},
        {'site': 'ifca-lcg2', 'flavor': 'cm4.large', 'file': 'c-ray/ifca-lcg2-2.json'},
        {'site': 'ifca-lcg2', 'flavor': 'm1.large', 'file': 'c-ray/ifca-lcg2-4.json'},
        {'site': 'ifca-lcg2', 'flavor': 'm1.xlarge', 'file': 'c-ray/ifca-lcg2-8.json'},
        {'site': 'ifca-lcg2', 'flavor': 'cm4.4xlarge', 'file': 'c-ray/ifca-lcg2-16.json'},
        {'site': 'iisas-fedcloud', 'flavor': 'm1.small', 'file': 'c-ray/iisas-fedcloud-1.json'},
        {'site': 'iisas-fedcloud', 'flavor': 'm1.medium', 'file': 'c-ray/iisas-fedcloud-2.json'},
        {'site': 'iisas-fedcloud', 'flavor': 'm1.large', 'file': 'c-ray/iisas-fedcloud-4.json'},
        {'site': 'iisas-fedcloud', 'flavor': 'm1.xlarge', 'file': 'c-ray/iisas-fedcloud-8.json'},
        {'site': 'ncg-ingrid-pt', 'flavor': 'svc1.s', 'file': 'c-ray/ncg-ingrid-pt-1.json'},
        {'site': 'ncg-ingrid-pt', 'flavor': 'svc2.s', 'file': 'c-ray/ncg-ingrid-pt-2.json'},
        {'site': 'ncg-ingrid-pt', 'flavor': 'svc2.m', 'file': 'c-ray/ncg-ingrid-pt-4.json'},
        {'site': 'ncg-ingrid-pt', 'flavor': 'svc2.l', 'file': 'c-ray/ncg-ingrid-pt-8.json'},
        {'site': 'ncg-ingrid-pt', 'flavor': 'svc2.xl', 'file': 'c-ray/ncg-ingrid-pt-16.json'},
        {'site': 'ncg-ingrid-pt', 'flavor': 'svc2.xxl', 'file': 'c-ray/ncg-ingrid-pt-32.json'}
    ]
    for result_info in results:
        site = facade.get_site(result_info['site'])
        flavor = facade.get_site_flavor_by_name(result_info['site'], result_info['flavor'])

        with open('eosc_perf/model/sample_data/{}'.format(result_info['file'])) as file:
            data_raw = file.read()
            data = json.loads(data_raw)
        if not controller._result_validator.validate_json(data_raw, benchmark.get_template()):
            raise ValueError("demo data " + result_info['file'] + " does *not* pass demo template")
        demo_results.append(Result(
            json_data=json.dumps(data),
            uploader=uploader,
            site=site,
            benchmark=benchmark,
            flavor=flavor))

    filters = {'filters': [
        {'type': 'site', 'value': sample_sites[0]['site'].get_short_name()},
        {'type': 'benchmark', 'value': benchmark.get_docker_name()}
    ]}
    results = facade.query_results(json.dumps(filters))
    # only add test results if there aren't any results from my fake machine
    if len(results) <= 0:
        for result in demo_results:
            _add_result(result)

    # Commit again to make sure
    db.session.commit()
