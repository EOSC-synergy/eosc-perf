"""Test data generation module.
Provides: add_dummies()"""

import json
from .data_types import Uploader, Site, Benchmark, Result, Tag, ResultIterator
from .database import db
from .facade import facade

def add_filler():
    """Add filler data that can be used to test search filtering."""

    filler_uploaders = [
        Uploader(identifier='TEST_USER_0', email='fake.address@protonmail.ch', name='Christophe'),
        Uploader(identifier='TEST_USER_1', email='idontknow1@gmail.com', name='Jonas'),
        Uploader(identifier='TEST_USER_2', email='idontknow2@gmail.com', name='Moritz'),
        Uploader(identifier='TEST_USER_3', email='idontknow3@gmail.com', name='Marc')
    ]

    filler_sites = [
        Site(
            short_name='paris',
            name="Paris Cluster",
            address='10.0.0.1',
            description="Université de Paris (Cluster)"),
        Site(
            short_name="berlin",
            name="Berlin Cluster",
            address='10.0.0.2',
            description="Freie Universität Berlin (Cluster)"),
        Site(
            short_name="karlsruhe",
            name="Karlsruhe Cluster",
            address='10.0.0.3',
            description="Karlsruher Institut für Technologie (Cluster)")
    ]

    filler_benchmarks = [
        Benchmark(docker_name='pihole/pihole:dev', uploader=filler_uploaders[1]),
        Benchmark(docker_name='someone/gpu_cuda', uploader=filler_uploaders[2]),
        Benchmark(docker_name='someone/cpu_pi', uploader=filler_uploaders[3]),
        Benchmark(docker_name='someone/various', uploader=filler_uploaders[0]),
        Benchmark(docker_name='someone/other', uploader=filler_uploaders[1]),
        Benchmark(docker_name='someone/benchmarks', uploader=filler_uploaders[2]),
        Benchmark(docker_name='someone/here', uploader=filler_uploaders[3])
    ]

    tags = [
        Tag(name='gpu'),
        Tag(name='cpu'),
        Tag(name='obsolete'),
        Tag(name='testing')
    ]

    filler_results = []
    for uploader in filler_uploaders:
        for site in filler_sites:
            for benchmark in filler_benchmarks:
                for tag in tags:
                    result = Result(
                        json="{}",
                        uploader=uploader,
                        site=site,
                        benchmark=benchmark, tags=[tag])
                    filler_results.append(result)

    for test_uploader in filler_uploaders:
        try:
            facade.get_uploader(test_uploader.get_id())
        except facade.NotFoundError:
            facade.add_uploader(json.dumps({
                'id': test_uploader.get_id(),
                'email': test_uploader.get_email(),
                'name': test_uploader.get_name()
            }))

    for test_site in filler_sites:
        try:
            facade.get_site(test_site.get_short_name())
        except facade.NotFoundError:
            facade.add_site(json.dumps({
                'short_name': test_site.get_short_name(),
                'address': test_site.get_address(),
                'name': test_site.get_name(),
                'description': test_site.get_description()
            }))

    for test_tag in tags:
        try:
            facade.get_tag(test_tag.get_name())
        except facade.NotFoundError:
            facade.add_tag(test_tag.get_name())

    for test_benchmark in filler_benchmarks:
        try:
            facade.get_benchmark(test_benchmark.get_docker_name())
        except facade.NotFoundError:
            facade.add_benchmark(
                test_benchmark.get_docker_name(),
                test_benchmark.get_uploader().get_id())

    filters = {'filters': [
        {'type': 'site', 'value': filler_sites[0].get_short_name()},
        {'type': 'benchmark', 'value': filler_benchmarks[0].get_docker_name()}
    ]}
    results = facade.query_results(json.dumps(filters))
    # only add test results if there aren't any results
    if len(results) <= 0:
        for test_result in filler_results:
            facade.add_result(test_result.get_json(), json.dumps({
                'uploader': test_result.get_uploader().get_id(),
                'site': test_result.get_site().get_short_name(),
                'benchmark': test_result.get_benchmark().get_docker_name(),
                'tags': [tag.get_name() for tag in test_result.get_tags()]
            }))

    # make data added up to this point visible and useable
    iterator = ResultIterator(db.session)
    for test_result in iterator:
        test_result.set_hidden(False)
    for test_site in facade.get_sites():
        test_site.set_hidden(False)
    for test_benchmark in facade.get_benchmarks():
        test_benchmark.set_hidden(False)

def add_demo():
    """Add data that is good for demonstration."""

    demo_uploader = Uploader(
    identifier='DIAGRAM_USER',
    email='diagram@example.com',
    name='Diagram (Do not use)')

    demo_site = Site(
        short_name='diagram_site',
        name="Diagram Site (Do not use)",
        address='127.0.0.1',
        description='Diagram test site entry (Do not use)')

    demo_benchmark = Benchmark(docker_name='donotuse/diagram:test', uploader=demo_uploader)

    # generate a series of results with values for testing the diagram
    demo_results = []
    # skip first result for demo...
    for i in range(2, 17):
        # Numbers generated by Amdahl's Law, 1/(1-p+p/s) where p = speedup = 0.75, s = corecount
        speedup = 0.75
        data = {
            'user_args': {
                'num_gpus': i
            },
            'training': {
                'result': {
                    # generated following amdahl's law
                    'average_examples_per_sec': 1/(1-speedup+speedup/i) * 100
                }
            }
        }
        demo_results.append(Result(
            json=json.dumps(data),
            uploader=demo_uploader,
            site=demo_site,
            benchmark=demo_benchmark))

    try:
        facade.get_uploader(demo_uploader.get_id())
    except facade.NotFoundError:
        facade.add_uploader(json.dumps({
            'id': demo_uploader.get_id(),
            'email': demo_uploader.get_email(),
            'name': demo_uploader.get_name()
        }))

    try:
        facade.get_site(demo_site.get_short_name())
    except facade.NotFoundError:
        facade.add_site(json.dumps({
            'short_name': demo_site.get_short_name(),
            'address': demo_site.get_address(),
            'name': demo_site.get_name(),
            'description': demo_site.get_description()
        }))

    try:
        facade.get_benchmark(demo_benchmark.get_docker_name())
    except facade.NotFoundError:
        facade.add_benchmark(
            demo_benchmark.get_docker_name(),
            demo_benchmark.get_uploader().get_id())

    filters = {'filters': [
        {'type': 'site', 'value': demo_site.get_short_name()},
        {'type': 'benchmark', 'value': demo_benchmark.get_docker_name()}
    ]}
    results = facade.query_results(json.dumps(filters))
    # only add test results if there aren't any results
    if len(results) <= 0:
        for result in demo_results:
            facade.add_result(result.get_json(), json.dumps({
                'uploader': result.get_uploader().get_id(),
                'site': result.get_site().get_short_name(),
                'benchmark': result.get_benchmark().get_docker_name(),
                'tags': [test_tag.get_name() for test_tag in result.get_tags()]
            }))

    # make data added up to this point visible and useable
    iterator = ResultIterator(db.session)
    for test_result in iterator:
        test_result.set_hidden(False)
    for test_site in facade.get_sites():
        test_site.set_hidden(False)
    for test_benchmark in facade.get_benchmarks():
        test_benchmark.set_hidden(False)
