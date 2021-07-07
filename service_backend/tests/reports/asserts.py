"""Function asserts for tests"""
from urllib import parse

from tests.benchmarks.asserts import correct_benchmark, match_benchmark
from tests.results.asserts import correct_result, match_result
from tests.sites.asserts import (correct_flavor, correct_site, match_flavor,
                                 match_site)


def correct_benchmark_report(json):
    """Checks the json report contains the correct attributes."""
    assert 'benchmark' in json
    correct_report(json)
    correct_benchmark(json['benchmark'])

    return True


def correct_result_report(json):
    """Checks the json report contains the correct attributes."""
    assert 'result' in json
    correct_report(json)
    correct_result(json['result'])

    return True


def correct_site_report(json):
    """Checks the json report contains the correct attributes."""
    assert 'site' in json
    correct_report(json)
    correct_site(json['site'])

    return True


def correct_flavor_report(json):
    """Checks the json report contains the correct attributes."""
    assert 'site' in json
    correct_report(json)
    correct_site(json['site'])
    correct_flavor(json['flavor'])

    return True


def correct_report(json):
    """Checks the json report contains the correct attributes."""
    assert 'date' in json and type(json['date']) is str
    assert 'verified' in json and type(json['verified']) is bool
    assert 'verdict' in json and type(json['verdict']) is bool
    assert 'message' in json and type(json['message']) is str

    return True


def match_benchmark_report(json, report):
    """Checks the json elements matches the report object."""
    match_report(json, report)
    match_benchmark(json['benchmark'], report.benchmark)

    return True


def match_result_report(json, report):
    """Checks the json elements matches the report object."""
    match_report(json, report)
    match_result(json['result'], report.result)

    return True


def match_site_report(json, report):
    """Checks the json elements matches the report object."""
    match_report(json, report)
    match_site(json['site'], report.site)

    return True


def match_flavor_report(json, report):
    """Checks the json elements matches the report object."""
    match_report(json, report)
    match_site(json['site'], report.site)
    match_flavor(json['flavor'], report.flavor)

    return True


def match_report(json, report):
    """Checks the json elements matches the report object."""
    assert json['id'] == str(report.id)
    assert json['date'] == str(report.date.date())
    assert json['verified'] == report.verified
    assert json['verdict'] == report.verdict
    assert json['message'] == report.message

    return True


def match_query(json, url):
    """Checks the json elements matches the url query."""
    presult = parse.urlparse(url)
    query_items = parse.parse_qs(presult.query)

    # Report checks
    if 'date' in query_items:
        assert json['date'] in query_items['date']
    if 'verified' in query_items:
        assert str(json['verified']) in query_items['verified']
    if 'verdict' in query_items:
        assert str(json['verdict']) in query_items['verdict']

    # If benchmark report checks
    if presult.path.split('/')[2] == "benchmarks":
        if 'docker_image' in query_items:
            assert json['benchmark']['docker_image'] in query_items['docker_image']
        if 'docker_tag' in query_items:
            assert json['benchmark']['docker_tag'] in query_items['docker_tag']

   # If result report checks
    if presult.path.split('/')[2] == "results":
        if 'docker_image' in query_items:
            assert json['result']['docker_image'] in query_items['docker_image']
        if 'docker_tag' in query_items:
            assert json['result']['docker_tag'] in query_items['docker_tag']
        if 'site_name' in query_items:
            assert json['result']['site_name'] in query_items['site_name']
        if 'flavor_name' in query_items:
            assert json['result']['flavor_name'] in query_items['flavor_name']

   # If site report checks
    if presult.path.split('/')[2] == "sites":
        if 'site_name' in query_items:
            assert json['site']['name'] in query_items['site_name']

   # If flavor report checks
    if presult.path.split('/')[2] == "flavors":
        if 'site_name' in query_items:
            assert json['site']['name'] in query_items['site_name']
        if 'flavor_name' in query_items:
            assert json['flavor']['name'] in query_items['flavor_name']

    return True


def match_body(json, body):
    """Checks the json elements matches the body dict."""
    if type(body) is list:
        for n in range(len(body)):
            match_body(json[n], body[n])
    elif type(body) is dict:
        for k in body:
            assert k in json
            match_body(json[k], body[k])
    else:
        assert json == body

    return True
